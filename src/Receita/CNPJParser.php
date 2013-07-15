<?php
namespace Receita;

class CNPJParser {

  // expected text elements
  const cnpjtipo = 'NÚMERO DE INSCRIÇÃO';
  const abertura = 'DATA DE ABERTURA';
  const nome = 'NOME EMPRESARIAL';
  const fantasia = 'TÍTULO DO ESTABELECIMENTO (NOME DE FANTASIA)';
  const atividade_principal = 'CÓDIGO E DESCRIÇÃO DA ATIVIDADE ECONÔMICA PRINCIPAL';
  const atividades_secundarias = 'CÓDIGO E DESCRIÇÃO DAS ATIVIDADES ECONÔMICAS SECUNDÁRIAS';
  const natureza_juridica = 'CÓDIGO E DESCRIÇÃO DA NATUREZA JURÍDICA';
  const logradouro = 'LOGRADOURO';
  const numero = 'NÚMERO';
  const complemento = 'COMPLEMENTO';
  const cep = 'CEP';
  const bairro = 'BAIRRO/DISTRITO';
  const municipio = 'MUNICÍPIO';
  const uf = 'UF';
  const situacao = 'SITUAÇÃO CADASTRAL';
  const data_situacao = 'DATA DA SITUAÇÃO CADASTRAL';
  const motivo_situacao = 'MOTIVO DE SITUAÇÃO CADASTRAL';
  const situacao_especial = 'SITUAÇÃO ESPECIAL';
  const data_situacao_especial = 'DATA DA SITUAÇÃO ESPECIAL';

  // possible strange activities
  const nao_informada = 'Não informada';
  const asterisks = '********';

  // array to hold all activities seen
  private $activities = array();

  // array with fields title
  private $fields = array(
    self::cnpjtipo => 'cnpj/tipo',
    self::abertura => 'abertura',
    self::nome => 'nome',
    self::fantasia => 'fantasia',
    self::atividade_principal => 'atividade_principal',
    self::atividades_secundarias => 'atividades_secundarias',
    self::natureza_juridica => 'natureza_juridica',
    self::logradouro => 'logradouro',
    self::numero => 'numero',
    self::complemento => 'complemento',
    self::cep => 'cep',
    self::bairro => 'bairro',
    self::municipio => 'municipio',
    self::uf => 'uf',
    self::situacao => 'situacao',
    self::data_situacao => 'data_situacao',
    self::motivo_situacao => 'motivo_situacao',
    self::situacao_especial => 'situacao_especial',
    self::data_situacao_especial => 'data_situacao_especial',
  );

  private function formatActivity($text)
  {
    $ret = array();
    if($text==self::nao_informada or $text==self::asterisks){
      $ret['code'] = '00.00-0-00';
      $ret['text'] = $text;
    } else {
      $split = explode(' - ',$text);
      $ret['code'] = trim($split[0]);
      $ret['text'] = trim($split[1]);
    }
    $ret['text'] = str_replace('"','',$ret['text']);
    $this->activities[$ret['code']] = $ret['text'];
    return $ret;
  }

  public function getActivities()
  {
    return $this->activities;
  }

  public function parse($html)
  {
    // array with final data
    $data = array();

    // initialize info array
    $info = array();
    foreach($this->fields as $key => $value){
      if($value=='atividade_principal' or $value=='atividades_secundarias' or $value=='natureza_juridica')
        $info[$key]['item'] = array();
      else
        $info[$key]['item'] = -1;
      $info[$key]['data'] = $value;
    }

    // create DOM document (ignore errors)
    $document = new \DOMDocument();
    @$document->loadHTML($html);

    // create XPath
    $xpath = new \DOMXPath($document);

    // get all font elements
    $fonts = $xpath->query("//font");

    // find where is the information we want
    for($i=0;$i<$fonts->length;$i++){
      $item = $fonts->item($i);
      $text = trim($item->textContent);
      if(array_key_exists($text,$info)){
        if($text==self::atividade_principal or $text==self::atividades_secundarias or $text==self::natureza_juridica)
          $info[$text]['item'][] = $i+1;
        else if($info[$text]['item']==-1)
          $info[$text]['item'] = $i+1;
      }
    }

    // get the information
    foreach($info as $key => $value){
      if($value['item']==-1) continue;

      // get the item of this element
      if(is_array($value['item']))
        $item = $fonts->item($value['item'][0]);
      else
        $item = $fonts->item($value['item']);

      switch($value['data']){
        // cnpj and type
        case 'cnpj/tipo':
          $data['cnpj'] = $item->childNodes->item(1)->textContent;
          $data['tipo'] = $item->childNodes->item(3)->textContent;
          break;

        case 'atividade_principal':
          $text = preg_replace('!\s+!',' ',trim($item->textContent));
          $data[$value['data']][] = $this->formatActivity($text);
          break;

        // may have multiple secundary activities
        case 'atividades_secundarias':
          $data[$value['data']] = array();
          for($i=0;$i<count($value['item']);$i++){
            $from = $value['item'][$i];
            $to = $info[self::natureza_juridica]['item'][$i];
            for($j=$from;$j<$to-1;$j++){
              $item = $fonts->item($j);
              $text = preg_replace('!\s+!',' ',trim($item->textContent));
              $data[$value['data']][] = $this->formatActivity($text);
            }
          }
          break;

        default:
          $data[$value['data']] = preg_replace('!\s+!',' ',trim($item->textContent));
      }
    }

    return $data;
  }

}
?>
