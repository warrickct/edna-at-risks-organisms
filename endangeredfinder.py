import csv
import re
import requests
from collections import OrderedDict

# 'dev': 'http://localhost:8000/edna/api/v1.0/abundance?otu=',
# 'prod': 'https://edna.nectar.auckland.ac.nz/enda/api/v1.0/abundance?otu=',

sample_otu_dev_url = 'http://localhost:8000/edna/api/v1.0/abundance?otu='

otu_dev_url = 'http://localhost:8000/edna/api/v1.0/abundance?otu='

site_dict = {}
otu_dict = {}

def _get_search_data(text):
    # url = format('https://edna.nectar.auckland.ac.nz/edna/api/abundance?otu=&term=%s' % term)
    term = "&text=" + text
    url = format(sample_otu_dev_url + term)
    print(url)

    response = requests.get(url)
    results = response.json()
    print(results)
    return results 

def _create_site_lookup(sites):
    '''iterates the site metadata array and organises them by id as key'''
    if site_dict:
        return
    for site in sites:
        print(site)
        site_dict[site['id']] = site

def get_otu_info(otu_id):
    ''' queries for info regarding an otu. Tries local dict first then resorts to querying api as last resort'''
    if otu_id in otu_dict:
        return otu_dict[otu_id]
    else:
        url = 'http://localhost:8000/edna/api/v1.0/otu/' + str(otu_id)
        response = requests.get(url)
        json = response.json()
        name = json['otu_names'][0]
        print(name)


with open('./endangered_files/risk_organisms_Simon_Feb18.csv', 'r') as csvfile:
    with open('output.csv', 'w') as output_file:
        reader = csv.reader(csvfile)
        writer = csv.writer(output_file, delimiter=",")
        for line in reader:
            query = line[0]
            # re sub removed '(' ')' '[' ']' and replaces with ''
            cleaned_query = re.sub(r'(?:(?<=\().+?(?=\))|(?<=\[).+?(?=\]))', "", line[0])
            print(cleaned_query)  
            for endangered_segment in cleaned_query.split(' '):
                if (endangered_segment != ''):
                    # print(term)
                    response_data = _get_search_data(endangered_segment)
                    sample_otus = response_data['sample_otu_data']
                    _create_site_lookup(response_data['sample_contextual_data']) 
                    if len(sample_otus) > 0:
                        for sample_otu in sample_otus:
                            print(sample_otu)
                            otu_name = get_otu_info(sample_otu[0])
                            sample_identifier = site_dict[sample_otu[1]]
                            value = [sample_otu[2]]
                            # for field in sample_otu:
                            #     if field == "":
                            #         otu_name = sample_otu[field]
                            #         print(otu_name)
                            #         continue
                            #     site = field
                            #     value = sample_otu[field]
                            writer.writerow([query, endangered_segment, otu_name, sample_identifier, value])
                    else:
                        writer.writerow([query, endangered_segment])
