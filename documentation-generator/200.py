#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

'''Take CSV and generate RDF from it'''

########################################
# How to read and understand this file #
# 1. Start from the end of the file
# 2. This script reads CSV files explicitly declared
# 3. It generates RDF terms using rdflib for Classes and Properties
# 4. It writes those terms to a file - one per each module
# 5. It combines all written files into dpv.ttl and dpv-gdpr.ttl

# This script assumes the input if well structured and formatted
# If it isn't, the 'erors' may silently propogate

# CSV FILES are in IMPORT_CSV_PATH
# RDF FILES are written to EXPORT_DPV_MODULE_PATH

# CONTRIBUTION: If anyone is willing to turn these scripts into
# an equivalent RML/R2RML or similar mappings, please let us know
########################################

import csv
from collections import namedtuple
import json

from rdflib import Graph, Namespace
from rdflib.compare import graph_diff
from rdflib.term import Literal, URIRef, BNode

import logging
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug
INFO = logging.info

from vocab_management import *
import vocab_schemas

PROPOSED = {}

def load_CSV(filepath):
    with open(filepath) as fd:
        csvreader = csv.reader(fd)
        # First row contains header/labels, which give the count of 
        # attributes to extract from each row.
        # CAUTION: Google Sheets mangles the CSV where there are empty 
        # columns in the row towards the end. To fix this, we presume
        # there are no empty headers in the CSV.
        header = [x for x in next(csvreader) if x]
        count = len(header)
        terms = []
        for row in csvreader:
            # skip empty rows
            if len(row) == 0 or not row[0].strip():
                continue
            # extract required amount of terms, ignore any field after that
            row = [term.strip() for term in row[:count]]
            rowdata = {}
            for index, item in enumerate(row):
                rowdata[header[index]] = row[index]
            terms.append(rowdata)
    return header, terms


def serialize_graph(triples, filepath):
    '''serializes triples at filepath with defined formats'''
    graph = Graph()
    for prefix, namespace in NAMESPACES.items():
        graph.namespace_manager.bind(prefix, namespace)
    for triple in triples:
        graph.add(triple)
    for ext, format in RDF_SERIALIZATIONS.items():
        graph.serialize(f'{filepath}.{ext}', format=format)
    INFO(f'wrote {filepath}.[{",".join(RDF_SERIALIZATIONS)}]')
    # Serialise OWL variant
    # filepath is the same, but the extension is {name}-owl.[ttl,owl]
    # conversion to manchester syntax happens through external script
    # TODO: What IRI to use for OWL variant?
    # Options:
    # 1) same IRI e.g. https://w3id.org/dpv#Concept
    # 2) different IRI e.g. https://w3id.org/dpv/owl#Concept
    #    /owl is the suffix to distinguish owl variant
    # 3) current IRI e.g. https://w3id.org/dpv/dpv-owl#Concept
    #    /dpv-owl is the prefix to distinguish owl variant
    # TODO: Add skos:exactMatch between default and OWL concepts
    graph.update("""
        DELETE { ?s rdf:type skos:Concept }
        INSERT { ?s rdf:type owl:Class }
        WHERE { ?s rdf:type rdfs:Class }
        """)
    graph.update("""
        DELETE { ?s rdf:type skos:Concept }
        INSERT { ?s rdf:type owl:ObjectProperty }
        WHERE { ?s rdf:type rdf:Property }
        """)
    graph.update("""
        DELETE { ?s skos:inScheme ?o }
        WHERE { ?s skos:inScheme ?o }
        """)
    graph.update("""
        DELETE { ?s rdf:type skos:ConceptScheme }
        WHERE { ?s rdf:type skos:ConceptScheme }
        """)
    graph.update("""
        DELETE { ?s skos:broader ?o . ?o skos:narrower ?s  }
        INSERT { ?s rdfs:subClassOf ?o }
        WHERE { ?s skos:broader ?o }
        """)
    # TODO: SPARQL CONSTRUCT to create domain/range values for properties
    # use existing dcam:domainIncludes/rangeIncludes
    # convert to owl:unionOf ( domain/range )
    # problem: how to construct rdf:Collection using SPARQL?
    for ext, format in OWL_SERIALIZATIONS.items():
        graph.serialize(f'{filepath}-owl.{ext}', format=format)
    # TODO: Call converter from OWL to OMN
    INFO(f'wrote {filepath}-owl.[{",".join(OWL_SERIALIZATIONS)}]')


