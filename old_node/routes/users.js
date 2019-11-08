var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  let json = {'Tracy': ['Boo', 'JesusFreak1998', 'Blue'], 'Stuart': ['Bae', 'Enters', 'Red']};

  res.send(json);
});

module.exports = router;

/*
Sample JSON

user = {
	'Password': pass,
	'Colors': [self, other]
	'Names': [self, other]

*/
