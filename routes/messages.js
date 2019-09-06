var express = require('express');
var router = express.Router();
let fs = require('fs');
let bodyParser = require('body-parser');
let path = "./public/messageLog.html"

router.get('/', function (req, res, next) {
    fs.readFile(path, function (err, data) {
        console.log(`Response is (${err}, ${data})`);
        res.write(data);
        res.end();
    });
});

router.post('/', function (req, res, next) {
    let text = req.body.msg;
    fs.appendFile(path, text, function (err) {
        if (err) throw err;
        console.log('Saved!');
    });
});

module.exports = router;
