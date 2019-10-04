const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(path.join(__dirname, 'build', 'media'), {
  maxAge: 86400000,
}));
app.use(express.static(path.join(__dirname, 'build')));

app.get('/*', function(req, res) {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.listen(3003);
