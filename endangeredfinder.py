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
    duplicate_results = []
    for terms in organisms_to_search:
        for term in terms[:2]:
            # print(term)
            url = format('http://localhost:8000/edna/abundance?term=%s' % term)
            response = requests.get(url)
            response_json = response.json()
            abundance_results = response_json['data']
            if len(abundance_results)>0:
                for abundance_entry in abundance_results:
                    otu_name = abundance_entry['']
                    if otu_name in duplicate_results:
                        print("Duplicate found - Skipping result % s" % otu_name)
                        break
                    else:
                        duplicate_results.append(otu_name)
                    sample_values = []
                    for field in abundance_entry:
                        if field !='':
                            abundance_value = abundance_entry[field] 
                            if abundance_value > 0:
                                sample_values.append([field, abundance_value])
                    # print(duplicate_results)
                    writer.writerow({'otu_name': otu_name, 'sample_values': sample_values})