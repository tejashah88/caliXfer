from assist_api import AssistAPI

if __name__ == '__main__':
    api = AssistAPI(dump_json=True)
    years = api.fetch_academic_years()
    src_schools = api.fetch_institutions()
    for src_school in src_schools:
        print(src_school)

