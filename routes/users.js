var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  let json = {};
  json['users'] = {'test': 'pass', 'john': 'smith'};

  res.send(json);
});

module.exports = router;
