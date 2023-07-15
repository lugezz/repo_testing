import csv
import logging
import os
import re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError as GoogleHttpError
from io import StringIO
from lxml import html
import typer

from ats_scrap.utils import (
    clean_link, dict_to_json, get_cached_result,
    get_domain, get_html, hash_link,
    json_to_dict, load_txt,
    Settings, TEMP_FOLDER, path_here,
)

api_key = os.environ['GOOGLE_API_KEY']
app = typer.Typer()
ATS_TO_SCRAP = json_to_dict(path_here('ats_to_scrap.json'), temp_folder=None)
EXCL_URLS = load_txt('excluded_urls.txt')
logger = logging.getLogger(__name__)


def companies_from_string(str_param, scrap_param, position, exclude_str=''):
    """
    Return a list of potential companies with the scrap_param
    """
    resp = ''
    tmp = re.split(scrap_param, str_param)

    if len(tmp) > 1:
        resp = tmp[position]

    resp = resp.split('/')[0].replace(exclude_str, '').strip()
    resp = resp if len(resp) > 1 else ''

    return resp


def get_companies_from_xpath(url, xpath_arg, exclude_str='', ats_name=''):
    html_str = get_html(url, f'{ats_name} - {hash_link(url)}.html')
    get_results = {}

    try:
        tree = html.parse(StringIO(html_str))
    except Exception as e:
        get_results['error'] = [f'{e}']
        return get_results

    if html_str:
        results = tree.xpath(xpath_arg)
        for result in results:
            result = result.replace(exclude_str, '').strip()
            result = result if len(result) > 1 else ''

            if result:
                my_urls = get_results.get(result, set())
                my_urls.add(url)
                get_results[result] = my_urls

    return get_results


class Ats:
    valid_scrap_types = ['scrap_xml', 'before_scrap_param', 'after_scrap_param',
                         'before_title', 'after_title']

    def __init__(self, name, look_for='', pattern='', scrap_param='',
                 scrap_type='scrap_xml', type_of_search='inurl:', exclude_str=''):

        self.exclude_str = exclude_str
        self.look_for = name if not look_for else look_for
        self.name = name
        self.scrap_type = scrap_type
        self.type_of_search = type_of_search

        assert scrap_type in self.valid_scrap_types, f'{scrap_type} is not valid'
        if scrap_type == 'scrap_xml':
            if not scrap_param:
                self.scrap_param = '//img[contains(@class, "logo")]/@alt'
            else:
                self.scrap_param = scrap_param
        else:
            self.pattern = pattern if pattern else f'.{self.look_for}'
            if scrap_type == 'after_scrap_param' and self.pattern[-1] != "/":
                self.pattern = f'{self.pattern}/'

    def get_step0(self):
        """
        Get specific result step0.json
        step0.json should be already created
        """
        step0_json = get_step0()
        ats_dict = step0_json.get(self.name,
                                  {'found_results': 0, 'processed_results': 0, 'results': {}})

        if not Settings.update_search:
            # If update_search is already logged
            logger.info(f'{"-"*20} Search results for {self.name.upper()} {"-"*20}')
            logger.info(ats_dict)

        return ats_dict

    def get_cse_results(self):
        resp = get_cse_results(self.look_for, Settings.max_search, self.type_of_search)
        logger.info(f'{"-"*20} Search results for {self.name.upper()} {"-"*20}')
        logger.info(resp)

        return resp

    def get_companies(self):
        step0 = self.get_step0()
        resp = {'found_results': step0['found_results'],
                'processed_results': step0['processed_results'],
                'companies': {}}

        if self.scrap_type == 'scrap_xml':
            this_links = get_url_from_results(step0['results'], cleaned_url=False)

            for link in this_links:
                tmp_comps = get_companies_from_xpath(link[1], self.scrap_param, ats_name=self.name)
                resp['companies'].update(tmp_comps)

        elif 'scrap_param' in self.scrap_type:
            # In URL (After or before)
            this_urls = get_url_from_results(step0['results'])

            if this_urls:
                for url in this_urls:
                    position = 0 if self.scrap_type == 'before_scrap_param' else 1
                    tmp_comp_from_url = companies_from_string(url[1], self.pattern, position, self.exclude_str)
                    if tmp_comp_from_url:
                        comp_urls = resp.get(tmp_comp_from_url, set())
                        comp_urls.add(url[1])
                        resp['companies'][tmp_comp_from_url] = comp_urls

        elif '_title' in self.scrap_type:
            this_titles = get_url_from_results(step0['results'])
            position = 0 if self.scrap_type == 'before_title' else 1

            if this_titles:
                for title in this_titles:
                    tmp_comp_from_url = companies_from_string(title[0], self.pattern, position, self.exclude_str)
                    if tmp_comp_from_url:
                        comp_urls = resp.get(tmp_comp_from_url, set())
                        comp_urls.add(title[1])
                        resp['companies'][tmp_comp_from_url] = comp_urls

        logger.info(f'Searches for {self.name.upper()}: {Settings.max_search}, Obtained urls:\
        {resp["processed_results"]} ({"{:.0%}".format(resp["processed_results"]/Settings.max_search)}) ')

        avg = 0 if resp['processed_results'] == 0 else len(resp) / resp['processed_results']
        logger.info(f'Companies found for {self.name.upper()}: {len(resp)}({"{:.0%}".format(avg)})')

        return resp


