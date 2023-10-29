from rdflib import Graph, Namespace
from rdflib.compare import graph_diff
from rdflib.term import Literal, URIRef, BNode
from vocab_management import *


def construct_class(item, data, namespace):
    triples = []
    # TODO: check for external terms
    # external terms are of type 'prefix:term'
    # They should not be declared as skos:
    item, namespace = _get_term_from_prefix_notation(item, namespace)
    triples.append((namespace[item], RDF.type, SKOS.Concept))
    triples.append((namespace[item], RDF.type, RDFS.Class))
    return triples


def construct_property(item, data, namespace):
    triples = []
    # TODO: check for external terms
    # external terms are of type 'prefix:term'
    # They should not be declared as skos:Concept
    item, namespace = _get_term_from_prefix_notation(item, namespace)
    triples.append((namespace[item], RDF.type, RDF.Property))
    triples.append((namespace[item], RDF.type, SKOS.Concept))
    return triples


def construct_label(item, data, namespace):
    triples = []
    term, namespace = _get_term_from_prefix_notation(data['Term'], namespace)
    triples.append((namespace[term], SKOS.prefLabel, Literal(item, lang='en')))
    return triples

def contruct_description(item, data, namespace):
    triples = []
    term, namespace = _get_term_from_prefix_notation(data['Term'], namespace)
    triples.append((namespace[term], SKOS.definition, Literal(item, lang='en')))
    return triples


def construct_parent(item, data, namespace):
    # parent will be of the form prefix:term
    triples = []
    term, namespace = _get_term_from_prefix_notation(data['Term'], namespace)
    # TODO: remove dpv:Concept as a concept
    # TODO: handle taxonomy i.e. as instances of a topconcept 
    # TODO: create helper function for common parent code
    # this to avoid introducing regressions when one function
    # changes and I forget to make changes in the other
    parents = item.split(',')
    for parent in parents:
        parent = parent.strip()
        if parent == 'dpv:Concept':
            parent = NAMESPACES['skos']['Concept']
        else:
            prefix, parentterm = parent.split(':')
            parent = NAMESPACES[prefix][parentterm]
        if data['ParentType'] == 'a':
            triples.append((namespace[term], RDF.type, parent))
        elif data['ParentType'] == 'sc':
            triples.append((namespace[term], RDFS.subClassOf, parent))
            triples.append((namespace[term], SKOS.broader, parent))
            triples.append((parent, SKOS.narrower, namespace[term]))
    return triples


def construct_parent_taxonomy(item, data, namespace):
    # parent will be of the form prefix:term
    triples = []
    term, namespace = _get_term_from_prefix_notation(data['Term'], namespace)
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
        if data['ParentType'] in ('a', 'sc'):
            triples.append((namespace[term], RDF.type, parent))
        else:
            prefix_top, topconcept = data['ParentType'].split(':')
            topconcept = NAMESPACES[prefix_top][topconcept]
            triples.append((namespace[term], RDF.type, topconcept))
            # TODO: check skos broader/narrower transitive 
            triples.append((namespace[term], SKOS.broader, parent))
            triples.append((parent, SKOS.narrower, namespace[term]))
    return triples


def construct_parent_property(item, data, namespace):
    # parent will be of the form prefix:term
    triples = []
    term = namespace[data['Term']]
    # TODO: remove dpv:Relation as a concept
    parents = item.split(',')
    for parent in parents:
        parent = parent.strip()
        if parent == 'dpv:Relation':
            continue
        else:
            prefix, parentterm = parent.split(':')
            parent = NAMESPACES[prefix][parentterm]
        triples.append((term, RDFS.subPropertyOf, parent))
        triples.append((term, SKOS.broader, parent))
        triples.append((parent, SKOS.narrower, term))
    return triples


def construct_domain(item, data, namespace):
    # domain and range are of type prefix:term
    triples = []
    domains = item.split(',')
    term, namespace = _get_term_from_prefix_notation(data['Term'], namespace)
    for domain in domains:
        domain = domain.strip()
        if domain == "dpv:Concept":
            continue
        prefix, domainterm = domain.split(':')
        domain = NAMESPACES[prefix][domainterm]
        triples.append((namespace[term], DCAM.domainIncludes, domain))
        triples.append((namespace[term], SCHEMA.domainIncludes, domain))
    return triples


def construct_range(item, data, namespace):
    # range and range are of type prefix:term
    triples = []
    ranges = item.split(',')
    term, namespace = _get_term_from_prefix_notation(data['Term'], namespace)
    for range in ranges:
        range = range.strip()
        if range == "dpv:Concept":
            continue
        prefix, rangeterm = range.split(':')
        range = NAMESPACES[prefix][rangeterm]
        triples.append((namespace[term], DCAM.rangeIncludes, range))
        triples.append((namespace[term], SCHEMA.rangeIncludes, range))
    return triples


def construct_value(item, data, namespace):
    triples = []
    if not item:
        return triples
    triples.append((namespace[data['Term']], RDF.value, Literal(item)))
    return triples


def construct_related_terms(item, data, namespace):
    triples = []
    term = namespace[data['Term']]
    # TODO: make related be a URI
    triples.append((term, SKOS.related, Literal(item, lang='en')))
    return triples


def construct_comment(item, data, namespace):
    triples = []
    term = namespace[data['Term']]
    triples.append((term, SKOS.note, Literal(item, lang='en')))
    return triples


def construct_source(item, data, namespace):
    triples = []
    term = namespace[data['Term']]
    # TODO: make source be a URI or a Literal (if startswith http)
    triples.append((term, DCT.source, Literal(item, lang='en')))
    return triples


def construct_date_created(item, data, namespace):
    triples = []
    term = namespace[data['Term']]
    triples.append((term, DCT.created, Literal(item, datatype=XSD.date)))
    return triples


def construct_date_modified(item, data, namespace):
    triples = []
    if not item:
        return
    term = namespace[data['Term']]
    triples.append((term, DCT.modified, Literal(item, datatype=XSD.date)))
    return triples


def construct_contributors(item, data, namespace):
    triples = []
    term = namespace[data['Term']]
    # TODO: make contributor be URI or a literal (if website available)
    triples.append((term, DCT.contributor, Literal(item, lang='en')))
    return triples


def construct_resolution(item, data, namespace):
    return []


def construct_status(item, data, namespace):
    return [(namespace[data['Term']], SW.term_status, Literal(item, lang='en'))]



def _get_term_from_prefix_notation(term, namespace):
    if ':' in term:
        prefix, term = term.split(':')
        namespace = NAMESPACES[prefix]
    return term, namespace
