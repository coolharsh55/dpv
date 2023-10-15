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
        }
    }
}

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
            # DEBUG(row)
            terms.append(row)
    return header, terms


global_triples = []
# iterate over all CSV files for specific vocab e.g. dpv
for vocab, vocab_data in CSVFILES.items():
    # work with modules within each structure e.g core
    namespace = NAMESPACES[vocab]
    DEBUG(f'VOCAB: {vocab} with NAMESPACE: {namespace}')
    vocab_triples = []
    for module, module_data in vocab_data.items():
        DEBUG('MODULE: {module}')
        # get schemas and data for each csv in module
        module_triples = []
        for schema_name, filepath in module_data.items():
            DEBUG(f'HANDLING: {vocab}-{module} -- {schema_name}')
            schema = vocab_schemas.get_schema(schema_name)
            # RESUMEHERE: take the schema and create a copy of it for row
            # data such the the row is a dict and can be used with
            # form data['header-label'] e.g. data['ParentType']
            # Then in vocab_funcs get the data required i.e. IRI and
            # ParentType using the dict rather than relying on row index.
            DEBUG(f'Using schema: {schema_name}')
            header, csvdata = load_CSV(filepath)
            for row in csvdata:
                for index, item in enumerate(row):
                    func = schema[header[index]]
                    # TODO: filter proposed terms to another dict
                    # empty func or item means no triples to be generated
                    if func is None:
                        continue
                    if not item:
                        continue
                    # DEBUG(f'{func} :: {item}')
                    module_triples += func(item, row, namespace)
        for triple in module_triples:
            DEBUG(triple)
        vocab_triples += module_triples
    global_triples += vocab_triples
