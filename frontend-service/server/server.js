const express = require('express');

const app = express();
app.use(express.json())

app.set("port", process.env.PORT || 3003);

// Serve static assets in production
if (process.env.NODE_ENV === 'production') {

  app.use(express.static('client/build', {
    etag: true,
    lastModified: true,
    setHeaders: (res, path) => {
      res.setHeader(
        'Cache-Control',
        /\\.[0-9a-f]{8}\\./.test(path) ? 'max-age=31536000' : 'no-cache'
      );
    },
  }));
}

app.use('/api', require('./api.js'));

// Fallback to index.html in production
if (process.env.NODE_ENV === 'production') {
  app.get('*', (req, res) => {
    res.sendFile(__dirname + '/client/build/index.html');
  });
}

app.listen(app.get('port'));
console.log('App is listening on port ' + app.get('port'));
