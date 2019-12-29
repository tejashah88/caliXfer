const axios = require('axios');
const memoize = require('memoizee');

const api = axios.create({
  baseURL: 'http://localhost:5000'
});

const AssistAPI = {
  fetchYears() {
    return api.get('/academic-years')
      .then(res => res.data)
      .then(years => {
        return years.map(year => {
          return { 'id': year['id'], 'fall-year': `${year['fall-year']} - ${year['fall-year']+1}` };
        });
      });
  },
  fetchSourceInstitutions() {
    return api.get('/origin-institutions').then(res => res.data);
  },
  fetchTargetInstitutions(srcSchoolId) {
    return api.get('/dest-institutions', {
      params: {
        'src_school_id': srcSchoolId
      }
    }).then(res => res.data);
  },
  fetchMajor(srcSchoolId, dstSchoolId, yearId) {
    return api.get('/fetch-agreements-by-category', {
      params: {
        'src_school_id': srcSchoolId,
        'dst_school_id': dstSchoolId,
        'year_id': yearId,
        'category_code': 'major'
      }
    }).then(res => res.data.reports);
  }
};

const MemoizedAssistAPI = Object.keys(AssistAPI)
  .reduce((acc, key) => {
    acc[key] = memoize(AssistAPI[key]);
    return acc;
  }, {});

module.exports = MemoizedAssistAPI;