const express = require('express');

const app = express();
app.use(express.json())

const port = process.env.PORT || 3003;
app.set("port", port);

// Serve static assets in production
if (process.env.NODE_ENV === 'production') {
  const hashedFilePathPattern = new RegExp('\\.[0-9a-f]{8}\\.');

  app.use(express.static('client/build', {
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
}

app.use('/api', require('./api.js'));

// Handles any requests that don't match the ones above
if (process.env.NODE_ENV === 'production') {
  app.get('*', (req, res) => {
    res.sendFile(__dirname + '/client/build/index.html');
  });
}

app.listen(port);
console.log('App is listening on port ' + port);
