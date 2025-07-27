const express = require('express');
const fs = require('fs');
const app = express();
const port = 3001;

app.get('/news', (req, res) => {
  fs.readFile('news.json', 'utf8', (err, data) => {
    if (err) {
      res.status(500).send('Error reading news data');
      return;
    }
    res.json(JSON.parse(data));
  });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
