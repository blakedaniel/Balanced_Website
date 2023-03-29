#!bin/bash

# login to postgres
psql -U admin balanced

# delete all rows from betteretf_yahooraw, betteretf_threeyearhistory, betteretf_sectorsbreakdown, betteretf_holdingsbreakdown, betteretf_fund
DELETE FROM betteretf_yahooraw;
DELETE FROM betteretf_threeyearhistory;
DELETE FROM betteretf_sectorsbreakdown;
DELETE FROM betteretf_holdingsbreakdown;
DELETE FROM betteretf_fund;