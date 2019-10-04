const express = require('express');
const path = require('path');
const app = express();

const hashedFilePathPattern = new RegExp('\\.[0-9a-f]{8}\\.');

app.use(express.static(path.join(__dirname, 'build'), {
  etag: true,
  lastModified: true,
  setHeaders: function (res, path) {
    if (hashedFilePathPattern.test(path)) {
      res.setHeader('Cache-Control', 'max-age=31536000');
    }
    else {
      res.setHeader('Cache-Control', 'no-cache');
    }
  },
}));

app.get('/*', function(req, res) {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(3003);
