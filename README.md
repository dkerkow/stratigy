stratigy
========

Web application for working with stratigraphic data

Development
-----------

The stratigy project is using Vagrant as development environment. It provides an 
interface for handling different providers, in this case Virtualbox. 
The properties of the virtual machine are configured in the Vagrantfile. 

### Setup Development Environment

 - Install Virtualbox
 - Install Vagrant as described here: http://docs.vagrantup.com/v2/installation/index.html
 - Clone Repository:
 
 ```bash
 # with ssh:
 git clone git@github.com:dkerkow/stratigy.git
 # with https:
 git clone https://github.com/dkerkow/stratigy.git
 ```
 
 - run vagrant:
 
 ```bash
 # start or resume virtual machine (runs the provisioning, if there wasnt a saved state) :
 vagrant up
 # ssh into virtual machine as user vagrant:
 vagrant ssh
 # save virtual machine and turn off
 vagrant suspend
 # destroy virtual machine before rebuilding it:
 vagrant destroy
 ```
 
 - run development server:
 
 ```bash
 vagrant ssh
 
 # start as user stratigy
 sudo su - stratigy
 
 # change to app directory
 cd /vagrant
 
 # to create database on first run, log into interactive ipython shell
 python shell.py
 >>> from app import db
 >>> db.create_all()
  
 # run server 
 python run.py
 
 # site will be accessible on http://localhost:5000 in local browser
 
 # to populate database with test data, run:
 psql stratigy_development -f insert_test_data.sql
 ``` 
 
