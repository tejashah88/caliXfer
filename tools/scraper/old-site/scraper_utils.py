from urllib.request import urlopen
import re

from bs4 import BeautifulSoup

get_parsed_html = lambda url: BeautifulSoup(urlopen(url), 'html.parser')

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