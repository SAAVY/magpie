#!/bin/bash
# Create DB script

POSTGRES_ADMIN=postgres
DBUSER=postgres
DBNAME=postgres_magpie
TABLENAME=magpie_cache

sudo -u $POSTGRES_ADMIN createdb -O $DBUSER $DBNAME
hostName=$(sudo netstat -plunt |grep postgres)
echo $hostName | cut -d " " -f 4

psql -d $DBNAME -c $"CREATE TABLE IF NOT EXISTS $TABLENAME ( url TEXT PRIMARY KEY NOT NULL, metadata TEXT, created_date datetime default NULL );"
