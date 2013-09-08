var exec = require('child_process').exec;
var fs = require('fs');
var express = require('express');
var app = express();

function isNumeric(input){
  var RE = /^\d*$/;
  return (RE.test(input));
}

app.configure(function(){
  app.use('/receita/v1/cnpj/images', express.static(__dirname + '/images', 86400000));
});

app.get('/receita/v1/cnpj/:cnpj:ext(\.json|\.html|)',function(req,res){
  if(req.params.cnpj.length != 14 || !isNumeric(req.params.cnpj))
    res.send(200, { error: 'invalid' });
  else {
    child = exec('php engine.php '+req.params.cnpj+' '+req.params.ext,
      function (err,stdout,stderr){
        if (err === null) {
          if(req.params.ext == '.html'){
            res.send(200, stdout);
          } else {
            var obj = JSON.parse(stdout);
            res.send(200, obj);
          }
        } else {
          if(err.code == 2) {
            res.send(200, { error: 'cnpj rejected' });
          } else {
            res.send(500, { error: 'Server Internal Error' });
          }
        }
      });
  }
});

app.listen(8080);
