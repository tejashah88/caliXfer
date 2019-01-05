import os
import json

from old_site.scrape_possibilities import scrape_dest_schools, scrape_dest_school_majors, determine_max_year_range
from old_site.scrape_content import scrape_articulation_by_major
from old_site.parse_agreements import parse_major_agreement

from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)

def write_text(filename, contents):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as file:
        file.write(contents)

write_json = lambda filename, json_contents: write_text(filename, json.dumps(json_contents, ensure_ascii=False, indent=2))

def dump_dvc_dest_schools_with_majors():
    major_count = 0
    fail_count = 0
    ROOT_DIR = '../data/dump-dvc-info/'

    origin_school = 'DIABLO'
    target_year_range = '16-17'

    dest_schools = scrape_dest_schools(origin_school, target_year_range)
    write_json(ROOT_DIR + 'destination_schools.json', dest_schools)

    for dest in dest_schools:
        print(dest)
        majors = scrape_dest_school_majors(origin_school, target_year_range, dest['id'])
        actual_year_range = determine_max_year_range(origin_school, target_year_range, dest['id'])

        write_json(ROOT_DIR + f'majors/{dest["id"]}.json', majors)
        print('# of majors:', len(majors))

        for major in majors:
            print(origin_school, actual_year_range, dest['id'], major['id'])
            try:
                agreement = scrape_articulation_by_major(origin_school, actual_year_range, dest['id'], major['id'])
                write_text(ROOT_DIR + f'agreements/{dest["id"]}/{major["id"]}.txt', agreement)
                major_count += 1
            except Exception as ex:
                print(f"     {Back.RED}GET OPERATION FAILED! REASON: {ex}")
                fail_count += 1


    print('total # of agreements processed:', major_count)
    print('total # of agreements failed:', fail_count)

if __name__ == '__main__':
    dump_dvc_dest_schools_with_majors()