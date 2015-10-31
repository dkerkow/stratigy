stratigy
========

Web application for working with stratigraphic data

Development
-----------

The stratigy project is using Vagrant as development environment. It
provides an interface for handling different providers, in this case
Virtualbox and LXC. Virtualbox is the generic option, because it works
on all platforms. LXC just works on Linux, but has the advantage of not
virtualizing a complete guest system, but using the kernel of the host
instead, which saves a lot of ressources on the host.
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
 vagrant up [--provider=lxc]
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

### Deploy Stratigy on a Server

This repository provides a set of configuration examples, fitted for deploying Stratigy to an Ubuntu 14.04 Server. Other Linux/Unix distributionsvwill work, too. But in this case you would probably have to customize the configuration for yourself.

The recommended software stack is:

 - **Ubuntu 14.04**
 - **Nginx** Webserver as reverse proxy, delivering static content
 - **gunicorn** as application server, execution the stratigy python app.
 - **supervisord** as watchdog for starting, stopping and auto-reloading gunicorn on maintenance and crashes

In contrary to the above, PostgreSQL is a hard dependency for the database part, as stratigy is using features not present in MySQL or other.

In the folder `provision/` you will find configuration examples for the recommended software stack. Copy, rename and customize them to your needs and put them in place.
