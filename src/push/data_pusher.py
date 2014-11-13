'''
Created on Nov 12, 2014

@author: alexandru-m-g
'''
import requests
import urllib
import json
import logging

log = logging.getLogger(__name__)

solr_retrieve_url = 'http://localhost:8983/solr/org_collection/browse?wt=json'
solr_update_url = 'http://localhost:8983/solr/org_collection/update/json?commit=true'


class SolrDataPusher:

    def retrieve(self, key_list):
        if key_list:
            temp_key_list = ('"{}"'.format(key) for key in key_list)
            keys_str = ' '.join(temp_key_list)
            params = urllib.urlencode(
                {'fq': 'id:(' + keys_str + ')', 'rows': len(key_list)})
            url = solr_retrieve_url + '&' + params
            print 'Retrieve url is: ' + url
            log.info('Retrieve url is: ' + url)
            response = requests.get(
                url, headers={'content-type': 'application/json'})
            jsonObj = response.json()
            if 'response' in jsonObj:
                documents = jsonObj['response']['docs']
                print 'Retrieved {} docs'.format(len(documents))
                log.info('Retrieved {} docs'.format(len(documents)))
                return documents
        return []

    def push(self, org_dict):

        documents = self.retrieve([key for key in org_dict])
        self._update_dictionary(documents, org_dict)

        jsonEl = json.dumps(org_dict.values())
        log.info("Posting to solr data for {}".format(str(org_dict.keys())))
        # from requests.auth import HTTPBasicAuth
        # requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))
        response = requests.post(
            solr_update_url, jsonEl, headers={'content-type': 'application/json'})
    #     print "Posted json: " + jsonEl
        print response.content

    def _update_dictionary(self, org_list, org_dict):
        for old_org in org_list:
            org_id = old_org['id']
            org = org_dict[org_id]

            # update org
            if 'locations' in old_org:
                org['locations'] = list(
                    set(org['locations'] + old_org['locations']))
            if 'sources' in old_org:
                org['sources'] = list(
                    set(org['sources'] + old_org['sources']))
            if 'source_links' in old_org:
                org['source_links'] = list(
                    set(org['source_links'] + old_org['source_links']))
            if 'roles' in old_org:
                org['roles'] = list(
                    set(org['roles'] + old_org['roles']))
            if 'count' in old_org:
                org['count'] += old_org['count']
