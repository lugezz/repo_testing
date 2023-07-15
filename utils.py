import hashlib
import json
import logging
import requests
import os
import re
import subprocess
import time
from urllib.parse import urlparse


logger = logging.getLogger(__name__)
TEMP_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp')
REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}


class Settings:
    max_download_attempts = 3
    max_search = 2000
    max_solve_redirect_attempts = 3
    update_cache = True
    update_search = True
    update_search_cache = False


def get_domain(url):
    if isinstance(url, list):
        url = url[-1]
    dom = urlparse(url.lower()).netloc
    # get the latest two parts XXX.XX
    dom = '.'.join(dom.split('.', -2)[-2:])
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
    file_dict = dict(attempts=0, contents=None, error='')
    persist = False
    try:
        file_dict = json.loads(file_cache_lookup(fname, 'cache') or '{}') or file_dict
        if should_update(file_dict, update, Settings.max_download_attempts):
            logger.info(f'Downloading:{url}')
            r = requests.get(
                url,
                headers=REQUEST_HEADERS,
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
        file_cache_store(json.dumps(file_dict), fname, 'cache')
    return file_dict


def get_cached_result(resource, q, cx, start, update=False):
    searched_ats = q.split(':')[1]
    fname = f'Search for {searched_ats} - {hash_link(q+str(start))}'
    persist = False

    result = resource.list(q=q, cx=cx, start=start).execute()

    # Remove some special characters
    fname = re.sub("\\*|\\-|/", "", fname)
    q = re.sub("\\*|\\-|/", "", q)
    file_dict = json.loads(file_cache_lookup(repr(fname), 'cache') or '{}')

    if not file_dict or update:
        logger.info(f'Downloading:{q} from {start}')
        file_dict = result
        persist = True

    if persist:
        file_cache_store(json.dumps(file_dict), fname, 'cache')
    return result


def get_cached_bing_result(headers, endpoint, query, params, update=False):
    searched_ats = query.split(':')[1] if ':' in query else query

    fname = f'Search for {searched_ats} - {hash_link(query + str(params["offset"]))}'
    # Remove some special characters
    fname = re.sub("\\*|\\-|/", "", fname)
    file_dict = json.loads(file_cache_lookup(fname, 'cache') or '{}')

    if not file_dict or update:
        logger.info(f'Downloading:{query} - from {params["offset"]} ')
        # Search process if it's not in cache or configured to be updated
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()

        file_dict = results
        file_cache_store(json.dumps(file_dict), fname, 'cache')

    return file_dict


def get_sized_request(url, fname, size=1024 * 1024, timeout=10, update=False):
    fname = f'{fname}.sized.json'
    file_dict = dict(attempts=0, contents='', error='')
    persist = False
    try:
        file_dict = json.loads(file_cache_lookup(fname, 'cache') or '{}') or file_dict
        if should_update(file_dict, update, Settings.max_download_attempts):
            logger.info(f'Downloading:{url}')
            r = requests.get(
                url,
                headers=REQUEST_HEADERS,
                stream=True,
                timeout=timeout,
            )
            r.raise_for_status()
            for chunk in r.iter_content(size):
                # Since we are doing an arbitrary size we may encounter errors like
                # 'utf-8' codec can't decode byte 0xe2 in position 10239: unexpected end of data
                contents = chunk.decode('utf8', 'ignore')
                break
            file_dict['contents'] = contents
            file_dict['error'] = ''
            persist = True
    except Exception as e:
        file_dict['error'] = f'{e}'
        file_dict['attempts'] += 1
        persist = True
    if persist:
        file_cache_store(json.dumps(file_dict), fname, 'cache')
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


def should_update(dict, update=False, attempts=3):
    resp = (update
            or (not dict['contents'] and not dict['error'])
            or (dict['error'] and dict['attempts'] < attempts))

    return resp


redirect_cache = None


def solve_redirect_cached(url, update=False):
    global redirect_cache
    url_dict = dict(attempts=0, contents='', error='')
    persist = False
    contents = ''
    cache_fname = 'redirects_cache.json'
    cache = redirect_cache or json.loads(file_cache_lookup(cache_fname, 'cache') or '{}')
    try:
        url_dict = cache.setdefault(url, url_dict)
        if should_update(url_dict, update, Settings.max_solve_redirect_attempts):
            contents = solve_redirect(url)
            cache[url]['contents'] = clean_url(contents)
            cache[url]['error'] = ''
            persist = True
    except Exception as e:
        cache[url]['error'] = f'{e}'
        cache[url]['attempts'] += 1
        persist = True
    if persist:
        file_cache_store(json.dumps(cache, indent=1), cache_fname, 'cache')
    redirect_cache = cache
    return url_dict


def solve_redirect(url):
    logger.info(f'Solving redirect: {url}')
    p, out, err = exec_cmd(['curl', '-v', url])
    time.sleep(1)
    err = err.decode('utf8')
    for line in err.splitlines():
        if line.lower().startswith('< location: '):
            return line[len('< Location: '):]
    out = out.decode("utf8")
    if 'Expired Job' in out:
        for line in out.splitlines():
            if '<p>This job posting has expired. <a href=' in line:
                url = line.split('href="')[1].split('"')[0]
                return url
    raise LookupError(f'{p.returncode}\n{out!r}\n{err!r}')


def hash_link(url):
    return hashlib.sha256(url.encode('utf8')).hexdigest()


def load_ats_domains():
    with open(path_here('ats_domains.txt')) as fp:
        domains = [d.lower().strip().split(':')[0] for d in fp.readlines()
                   if d.strip() and not d.strip().startswith('#')]
    assert all(len(d.split('.')) == 2 for d in domains)
    return domains


def path_here(filename):
    directory = os.path.dirname(__file__)
    return os.path.join(directory, filename)


def clean_link(link):
    if '//' in link:
        resp = link.split('//')[1]
    else:
        resp = link

    return resp.replace('www.', '').rstrip('/')


def load_txt(txt_file):
    with open(path_here(txt_file)) as fp:
        resp = [d.lower().rstrip('\n') for d in fp.readlines() if not d.strip().startswith('#')]
    return resp


def json_to_dict(json_file, temp_folder=TEMP_FOLDER):
    if temp_folder:
        path = os.path.join(temp_folder, json_file)
    else:
        path = json_file
    with open(path) as d:
        dict_data = json.load(d)
    return dict_data


def dict_to_json(dictionary, fname, temp_folder=TEMP_FOLDER):
    if not os.path.exists(temp_folder):
        if temp_folder:
            os.makedirs(temp_folder)
    file_path = os.path.join(temp_folder, fname)

    with open(file_path, 'w') as fp:
        json.dump(dictionary, fp, indent=1)
