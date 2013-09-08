<?php
$base = dirname(__FILE__);
require_once $base . '/../vendor/autoload.php';
require_once $base . '/../src/Receita/CNPJClient.php';
require_once $base . '/../src/Receita/CNPJParser.php';
require_once $base . '/../tools/common.php';

// constant to control delay
define("INTERVAL", 0.5);
define("CACHETTL", 60*60*24*2);

// check arguments
if(!$argc>=2){
  exit(100);
}

// decide output format
if($argc>=3){
  $format = $argv[2];
} else {
  $format = 'json';
}

if(!is_dir($base.'/cache') or !is_writable($base.'/cache')){
  exit(101);
}

// get cnpj
$cnpj = $argv[1];

// try to find in cache
$htmlPath = $base.'/cache/'.$cnpj.'.html';
$jsonPath = $base.'/cache/'.$cnpj.'.json';
if(is_file($jsonPath) and is_readable($jsonPath) and time()-filemtime($jsonPath) <= CACHETTL){
  $data = file_get_contents($jsonPath);
  if($data=='bad') exit(2);
  if($format=='json')
    echo $data;
  else {
    echo file_get_contents($htmlPath);
  }
  exit(0);
}

// captcha decode counters
$attempts = 0;
$success  = 0;

// for this cnpj
$cnpjClient = new Receita\CNPJClient($cnpj);
if(!$cnpjClient) {
  exit(102);
}

while(true) {

  // try to get information
  try {
    $html = $cnpjClient->run();
  } catch (Exception $e) {
    exit(1);
  }

  // attempts to decode the captcha
  $attempts++;

  // in case of no exception but false return, something went wrong with
  // Receita's website or we could not decode the captcha (keep trying)
  if ($html==false) {
    sleep(INTERVAL);
  } else {
    // or break in the case of success
    break;
  }
}

// captcha decode success
$success++;

// 'bad' is returned in case of invalid CNPJ
if ($html=='bad') {
  file_put_contents($jsonPath,'bad');
  exit(2);
} else {
  $parser = new Receita\CNPJParser();
  $data = $parser->parse($html);
  file_put_contents($jsonPath,json_encode($data));
  file_put_contents($htmlPath,iconv('ISO-8859-1','UTF-8',$html));
  if($format=='json')
    echo json_encode($data);
  else
    echo $html;
}
?>
