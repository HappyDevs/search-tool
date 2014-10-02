#!/usr/bin/python
import requests
import json
from io import StringIO
import urllib
import parse


# get files from ckan

def get_files(file_map_name, action, org_list_url, pkg_url):
    url = action + org_list_url
    orgs_list = get_org_list(url)
    url = action + pkg_url
    pkg_list = get_packages_by_org_list(url, orgs_list)
    urls = {}
    print "LIST get_src_by_pkg"
    for pkg in pkg_list:
        try:
            title, value = get_src_by_pkg(pkg)
        except IndexError:
            print "Error getting info from " + str(pkg)
            continue
        urls[title] = value
    print "END LIST get_src_by_pkg"
    map_file_content = {}
    i = 0
    for p_name, p_url in urls.iteritems():
        i += 1
        print 'START download ' + p_name + ' from ' + p_url
        try:
            download_file(i, p_url)
        except (RuntimeError, IOError):
            print 'ERROR trying to retrieve ' + p_url
            i -= 1
            continue
        map_file_content[i] = {
            'name': p_name, 'url': p_url, 'file': 'files/' + str(i) + '.xml'}
        print 'Finish download '
    map_file_content[0] = {'no_files': i}
    with open(file_map_name, 'w') as outfile:
        json.dump(map_file_content, outfile)
    return map_file_content


# get a list of organizations

def get_org_list(url):
    print 'get_org_list'
    r = requests.post(url, data=json.dumps(
        {}), headers={'content-type': 'application/json'}, verify=False)
    io = StringIO(r.text)
    jRes = json.load(io)
    orgs_list = []
    if jRes['success']:
        orgs_list = jRes['result']
    print 'END get_org_list'
    return orgs_list


def get_packages_by_org_list(url, org_list):
    pkg_list = []
    i = 0
    print 'get_packages_by_org_list'
    for org in org_list:
        i += 1
        pkg_list = pkg_list + get_packages_by_org(url, org)
        if i > 1:
            break
    print 'END get_packages_by_org_list'
    return pkg_list


def get_packages_by_org(url, org):
    print 'get_packages_by_org' + str(url) + str(org)
    r = requests.post(url, data=json.dumps(
        {'fq': 'organization:' + org, 'rows': '1000000'}),
        headers={'content-type': 'application/json'}, verify=False)
    io = StringIO(r.text)
    jRes = json.load(io)
    pkg_list = []
    if jRes['success']:
        pkg_list = jRes['result']['results']
    print 'END get_packages_by_org'
    return pkg_list


def clean_url(url):
    url = url.replace('http://', '')
    url = url.replace('www.', '')
    return url


def get_src_by_pkg(pkg):
    pkg_url = pkg['resources'][0]['url']
    return pkg['title'], pkg_url


def download_file(i, p_url):
    urllib.URLopener().retrieve(p_url, files_dir + str(i) + '.xml')


# some settings
file_map_name = 'file_map.ini'
base = 'http://iatiregistry.org/api/3/'
action = base + 'action/'
org_list_url = 'organization_list'
pkg_url = 'package_search'
files_dir = '../../resources/files/'

# map_file_content = run_download(file_map_name, action, org_list_url, pkg_url)

# for k in map_file_content:
#     file = map_file_content[k]['file']
#     print 'START parsing ... ' + file
#     name = map_file_content[k]['name']
#     url = map_file_content[k]['url']
#     res = parse.parse_file(file, name, url)
#     print res
#     print 'END parsing ... ' + map_file_content[k]['file']
#
# print 'END to process files'


def run_download():
    print 'Start downloading files ....'
    map_file_content = get_files(file_map_name, action, org_list_url, pkg_url)
    print map_file_content
    print 'End downloading files'
    return map_file_content
