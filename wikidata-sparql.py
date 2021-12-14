# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT DISTINCT ?vat ?rorId WHERE {
  ?org (p:P3608/ps:P3608) ?vat;
    (p:P6782/ps:P6782) ?rorId.
}
"""


def get_results(endpoint_url, query):
    user_agent = "PIC-to-ROR/0.1 (https://github.com/paulmillar/PIC-to-ROR) Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

print("Querying WikiData to discover EU VAT numbers")
results = get_results(endpoint_url, query)

print("Found {} ROR organisation with their corresponding EU VAT number".format(len(results["results"]["bindings"])))

vatToRor={}
for result in results["results"]["bindings"]:
    vat=result['vat']['value']
    ror="https://ror.org/{}".format(result['rorId']['value'])
    vatToRor[vat]=ror

