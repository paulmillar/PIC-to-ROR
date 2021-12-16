# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

#
#  See also https://www.wikidata.org/wiki/Property:P5785
#  Wikidata has some PIC numbers

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT DISTINCT ?org ?vat ?rorId WHERE {
  ?org (p:P3608/ps:P3608) ?vat;
    (p:P6782/ps:P6782) ?rorId.
}
"""

query_pic_to_ror = """SELECT DISTINCT ?org ?pic ?rorId WHERE {
  ?org (p:P5785/ps:P5785) ?pic;
    (p:P6782/ps:P6782) ?rorId.
}
"""

query_org_to_ror = """SELECT DISTINCT ?org ?rorId WHERE {
  ?org (p:P6782/ps:P6782) ?rorId
}
"""


def get_results(endpoint_url, query):
    """Make a specific query against Wikidata."""
    user_agent = "PIC-to-ROR/0.1 (https://github.com/paulmillar/PIC-to-ROR) Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def query_ror_ids():
    """Query Wikidata to learn all organisations for which it knows an
    ROR.
    """
    results = get_results(endpoint_url, query)

    ror_by_qid={}
    for result in results["results"]["bindings"]:
        org=result['org']['value']
        ror="https://ror.org/{}".format(result['rorId']['value'])
        ror_by_qid[org]=ror
    return ror_by_qid


def pic_to_ror():
    """Query Wikidata to learn all organisations for which it knows both a
       PIC and an ROR.
    """
    results = get_results(endpoint_url, query_pic_to_ror)

    picToRor={}
    for result in results["results"]["bindings"]:
        pic=result['pic']['value']
        org=result['org']['value']
        ror="https://ror.org/{}".format(result['rorId']['value'])
        picToRor[pic]={"ror": ror, "id": org}
    return picToRor


def vat_to_ror():
    """Query Wikidata to learn all organisations for which it knows both a
       EU VAT number and an ROR.
    """
    results = get_results(endpoint_url, query)

    vatToRor={}
    for result in results["results"]["bindings"]:
        vat=result['vat']['value']
        org=result['org']['value']
        ror="https://ror.org/{}".format(result['rorId']['value'])
        vatToRor[vat]={"ror": ror, "id": org}
    return vatToRor
