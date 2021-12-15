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
    """Query wikidata to discover all organisations for which wikidata
    knows both the EU VAT number and the ROR identifier.  The returned
    value is a dict with keys VAT number and the values are ROR
    identifiers.
    """
    user_agent = "PIC-to-ROR/0.1 (https://github.com/paulmillar/PIC-to-ROR) Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def vat_to_ror():
    results = get_results(endpoint_url, query)

    vatToRor={}
    for result in results["results"]["bindings"]:
        vat=result['vat']['value']
        ror="https://ror.org/{}".format(result['rorId']['value'])
        vatToRor[vat]=ror

    return vatToRor

