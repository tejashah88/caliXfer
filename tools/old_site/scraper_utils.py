import re

from bs4 import BeautifulSoup

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# "Borrowed" from https://www.peterbe.com/plog/best-practice-with-retries-with-requests
def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def resilient_get(url):
    return requests_retry_session().get(url).content

# we use html5lib since other parsers will randomly cut off part of the text
get_parsed_html = lambda url: BeautifulSoup(resilient_get(url), 'html5lib')

search_between = lambda target, start, end: re.search('{0}(.*){1}'.format(start, end), target).group(1)

clean_str = lambda string: re.sub('\\s+', ' ', string).strip()

simplify_names = lambda name: name \
    .replace('California Polytechnic University,', 'Cal Poly') \
    .replace('California State University,', 'CSU') \
    .replace('University of California,', 'UC')

def parse_options(html, selector):
    results = []
    for option in html.select(selector):
        if option['value']:
            txt, val = option.text.strip(), option['value'].strip()
            results.append((txt, val))

    return results