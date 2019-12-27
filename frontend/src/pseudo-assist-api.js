const axios = require('axios');
const memoize = require("memoizee");

const api = axios.create({
  baseURL: 'http://localhost:5000'
});

const AssistAPI = {
  fetchSourceInstitutions() {
    return api.get('/fetch-src-institutions').then(res => res.data);
  },
  fetchTargetInstitutions(srcSchoolId) {
    return api.get('/fetch-dst-institutions', { params: { 'src_school_id': srcSchoolId }}).then(res => res.data);
  },
  fetchMajor(srcSchoolId, dstSchoolId, yearId) {
    return api.get('/fetch-agreements-by-category', { params: { 'src_school_id': srcSchoolId, 'dst_school_id': dstSchoolId, 'year_id': yearId, 'category_code': 'major' }}).then(res => res.data.reports);
  }
};

const MemoizedAssistAPI = Object.keys(AssistAPI)
  .reduce((acc, key) => {
    acc[key] = memoize(AssistAPI[key]);
    return acc;
  }, {});

module.exports = MemoizedAssistAPI;