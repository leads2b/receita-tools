<?php
$base = dirname(__FILE__);
require_once $base . '/../vendor/autoload.php';
require_once $base . '/../src/Receita/CNPJParser.php';
require_once $base . '/common.php';

function usage()
{
  print "activities.php [-m|-s|-l]\n";
  exit();
}

// check arguments
if(!$argc>=2){
  usage();
}

// kind of activities
$mainActivities = false;
$secondaryActivities = false;
$listActivities = false;

if($argv[1]=='-m'){
  $mainActivities = true;
}

if($argv[1]=='-s'){
  $secondaryActivities = true;
}

if($argv[1]=='-l'){
  $listActivities = true;
}

if(!$mainActivities and !$secondaryActivities and !$listActivities){
  usage();
}

// check if can read 'data' folder
if (!(is_dir('data') && is_readable('data'))) {
  file_put_contents("php://stderr", "error: unable to find" .
    " 'data' directory.\n");
  exit();
}

// parser instance
$parser = new Receita\CNPJParser();

// get data
$cnpjData = find_parse_data($parser);

// write output csv file to stdout
$out = fopen('php://output','w');
if($listActivities){
  $activities = $parser->getActivities();
  foreach($activities as $activity=>$description){
    $outData = array();
    $outData[] = $activity;
    $outData[] = $description;
    fputcsv($out,$outData,';','"');
  }
} else {
  foreach($cnpjData as $cnpj=>$data){
    if($mainActivities){
      $field = 'atividade_principal';
    }

    if($secondaryActivities){
      $field = 'atividades_secundarias';
    }

    for($i=0;$i<count($data[$field]);$i++){
      if($secondaryActivities and $data[$field][$i]['code']=='00.00-0-00')
        continue;

      $outData = array();
      $outData[] = $cnpj;
      $outData[] = $data[$field][$i]['code'];
      fputcsv($out,$outData,';','"');
    }
  }
}
fclose($out);

?>
