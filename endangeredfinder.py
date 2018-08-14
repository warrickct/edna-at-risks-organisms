import csv
import requests
from collections import OrderedDict

def _get_search_data(term):
    url = format('https://edna.nectar.auckland.ac.nz/edna/api/abundance?term=%s' % term)
    response = requests.get(url)
    response_json = response.json()
    results = response_json['data']
    return results 

# with open('risk_organisms_Simon_Feb18.csv', 'r') as csvfile:
#     with open('output.csv', 'w') as output_file:
#         reader = csv.reader(csvfile)
#         fieldnames = ["query", "term", "otu", "site", "value"]
#         writer = csv.DictWriter(output_file, fieldnames)
#         for line in reader:
#             output_dict = OrderedDict({
#                 'query': "",
#                 'term': "",
#                 'otu': "",
#                 'site':"",
#                 'value':""
#             })
#             output_dict['query'] = line[0]
#             for term in line[0].split(' '):
#                 if term == '':
#                     continue
#                 output_dict["term"] = term
#                 for otu_entry in _get_search_data(term):
#                     if len(_get_search_data) == 0:
#                         break
#                     output_dict["otu"] = otu_entry['']
#                     del otu_entry['']
#                     for site in otu_entry:
#                         output_dict["site"] = site
#                         output_dict["value"] = otu_entry[site]
#             if (output_dict['otu'] != "" and output_dict['value'] != ""):
#                 print(output_dict)
#                 writer.writerow(output_dict)


with open('risk_organisms_Simon_Feb18.csv', 'r') as csvfile:
    with open('output.csv', 'w') as output_file:
        reader = csv.reader(csvfile)
        fieldnames = ["query", "term", "otu", "site", "value"]
        writer = csv.writer(output_file, delimiter=",")
        for line in reader:
            query = line[0]
            # print(query)  
            for term in query.split(' '):
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
