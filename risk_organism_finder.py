import csv
import re
import requests
import glob
from collections import OrderedDict
import os

# 'dev': 'http://localhost:8000/edna/api/v1.0/abundance?otu=',
# 'prod': 'https://edna.nectar.auckland.ac.nz/enda/api/v1.0/abundance?otu=',


# TODO: Don't Repeat Yourself
dev_base ='http://localhost:8000/edna/api/v1.0/' 
prod_base = 'https://edna.nectar.auckland.ac.nz/edna/api/v1.0/'

abundance_slug = 'abundance?otu='
sample_context_slug = 'sample_context/'
otu_slug = 'otu/'

abundance_dev_api = dev_base + abundance_slug
prod_api = prod_base + abundance_slug

active_sample_context_api = prod_base + sample_context_slug

active_otu_api = prod_base + otu_slug

api_base_url = prod_api

site_dict = {}
otu_dict = {}

def _get_sample_otus(terms):
    url = api_base_url
    for term in terms:
        term = "&text=" + term
        url = url + term
    print(url)
    response = requests.get(url)
    results = response.json()
    return results 

def get_site_info(site_id):
    ''' attempts to get sample identifier from lookup, if fails then requests from database.'''
    print(site_id)
    if site_id in site_dict:
        return site_dict[site_id]
    else:
        url = active_sample_context_api + str(site_id)
        response = requests.get(url)
        json = response.json()
        name = json['name']
        site_dict[site_id] = name
        return name

def get_otu_name(otu_id):
    ''' queries for info regarding an otu. Tries local dict first then resorts to querying api as last resort'''
    if otu_id in otu_dict:
        return otu_dict[otu_id]
    else:
        url = active_otu_api + str(otu_id)
        response = requests.get(url)
        json = response.json()
        name = json['otu_names'][0]
        return name

def search_and_write_row(organism, row):

    def _all_taxons_above_genus(row, name):
        ''' Checks that all the terms within a search row are from the genus taxon or above to prevent false positives.'''
        if 'g__' in name:
            name_from_genus = name.split('g__')[1]
            print(name_from_genus)
            contains_all_terms = True
            for field in row:
                if field not in name_from_genus:
                    print("{} not in {}".format(field, name_from_genus))
                    contains_all_terms = False
            print("all terms in genus or above")
        else:
            contains_all_terms = False
        return contains_all_terms

    response_data = _get_sample_otus(row)
    sample_otus = response_data['sample_otu_data']
    # _create_site_lookup(response_data['sample_contextual_data']) 
    if len(sample_otus) > 0:
        for sample_otu in sample_otus:
            otu_code = get_otu_name(sample_otu[0])
            # sample_identifier = site_dict[sample_otu[1]]
            if _all_taxons_above_genus(row, otu_code):
                sample_identifier = get_site_info(sample_otu[1])
                value = [sample_otu[2]]
                writer.writerow([organism, otu_code, sample_identifier, value])
            else:
                writer.writerow([organism])
    else:
        writer.writerow([organism])

import ntpath

output_dir = './output/'

paths = glob.glob('./endangered_files/*.csv')
for path in paths:
    print(path)
    head, tail = ntpath.split(path)
    with open(path, 'r') as input_file:
        with open(output_dir + tail, 'w') as output_file:
            reader = csv.reader(input_file)
            next(reader)
            writer = csv.writer(output_file, delimiter=",")
            header = [ "risk organism", "organism matched", "containing sample", "abundance"]
            writer.writerow(header)
            for row in reader:
                for field in row:
                    field = re.sub(r'(?:(?<=\().+?(?=\))|(?<=\[).+?(?=\]))', "", field)
                    field.strip()
                genus = row[0]
                species = row[1]
                organism = genus + " " + species
                search_and_write_row(organism, row)
