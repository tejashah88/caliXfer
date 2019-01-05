from .scraper_utils import get_parsed_html, parse_options, search_between, clean_str, simplify_names

# scrape all possible origin schools from the dropdown
def scrape_origin_schools():
    ORIGIN_PAGE = 'http://www.assist.org/web-assist/welcome.html'
    html = get_parsed_html(ORIGIN_PAGE)

    origin_schools = []
    for (txt, val) in parse_options(html, 'option'):
        origin_schools.append({
            'name': simplify_names(txt),
            'id': val.split(".")[0]
        })
    return origin_schools

# This method scrapes the possible year list ranges from the dropdown. Note that some
# transfer paths may not have up-to-date articulation agreements and might fall back
# to an older version. See 'determine_max_year_range' for more info
def scrape_year_ranges(origin_school):
    DEST_PAGE = f'http://web2.assist.org/web-assist/{origin_school}.html'
    html = get_parsed_html(DEST_PAGE)

    year_ranges = []
    for (txt, _) in parse_options(html, 'select[name="ay"] option'):
        year_ranges.append(txt)

    return year_ranges

def scrape_dest_schools(origin_school, year_range):
    DEST_PAGE = f'http://web2.assist.org/web-assist/prompt.do?ia={origin_school}&ay={year_range}'
    html = get_parsed_html(DEST_PAGE)

    dest_schools = []
    for (txt, val) in parse_options(html, 'select[name="oia"] option'):
        (dest_type, dest_name) = txt.split(":")
        if dest_type.strip().lower() == 'from':
            continue

        dest_schools.append({
            'name': simplify_names(dest_name.strip()),
            'id': search_between(val, 'oia=', '&dir')
        })

    return dest_schools

def determine_max_year_range(origin_school, year_range, dest_school):
    FINAL_CONFIG_PAGE = f'http://web2.assist.org/web-assist/articulationAgreement.do?inst1=none&inst2=none&ia={origin_school}&ay={year_range}&oia={dest_school}&dir=1'
    html = get_parsed_html(FINAL_CONFIG_PAGE)

    year_range_warning = clean_str(html.find('div', class_ = 'aynote').text)
    if len(year_range_warning) > 0:
        max_year_range = search_between(year_range_warning, 'agreement is not available. The ', ' agreement will be shown instead.')
    else:
        max_year_range = year_range

    return max_year_range

def scrape_dest_school_majors(origin_school, year_range, dest_school):
    FINAL_CONFIG_PAGE = f'http://web2.assist.org/web-assist/articulationAgreement.do?inst1=none&inst2=none&ia={origin_school}&ay={year_range}&oia={dest_school}&dir=1'
    html = get_parsed_html(FINAL_CONFIG_PAGE)

    dest_school_majors = []
    for (txt, val) in parse_options(html, 'form[name="major"] > select[name="dora"] option'):
        if 'INFO' not in val and val != 'DEC PEND' and val != '-1':
            dest_school_majors.append({ 'name': txt, 'id': val })

    return dest_school_majors

def scrape_dest_school_depts(origin_school, year_range, dest_school):
    FINAL_CONFIG_PAGE = f'http://web2.assist.org/web-assist/articulationAgreement.do?inst1=none&inst2=none&ia={origin_school}&ay={year_range}&oia={dest_school}&dir=1'
    html = get_parsed_html(FINAL_CONFIG_PAGE)

    dest_school_depts = []
    origin_school_depts = []

    is_value_valid = lambda val: 'INFO' not in val and val != 'DEC PEND' and val != '-1'

    for (txt, val) in parse_options(html, 'form[name="sendDept"] > select[name="dora"] option'):
        if is_value_valid(val):
            origin_school_depts.append({ 'name': txt, 'id': val })

    for (txt, val) in parse_options(html, 'form[name="recvDept"] > select[name="dora"] option'):
        if is_value_valid(val):
            dest_school_depts.append({ 'name': txt, 'id': val })

    return { 'origin': origin_school_depts, 'destination': dest_school_depts }

def scrape_course_articulation_possibilites():
    print(len(scrape_origin_schools()))
    print(len(scrape_year_ranges('DIABLO')))

    # final_res = scrape_year_ranges('DIABLO')
    # final_res = scrape_dest_schools('DIABLO', '16-17')
    # final_res = determine_max_year_range('DIABLO', '16-17', 'CSUB')
    # final_res = determine_max_year_range('DIABLO', '16-17', 'UCB')
    # final_res = scrape_dest_school_majors('DIABLO', '16-17', 'UCB')
    # final_res = scrape_dest_school_depts('DIABLO', '16-17', 'UCB')
    # final_res = scrape_dest_school_majors('ALAMEDA', '16-17', 'UCSFP')
    # final_res = scrape_dest_school_depts('ALAMEDA', '16-17', 'UCSFP')
    # print(final_res)
    pass

if __name__ == '__main__':
    scrape_course_articulation_possibilites()