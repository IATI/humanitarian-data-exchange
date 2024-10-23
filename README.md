# Humanitarian Data Exchange

Contains scripts for working with IATI data on the Humanitarian Data Exchange CKAN site: https://data.humdata.org/organization/iati

Terminology: CKAN has "datasets" and each "dataset" has multiple "resources". 
Confusingly, IATI also uses the term "dataset" at times. "dataset" in this repository refers to a CKAN dataset.

The datasets directory contains information on each dataset. 
It does not contain the full CKAN data, instead it contains what is different between each data set and information vital to work with the datasets.

## Getting data from CKAN

The pull_datasets.py script gets the latest information from CKAN and updates the datasets directory with it.
It also does some checks to make sure the data is as expected.
