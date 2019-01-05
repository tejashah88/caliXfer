import hug
import bjoern
import pymongo

from tools.old_site.scrape_possibilities import *
from tools.old_site.scrape_content import *

@hug.get('/options/origins')
def get_origin_schools():
    return scrape_origin_schools()

@hug.get('/options/year-range')
def get_year_ranges(origin):
    return scrape_year_ranges(origin)

@hug.get('/options/destinations')
def get_dest_schools(origin, years):
    return scrape_dest_schools(origin, years)

@hug.get('/options')
def get_possible_majors(origin, years, dest):
    return scrape_dest_majors(origin, years, dest)

@hug.get('/agreements/major', output=hug.output_format.text)
def get_articulation_agreement_by_major(origin, years, dest, major):
    return scrape_articulation_by_major(origin, years, dest, major)

if __name__ == '__main__':
    IP = '127.0.0.1'
    PORT = 8080
    print(f'Running server on {IP}:{PORT}')
    bjoern.run(__hug_wsgi__, IP, PORT)