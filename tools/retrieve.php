<?php
$base = dirname(__FILE__);
require_once $base . '/../vendor/autoload.php';
require_once $base . '/../src/Receita/CNPJClient.php';
require_once $base . '/common.php';

// constant to control delay
define("INTERVAL", 0.5);

// reports attempts and show success rate
function report(&$attempts, &$success)
{
  echo "Report: ".$success."/".$attempts." (".$success/$attempts.")\n";
}

// usage information
function usage()
{
  print "retrieve.php <csv-file>\n";
  exit();
}

// check arguments
if (!$argc>=2) {
  usage();
}

// check file is readable
$file = $argv[1];
if (!(file_exists($file) && is_readable($file))) {
  file_put_contents("php://stderr", "error: unable to open csv file.\n");
  exit();
}

// check if can write to 'data' folder
if (!(is_dir('data') && is_writable('data'))) {
  file_put_contents("php://stderr", "error: unable to find or write to" .
    " 'data' directory.\n");
  exit();
}

// read it as csv
$handle = fopen($file, "r");
$list = array();
while (($data = fgetcsv($handle, 1024, ";", '"')) !== FALSE) {
  $data[1] = fix_cnpj($data[1]);
  $list[]  = $data;
}

// captcha decode counters
$attempts = 0;
$success  = 0;

// for each cnpj
foreach($list as $item) {
  $cnpj = $item[1];
  echo $cnpj.": ";

  $cnpjClient = new Receita\CNPJClient($cnpj);
  if(!$cnpjClient) {
    echo "E\n";
    continue;
  }
  while(true) {

    // try to get information
    try {
      $html = $cnpjClient->run();
    } catch (Exception $e) {
      echo "E";
      sleep(INTERVAL);
      continue;
    }

    // attempts to decode the captcha
    $attempts++;

    // in case of no exception but false return, something went wrong with
    // Receita's website or we could not decode the captcha (keep trying)
    if ($html==false) {
      echo ".";
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
    echo "I\n";
  } else {
    echo "S\n";
    file_put_contents('data/'.$cnpj.'.html',$html);
  }
  sleep(INTERVAL);
}

// report at the end
report($attempts,$success);

?>
