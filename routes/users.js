var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  let json = {'Tracy': ['Rice', 'Bae', 'Blue'], 'Stuart': ['Enters', 'Boo', 'Red']};

  res.send(json);
});

module.exports = router;
