import re
import json
import os

import urllib.request
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from tika import tika, parser

# "Borrowed" from https://www.peterbe.com/plog/best-practice-with-retries-with-requests
def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None
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
    try:
        return requests_retry_session().get(url).content
    except Exception as ex:
        print(f'Warning: GET request failed: {ex}')
        return None

def download_file(url, filename, retries_left=5):
    if retries_left != 0:
        if not os.path.isfile(filename):
            parent_folder = os.path.dirname(filename)
            os.makedirs(parent_folder, exist_ok=True)
            try:
                urllib.request.urlretrieve(url, filename)
            except KeyboardInterrupt:
                raise
            except:
                print(f'ALERT: Retrying {url}...')
                download_file(url, filename, retries_left - 1)
    else:
        print(f'ALERT: Aborting {url}!')

def simplify_school_names(name):
    name_map = [
        ('California Polytechnic University,',  'Cal Poly'  ),
        ('California State University,',        'CSU'       ),
        ('University of California,',           'UC'        ),
    ]

    for (old_name, new_name) in name_map:
        name = name.replace(old_name, new_name)

    return name

class AssistAPI:
    """
    A wrapper class for fetching resources from assist.org's (hidden) API
    """
    PARENT_DIR = os.path.dirname(__file__)
    RAW_JSON_PATH = f'{PARENT_DIR}/json-dump/raw'
    CLEAN_JSON_PATH = f'{PARENT_DIR}/json-dump/clean'
    REPORTS_PATH = f'{PARENT_DIR}/reports'

    def __init__(self, online_only=False, dump_json=False, save_reports=True):
        self.dump_json = dump_json
        self.save_reports = save_reports
        self.online_only = online_only

        if self.dump_json:
            os.makedirs(self.RAW_JSON_PATH, exist_ok=True)
            os.makedirs(self.CLEAN_JSON_PATH, exist_ok=True)

        tika.checkTikaServer()

    def _dump_json(self, content, full_filepath):
        parent_folder = os.path.dirname(full_filepath)
        os.makedirs(parent_folder, exist_ok=True)

        with open(full_filepath, 'w') as fp:
            json.dump(content, fp, indent=4)

    def _read_json(self, full_filepath):
        try:
            with open(full_filepath, 'r') as fp:
                contents = json.load(fp)
            return contents
        except (IOError, json.decoder.JSONDecodeError):
            return None

    def _dump_raw_json(self, content, filepath):
        self._dump_json(content, f'{self.RAW_JSON_PATH}/{filepath}')

    def _dump_clean_json(self, content, filepath):
        self._dump_json(content, f'{self.CLEAN_JSON_PATH}/{filepath}')

    def _read_raw_json(self, filepath):
        return self._read_json(f'{self.RAW_JSON_PATH}/{filepath}')

    def _read_clean_json(self, filepath):
        return self._read_json(f'{self.CLEAN_JSON_PATH}/{filepath}')

    def _obtain_raw_json(self, filepath, url):
        raw_json = None if self.online_only else self._read_raw_json(filepath)

        if raw_json is None:
            data = resilient_get(url)
            if data is not None:
                raw_json = json.loads(data)

                if self.dump_json:
                    self._dump_raw_json(raw_json, filepath)

        return raw_json

    def fetch_academic_years(self):
        FILEPATH = 'academic-years.json'
        URL = 'https://assist.org/api/AcademicYears'

        raw_years = self._obtain_raw_json(FILEPATH, URL)

        clean_years = []
        for year in raw_years:
            clean_years.append({
                'id': year['Id'],
                'fall-year': year['FallYear']
            })

        if self.dump_json:
            self._dump_clean_json(clean_years, FILEPATH)

        return clean_years

    def fetch_source_schools(self):
        FILEPATH = 'src-institutions.json'
        URL = 'https://assist.org/api/institutions'

        raw_schools = self._obtain_raw_json(FILEPATH, URL)

        clean_schools = []
        for school in raw_schools:
            clean_schools.append({
                'id': school['id'],
                'names': {
                    'current': simplify_school_names(school['names'][0]['name']),
                    'alternative': [{'name': simplify_school_names(alt_name['name']), 'from-year': alt_name['fromYear']} for alt_name in school['names'][1:]]
                },
                'code': school['code'].strip(),
                'use-legacy-report': school['prefers2016LegacyReport'],
                'is-community-college': school['isCommunityCollege'],
            })

        if self.dump_json:
            self._dump_clean_json(clean_schools, FILEPATH)

        return clean_schools

    def fetch_destination_schools(self, start_school_id):
        FILEPATH = f'dst-institutions/{start_school_id}.json'
        URL = f'https://assist.org/api/institutions/{start_school_id}/agreements'

        raw_schools = self._obtain_raw_json(FILEPATH, URL)

        clean_schools = []
        for option in raw_schools:
            clean_schools.append({
                'id': option['institutionParentId'],
                'name': simplify_school_names(option['institutionName']),
                'code': option['code'].strip(),
                'is-community-college': option['isCommunityCollege'],
                'sending-year-ids': option.get('sendingYearIds'),
                'receiving-year-ids': option.get('receivingYearIds')
            })

        if self.dump_json:
            self._dump_clean_json(clean_schools, FILEPATH)

        return clean_schools

    def fetch_categories_of_agreements(self, start_school_id, end_school_id, year_id):
        FILEPATH = f'categories/{start_school_id}/{end_school_id}/{year_id}.json'
        URL = f'https://assist.org/api/agreements/categories?sendingInstitutionId={start_school_id}&receivingInstitutionId={end_school_id}&academicYearId={year_id}'

        raw_categories = self._obtain_raw_json(FILEPATH, URL)

        clean_categories = []
        for category in raw_categories:
            clean_categories.append({
                'name': category['label'],
                'code': category['code'],
                'has-reports': category['hasReports']
            })

        if self.dump_json:
            self._dump_clean_json(clean_categories, FILEPATH)

        return clean_categories


    def fetch_agreements_by_category(self, start_school_id, end_school_id, year_id, category_code):
        FILEPATH = f'agreements/{start_school_id}/{end_school_id}/{year_id}/{category_code}.json'
        URL = f'https://assist.org/api/agreements?sendingInstitutionId={start_school_id}&receivingInstitutionId={end_school_id}&academicYearId={year_id}&categoryCode={category_code}'

        raw_agreements = self._obtain_raw_json(FILEPATH, URL)

        clean_agreements = {'reports': [], 'all-reports': []}

        for agreement in raw_agreements['reports']:
            clean_agreements['reports'].append({
                'name': agreement['label'],
                'id': agreement['key'],
            })

        for agreement in raw_agreements['allReports']:
            clean_agreements['all-reports'].append({
                'name': agreement['label'],
                'id': agreement['key'],
            })

        if self.dump_json:
            self._dump_clean_json(clean_agreements, FILEPATH)

        return clean_agreements


    def download_report_text(self, agreement_id, download_only=False):
        FILEPATH = f'{self.REPORTS_PATH}/{agreement_id}.pdf'
        URL = f'https://assist.org/api/artifacts/{agreement_id}'

        download_file(URL, FILEPATH)

        if download_only:
            return ''

        parsed_pdf = parser.from_file(FILEPATH)
        raw_text = parsed_pdf['content']

        clean_text = ""
        for line in raw_text.split('\n'):
            if len(line.strip()) > 0:
                clean_text += line + '\n'
            else:
                clean_text += '\n'

        return re.sub('\\n{3,}', '\\n', clean_text).strip()

if __name__ == "__main__":
    api = AssistAPI(dump_json=True)
    years = api.fetch_academic_years()
    schools = api.fetch_institutions()
    api.fetch_agreement_options_by_school(114)
    # print(api.fetch_categories_of_agreements(114, 141, 67))
    print(api.fetch_agreements_by_category(114, 141, 67, 'major'))
    # print(api.download_report_text(13739252))
