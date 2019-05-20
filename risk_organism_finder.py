import csv
import re
import requests
import glob
from collections import OrderedDict

# 'dev': 'http://localhost:8000/edna/api/v1.0/abundance?otu=',
# 'prod': 'https://edna.nectar.auckland.ac.nz/enda/api/v1.0/abundance?otu=',

sample_otu_dev_url = 'http://localhost:8000/edna/api/v1.0/abundance?otu='
otu_dev_url = 'http://localhost:8000/edna/api/v1.0/abundance?otu='
site_dict = {}
otu_dict = {}

def _get_sample_otus(text):
    # url = format('https://edna.nectar.auckland.ac.nz/edna/api/abundance?otu=&term=%s' % term)
    term = "&text=" + text
    url = format(sample_otu_dev_url + term)

    response = requests.get(url)
    results = response.json()
    return results 

def get_site_info(site_id):
    ''' attempts to get sample identifier from lookup, if fails then requests from database.'''
    print(site_id)
    if site_id in site_dict:
        return site_dict[site_id]
    else:
        url = 'http://localhost:8000/edna/api/v1.0/sample_context/' + str(site_id)
        response = requests.get(url)
        json = response.json()
        name = json['name']
        site_dict[site_id] = name
        return name

def get_otu_info(otu_id):
    ''' queries for info regarding an otu. Tries local dict first then resorts to querying api as last resort'''
    if otu_id in otu_dict:
        return otu_dict[otu_id]
    else:
        url = 'http://localhost:8000/edna/api/v1.0/otu/' + str(otu_id)
        response = requests.get(url)
        json = response.json()
        name = json['otu_names'][0]
        return name

def search_and_write_row(organism, taxon):
    response_data = _get_sample_otus(taxon)
    sample_otus = response_data['sample_otu_data']
    # _create_site_lookup(response_data['sample_contextual_data']) 
    if len(sample_otus) > 0:
        for sample_otu in sample_otus:
            otu_name = get_otu_info(sample_otu[0])
            # sample_identifier = site_dict[sample_otu[1]]
            sample_identifier = get_site_info(sample_otu[1])
            value = [sample_otu[2]]
            writer.writerow([organism, taxon, otu_name, sample_identifier, value])
    else:
        writer.writerow([organism, taxon])

paths = glob.glob('./endangered_files/*.csv')
for path in paths:
    print(path)
    with open(path, 'r') as csvfile:
        with open(path + '-output', 'w') as output_file:
            reader = csv.reader(csvfile)
            writer = csv.writer(output_file, delimiter=",")
            header = ["risk organism", "taxon searched", "organism matched", "containing sample", "abundance"]
            writer.writerow(header)
            for row in reader:
                for field in row:
                    field = re.sub(r'(?:(?<=\().+?(?=\))|(?<=\[).+?(?=\]))', "", field)
                genus = row[0]
                species = row[1]
                organism = genus + " " + species
                if species:
                    # species = "s__" + species
                    search_and_write_row(organism, species)
                elif genus:
                    # genus = "g__" + genus
                    search_and_write_row(organism, genus)
