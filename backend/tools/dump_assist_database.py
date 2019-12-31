from assist_api import AssistAPI

if __name__ == '__main__':
    api = AssistAPI(dump_json=True)
    years = api.fetch_academic_years()
    src_schools = api.fetch_source_schools()
    for src_school in src_schools:
        print('src school ID', src_school['id'])
        dst_schools = api.fetch_destination_schools(src_school['id'])
        for dst_school in dst_schools:
            print('  dst school ID', dst_school['id'])

            if dst_school['sending-year-ids']:
                for year_id in dst_school['sending-year-ids']:
                    print('    year ID (send)', year_id)
                    agreements = api.fetch_agreements_by_category(src_school['id'], dst_school['id'], year_id, 'major')

                    for agreement in agreements['reports']:
                        print('      agreement ID', agreement['id'])
                        api.download_report_text(agreement['id'], download_only=True)

            if dst_school['receiving-year-ids']:
                for year_id in dst_school['receiving-year-ids']:
                    print('    year ID (receive)', year_id)
                    agreements = api.fetch_agreements_by_category(src_school['id'], dst_school['id'], year_id, 'major')

                    for agreement in agreements['reports']:
                        print('      agreement ID', agreement['id'])
                        api.download_report_text(agreement['id'], download_only=True)

