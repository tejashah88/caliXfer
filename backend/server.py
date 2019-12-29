import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# import bjoern
# import pymongo

from tools.assist_api import AssistAPI

app = Flask(__name__)
CORS(app)
api = AssistAPI()

@app.route('/academic-years')
def fetch_years():
    return jsonify(api.fetch_academic_years())

@app.route('/origin-institutions')
def fetch_src_institutions():
    return jsonify(api.fetch_institutions())

@app.route('/dest-institutions')
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

if __name__ == '__main__':
    app.run(debug=True)
    # IP = '127.0.0.1'
    # PORT = 8080
    # print(f'Running server on {IP}:{PORT}')
    # bjoern.run(app.wsgi_app, IP, PORT)