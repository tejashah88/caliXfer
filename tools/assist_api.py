import re
import json
import os

from tika import parser

from scraper_utils import resilient_get, download_file, clean_str

class AssistAPI:
    """
    A wrapper class for fetching resources from assist.org's (hidden) API
    """
    RAW_JSON_PATH = './json-dump/raw'
    CLEAN_JSON_PATH = './json-dump/clean'

    def __init__(self, dump_json=False, save_reports=True):
        self.dump_json = dump_json
        self.save_reports = save_reports

        if self.dump_json:
            os.makedirs(self.RAW_JSON_PATH, exist_ok=True)
            os.makedirs(self.CLEAN_JSON_PATH, exist_ok=True)

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
        raw_json = self._read_raw_json(filepath)
        if raw_json is None:
            raw_json = json.loads(resilient_get(url))

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

    def fetch_institutions(self):
        FILEPATH = 'institutions.json'
        URL = 'https://assist.org/api/institutions'

        raw_schools = self._obtain_raw_json(FILEPATH, URL)

        clean_schools = []
        for school in raw_schools:
            clean_schools.append({
                'id': school['id'],
                'names': {
                    'current': school['names'][0]['name'],
                    'alternative': [{'name': alt_name['name'], 'from-year': alt_name['fromYear']} for alt_name in school['names'][1:]]
                },
                'code': school['code'].strip(),
                'use-legacy-report': school['prefers2016LegacyReport'],
                'community-college': school['isCommunityCollege'],
            })

        if self.dump_json:
            self._dump_clean_json(clean_schools, FILEPATH)

        return clean_schools

    def fetch_agreement_options_by_school(self, start_school_id):
        FILEPATH = f'agreement-options/{start_school_id}/options.json'
        URL = f'https://assist.org/api/institutions/{start_school_id}/agreements'

        raw_options = self._obtain_raw_json(FILEPATH, URL)

        clean_options = []
        for option in raw_options:
            clean_options.append({
                'school-id': option['institutionParentId'],
                'school-name': option['institutionName'],
                'school-code': option['code'],
                'community-college': option['isCommunityCollege'],
                'sending-year-ids': option.get('sendingYearIds'),
                'receiving-year-ids': option.get('receivingYearIds')
            })

        if self.dump_json:
            self._dump_clean_json(clean_options, FILEPATH)

        return clean_options

    def fetch_categories_of_agreements(self, start_school_id, end_school_id, year_id):
        FILEPATH = f'categories/{start_school_id}/{end_school_id}/{year_id}/categories.json'
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
        FILEPATH = f'categories/{start_school_id}/{end_school_id}/{year_id}/{category_code}/agreements.json'
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


    def download_report_text(self, agreement_id):
        FILEPATH = f'reports/{agreement_id}/report.pdf'
        URL = f'https://assist.org/api/artifacts/{agreement_id}'

        download_file(URL, FILEPATH)

        parsed_pdf = parser.from_file(filename)
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
    print(api.fetch_agreements_by_category(114, 141, 67, 'dept'))
    # print(api.download_report_text(13739252))
