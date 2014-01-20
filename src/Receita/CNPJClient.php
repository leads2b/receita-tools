<?php
namespace Receita;

use Guzzle\Http\Client;
use Guzzle\Plugin\Cookie\CookiePlugin;
use Guzzle\Plugin\Cookie\CookieJar\ArrayCookieJar;

class CNPJClient {

  // constants
  const receitaURL = 'http://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/';

  // attributes
  private $client;
  private $verbose;
  private $captchaOnly;
  private $base;

  // temp files
  private $captcha;
  private $filter;
  private $tessout;

  public function __construct($cnpj, $verbose=false, $captchaOnly=false)
  {
    // store attributes
    $this->cnpj        = $cnpj;
    $this->verbose     = $verbose;
    $this->captchaOnly = $captchaOnly;

    // base directory and Guzzle cliente storage
    $this->base    = dirname(__FILE__);
    $this->client  = new Client(self::receitaURL,array('redirect.disable' => true));

    // add the cookie plugin (so cookies are kept beetwen requests)
    $cookiePlugin = new CookiePlugin(new ArrayCookieJar());
    $this->client->addSubscriber($cookiePlugin);

    // create some temporary files for captcha management
    $this->captcha = tempnam(sys_get_temp_dir(),'cap');
    $this->filter  = tempnam(sys_get_temp_dir(),'fil');
    $this->tessout = tempnam(sys_get_temp_dir(),'tes');

    if(!$this->captcha or !$this->filter or !$this->tessout)
      return false;
  }

  public function __destruct()
  {
    @unlink($this->captcha);
    @unlink($this->captcha.'.gif');
    @unlink($this->filter);
    @unlink($this->filter.'.gif');
    @unlink($this->tessout);
    @unlink($this->tessout.'.txt');
  }

  private function fix_captcha($text)
  {
    $text = strtoupper($text);
    $n = strlen($text);
    $res = '';
    for($i=0;$i<$n;$i++){
      if($text[$i]>='0' and $text[$i]<='9')
        $res .= $text[$i];
      if($text[$i]>='A' and $text[$i]<='Z')
        $res .= $text[$i];
    }
    return $res;
  }

  private function get_location($headers)
  {
    $headers = explode("\n",$headers);
    for($i=0;$i<count($headers);$i++){
      $header = explode(':',$headers[$i]);
      if($header[0]=='Location')
        return trim($header[1]);
    }
    return false;
  }

  private function filter($file)
  {
    $img = @imagecreatefromgif($file);
    if(!$img) return false;
    return false;
  }

  public function run()
  {
    // get first two pages
    $response = $this->client->get('cnpjreva_solicitacao.asp')->send();
    if($response->getStatusCode()!=200) return false;

    $response = $this->client->get('cnpjreva_solicitacao2.asp')->send();
    if($response->getStatusCode()!=200) return false;

    // parse the response data
    $html = $response->getBody()->__toString();
    if(!$html) return false;

    // create DOM document (ignore errors)
    $document = new \DOMDocument();
    @$document->loadHTML($html);

    // find the image with id imgcaptcha
    $xpath = new \DOMXPath($document);
    $captcha = $xpath->query("//img[@id='imgcaptcha']");

    // get the captcha URL
    $captchaURL = $captcha->item(0)->attributes->getNamedItem('src')->value;

    // download and save the captcha
    $response = $this->client->get($captchaURL)->send();
    if($response->getStatusCode()!=200) return false;

    $img = $response->getBody()->__toString();
    $file = fopen($this->captcha.'.gif','w');
    fwrite($file,$img);
    fclose($file);

    // stop processing if only needs the captcha (return the captcha path)
    if($this->captchaOnly)
      return $this->captcha.'.gif';

    // filter
    exec('python "'.$this->base.'/CaptchaFilter.py" "'.$this->captcha.'.gif" "'.$this->filter.'.gif"',$output);
    exec('tesseract "'.$this->filter.'.gif" "'.$this->tessout.'" &>/dev/null',$output);
    $captcha_text = trim(file_get_contents($this->tessout.'.txt'));
    $captcha_text = $this->fix_captcha($captcha_text);

    // find the form viewstate input
    $viewstate = $xpath->query("//input[@id='viewstate']");
    $viewstate = $viewstate->item(0)->attributes->getNamedItem('value')->value;

    // its known that the captcha should be 6 chars long, so dont even bother
    // trying anything other than that
    if(strlen($captcha_text)!=6) return false;

    if($this->verbose)
      echo "Trying captcha: ".$captcha_text."\n";

    // post data (do not redirect)
    $response = $this->client->post('valida.asp', null, array(
      'origem' => 'comprovante',
      'viewstate' => $viewstate,
      'cnpj' => $this->cnpj,
      'captcha' => $captcha_text,
      'captchaAudio' => '',
      'submit1' => 'Consultar',
      'search_type' => 'cnpj'
    ))->send();
    if($response->getStatusCode()!=302) return false;

    // get location (if captcha ok or not)
    // and check for wrong captcha
    $location = $this->get_location($response->getRawHeaders());
    if(!$location or !strpos($location,"Vstatus.asp")) return false;

    // its valid captcha, but we should check if the cnpj is valid
    $response = $this->client->get($location)->send();
    if($response->getStatusCode()!=302) return false;
    $location = $this->get_location($response->getRawHeaders());
    if(strpos($location,'Erro')>0) return 'bad';

    $response = $this->client->get('Cnpjreva_Campos.asp')->send();
    if($response->getStatusCode()!=302) return false;

    $response = $this->client->get('Cnpjreva_Comprovante.asp')->send();
    if($response->getStatusCode()!=200) return false;

    return $response->getBody()->__toString();
  }

}
?>
