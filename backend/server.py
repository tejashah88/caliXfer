import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# import bjoern
# import pymongo

# apparently trying to import modules from the parent directory is near impossible without this hack
import sys
sys.path.append("..")


from tools.assist_api import AssistAPI
# from tools.old_site.scrape_possibilities import *
# from tools.old_site.scrape_content import *

app = Flask(__name__)
CORS(app)
api = AssistAPI()

@app.route('/fetch-src-institutions')
def fetch_src_institutions():
    return jsonify(api.fetch_institutions())

@app.route('/fetch-dst-institutions')
def fetch_dst_institutions():
    src_school_id = request.args.get('src_school_id')
    return jsonify(api.fetch_agreement_options_by_school(src_school_id))

@app.route('/fetch-agreements-by-category')
def fetch_agreements_by_category():
    src_school_id = request.args.get('src_school_id')
    dst_school_id = request.args.get('dst_school_id')
    year_id = request.args.get('year_id')
    category_code = request.args.get('category_code')
    return jsonify(api.fetch_agreements_by_category(src_school_id, dst_school_id, year_id, category_code))

# @app.route('/get-origin-schools')
# def get_origin_schools():
#     return jsonify(scrape_origin_schools())

# @app.route('/get-year-ranges')
# def get_year_ranges(origin):
#     return jsonify(scrape_year_ranges(origin))

# @app.route('/get-destination-schools')
# def get_dest_schools(origin, years):
#     return jsonify(scrape_dest_schools(origin, years))

# @app.route('/get-possible-majors')
# def get_possible_majors(origin, years, dest):
#     return jsonify(scrape_dest_majors(origin, years, dest))

# @app.route('/get-agreement')
# def get_articulation_agreement_by_major(origin, years, dest, major):
#     return scrape_articulation_by_major(origin, years, dest, major)

if __name__ == '__main__':
    app.run(debug=True)
    # IP = '127.0.0.1'
    # PORT = 8080
    # print(f'Running server on {IP}:{PORT}')
    # bjoern.run(app.wsgi_app, IP, PORT)