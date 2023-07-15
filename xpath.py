#!/usr/bin/env python3
import hashlib
from io import StringIO
import json
from lxml import html
import os
from pprint import pprint
import requests

REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
TEMP_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp')

class Settings:
    max_download_attempts = 3
    max_search = 20
    max_solve_redirect_attempts = 3
    update_search = True
    update_cache = True

def get_html(url, fname, update=False):
    return get_cached_request(url, fname, update)['contents']

def get_cached_request(url, fname, update=False, timeout=10):
    fname = f'{fname}.json'
    file_dict = dict(attempts=0, contents=None, error='')
    persist = False
    try:
        file_dict = json.loads(file_cache_lookup(fname) or '{}') or file_dict
        if (update
            or (file_dict['contents'] is None and not file_dict['error'])
            or (file_dict['error'] and file_dict['attempts'] < Settings.max_download_attempts)):
            r = requests.get(
                url,
                headers = REQUEST_HEADERS,
                timeout=timeout
            )
            contents = r.text
            file_dict['contents'] = contents
            file_dict['error'] = ''
            persist = True
    except Exception as e:
        file_dict['error'] = f'{e}'
        file_dict['attempts'] += 1
        persist = True
    if persist:
        file_cache_store(json.dumps(file_dict), fname)
    return file_dict

def hash_link(url):
    return hashlib.sha256(url.encode('utf8')).hexdigest()

def file_cache_store(contents, fname, temp_folder=TEMP_FOLDER):
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    file_path = os.path.join(temp_folder, fname)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(contents)
    return file_path

def file_cache_lookup(fname, temp_folder=TEMP_FOLDER):
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    file_path = os.path.join(temp_folder, fname)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

def main():
    # url = 'http://xmlfeed.jobcentral.com/'
    url = 'https://career8.successfactors.com/career?company=NCLPROD'
    html_str = get_html(url, f'{hash_link(url)}.html')
    #print(html_str)
    tree = html.parse(StringIO(html_str))
    # Este r = tree.xpath("//table[5]/tr/td[1]/text()")
    r = tree.xpath("//div[@id= 'logo']//img/@alt")
    r = tree.xpath("//input[@id='company']/@value")
    #r = tree.xpath("//img[contains(@class, 'css-1t8sqvc')]/@alt")
    #r = tree.xpath("//img[contains(@class, 'logo')]/@alt")
    pprint(r)


if __name__ == '__main__':
    main()