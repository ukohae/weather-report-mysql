#!/bin/bash

mkdir file
cat "hello" > testing.txt
sudo yum -y update
sudo yum -y install aspell aspell-en httpd24 mysql mysql-server php56 php56-cli php56-gd php56-intl php56-mbstring php56-mysqlnd php56-opcache php56-pdo php56-soap php56-xml php56-xmlrpc php56-pspell --skip-broken
sudo yum list installed
sudo /sbin/chkconfig httpd on
sudo /sbin/chkconfig mysqld on  
sudo /sbin/service httpd start
sudo /sbin/service mysqld start
sudo mysqladmin -u root password '123a'