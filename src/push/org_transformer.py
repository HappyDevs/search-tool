'''
Created on Nov 12, 2014

@author: alexandru-m-g
'''


class OrgTransformer:

    def transform(self, org_dict):
        transformed_dict = {}
        for item in org_dict.values():
            transformed_item = {'id': unicode(item['orgID']).encode('utf-8'),
                                'code': item['orgCode'],
                                'name': item['orgName'],
                                'locations': item['location'],
                                'sources': [item['sourceName']],
                                'source_links': [item['sourceURL']],
                                'roles': item['orgRole'],
                                'count': item['counter']
                                }
            transformed_dict[transformed_item['id']] = transformed_item

        return transformed_dict
