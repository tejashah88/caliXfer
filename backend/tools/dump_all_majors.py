import os
import json

from tqdm import tqdm
from assist_api import AssistAPI

if __name__ == '__main__':
    api = AssistAPI()
    years = api.fetch_academic_years()
    src_schools = api.fetch_source_schools()

    PARENT_DIR = os.path.dirname(__file__)
    EXTRACTED_JSON_PATH = f'{PARENT_DIR}/json-dump/extracted'
    ALL_MAJORS_PATH = f'{EXTRACTED_JSON_PATH}/all-majors.json'

    all_majors = []

    for src_school in tqdm(src_schools):
        dst_schools = api.fetch_destination_schools(src_school['id'])
        for dst_school in dst_schools:

            if dst_school['sending-year-ids']:
                for year_id in dst_school['sending-year-ids']:
                    agreements = api.fetch_agreements_by_category(src_school['id'], dst_school['id'], year_id, 'major')
                    all_majors += [agreement['name'].strip() for agreement in agreements['reports']]

            if dst_school['receiving-year-ids']:
                for year_id in dst_school['receiving-year-ids']:
                    agreements = api.fetch_agreements_by_category(src_school['id'], dst_school['id'], year_id, 'major')
                    all_majors += [agreement['name'].strip() for agreement in agreements['reports']]

    os.makedirs(EXTRACTED_JSON_PATH, exist_ok=True)
    with open(ALL_MAJORS_PATH, 'w') as fp:
        json.dump(all_majors, fp, indent=4)

