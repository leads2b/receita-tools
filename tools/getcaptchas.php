<?php
$base = dirname(__FILE__);
require_once $base . '/../vendor/autoload.php';
require_once $base . '/../src/Receita/CNPJClient.php';
require_once $base . '/common.php';

// create instance to recover captchas only
$client = new Receita\CNPJClient(null,false,true);

// check if can write to 'captchas' folder
if (!(is_dir('captchas') && is_writable('captchas'))) {
  file_put_contents("php://stderr", "error: unable to find or write to" .
    " 'captchas' directory.\n");
  exit();
}

// user information
echo "retrieving captchas forever\n";
echo "abort when you had enough\n";

// get captchas and write them to folder
while(true){
  $captchaPath = $client->run();
  if($captchaPath){
    $file = tempnam('./captchas/','cap');
    if(copy($captchaPath,$file))
      rename($file,$file.'.gif');
  }
  sleep(0.5);
  echo ".";
}
?>
