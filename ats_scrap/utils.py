import requests
import os
import subprocess
import logging
from urllib.parse import urlparse
import hashlib
import json
import time


logger = logging.getLogger(__name__)
TEMP_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp')
REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
class settings:
    max_download_attempts = 2

def get_domain(url):
    if isinstance(url, list):
        url = url[-1]
    dom = urlparse(url.lower()).netloc
    # get the latest two parts XXX.XX
    dom = '.'.join(dom.split('.',-2)[-2:])
    # remove the port if present
    dom = dom.split(':')[0]
    return dom


def clean_urls(urls: list):
    clean = [] 
    for u in urls:
        if isinstance(u, list):
            clean.append(clean_urls(u))
        else:
            clean.append(clean_url(u))
    return clean


def clean_url(url):
    if url.startswith('https://ad.doubleclick.net/'):
        url = url.split('?', 1)[1]
    return url


def get_html(url, fname, update=False):
    return get_cached_request(url, fname, update)['contents']

def get_cached_request(url, fname, update=False, timeout=10):
    fname = f'{fname}.json'
    file_dict = dict(attempts=0, contents='', error='')
    persist = False
    try:
        file_dict = json.loads(file_cache_lookup(fname) or '{}') or file_dict
        if (update
            or (not file_dict['contents'] and not file_dict['error'])
            or (file_dict['error'] and file_dict['attempts'] < settings.max_download_attempts)):
            logger.info(f'Downloading:{url}')
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

def get_sized_request(url, fname, size=1024 * 10, timeout=10, update=False):
    fname = f'{fname}.sized.json'
    file_dict = dict(attempts=0, contents='', error='')
    persist = False
    try:
        file_dict = json.loads(file_cache_lookup(fname) or '{}') or file_dict
        if (update
            or (not file_dict['contents'] and not file_dict['error'])
            or (file_dict['error'] and file_dict['attempts'] < settings.max_download_attempts)):
            logger.info(f'Downloading:{url}')
            r = requests.get(
                url,
                headers = REQUEST_HEADERS,
                stream=True,
                timeout=timeout,
            )
            r.raise_for_status()
            for chunk in r.iter_content(size):
                contents = chunk.decode('utf8')
                break
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


def exec_cmd(cmd):
    logger.debug('Running: %r' % cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    out, err = p.communicate()
    logger.debug('out: %r\nerr:%r', out, err)
    return p, out, err

redirect_cache = None
def solve_redirect_cached(url, update=False):
    global redirect_cache
    url_dict = dict(attempts=0, contents='', error='')
    persist = False
    contents = ''
    cache_fname = 'redirects_cache.json'
    cache = redirect_cache or json.loads(file_cache_lookup(cache_fname) or '{}')
    try:
        url_dict = cache.setdefault(url, url_dict)
        if (update
            or (not url_dict['contents'] and not url_dict['error'])
            or (url_dict['error'] and url_dict['attempts'] < settings.max_download_attempts)):
            contents, err = solve_redirect(url)
            if contents:
                cache[url]['contents'] = clean_url(contents)
                cache[url]['error'] = ''
                persist = True
            else:
                cache[url]['error'] = err
                cache[url]['attempts'] += 1
                persist = True
    except Exception as e:
        cache[url]['error'] = f'{e}'
        cache[url]['attempts'] += 1
        persist = True
    if persist:
        file_cache_store(json.dumps(cache, indent=1), cache_fname)
    redirect_cache = cache
    return url_dict


def solve_redirect(url):
    logger.info(f'Solving redirect: {url}')
    p, out, err = exec_cmd(['curl', '-v', url])
    time.sleep(1)
    err = err.decode('utf8')
    for l in err.splitlines():
        if l.lower().startswith('< location: '):
            return l[len('< Location: '):], ''
    return '', f'{out.decode("utf8")}\n{err}'


def hash_link(url):
    return hashlib.sha256(url.encode('utf8')).hexdigest()


def load_ats_domains():
    with open(path_here('ats_domains.txt')) as fp:
        domains = [d.lower().strip().split(':')[0] for d in fp.readlines()
                        if d.strip() 
                        and not d.strip().startswith('#')]
    assert all(len(d.split('.')) == 2 for d in domains)
    return domains


def path_here(filename):
    directory = os.path.dirname(__file__)
    return os.path.join(directory, filename)

