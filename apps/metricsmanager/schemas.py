from collections import OrderedDict
from rest_framework.reverse import reverse
from django.templatetags.static import static


class Schemas(object):

    def get_schema(self, ident, request):
        result = getattr(self, '_' + ident + '_schema')(request)
        return result

    def _metric_schema(self, request):
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('metric',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for an unit'
        s['type'] = 'object'
        s['links'] = self._metric_links(request)
        s['properties'] = self._metric_properties(request)

        return s

    def _metric_create_schema(self, request):
        s = self._metric_properties(request)
        s.pop('issued')
        s.pop('modified')
        s.pop('id')
        s.pop('version')
        s.pop('unit')
        s['unit'] = OrderedDict([
            ('description', 'An ID of an unit'),
            ('type', 'integer')
        ])

        s['data']['properties']['table']['items']['properties'].pop('row')
        s.pop('language')
        s['language'] = OrderedDict([
            ('description', 'An ID of an language'),
            ('type', 'integer')
        ])
        s.pop('external_resource')
        s['external_resource'] = OrderedDict([
            ('description', 'An ID of an external resource'),
            ('type', 'integer')
        ])

        return s

    def _metric_links(self, request):
        l = [
            OrderedDict([
                ('title', 'List of all metrics'),
                ('rel', 'collection'),
                ('href', reverse('metric-list')),
                ('method', 'GET'),
                ('mediaType', 'application/json')
            ]),
            OrderedDict([
                ('title', 'Filter the metric data'),
                ('rel', 'filter'),
                ('href', reverse('metric-list') + '/{id}'),
                ('method', 'GET'),
                ('mediaType', 'application/json'),
                ('encType', 'application/x-www-form-urlencode'),
                ('schema', OrderedDict([
                    ('type', 'object'),
                    ('properties', OrderedDict([
                        ('sort', OrderedDict([
                            ('description', 'Sorting order of the metric data'),
                            ('type', 'string')
                        ])),
                        ('extras', OrderedDict([
                            ('description', 'Filtering by named extra columns'),
                            ('type', 'string')
                        ]))
                    ]))
                ]))
            ]),
            OrderedDict([
                ('title', 'Edit this metric'),
                ('rel', 'update'),
                ('href', reverse('metric-list') + '/{id}'),
                ('method', 'PUT'),
                ('mediaType', 'application/json'),
                ('encType', 'application/json'),
                ('schema', OrderedDict([
                    ('type', 'object'),
                    ('$ref', reverse('schema-detail', request=request, args=('metric_create',))),
                    ('required', [
                        'title',
                        'acronym',
                        'description',
                        'keywords',
                        'unit',
                        'language',
                        'policy_domains'
                    ])
                ]))
            ]),
            OrderedDict([
                ('title', 'Delete this metric'),
                ('rel', 'delete'),
                ('href', reverse('metric-list') + '/{id}'),
                ('method', 'DELETE'),
                ('mediaType', 'application/json')
            ])
        ]
        return l


    def _metric_properties(self, request):
        p = OrderedDict()

        p['spatial'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/spatial'),
            ('type', 'string')
        ])
        p['resource_url'] = OrderedDict([
            ('description', 'https://schema.org/isBasedOnUrl'),
            ('type', 'string')
        ])
        p['unit'] = OrderedDict([
            ('type', 'object'),
            ('$ref', reverse('schema-detail', request=request, args=('unit',)))
        ])
        p['language'] = OrderedDict([
            ('type', 'object'),
            ('$ref', reverse('schema-detail', request=request, args=('language',)))
        ])
        p['external_resource'] = OrderedDict([
            ('type', 'object'),
            ('$ref', reverse('schema-detail', request=request, args=('external_resource',)))
        ])
        p['resource_issued'] = OrderedDict([
            ('description', 'The date the resource was issued, refering to resource_url'),
            ('type', 'string')
        ])
        p['issued'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/issued'),
            ('type', 'string')
        ])
        p['modified'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/modified'),
            ('type', 'string')
        ])
        p['policy_domains'] = OrderedDict([
            ('description', 'The policy domains associated with this metric'),
            ('type', 'array'),
            ('items', OrderedDict([
                ('description', 'Policy domain object'),
                ('type', 'object'),
                ('properties', self._policy_domain_schema(request))
            ]))
        ])
        p['data'] = OrderedDict([
            ('description', 'The actual data of the metric'),
            ('type', 'object'),
            ('properties', self._metric_data_schema(request))
        ])
        p['id'] = OrderedDict([
            ('description', 'Unique identifier of the metric'),
            ('type', 'integer')
        ])
        p['title'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/title'),
            ('type', 'string')
        ])
        p['acronym'] = OrderedDict([
            ('description', 'A shorter title for the metric'),
            ('type', 'string')
        ])
        p['description'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/description'),
            ('type', 'string')
        ])
        p['keywords'] = OrderedDict([
            ('description', 'http://schema.org/keywords'),
            ('type', 'string')
        ])
        p['publisher'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/publisher'),
            ('type', 'string')
        ])
        p['license'] = OrderedDict([
            ('description', 'http://purl.org/dc/terms/license'),
            ('type', 'string')
        ])
        p['version'] = OrderedDict([
            ('description', 'https://schema.org/version'),
            ('type', 'integer')
        ])
        p['formula'] = OrderedDict([
            ('description', 'The calculation formula for a derived metric'),
            ('type', 'string')
        ])

        return p

    def _metric_data_schema(self, request):
        p = OrderedDict()

        p['extra_columns'] = OrderedDict([
            ('description', 'Extra columns used in the table'),
            ('type', 'array'),
            ('items', OrderedDict([
                ('description', 'Column-Names'),
                ('type', 'string'),
            ]))
        ])
        p['table'] = OrderedDict([
            ('description', 'Tabular data of the metric'),
            ('type', 'array'),
            ('items', OrderedDict([
                ('description', 'List of table rows'),
                ('type', 'object'),
                ('properties', OrderedDict([
                    ('row', OrderedDict([
                        ('description', 'The number of the row'),
                        ('type', 'integer')
                    ])),
                    ('from', OrderedDict([
                        ('description', 'The from-date of the row'),
                        ('type', 'string')
                    ])),
                    ('to', OrderedDict([
                        ('description', 'The to-date of the row'),
                        ('type', 'string')
                    ])),
                    ('anyOf', OrderedDict([
                    ('description', 'Actual Value of any extra column'),
                    ('$ref', '#/properties/extra_columns'),
                    ('type', 'string')
                ])),
                ])),

                ('additionalProperties', True)
            ]))
        ])


        return p

    def _policy_domain_schema(self, request):
        p = OrderedDict()

        p['title'] = OrderedDict([
            ('description', 'Title of the policy domain'),
            ('type', 'string')
        ])
        p['id'] = OrderedDict([
            ('description', 'Unique identifier of the policy domain'),
            ('type', 'integer')
        ])
        p['description'] = OrderedDict([
            ('description', 'Description of the policy domain'),
            ('type', 'string'),
        ])

        return p


    def _external_resource_schema(self, request):
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('external_resource',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for an external resource'
        s['type'] = 'object'
        s['properties'] = self._external_resource_properties(request)

        return s

    def _external_resource_properties(self, request):
        p = OrderedDict()

        p['title'] = OrderedDict([
            ('description', 'Title of the external resource'),
            ('type', 'string')
        ])
        p['id'] = OrderedDict([
            ('description', 'Unique identifier of the external resource'),
            ('type', 'integer')
        ])
        p['url'] = OrderedDict([
            ('description', 'URL of the external resource'),
            ('type', 'string'),
        ])
        p['api_url'] = OrderedDict([
            ('description', 'URL of the API of the external resource'),
            ('type', 'string'),
        ])

        return p


    def _language_schema(self, request):
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('unit',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for an language'
        s['type'] = 'object'
        s['properties'] = self._language_properties(request)

        return s

    def _language_properties(self, request):
        p = OrderedDict()

        p['title'] = OrderedDict([
            ('description', 'Title of the language'),
            ('type', 'string')
        ])
        p['id'] = OrderedDict([
            ('description', 'Unique identifier of the language'),
            ('type', 'integer')
        ])
        p['code'] = OrderedDict([
            ('description', 'Unique code of the language'),
            ('type', 'string'),
            ('maxLength', 2),
            ('minLength', 2),
        ])
        return p

    def _unit_schema(self, request):
        s = OrderedDict()

        s['id'] = reverse('schema-detail', request=request, args=('unit',))
        s['$schema'] = 'http://json-schema.org/draft-04/hyper-schema#'
        s['description'] = 'Schema for an unit'
        s['type'] = 'object'
        s['properties'] = self._unit_properties(request)

        return s

    def _unit_properties(self, request):
        p = OrderedDict()

        p['description'] = OrderedDict([
            ('description', 'Description of the unit'),
            ('type', 'string')
        ])
        p['title'] = OrderedDict([
            ('description', 'Title of the unit'),
            ('type', 'string')
        ])
        p['id'] = OrderedDict([
            ('description', 'Unique identifier of the unit'),
            ('type', 'integer')
        ])
        p['unit_category'] = OrderedDict([
            ('description', 'The category of the unit'),
            ('type', 'object'),
            ('properties', OrderedDict([
                ('id', OrderedDict([
                    ('description', 'Unique identifier of the unit category'),
                    ('type', 'integer')
                ])),
                ('title', OrderedDict([
                    ('description', 'Title of the unit category'),
                    ('type', 'string')
                ]))
            ]))
        ])


        return p


    def _local_schema(self, request, id):
        return 'http://' + request.get_host() + '/static/schema.html#' + id
