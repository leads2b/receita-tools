<?php

// allow only numeric data
function fix_cnpj($cnpj){
  $cnpj = trim($cnpj);
  $size = strlen($cnpj);

  $ret = "";
  for($i=0;$i<$size;$i++)
    if($cnpj[$i]>='0' and $cnpj[$i]<='9')
      $ret .= $cnpj[$i];
  return $ret;
}

// open data directory and parse each file
function find_parse_data($parser){
  $cnpjData = array();
  if($handle = opendir('data')){
    while (false !== ($file = readdir($handle))){
      $path = 'data/'.$file;
      if(is_file($path)){
        $cnpj = basename($path,'.html');
        $data = file_get_contents($path);
        $cnpjData[$cnpj] = $parser->parse($data);
      }
    }
    closedir($handle);
  }
  return $cnpjData;
}

?>
