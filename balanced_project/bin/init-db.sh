#!/bin/bash

set -e

# Perform all actions as $POSTGRES_USER
export PGUSER="$POSTGRES_USER"

#
"psql" <<- 'EOSQL'
CREATE DATABASE balanced; 
EOSQL
