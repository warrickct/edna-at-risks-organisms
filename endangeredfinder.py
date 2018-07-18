import csv
import requests


organisms_to_search = []
with open('risk_organisms_Simon_Feb18.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        organism_terms = line[0].split(' ')
        # remove the empty spaces between terms.
        while '' in organism_terms:
            organism_terms.remove('')
        organisms_to_search.append(organism_terms)

with open('output.csv', 'w') as output_file:
    fieldnames = ['otu_name', 'sample_values']
    writer = csv.DictWriter(output_file, fieldnames)
    for terms in organisms_to_search:
        for term in terms:
            url = format('http://localhost:8000/edna/abundance?term=%s' % term)
            response = requests.get(url)
            response_json = response.json()
            sample_values = []
            abundance_results = response_json['data']
            if len(abundance_results)>0:
                for abundance_entry in abundance_results:
                    # print(abundance_entry)
                    for field in abundance_entry:
                        if field=='':
                            otu_name = abundance_entry[field]
                        else:
                            abundance_value = abundance_entry[field] 
                            if abundance_value > 0:
                                sample_values.append([field, abundance_value])
                writer.writerow({'otu_name': otu_name, 'sample_values': sample_values})