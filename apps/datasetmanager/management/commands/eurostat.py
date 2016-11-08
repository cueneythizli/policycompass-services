from django.core.management.base import BaseCommand, CommandError
from apps.datasetmanager.models import Dataset
from django.db import models
from django.apps import apps as django_apps
from collections import OrderedDict
from django.conf import settings
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

            for row in range(0, len(rowArrays)):
                values = {}
                spatial = ""
                for individual in individuals_list:
                    if rowArrays[row][0] == individual.title:
                        spatial = individual.title

                for i in range(1, len(colHeadersValues)):
                    if type(rowArrays[row][i]) is str:
                        values[colHeadersValues[i]] = None
                    else:
                        values[colHeadersValues[i]] = rowArrays[row][i]


                resultArray.append({"row":row+1, "individual":spatial, "values":values})


            headers = {'content-type': 'application/json', 'x-user-path':'https://adhocracy-prod.policycompass.eu/api/principals/users/0000072/',
                       'x-user-token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE0Nzg1Mjg2NDIsInN1YiI6Ii9wcmluY2lwYWxzL3VzZXJzLzAwMDAwNzIiLCJleHAiOjE0ODExMjA2NDJ9.HhV3dnlZp_B_A0q6Ijq7MMwC8tbcDMz72ZqP2XW9WCumLZVVoMoGSaxk7CyZkC-F4jSHrx4htn9h5ZqOx35l3Q'}

            payload = {"time":
                    {"resolution":"year","start":colHeadersValues[1],"end":colHeadersValues[len(colHeadersValues)-1]},
                    "resource":{"issued":datetime.datetime.today().strftime('%Y-%m-%d'),
                        "external_resource":71,
                        "url":"http://appsso.eurostat.ec.europa.eu/nui/show.do?dataset="+ str(code) +"&lang=en"
                    },
                    "policy_domains":[1],
                    "title":array['label'],
                    "keywords":array['label'],
                    "license_id":96,
                    "description":array['label'],
                    "spatials":spatials,
                    "language_id":38,
                    "indicator_id":new_indicator.id,
                    "class_id":1,
                    "user_id":1,
                    "unit_id":25,
                    "data":{"table":resultArray},
                    "is_draft":True}



            print("payload " , json.dumps({"table":resultArray}))

            result = requests.post(settings.PC_SERVICES['references']['base_url'] + '/api/v1/datasetmanager/datasets', data=json.dumps(payload), headers=headers)

