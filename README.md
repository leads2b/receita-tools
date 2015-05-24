receita-tools
=============

Set of tools to allow automated information recovery from the
Secretary of the Federal Revenue of Brazil website. This set of
tools will use the [receitaws.com.br](http://receitaws.com.br/)
web service to retrieve information about all Brazilian
companies you like.

You can find a number of tools in the `tools` folder. Those
tools are designed so you can easily run them on a regular
basis to generate CSV files with all retrieved data. You can
then use those files to import the relevant data to the
system you want (or even directly to a database).


Webservice performance
----------------------

The performance of the webservice is very limited. This is
because Receita's website is very actively blocking access
when there is an elevated number of requests from a single
IP. We try to run workers on multiple IPs to allow a faster
response, but in any case, your code must be prepared to wait
for a long time for a response (5mins+). Results are cached,
so if you prefer, you can trigger lots of requests, and check
their results after some time.


About Captcha Decoding
----------------------

There will be no information about how captcha decoding is
made by the web service. The last time this information was
available there was changes that broken the service.
Basic company information should be available in an easy
way so we can have a more transparent business in the
country.

Decoding percentages will be available in the future, but
they are not really good. If you know a way to achieve +70%
of success decoding it, please let me know. There's a tool
to download some sample captchas to help any development on
that area.
