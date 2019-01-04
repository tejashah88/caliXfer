from .scraper_utils import get_parsed_html

# major:            http://web2.assist.org/cgi-bin/REPORT_2/Rep2.pl?    aay=16-17   &dora=EECS     &ay=16-17    &ria=UCB    &ia=DIABLO  &dir=1  &oia=UCB    &event=19   &agreement=aa   &sia=DIABLO     &sidebar=false  &rinst=right  &mver=2     &kind=5     &dt=2
# by orig dept:     http://web2.assist.org/cgi-bin/REPORT_2/Rep2.pl?    aay=16-17   &dora=COMSC    &ay=16-17    &ria=UCB    &ia=DIABLO  &dir=1  &oia=UCB    &event=18   &agreement=aa   &sia=DIABLO     &sidebar=false  &rinst=right  &mver=2     &kind=5     &dt=2   &swap=0
# by dest dept:     http://web2.assist.org/cgi-bin/REPORT_2/Rep2.pl?    aay=16-17   &dora=COMPSCI  &ay=16-17    &ria=UCB    &ia=DIABLO  &dir=1  &oia=UCB    &event=18   &agreement=aa   &sia=DIABLO     &sidebar=false  &rinst=right  &mver=2     &kind=5     &dt=2   &swap=1

def get_text(url):
    html = get_parsed_html(url)
    return html.pre.text

def scrape_articulation_by_major(origin_school, year_range, dest_school, major):
    TARGET_URL = f'http://web2.assist.org/cgi-bin/REPORT_2/Rep2.pl?agreement=aa&event=19&ia={origin_school}&oia={dest_school}&ay={year_range}&aay={year_range}&dora={major}&sia={origin_school}&ria={dest_school}&sidebar=false&rinst=right&mver=2&kind=5&dt=2&dir=1'
    return get_text(TARGET_URL)

def scrape_articulation_by_origin_dept(origin_school, year_range, dest_school, origin_dept):
    TARGET_URL = f'http://web2.assist.org/cgi-bin/REPORT_2/Rep2.pl?agreement=aa&event=18&ia={origin_school}&oia={dest_school}&ay={year_range}&aay={year_range}&dora={origin_dept}&sia={origin_school}&ria={dest_school}&sidebar=false&rinst=right&mver=2&kind=5&dt=2&dir=1&swap=0'
    return get_text(TARGET_URL)

def scrape_articulation_by_dest_dept(origin_school, year_range, dest_school, dest_dept):
    TARGET_URL = f'http://web2.assist.org/cgi-bin/REPORT_2/Rep2.pl?agreement=aa&event=18&ia={origin_school}&oia={dest_school}&ay={year_range}&aay={year_range}&dora={dest_dept}&sia={origin_school}&ria={dest_school}&sidebar=false&rinst=right&mver=2&kind=5&dt=2&dir=1&swap=1'
    return get_text(TARGET_URL)

if __name__ == "__main__":
    final_res = scrape_articulation_by_major('DIABLO', '16-17', 'UCB', 'EECS')
    # final_res = scrape_articulation_by_origin_dept('DIABLO', '16-17', 'UCB', 'COMSC')
    # final_res = scrape_articulation_by_dest_dept('DIABLO', '16-17', 'UCB', 'COMPSCI')
    print(final_res)
