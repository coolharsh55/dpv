from rdflib import Graph, Namespace
from rdflib.compare import graph_diff
from rdflib.term import Literal, URIRef, BNode
from vocab_management import *


def construct_class(item, data, namespace):
    triples = []
    # TODO: check for external terms
    # external terms are of type 'prefix:term'
    # They should not be declared as skos:Concept
    triples.append((namespace[item], RDF.type, SKOS.Concept))
    triples.append((namespace[item], RDF.type, RDFS.Class))
    return triples


def construct_property(item, data, namespace):
    triples = []
    # TODO: check for external terms
    # external terms are of type 'prefix:term'
    # They should not be declared as skos:Concept
    triples.append((namespace[item], RDF.type, RDF.Property))
    return triples


def construct_label(item, data, namespace):
    triples = []
    term = namespace[data['Term']]
    triples.append((term, SKOS.prefLabel, Literal(item, lang='en')))
    return triples

def contruct_description(item, data, namespace):
    triples = []
    term = namespace[data['Term']]
    triples.append((term, SKOS.definition, Literal(item, lang='en')))
    return triples


def construct_parent(item, data, namespace):
    # parent will be of the form prefix:term
    triples = []
    term = namespace[data['Term']]
    # DEBUG(f"constructing parent: {item} for {data['Term']}")
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
        # DEBUG(f'parent identified: {parent}')
        if data['ParentType'] == 'a':
            triples.append((term, RDF.type, parent))
        elif data['ParentType'] == 'sc':
            triples.append((term, RDFS.subClassOf, parent))
    return triples


def construct_parent_taxonomy(item, data, namespace):
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
        if data['ParentType'] in ('a', 'sc'):
            triples.append((term, RDF.type, parent))
        else:
            # DEBUG(data['ParentType'])
            prefix_top, topconcept = data['ParentType'].split(':')
            topconcept = NAMESPACES[prefix_top][topconcept]
            triples.append((term, RDF.type, topconcept))
            # TODO: check skos broader/narrower transitive 
            triples.append((term, SKOS.broader, parent))
    return triples


def construct_parent_property(item, data, namespace):
    # parent will be of the form prefix:term
    triples = []
    term = namespace[data['Term']]
    # TODO: remove dpv:Relation as a concept
    parents = item.split(',')
    triples.append((term, RDF.type, RDF.Property))
    for parent in parents:
        parent = parent.strip()
        if parent == 'dpv:Relation':
            continue
        else:
            prefix, parentterm = parent.split(':')
            parent = NAMESPACES[prefix][parentterm]
        # DEBUG(f'parent identified: {parent}')
        triples.append((term, RDFS.subPropertyOf, parent))
    return triples


def construct_domain(item, data, namespace):
    # domain and range are of type prefix:term
    triples = []
    term = namespace[data['Term']]
    domains = item.split(',')
    for domain in domains:
        domain = domain.strip()
        if domain == "dpv:Concept":
            continue
        prefix, domainterm = domain.split(':')
        domain = NAMESPACES[prefix][domainterm]
        # DEBUG(f'domain identified: {domain}')
        triples.append((term, DCAM.domainIncludes, domain))
    return triples


def construct_range(item, data, namespace):
    # range and range are of type prefix:term
    triples = []
    term = namespace[data['Term']]
    ranges = item.split(',')
    for range in ranges:
        range = range.strip()
        if range == "dpv:Concept":
            continue
        prefix, rangeterm = range.split(':')
        range = NAMESPACES[prefix][rangeterm]
        # DEBUG(f'range identified: {range}')
        triples.append((term, DCAM.rangeIncludes, range))
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

