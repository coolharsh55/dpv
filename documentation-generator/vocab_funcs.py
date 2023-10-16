from rdflib import Graph, Namespace
from rdflib.compare import graph_diff
from rdflib.term import Literal, URIRef, BNode
from vocab_management import *


def construct_iri(item, data, namespace):
    triples = []
    # TODO: check for external terms
    # external terms are of type 'prefix:term'
    # They should not be declared as skos:Concept
    triples.append((namespace[item], RDF.type, SKOS.Concept))
    return triples


def construct_label(item, data, namespace):
    return []


def contruct_description(item, data, namespace):
    return []


def construct_parent(item, data, namespace):
    # parent will be of the form prefix:term
    triples = []
    term = namespace[data['Term']]
    # DEBUG(f"constructing parent: {item} for {data['Term']}")
    # TODO: remove dpv:Concept as a concept
    # TODO: handle taxonomy i.e. as instances of a topconcept 
    parents = item.split(',')
    for parent in parents:
        parent = parent.strip()
        if parent == 'dpv:Concept':
            parent = NAMESPACES['skos']['Concept']
        else:
            prefix, parentterm = parent.split(':')
            parent = NAMESPACES[prefix][parentterm]
        # DEBUG(f'parent identified: {parent}')
        if data['ParentType'] == 'a':
            triples.append((term, RDF.type, parent))
        elif data['ParentType'] == 'sc':
            triples.append((term, RDFS.subClassOf, parent))
    return triples


def construct_value(item, data, namespace):
    return []


def construct_related_terms(item, data, namespace):
    return []


def construct_comment(item, data, namespace):
    return []


def construct_source(item, data, namespace):
    return []


def construct_date_created(item, data, namespace):
    return []


def construct_date_modified(item, data, namespace):
    return []


def construct_contributors(item, data, namespace):
    return []


def construct_resolution(item, data, namespace):
    return []
