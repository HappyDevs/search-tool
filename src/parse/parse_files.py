#!/usr/bin/python
import xml.etree.ElementTree as ET
import json
from __builtin__ import file
import get_files as get_files

#configurations or params
orgs = ['participating-org', 'reporting_org', 'provider-org', 'receiver-org']
# result = {}
res_dir = '../../resources/'
conf_file = get_files.file_map
#conf_file = res_dir + conf_filename


def run_parse(transformer, pusher):
    with open(conf_file, 'r+') as f:
        data = json.load(f)
        no_files = data['0']['no_files']
        print data['1']['url']
        for i in range(1, no_files):
            f_file = data[str(i)]['file']
            f_url = data[str(i)]['url']
            f_name = data[str(i)]['name']
            print 'START parsing ... ' + f_file + ' from URL: ' + f_url
            res = parse_file(f_file, f_name, f_url)
            if res:
                org_dict = transformer.transform(res)
                pusher.push(org_dict)
                print 'END parsing ... ' + f_file
            else:
                print 'NOT parsing, wrong format: ' + f_file


# methods
def addOrg(res, item):
    if item['orgID'] not in res:
        newIt = res[item['orgID']] = item
        newIt['counter'] = 0
        if 'orgRole' not in item:
            newIt['orgRole'] = []
        else:
            newIt['orgRole'] = [item['orgRole']]
    else:
        exIt = res[item['orgID']]
        if 'orgRole' in item and item['orgRole'] not in exIt['orgRole']:
            exIt['orgRole'].append(item['orgRole'])


def addLoc(res, orgID, locsDict):
    if 'location' not in res[orgID]:
        res[orgID]['location'] = list(locsDict)
    else:
        crtList = res[orgID]['location']
        resList = list(set(crtList + list(locsDict)))
        res[orgID]['location'] = resList


def addOrgList(result, orgID, orgList, locsDict):
    for org in orgList:
        addOrg(result, org)
    addLoc(result, orgID, locsDict)
    result[orgID]['counter'] += 1


def parse(file, orgs, result, name, url):
   # actST = 0
    items = {}
    locs = {}
    try:
        for event, elem in ET.iterparse(file, events=('start', 'end')):
            if event == 'start':
             #           if elem.tag == 'iati-activity':
                #                actST = 1
                if elem.tag == 'location':
                    for loc in elem:
                        if loc.tag == 'name':
                            locs[unicode(loc.text)] = unicode(loc.text)
                if elem.tag in orgs:
                    item = {}
                    orgName = unicode(elem.text).strip()
                    item['orgName'] = orgName  # orgName.encode('utf-8')
    #                 if 'ref' in elem.attrib:
                    item['orgCode'] = unicode(
                        elem.attrib.get('ref', None)).strip()
                    if (item['orgCode'] and item['orgCode'] != u'None') or (item['orgName'] and item['orgName'].strip()):
                        item['orgID'] = unicode(
                            item['orgName'].lower().replace(
                                ' ', '__') + '#' + item['orgCode'])
                        orgID = item['orgID']
                        item['sourceName'] = unicode(name)
                        item['sourceURL'] = unicode(url)
                        if 'role' in elem.attrib:
                            item['orgRole'] = unicode(elem.attrib['role'])
                        item['location'] = []
                        if orgID not in items:
                            items[orgID] = [item]
                        else:
                            items[orgID].append(item)
            if event == 'end':
                if elem.tag == 'iati-activity':
                    for it in items:
                        addOrgList(result, it, items[it], locs)
      #              actST = 0
                    items = {}
                    locs = {}
    except ET.ParseError, e:
        print 'Could not parse as xml: ' + file
        print str(e)
    return result


def parse_file(file, name, url):
    return parse(file, orgs, {}, name, url)