global_triples = []
# iterate over all CSV files for specific vocab e.g. dpv
for vocab, vocab_data in CSVFILES.items():
    # work with modules within each structure e.g core
    namespace = NAMESPACES[vocab]
    INFO('-'*40)
    INFO(f'VOCAB: {vocab} ({namespace})')
    INFO('-'*40)
    vocab_triples = []
    PROPOSED[vocab] = {}
    for module, module_data in vocab_data.items():
        # get schemas and data for each csv in module
        module_triples = []
        PROPOSED[vocab][module] = []
        for schema_name, filepath in module_data.items():
            schema = vocab_schemas.get_schema(schema_name)
            INFO(f'MODULE: {module}')
            INFO(f'parsing {filepath} with schema: {schema_name}')
            header, csvdata = load_CSV(filepath)
            # clean data (dangling spaces)
            header = [x.strip() for x in header]
            # csvdata is a list of dicts containing column:value
            for row in csvdata:
                if not row['Term']: # skip empty rows
                    continue
                # clean data (dangling spaces)
                row = {x.strip():y.strip() for x,y in row.items()}
                # filter proposed terms
                if 'Status' not in row:
                    continue
                if row['Status'] == 'proposed':
                    # TODO: skip rows if they don't have a status
                    PROPOSED[vocab][module].append(row['Term'])
                    continue
                # skip empty rows, annotations, deprecated concepts
                if row['Status'] not in VOCAB_TERM_ACCEPT:
                    continue
                # create a dict to hold the row data
                for index, item in enumerate(row.values()):
                    # get function to handle column value
                    func = schema[header[index]]
                    # empty func or item means no triples to be generated
                    if func is None:
                        continue
                    if not item:
                        continue
                    module_triples += func(item, row, namespace, header[index])
        classes = []
        properties = []
        for s, p, o in module_triples:
            # DEBUG(f'{s} {p} {o}')
            if p != RDF.type: continue
            if o == RDFS.Class: classes.append(s)
            elif o == RDF.Property: properties.append(s)
        if classes:
            module_triples.append((namespace[f"{module.replace('_','-')}-classes"], RDF.type, SKOS.ConceptScheme))
            for c in classes:
                module_triples.append((c, SKOS.inScheme, namespace[f"{module.replace('_','-')}-classes"]))
                if c in EXAMPLES:
                    for ex in EXAMPLES[c]:
                        module_triples.append((c, VANN.example, DEX[ex]))
        if properties:
            module_triples.append((namespace[f"{module.replace('_','-')}-properties"], RDF.type, SKOS.ConceptScheme))
            for p in properties:
                module_triples.append((p, SKOS.inScheme, namespace[f"{module.replace('_','-')}-properties"]))
                if p in EXAMPLES:
                    for ex in EXAMPLES[p]:
                        module_triples.append((p, VANN.example, DEX[ex]))
        INFO(f'Triples: {len(module_triples)} accepted for {len(classes)} classes and {len(properties)} properties, with {len(PROPOSED[vocab][module])} proposed')
        # export module triples
        exportpath = RDF_STRUCTURE[vocab]['modules']
        filepath = f'{exportpath}/{module}'
        serialize_graph(module_triples, filepath)
        vocab_triples += module_triples
    # export vocab triples
    exportpath = RDF_STRUCTURE[vocab]['main']
    filepath = f'{exportpath}/{vocab}'
    serialize_graph(vocab_triples, filepath)
    INFO(f'VOCAB triples: {len(vocab_triples)} accepted, {sum((len(m) for m in PROPOSED[vocab].values()))} proposed')
    global_triples += vocab_triples
INFO('-'*40)
INFO(f'TOTAL triples: {len(global_triples)} accepted')
INFO('-'*40)


INFO('Creating collated collections')
INFO('-'*40)

collations = ({
    'name': 'legal',
    'input': (
        f'{EXPORT_RDF_PATH}/legal/eu/legal-eu.ttl',
        f'{EXPORT_RDF_PATH}/legal/de/legal-de.ttl',
        f'{EXPORT_RDF_PATH}/legal/ie/legal-ie.ttl',
        f'{EXPORT_RDF_PATH}/legal/gb/legal-gb.ttl',
        f'{EXPORT_RDF_PATH}/legal/us/legal-us.ttl',
        ),
    'output': f'{EXPORT_RDF_PATH}/legal/legal',
},)

for collation in collations:
    INFO(f"Collating {collation['name']}")
    triples = Graph()
    for filepath in collation['input']:
        triples.parse(filepath)
    serialize_graph(triples, collation['output'])
    INFO(f"Collected {len(triples)} triples into {collation['output']}")

INFO('-'*40)