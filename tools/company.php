<?php
$base = dirname(__FILE__);
require_once $base . '/../vendor/autoload.php';
require_once $base . '/../src/Receita/CNPJClient.php';
require_once $base . '/../src/Receita/CNPJParser.php';
require_once $base . '/common.php';

// helpers
$type = array(
  'MATRIZ' => 'M',
  'FILIAL' => 'F',
);

$fields = array(
  'cnpj','tipo','abertura','nome','fantasia','natureza_juridica','logradouro',
  'numero','complemento','cep','bairro','municipio','uf','situacao',
  'data_situacao','motivo_situacao','situacao_especial',
  'data_situacao_especial'
);

// check if can read 'data' folder
if (!(is_dir('data') && is_readable('data'))) {
  file_put_contents("php://stderr", "error: unable to find" .
    " 'data' directory.\n");
  exit();
}

// parser instance
$parser = new Receita\CNPJParser();

// data array
$cnpjData = find_parse_data($parser);

// write output csv file to stdout
$out = fopen('php://output','w');
foreach($cnpjData as $cnpj=>$data){
  $outData = array();
  foreach($fields as $field){
    if($field=='tipo')
      $outData[] = $type[$data[$field]];
    else
      $outData[] = $data[$field];
  }
  fputcsv($out,$outData,';','"');
}
fclose($out);
?>
