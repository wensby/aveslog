const axios = require('axios');

axios.defaults.baseURL = 'http://api-service:3002';

const setupAxios = (req, res, next) => {
  if (req.headers['accesstoken']) {
    req.axios = axios.create({
      headers: {
        accessToken: req.headers['accesstoken']
      }
    });
    next();
  }
  else {
    req.axios = axios.create();
    next();
  }
};

module.exports = { setupAxios };
