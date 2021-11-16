import os
import json
import re

def replaceAll(str, old, new):
    while old in str:
        str = str.replace(old, new)
    return str.strip()

if __name__ == '__main__':
    PARENT_DIR = os.path.dirname(__file__)
    EXTRACTED_JSON_PATH = f'{PARENT_DIR}/json-dump/extracted'
    os.makedirs(EXTRACTED_JSON_PATH, exist_ok=True)

    ALL_RAW_MAJORS_PATH = f'{EXTRACTED_JSON_PATH}/all-majors.json'
    ALL_CLEANED_MAJORS_PATH = f'{EXTRACTED_JSON_PATH}/all-majors-cleaned.json'

    with open(ALL_RAW_MAJORS_PATH, 'r') as fp:
        all_majors = json.load(fp)

    print('Number of all majors found:', len(all_majors))
    unique_majors = sorted(list(set(all_majors)))
    print('Number of unique majors found (before filtering):', len(unique_majors))

    start_invalid = ('-', '=', '>')

    truly_unique_majors = unique_majors
    truly_unique_majors = [' '.join([word.title() if len(word) > 3 else word for word in major.split()]) for major in truly_unique_majors]
    truly_unique_majors = [re.sub(r'([/, -]*\(?(([B]\.?([F]\.?)?\W*[SAM])|([A]\.?\W*[B]))[.)]?[, \n)]*)', ' ', major).strip() for major in truly_unique_majors]
    truly_unique_majors = [replaceAll(major, '&', 'and').strip() for major in truly_unique_majors]
    truly_unique_majors = [major[:-4] if major.endswith('and') else major for major in truly_unique_majors]
    truly_unique_majors = [major[:-3] if major.endswith('or') else major for major in truly_unique_majors]
    truly_unique_majors = [major.strip() for major in truly_unique_majors if not major.startswith(start_invalid) and '{' not in major and '}' not in major]
    truly_unique_majors = sorted(list(set(truly_unique_majors)))
    print('Number of unique majors found (after filtering):', len(truly_unique_majors))

    with open(ALL_CLEANED_MAJORS_PATH, 'w') as fp:
        json.dump(truly_unique_majors, fp, indent=4)
    # [print(major) for major in truly_unique_majors[:100]]
