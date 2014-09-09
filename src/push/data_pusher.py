'''
Created on Sep 7, 2014

@author: alexandru-m-g
'''

import requests
import json
import logging
import random
import uuid
import hashlib

log = logging.getLogger(__name__)

locations = ['Bucharest', 'Budapest', 'Riga', 'New York', 'Washington', 'Paris', 'London', 'Berlin', 'Moscow', 'Tbilisi']
roles = ['Implementing', 'Executing', 'Reporting', 'Donor', 'Recipient']
sources = ['Yahoo', 'Google', 'Bing', 'Local', 'Other']
names = ['World', 'Nations', 'Union', 'Bank', 'International', 'European', 'American', 'Inter', 'African', 'Nations']

solr_url = 'http://localhost:8983/solr/org_collection/update/json?commit=true'

sample_org = {'id': 'id1',
              'code': 'code1',
              'name': 'sample name',
              'locations': ['Bucharest', 'Budapest'],
              'sources': ['sample source'],
              'roles': ['sample role'],
              'count': 1
              }

def push_to_solr(elem_list):
    jsonEl = json.dumps(elem_list)
    print "Before post"
    # from requests.auth import HTTPBasicAuth
    # requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))
    response = requests.post(solr_url, jsonEl, headers={'content-type': 'application/json'})
#     print "Posted json: " + jsonEl
    print response.content

def get_random_from_list(list, max_num_of_elements):
    result = []
    num_of_elements = random.randrange(1, max_num_of_elements+1)
    for i in range(0, num_of_elements):
        index = random.randrange(0, len(list))
        result.append(list[index])
    return result

def create_org():
    global names
    org_uuid = str(uuid.uuid4())
    name = " ".join(get_random_from_list(names, 3))
    hash = hashlib.md5(name+org_uuid).hexdigest()
    
    return {'id': hash,
              'code': org_uuid,
              'name': name,
              'locations': get_random_from_list(locations, 4),
              'sources': get_random_from_list(sources, 2),
              'roles': get_random_from_list(roles, 3),
              'count': random.randrange(1, 10)
              }

# push_to_solr(sample_org)
org_list = [create_org() for i in range(0,1000) ]
push_to_solr(org_list)
