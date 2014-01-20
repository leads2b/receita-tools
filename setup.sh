#!/bin/bash

# this script is just a helper to make it easier to install
# the necessary software to run this tools

# you may not want to run this script directlly as it was
# create to be only a reference

# install php cli
apt-get update
apt-get install -y --force-yes php5-cli php5-curl curl

# get composer
curl -sS https://getcomposer.org/installer | php
mv composer.phar /usr/local/bin/composer

# get receita-tools
git clone https://github.com/vkruoso/receita-tools.git
cd receita-tools
composer install

# installing tesseract and python PIL
apt-get install -y --force-yes build-essential imagemagick
apt-get install -y --force-yes tesseract-ocr tesseract-ocr-eng
apt-get install -y --force-yes libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev python-pip
apt-get install -y --force-yes python python-dev

if test -d /usr/lib/i386-linux-gnu/; then
  ln -fs /usr/lib/i386-linux-gnu/libz.so /usr/lib/libz.so
  ln -fs /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib/libjpeg.so
  ln -fs /usr/lib/i386-linux-gnu/libfreetype.so /usr/lib/libfreetype.so
fi

if test -d /usr/lib/x86_64-linux-gnu/; then
  ln -fs /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/libz.so
  ln -fs /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/libjpeg.so
  ln -fs /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/libfreetype.so
fi

pip install PIL
