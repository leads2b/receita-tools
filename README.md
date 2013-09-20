receita-tools
=============

Set of tools to allow automated information recovery from the
Secretary of the Federal Revenue of Brazil website. This set of
tools can crawl Receita's website, decode the captcha image
and retrieve information about all Brazilian companies you like.

You can find a number of tools in the `tools` folder. Those
tools are designed so you can easily run them on a regular
basis to generated CSV files with all retrieved data. You can
then use those files to import the relevant data to the
system you want (or even directly to a database).

Needed software
---------------

You need to have Python's Imagem Library installed. You can find
information on how to install it on your system
[here](https://pypi.python.org/pypi/PIL). If you are installing in a Linux
machine, check [this post](http://askubuntu.com/questions/156484/how-do-i-install-python-imaging-library-pil)
to read more about how to install the library (it can be tricky).

You also need to have installed the Tesseract OCR tool. You can find
information on how to install it on your system
[here](https://code.google.com/p/tesseract-ocr/). Remember to install
the english language as well.

About Captcha Decoding
----------------------

This library will run a simple filter over the downloaded captcha
and will run Tesseract over it. Experiments has shown an accuracy
of ~25-30%. I'm sure that this can be improved, and if you know
a better way of doing it feel free to contribute. There's a tool
to download some sample captchas to help any development on that
area.
