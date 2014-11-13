'''
Created on Nov 12, 2014

@author: alexandru-m-g
'''


class OrgTransformer:

    def transform(self, org_dict):
        key_list = []
        transformed_dict = {}
        for key, item in org_dict.iteritems():
            transformed_item = {'id': item['orgID'],
                                'code': item['orgCode'],
                                'name': item['orgName'],
                                'locations': item['location'],
                                'sources': [item['sourceName']],
                                'source_links': [item['sourceURL']],
                                'roles': item['orgRole'],
                                'count': item['counter']
                                }
            transformed_dict[transformed_item['id']] = transformed_item
            key_list.append(key)

        return transformed_dict
