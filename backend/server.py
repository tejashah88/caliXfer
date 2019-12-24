from flask import Flask, jsonify

# import bjoern
# import pymongo

# apparently trying to import modules from the parent directory is near impossible without this hack
import sys
sys.path.append("..")

from tools.old_site.scrape_possibilities import *
from tools.old_site.scrape_content import *

app = Flask(__name__)

@app.route('/get-origin-schools')
def get_origin_schools():
    return jsonify(scrape_origin_schools())

@app.route('/get-year-ranges')
def get_year_ranges(origin):
    return jsonify(scrape_year_ranges(origin))

@app.route('/get-destination-schools')
def get_dest_schools(origin, years):
    return jsonify(scrape_dest_schools(origin, years))

@app.route('/get-possible-majors')
def get_possible_majors(origin, years, dest):
    return jsonify(scrape_dest_majors(origin, years, dest))

@app.route('/get-agreement')
def get_articulation_agreement_by_major(origin, years, dest, major):
    return scrape_articulation_by_major(origin, years, dest, major)

if __name__ == '__main__':
    app.run(debug=True)
    # IP = '127.0.0.1'
    # PORT = 8080
    # print(f'Running server on {IP}:{PORT}')
    # bjoern.run(app.wsgi_app, IP, PORT)