#! /bin/sh

# Locale
update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

# Update Repositories:
apt-get update

# Install basic packages:
apt-get install -y \
    python-dev \
    python-software-properties \
    python-pip \
    build-essential \
    git \
    libproj-dev \
    libgeos-dev \
    libgdal-dev

# Add postgresql PPA:
sudo echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
    sudo apt-key add -

# Install Python dependencies from Python Package Index:
pip install -r /vagrant/requirements.txt

# Update package index:
apt-get update

# Install Packages from PPAs:
apt-get install -y \
    nginx postgresql-9.3 \
    postgresql-9.3-postgis \
    postgresql-contrib

# deploy custom pg_hba.conf and restart postgres server:
rm /etc/postgresql/9.3/main/pg_hba.conf
ln -s /vagrant/provisioning/pg_hba.conf /etc/postgresql/9.3/main/pg_hba.conf
service postgresql restart

# Create system and database user 'stratigy':
useradd stratigy --home /srv/stratigy --create-home --shell /bin/bash
sudo -u postgres psql -c 'CREATE USER stratigy PASSWORD 'secret';'

# add user stratigy to vagrant group for execution permission of app
usermod -aG vagrant stratigy 

# Setup databases:
sudo -u postgres createdb stratigy_development --owner=stratigy
sudo -u postgres createdb stratigy_test --owner=stratigy

# Setup PostGIS on databases
sudo -u postgres psql -d stratigy_development -c 'CREATE EXTENSION postgis;'
sudo -u postgres psql -d stratigy_test -c 'CREATE EXTENSION postgis;'
