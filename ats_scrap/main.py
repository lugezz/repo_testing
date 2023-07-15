#!/usr/bin/env python3
from utils import get_html, hash_link, file_cache_lookup, file_cache_store,\
    load_ats_domains, get_domain, get_sized_request,\
    solve_redirect_cached, get_cached_request
import logging
import json
import lxml.html
from io import StringIO
import re
import csv
from typing import Optional
from collections import defaultdict


logger = logging.getLogger(__name__)

JOBCENTRAL_URL = 'http://xmlfeed.jobcentral.com/index.asp'
JOBCENTRAL_JSON = 'jobcentral_com_index.json'
ATS_DOMAINS = load_ats_domains()


def get_jobcentral_links():
    html_str = get_html(JOBCENTRAL_URL, 'jobcentral_com_index.asp')
    logger.info('Parsing...')
    tree = lxml.html.parse(StringIO(html_str))
    links_comp = {}
    for href in tree.xpath('//a/@href'):
        if (href.startswith('/feeds/')
            and not href.endswith('.xsd')):
            links_comp[href] = href
    return links_comp


def get_jobcentral_json(update=False):
    contents = file_cache_lookup(JOBCENTRAL_JSON)
    if not contents or update:
        links_comp = get_jobcentral_links()
        file_cache_store(json.dumps(links_comp, indent=1), JOBCENTRAL_JSON)
        return links_comp
    return json.loads(contents)


def step0_jobcentral_links(update=False, max_feeds=-1):
    logger.info('Entering step0...')
    jobcentral_feeds = get_jobcentral_json(update)
    step0_output = {}
    for href, name in jobcentral_feeds.items():
        url = JOBCENTRAL_URL.rsplit('/',1)[0] + href
        file_dict = get_sized_request(url, f'{hash_link(url)}.xml', update=update)
        if not file_dict.get('error'):
            for l in file_dict.get('contents', '').splitlines():
                if '<link>' in l:
                    url = l[len('        <link><![CDATA['):-len(']]></link>')]
                    step0_output[name] = dict(urls=[url], step=0)
                    break
        else:
            step0_output[name] = dict(error=file_dict['error'], step=0)
        max_feeds -= 1
        if not max_feeds:
            break
    return step0_output


def step1_solve_redirects(step0_output, update=False):
    logger.info('Entering step1...')
    step1_output = {}
    for comp, comp_dict in step0_output.items():
        step1_output[comp] = comp_dict
        if comp_dict.get('error'):
            continue
        step1_output[comp] = comp_dict.copy()
        link = step1_output[comp]['urls'][-1]
        url_dict = solve_redirect_cached(link)
        if not url_dict.get('error'):
            dom = get_domain(url_dict['contents'])
            step1_output[comp] = dict(urls=[link, url_dict['contents']],
                                      domains=[dom] if dom in ATS_DOMAINS else [],
                                      is_ats=dom in ATS_DOMAINS,
                                      step=1)
        else:
            step1_output[comp] = dict(urls=[link],
                                      error=f'error:{url_dict["error"]} attempts:{url_dict["attempts"]}',
                                      step=1)
    return step1_output


def step2_dejobs_scrap(step1_output):
    logger.info('Entering step2...')
    step2_output = {}
    for comp, comp_dict in step1_output.items():
        step2_output[comp] = comp_dict
        if comp_dict.get('is_ats') or comp_dict.get('error'):
            continue
        url = comp_dict['urls'][-1]
        if get_domain(url) in ('dejobs.org'):
            file_dict = get_cached_request(url, f'{hash_link(url)}.html')
            if not file_dict['error']:
                html = file_dict['contents']
                m = re.findall('https:\/\/rr.jobsyn.org\/[A-Z0-9]+', html)
                step2_output[comp] = comp_dict.copy()
                step2_output[comp]['step'] = 2
                if m:
                    url_dict = solve_redirect_cached(m[0])
                    if not url_dict.get('error'):
                        apply_redirect = url_dict['contents']
                        step2_output[comp]['urls'].append(apply_redirect)
                        step2_output[comp]['is_ats'] = get_domain(apply_redirect) in ATS_DOMAINS
                        if step2_output[comp]['is_ats']:
                            step2_output[comp]['domains'].append(get_domain(apply_redirect))
                    else:
                        step2_output[comp]['error'] = f'error:{url_dict["error"]} attempts:{url_dict["attempts"]}'
                else:
                    step2_output[comp]['error'] = 'no dejobs regex link found'
            else:
                step2_output[comp]['error'] = file_dict['error']
    return step2_output


