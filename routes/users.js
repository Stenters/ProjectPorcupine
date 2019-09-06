var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  let json = {};
  json['users'] = {'test': 'pass', 'john': 'smith', 'Tracy': 'jesusfreak1998', 'Stuart': 'Enters'};

  res.send(json);
});

module.exports = router;
