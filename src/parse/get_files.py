#!/usr/bin/python
import requests
import json
from io import StringIO
import urllib
import logging
import time
import ConfigParser


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
            logging.error("ERROR getting info from: " + str(pkg))
            continue
        urls[title] = value
    print "END LIST get_src_by_pkg"
    map_file_content = {}
    i = 0
    for p_name, p_url in urls.iteritems():
        i += 1
        print 'START download ' + p_name + ' from ' + p_url
        attempts = 0
        ok = 1
        while attempts < no_attempts:
            try:
                download_file(i, p_url)
                print 'downloaded: ' + p_url
                logging.info('downloaded: ' + p_url)
                ok = 1
                break
            except (RuntimeError, IOError):
                print 'ERROR attempt' + str(attempts + 1) + ' for url:' + p_url
                attempts += 1
                ok = 0
                time.sleep(6)
        if ok == 0:
            i -= 1
            logging.error('ERROR url: ' + p_url)
            continue
        map_file_content[i] = {
            'name': p_name, 'url': p_url, 'file': files_dir + str(i) + '.xml'}
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
        if max_orgs != -1 and i > max_orgs:
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
base = 'http://iatiregistry.org/api/3/'
action = base + 'action/'
org_list_url = 'organization_list'
pkg_url = 'package_search'
conf_filename = 'file_map.json'

res_dir = '../../resources/'
config_file = res_dir + 'config.txt'
config = ConfigParser.ConfigParser()
config.readfp(open(config_file, 'r'))
base_dir = config.get('resources', 'base_dir')
files_dir = base_dir + config.get('resources', 'downloaded_files')
logs_dir = base_dir + config.get('resources', 'logs_dir')

#files_dir = res_dir + 'files/'
LOG_FILENAME = logs_dir + 'download.log'

#conf_file = files_dir + conf_filename
file_map_name = base_dir + conf_filename
no_attempts = 5
max_orgs = 3


def run_download():

    print 'Start downloading files ....'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
    map_file_content = get_files(file_map_name, action, org_list_url, pkg_url)
    print map_file_content
    print 'End downloading files'
    return map_file_content