def get_step0():
    resp = {}

    if not os.path.exists(os.path.join(TEMP_FOLDER, 'step0.json')):
        return resp

    resp = json_to_dict('step0.json')
    return resp


def get_url_from_results(results, cleaned_url=True):
    """
    Get all urls from the dictionary
    step0.json should be already created

    Output:
    [(Tit1, url1), (Tit2, url2)...]
    """
    resp = []

    for company, urls in results.items():
        for url in urls:
            if cleaned_url:
                url = clean_link(url)
            resp.append((company, url))

    return resp


def get_cse_results(ats_to_find, max_search, type_of_search='inurl:'):
    """
    Getting Links
    -------------
    Expected Output
    {found_results: 9900,
     processed_results: 100,
     results: {
        Title1: [link1, link2],
        Title2: [link1, link2, link3],
        }
    }
    """
    cse_results = {'found_results': 0, 'processed_results': 0, 'results': {}}
    resource = build('customsearch', 'v1', developerKey=api_key).cse()
    proc_res = 0

    for i in range(1, max_search, 10):
        try:
            search_query = f'{type_of_search}{ats_to_find}'
            result = get_cached_result(resource, q=search_query, cx='768d0b2297cff41e7',
                                       start=i, update=Settings.update_search_cache)
            if i == 1:
                # Just for the first time
                cse_results['found_results'] = result['searchInformation']['totalResults']

        except GoogleHttpError:
            logger.error("Quota exceeded for quota metric 'Queries' and limit 'Queries per day' of service")
            cse_results['results']['Error'] = ['Quota exceeded']
            break

        except BaseException as e:
            logger.error(f"Unexpected {e=}, {type(e)=}")
            cse_results['results']['Error'] = [f"Unexpected {e=}, {type(e)=}"]
            break

        for item in result.get('items', {}):
            title = item['title']
            link = item['link']

            if not get_domain(link) in EXCL_URLS:
                proc_res += 1
                if title in cse_results:
                    cse_results['results'][title].append(link)
                else:
                    cse_results['results'][title] = [link]

    cse_results['processed_results'] = proc_res
    return cse_results


def results_to_csv(dict_result, path):
    """
    Input Dict Result format
    {ATS1: {Company1: {url1, url2}},
    ATS2: {Company1: {url1, url2}, {Company2: {url1}}}
    """
    logger.info(f"Saving csv format results in {path}")
    summary = []
    # summary format
    # [('ats', 'found_results', 'processed_results', 'companies_found'), ...]

    with open(path, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(('ATS', 'Company', 'Url'))
        for ats, results in dict_result.items():
            companies = 0
            for company, urls in results['companies'].items():
                companies += 1
                for url in urls:
                    row = (ats, company, url)
                    writer.writerow(row)

            summary.append((ats, results['found_results'], results['processed_results'], str(companies)))

    # Summary report in specific csv - Path + "_summary"
    with open(f"{path.replace('.csv', '_summary.csv')}", 'w') as fp2:
        writer = csv.writer(fp2)
        writer.writerow(('ATS', 'Found Results', 'Result Pages',
                         'Links', 'Non Repeated Links', 'Companies Found'))
        for result in summary:
            links = min(Settings.max_search, int(result[1]))
            row = result[:2] + \
                (str(links // 10),) + \
                (str(links),) + \
                result[2:]
            writer.writerow(row)


def step0_search_results(ats_list):
    """
    Expected STEP 0 Getting Links from ATS search
    ------------------------------------
    {Title1: [link1, link2], Title2: [link1]}
    """
    step0 = {}
    for ats in ats_list:
        step0[ats.name] = ats.get_cse_results()

    return step0


def stepf_get_companies(ats_list):
    """
    Get companies in ats
    ------------------------------------

    Expected
    {ATS1: {Company 1: (url1, url2), Company 2: (url1, url2, url 3)},
    ATS2: {Company 1: (url1, url2), Company 2: (url1), Company 3: (url1), Company 4: (url1, url2)},
    ATS3: {},
    }
    """
    stepf = {}
    for ats in ats_list:
        stepf[ats.name] = ats.get_companies()

        logger.info(f'{"-"*20} Companies for {ats.name.upper()}: {len(stepf[ats.name]["companies"])} {"-"*20}')
        logger.info(stepf[ats.name])

    return stepf


@app.command()
def scrap():
    # Logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    handler = logging.FileHandler(os.path.join(TEMP_FOLDER, 'logfile.log'))
    logger.addHandler(handler)

    # STEP 0 ----------------- Getting Links from ATS search ---------------------
    ats_domains = []

    for ats, params in ATS_TO_SCRAP.items():
        ats_obj = Ats(name=ats, **params)
        ats_domains.append(ats_obj)

    if Settings.update_search:
        step0 = step0_search_results(ats_domains)
        dict_to_json(step0, 'step0.json')

    # We should have now ./tmp/step0.json

    results = stepf_get_companies(ats_domains)
    logger.info(f'{"-"*100}\n{"-"*30} FINAL RESULTS {"-"*30}')
    logger.info(results)
    # Output format
    # {ATS1: {
    #   found_results: 13400,
    #   processed_results: 100,
    #   companies: {Company1: {url1, url2}}
    # },
    # ATS2: {
    #   found_results: 9900,
    #   processed_results: 100,
    #   companies: {Company1: {url1, url2}, Company2: {url1}},
    # }

    results_to_csv(results, os.path.join(TEMP_FOLDER, "final_results.csv"))


if __name__ == '__main__':
    app()
