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

IMPORT_CSV_PATH = './vocab_csv'
EXPORT_DPV_PATH = '../dpv'
EXPORT_DPV_MODULE_PATH = '../dpv/modules'
EXPORT_DPV_GDPR_PATH = '../dpv-gdpr'
EXPORT_DPV_GDPR_MODULE_PATH = '../dpv-gdpr/modules'
EXPORT_DPV_DGA_PATH = '../dpv-dga'
EXPORT_DPV_DGA_MODULE_PATH = '../dpv-dga/modules'
EXPORT_DPV_PD_PATH = '../dpv-pd'
EXPORT_DPV_LEGAL_PATH = '../dpv-legal'
EXPORT_DPV_LEGAL_MODULE_PATH = '../dpv-legal/modules'
EXPORT_DPV_TECH_PATH = '../dpv-tech'
EXPORT_DPV_TECH_MODULE_PATH = '../dpv-tech/modules'
EXPORT_RISK_PATH = '../risk'
EXPORT_RISK_MODULE_PATH = '../risk/modules'
EXPORT_RIGHTS_EU_PATH = '../rights/eu'

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

CSVFILES = {
    'dpv': {
        'core': {
            'classes': f'{IMPORT_CSV_PATH}/BaseOntology.csv',
            # 'properties': f'{IMPORT_CSV_PATH}/BaseOntology_properties.csv',
        },
    },
    'dpv-pd': {
        'core': {
            'taxonomy': f'{IMPORT_CSV_PATH}/pd-core.csv',
        },
        'extended': {
            'taxonomy': f'{IMPORT_CSV_PATH}/pd-extended.csv',
        },
    },
}

EXPORTPATH = {
    'dpv': {
        'main': '../dpv',
        'modules': '../dpv/modules',
    },
    'dpv-pd': {
        'main': '../pd',
        'modules': '../pd/modules',
    },
}

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
        # DEBUG(f'CSV has header: {header}')
        terms = []
        for row in csvreader:
            # skip empty rows
            if not row[0].strip():
                continue
            # extract required amount of terms, ignore any field after that
            row = [term.strip() for term in row[:count]]
            rowdata = {}
            for index, item in enumerate(row):
                rowdata[header[index]] = row[index]
            # DEBUG(rowdata)
            terms.append(rowdata)
    return header, terms


def serialize_graph(triples, filepath):
    '''serializes triples at filepath with defined formats'''
    graph = Graph()
    for prefix, namespace in NAMESPACES.items():
        graph.namespace_manager.bind(prefix, namespace)
    for triple in triples:
        # DEBUG(triple)
        graph.add(triple)
    for ext, format in RDF_SERIALIZATIONS.items():
        graph.serialize(f'{filepath}.{ext}', format=format)
        INFO(f'wrote {filepath}.{ext}')


global_triples = []
# iterate over all CSV files for specific vocab e.g. dpv
for vocab, vocab_data in CSVFILES.items():
    # work with modules within each structure e.g core
    namespace = NAMESPACES[vocab]
    DEBUG(f'VOCAB: {vocab} with NAMESPACE: {namespace}')
    vocab_triples = []
    PROPOSED[vocab] = {}
    for module, module_data in vocab_data.items():
        DEBUG('MODULE: {module}')
        # get schemas and data for each csv in module
        module_triples = []
        PROPOSED[vocab][module] = []
        for schema_name, filepath in module_data.items():
            DEBUG(f'HANDLING: {vocab}-{module} -- {schema_name}')
            schema = vocab_schemas.get_schema(schema_name)
            DEBUG(f'Using schema: {schema_name}')
            header, csvdata = load_CSV(filepath)
            # csvdata is a list of dicts containing column:value
            for row in csvdata:
                # filter proposed terms
                if row['Status'] == 'proposed':
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
                    # DEBUG(f'{func} :: {item}')
                    module_triples += func(item, row, namespace)
        # export module triples
        exportpath = EXPORTPATH[vocab]['modules']
        filepath = f'{exportpath}/{module}'
        serialize_graph(module_triples, filepath)
        vocab_triples += module_triples
    # export vocab triples
    exportpath = EXPORTPATH[vocab]['main']
    filepath = f'{exportpath}/{vocab}'
    serialize_graph(vocab_triples, filepath)
    global_triples += vocab_triples
