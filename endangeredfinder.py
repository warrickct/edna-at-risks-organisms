import csv
import re
import requests
from collections import OrderedDict

def _get_search_data(term):
    url = format('https://edna.nectar.auckland.ac.nz/edna/api/abundance?term=%s' % term)
    response = requests.get(url)
    response_json = response.json()
    results = response_json['data']
    return results 

with open('risk_organisms_Simon_Feb18.csv', 'r') as csvfile:
    with open('output.csv', 'w') as output_file:
        reader = csv.reader(csvfile)
        writer = csv.writer(output_file, delimiter=",")
        for line in reader:
            query = line[0]
            cleaned_query = re.sub(r'(?:(?<=\().+?(?=\))|(?<=\[).+?(?=\]))', "", line[0])
            # print(query)  
            for term in cleaned_query.split(' '):
                
                if (term != ''):
                    # print(term)
                    otus = _get_search_data(term)
                    if len(otus) > 0:
                        # print(otus)
                        for otu in otus:
                            for field in otu:
                                if field == "":
                                    otu_name = otu[field]
                                    print(otu_name)
                                    continue
                                site = field
                                value = otu[field]
                                writer.writerow([query, term, otu_name, site, value])
                    else:
                        writer.writerow([query, term])
