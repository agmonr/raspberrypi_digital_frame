#!/bin/bash
# The script will remove mysql and all the databases and then install mysqly
sudo rm -rf /var/lib/mysql/mysql
sudo apt-get -y remove --purge mysql-server mysql-client mysql-common
sudo apt-get -y autoremove
sudo apt-get -y autoclean                                                                                                                                     
sudo apt-get -y install mysql-server             
