receita-tools
=============

|pypi| |license|

**Idiomas do README:** |ptbr| |en|

Um conjunto de ferramentas para permitir a automatização das informações
das empresas do Brasil do site da Receita Federal Brasileira. Este conjunto
de ferramentas utiliza o webservice
`receitaws.com.br <http://receitaws.com.br>`_ para recuperar as informações
das empresas que deseja.

.. contents::
   :local:

.. |pypi| image:: https://img.shields.io/pypi/v/receita-tools.svg?style=flat-square
    :target: https://pypi.python.org/pypi/receita-tools

.. |license| image:: https://img.shields.io/dub/l/vibe-d.svg?style=flat-square

.. |ptbr| image:: https://flagicons.lipis.dev/flags/4x3/br.svg
    :target: https://github.com/leads2b/receita-tools/blob/master/README.rst
    :height: 20px

.. |en| image:: https://flagicons.lipis.dev/flags/4x3/us.svg
    :target: https://github.com/leads2b/receita-tools/blob/master/README.en.rst
    :height: 20px

Instalação
----------

Para instalar as ferramentas a maneira mais fácil é utilizar o ``pip``::

    pip install receita-tools


Ferramentas para trabalhar com os dados da Receita
--------------------------------------------------

Este conjunto de ferramentas irá permitir recuperar informações de empresas
do site da Receita de uma forma simples. É possível recuperar informações
de várias empresas ao mesmo tempo. A ferramenta permite que arquivos CSV
seja criados a partir dos dados das empresas facilitando sua importação
para o seu sistema.

O Webservice
++++++++++++

Os comandos disponíveis utilizam o webservice **ReceitaWS**. Aqui estão
alguns links importantes sobre como o sistema funciona para leitura antes
de iniciar a utilização:

* `Documentação da API`_
* `FAQ`_
* `Preços`_

.. _Documentação da API: https://www.receitaws.com.br/api
.. _FAQ: https://www.receitaws.com.br/faq
.. _Preços: https://www.receitaws.com.br/pricing

O comando ``get``
+++++++++++++++++

O progrma de recuperação dos dados funciona com base em um arquivo CSV
contendo informações sobre os CNPJs que devem ser consultados. Este arquivo
deve ter ao menos uma coluna, e a primeira deve ser aquela que contém os CNPJs
das empresas que deseja as informações.

Utiliza o comando ``receita get cnpj.csv`` para iniciar as consultas baseado
neste aquivo CSV. Por padrão os dados recuperados serão salvos no diretório
``data`` relativo ao diretório de onde o comando foi executado. É possível
alterar o diretório de saída utilizando a oção ``--output``. É possível
especificar diretórios absolutos ou relativos.

Existem duas APIs para consulta, sendo uma Pública e outra Comercial. Abaixo
descrevemos como utilizar cada uma delas.

API Pública
***********

Por padrão o comando ``get`` utiliza a API Pública para recuperar as
informações sobre as empresas. Não é necessário fazer nenhuma outra
configuração, então você está pronto para utilizar o comando. Por exemplo,
para recuperar dados das empresas listadas no arquivo ``list.csv`` e salvar
os resultados no diretório ``cnpj_data`` usando a API Pública::

    receita get list.csv --output cnpj_data

API Comercial
*************

Para usar a API comercial é preciso prover duas informações extras: a
quantidade máxima de depreciação dos dados retornados (em dias) e o token
de acesso à API. Você pode gerar este token acessando seu painel de controle
no site ReceitaWS.

Assim que você tiver esta informações, é preciso prover o seu token como
a variável de ambiente ``RWS_TOKEN``. O parâmetro de depreciação precisa ser
indicado usando a opção ``-d``.

Para setar a variável de ambiente você pode usar o comando ``export`` ou
simplesmente definir a variável ao executar o comando. Este é um exemplo
utilizando o comando ``export`` e uma tolerância de 20 dias::

    export RWS_TOKEN="<my-token>"
    receita get list.csv --output cnpj_data -d 20

O comando ``build``
+++++++++++++++++++

Após utilizar o comando ``get`` os dados das empresas terão sido salvos
no sistema de arquivos local. O commando ``build`` é usado para ler estes
dados e gerar arquivos CSV consolidados com esta informação.

Se você não utilizou o diretório de saída padrão para salvar os dados,
é preciso informá-lo agora. Também é possível informar o diretório
onde os arquivos gerados serão salvos.

.. code::

    receita build --input cnpj_data --output results

Este comando irá gerar três arquivos no diretório de saída:

* **companies.csv**: dados das empresas salvas;
* **activities.csv**: lista das atividades das empresas (primárias/secundárias);
* **activities_seen.csv**: todas as atividades destas empresas.

Obtendo Ajuda
+++++++++++++

É possível utilizar a opção ``--help`` para obter ajuda sobre um comando.
Você também pode utilizá-lo com os subcomandos, como ``receita build --help``.
