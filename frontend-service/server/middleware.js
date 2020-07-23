const axios = require('axios');

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
