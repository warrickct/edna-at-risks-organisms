import csv
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
        fieldnames = ["query", "term", "otu", "site", "value"]
        output_dict = OrderedDict({
            'query': "",
            'term': "",
            'otu': "",
            'site':"",
            'value':""
        })
        writer = csv.DictWriter(output_file, fieldnames)
        for line in reader:
            output_dict['query'] = line[0]
            for term in line[0].split(' '):
                if term == '':
                    continue
                output_dict["term"] = term
                search_results = _get_search_data(term)
                for result in search_results:
                    if len(result) == 0:
                        continue
                    output_dict["otu"] = result['']
                    del result['']
                    for site in result:
                        output_dict["site"] = site
                        output_dict["value"] = result[site]
            if (output_dict['otu'] != "" and output_dict['value'] != ""):
                print(output_dict)
                writer.writerow(output_dict)