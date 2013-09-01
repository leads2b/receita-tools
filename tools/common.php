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

?>
