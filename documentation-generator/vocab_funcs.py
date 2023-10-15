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
    # TODO: check for multiple parents, which may be external
    # TODO: remove dpv:Concept as a concept
    if item == 'dpv:Concept':
        item = NAMESPACES['skos']['Concept']
    else:
        prefix, term = item.split(':')
        item = NAMESPACES[prefix][term]
    triples.append((namespace[data[0]], RDF.type, RDFS.Class))
    triples.append((namespace[data[0]], RDF.type, item))
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
