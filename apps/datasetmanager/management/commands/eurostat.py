from django.core.management.base import BaseCommand, CommandError
from apps.datasetmanager.models import Dataset
from django.db import models
from django.apps import apps as django_apps
from collections import OrderedDict
import json
import requests
import datetime
import pandas

class Command(BaseCommand):
    help = 'Eurostat'

    def handle(self, *args, **options):
        for code in args:
            data = requests.get("http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/" + str(code) + "?precision=1")

            if data.status_code == 400:
                errorDict = {"result": 400}
                errorString = str(errorDict).replace("'", '"')
                errorJson = json.loads(errorString)
                return Response(errorJson)
            elif data.status_code == 416:
                errorDict = {"result": 416}
                errorString = str(errorDict).replace("'", '"')
                errorJson = json.loads(errorString)
                return Response(errorJson)

            array = data.json(object_pairs_hook=OrderedDict)

            rowHeaders = array['dimension']['geo']['category']['label']

            rowHeadersValues = list(rowHeaders.values())

            rowLen = len(rowHeadersValues)

            colHeaders = array['dimension']['time']['category']['label']

            colHeadersVals = list(colHeaders.values())

            colLen = len(colHeadersVals) + 1

            colHeadersValues = []

            colHeadersValues.append("")

            for q in range(0, colLen - 1):
                colHeadersValues.append(colHeadersVals[q])

            val = array['value']

            values = list(val.values())

            rowArrays = []

            index = 0
            for row in range(0, rowLen):
                colArray = []
                position = row * (colLen - 1)
                colArray.append(rowHeadersValues[row])
                for col in range(0, colLen - 1):
                    if val.get(str(position + col)) is None:
                        colArray.append("")
                    else:
                        colArray.append(values[index])
                        index += 1

                rowArrays.append(colArray)

            Individual = django_apps.get_model("referencepool", "Individual")
            individuals_list = Individual.objects.all()

            DataClass = django_apps.get_model("referencepool", "DataClass")
            data_class = DataClass.objects.get(title="Country")

            Indicator = django_apps.get_model("indicatorservice", "Indicator")

            try:
                new_indicator = Indicator.objects.get(name=array['label'])
            except:
                new_indicator = Indicator(name=array['label'], description=array['label'])
                new_indicator.save()


            spatials = []


            for i in range(0, len(rowHeaders)):
                spatial_key = list(rowHeaders.keys())[i]
                spatial_value = list(rowHeaders.values())[i]
                found = False
                for individual in individuals_list:
                    if spatial_value == individual.title:
                        spatials.append(individual.id)
                        found = True

                if found is False:
                    new_individual = Individual(title=spatial_value, code=spatial_key, data_class=data_class)
                    new_individual.save()
                    spatials.append(new_individual.id)


            resultArray = []

            dataset_test = Dataset.objects.get(pk=19)

            print("dataset ", type(dataset_test.data))

            data_frame = {}
            for row in range(0, len(rowArrays)):
                valuesDict = {}
                for i in range(1, len(colHeadersValues)):
                    valuesDict[colHeadersValues[i]+"-01-01T00:00:00.000Z"] = rowArrays[row][i]

                #valuesDict = OrderedDict(sorted(valuesDict.items(), key=lambda t: t[0]))

                spatial = -1

                for individual in individuals_list:
                    if rowArrays[row][0] == individual.title:
                        spatial = individual.id

                data_frame[str(spatial)] = valuesDict



            data_dict = {"resolution":"year", "unit":25, "data_frame": str(data_frame)}

            #pandas_data = pandas.DataFrame(data_dict)

            dictString = str(data_dict).replace("{'", '{"')
            dictString = str(dictString).replace("':", '":')
            dictString = str(dictString).replace("['", '["')
            dictString = str(dictString).replace("]'", ']"')
            dictString = str(dictString).replace("']", '"]')
            dictString = str(dictString).replace("',", '",')
            dictString = str(dictString).replace(", '", ', "')
            dictString = str(dictString).replace("'", '"')

            print("data_dict ", dictString)


            new_dataset = Dataset(title=array['label'], description=array['label'], keywords=array['label'], time_resolution="year",
                                  time_start=colHeadersValues[1], time_end=colHeadersValues[len(colHeadersValues)-1],
                                  spatials=spatials, language_id=38, resource_issued=datetime.datetime.today().strftime('%Y-%m-%d'),
                                  resource_url="http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset="+ str(code) +"&lang=en",
                                  resource_id=71, unit_id=25, indicator_id=new_indicator.id, class_id=1, policy_domains=[1],
                                  license_id=96,
                                  data=dictString)

            new_dataset.save()



