#!/usr/bin/python
import xml.etree.ElementTree as ET

#configurations or params
file = 'in.xml'
orgs = ['participating-org', 'reporting_org', 'provider-org', 'receiver-org']
result = {}

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
    actST = 0
    items = {}
    locs = {}
    for event, elem in ET.iterparse(file, events=('start', 'end')):
        if event == 'start':
            if elem.tag == 'iati-activity':
                actST = 1
            if elem.tag == 'location':
                for loc in elem:
                    if loc.tag == 'name':
                        locs[unicode(loc.text)] = unicode(loc.text)
            if elem.tag in orgs:
                item = {}
                orgName = unicode(elem.text)
                item['orgName'] = orgName  # orgName.encode('utf-8')
#                 if 'ref' in elem.attrib:
                item['orgCode'] = unicode(elem.attrib.get('ref', None))
                item['orgID'] = unicode(str(item['orgName']).strip().lower().replace(
                    ' ', '__') + '#' + str(item['orgCode']))
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
                actST = 0
                items = {}
                locs = {}
    return result


def parse_file(file, name, url):
    return parse(file, orgs, result, name, url)
