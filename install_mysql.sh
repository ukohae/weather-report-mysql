#!/bin/bash

echo "welcome to mysql database installation wizard!!"
sudo hostnamectl set-hostname mysqlserver
sudo apt update -y
sudo apt install mysql-server
sudo mysql_secure_installation
sudo mysql