def step3_general_scrap(step2_output):
    logger.info('Entering step3...')
    step3_output = {}
    for comp, comp_dict in step2_output.items():
        step3_output[comp] = comp_dict
        if comp_dict.get('is_ats') or comp_dict.get('error'):
            continue
        step3_output[comp] = comp_dict.copy()
        step3_output[comp]['step'] = 3
        url = comp_dict['urls'][-1]
        try:
            file_dict = get_cached_request(url, f'{hash_link(url)}.html')
            if not file_dict['error']:
                html = file_dict['contents']
                tree = lxml.html.parse(StringIO(html))
                page_urls = []
                domains = []
                for href in tree.xpath('//a/@href'):
                    if href.startswith('http'):
                        dom = get_domain(href)
                        if dom in ATS_DOMAINS:
                            page_urls.append(href)
                            domains.append(dom)
                if domains:
                    step3_output[comp]['domains'].extend(domains)
                    step3_output[comp]['is_ats'] = bool(domains)
                    step3_output[comp]['urls'].append(page_urls)
            else:
                step3_output[comp]['error'] = file_dict['error']
        except Exception as e:
            step3_output[comp]['error'] = f'{e}'

        print (step2_output)
    return step3_output


def dump_csv(company_to_ats, path):
    logger.info('Entering dump_csv...')
    def get_domain_link(domain, urls):
        if isinstance(urls, list):
            for u in urls:
                if get_domain(u) == domain:
                    return u
        else:
            return urls
    def url_to_str(urls):
        if isinstance(urls, list):
            return  '  ' + '\n  '.join(urls)
        else:
            return urls
    def history_to_str(urls):
        return '\n--\n'.join(url_to_str(u) for u in urls)
    with open(path, 'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(('Domain', 'Is ATS','Company','Final Url', 'URL History', 'Step', 'Error'))
        for company in sorted(company_to_ats):
            comp_dict = company_to_ats[company]
            if not comp_dict.get('urls'):
                print(company, comp_dict)
                continue
            for domain in comp_dict.get('domains', [get_domain(comp_dict['urls'][-1])]):
                writer.writerow((domain, 'yes' if comp_dict.get('is_ats') else '',
                                 company,
                                 get_domain_link(domain, comp_dict['urls'][-1]),
                                 history_to_str(comp_dict['urls']),
                                 comp_dict['step'],
                                 comp_dict.get('error', '')))



def main(max_feeds:Optional[int]=200):
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    step0_output = step0_jobcentral_links(update=True, max_feeds=max_feeds)
    #print(step0_output)
    step1_output = step1_solve_redirects(step0_output)
    #print(step1_output)
    step2_output = step2_dejobs_scrap(step1_output)
    #print(step2_output)
    step3_output = step3_general_scrap(step2_output)
    #print(step3_output)
    dump_csv(step3_output, 'companies_to_ats_step3_output.csv')
    with open('step3_output.json', 'w') as fp:
        json.dump(step3_output, fp, indent=1)
    total = len(step3_output)
    ats_step_count = defaultdict(int)
    noats_step_count = defaultdict(int)
    error_step_count = defaultdict(int)
    for c,d in step3_output.items():
        if d.get('is_ats'):
            ats_step_count[d['step']] += 1
        elif d.get('error'):
            error_step_count[d['step']] += 1
        else:
            noats_step_count[d['step']] += 1
    def print_stats(name, stats, total):
        stat_total = 0
        ratio = lambda x: x/total*100
        print_str = ''
        for i in sorted(stats):
            print_str += f'step{i}: {ratio(stats[i])}, '
            stat_total += stats[i]
        logger.info(f'{name}: {{ {name}_total: {stat_total}, {print_str}}}')
    logger.info(f'Total: {total}')
    print_stats('ats', ats_step_count, total)
    print_stats('noats', noats_step_count, total)
    print_stats('error', error_step_count, total)


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    main()

