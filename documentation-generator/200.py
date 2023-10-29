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
EXPORT_PATH = '..'

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
            'properties': f'{IMPORT_CSV_PATH}/BaseOntology_properties.csv',
        },
        'personal_data': {
            'classes': f'{IMPORT_CSV_PATH}/PersonalData.csv',
            'properties': f'{IMPORT_CSV_PATH}/PersonalData_properties.csv',
        },
        'purposes': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Purpose.csv',
            'properties': f'{IMPORT_CSV_PATH}/Purpose_properties.csv',
        },
        'processing': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Processing.csv',
            'properties': f'{IMPORT_CSV_PATH}/Processing_properties.csv',
        },
        'TOM': {
            'taxonomy': f'{IMPORT_CSV_PATH}/TechnicalOrganisationalMeasure.csv',
            'properties': f'{IMPORT_CSV_PATH}/TechnicalOrganisationalMeasure_properties.csv',
        },
        'technical_measures': {
            'classes': f'{IMPORT_CSV_PATH}/TechnicalMeasure.csv',
        },
        'organisational_measures': {
            'classes': f'{IMPORT_CSV_PATH}/OrganisationalMeasure.csv',
        },
        'entities': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Entities.csv',
            'properties': f'{IMPORT_CSV_PATH}/Entities_properties.csv',
        },
        'entities_authority': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Entities_Authority.csv',
            'properties': f'{IMPORT_CSV_PATH}/Entities_Authority_properties.csv',
        },
        'entities_legalrole': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Entities_LegalRole.csv',
            'properties': f'{IMPORT_CSV_PATH}/Entities_LegalRole_properties.csv',
        },
        'entities_organisation': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Entities_Organisation.csv',
        },
        'entities_datasubject': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Entities_DataSubject.csv',
            'properties': f'{IMPORT_CSV_PATH}/Entities_DataSubject_properties.csv',
        },
        'legal_basis': {
            'taxonomy': f'{IMPORT_CSV_PATH}/LegalBasis.csv',
            'properties': f'{IMPORT_CSV_PATH}/LegalBasis_properties.csv',
        },
        'consent': {
            'properties': f'{IMPORT_CSV_PATH}/Consent_properties.csv',
        },
        'consent_types': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ConsentTypes.csv',
        },
        'consent_status': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ConsentStatus.csv',
        },
        'context': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Context.csv',
            'properties': f'{IMPORT_CSV_PATH}/Context_properties.csv',
        },
        'processing_context': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ProcessingContext.csv',
            'properties': f'{IMPORT_CSV_PATH}/ProcessingContext_properties.csv',
        },
        'processing_scale': {
            'taxonomy': f'{IMPORT_CSV_PATH}/ProcessingScale.csv',
            'properties': f'{IMPORT_CSV_PATH}/ProcessingScale_properties.csv',
        },
        'status': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Status.csv',
            'properties': f'{IMPORT_CSV_PATH}/Status_properties.csv',
        },
        'risk': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Risk.csv',
            'properties': f'{IMPORT_CSV_PATH}/Risk_properties.csv',
        },
        'jurisdiction': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Jurisdiction.csv',
            'properties': f'{IMPORT_CSV_PATH}/Jurisdiction_properties.csv',
        },
        'rights': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Rights.csv',
            'properties': f'{IMPORT_CSV_PATH}/Rights_properties.csv',
        },
        'rules': {
            'taxonomy': f'{IMPORT_CSV_PATH}/Rules.csv',
            'properties': f'{IMPORT_CSV_PATH}/Rules_properties.csv',
        },
    },
    'pd': {
        'core': {
            'taxonomy': f'{IMPORT_CSV_PATH}/pd-core.csv',
        },
        'extended': {
            'taxonomy': f'{IMPORT_CSV_PATH}/pd-extended.csv',
        },
    },
    'eu-gdpr': {
        'legal_basis': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_LegalBasis.csv',
        },
        'legal_basis_special': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_LegalBasis_SpecialCategory.csv',
        },
        'legal_basis_data_transfer': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_LegalBasis_DataTransfer.csv',
        },
        'rights': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_LegalRights.csv',
        },
        'data_transfers': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_DataTransfers.csv',
        },
        'dpia': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_DPIA.csv',
            'properties': f'{IMPORT_CSV_PATH}/GDPR_DPIA_properties.csv',
        },
        'compliance': {
            'taxonomy': f'{IMPORT_CSV_PATH}/GDPR_compliance.csv',
        },
    },
    'eu-dga': {
        'legal_basis': {
            'taxonomy': f'{IMPORT_CSV_PATH}/DGA_LegalBasis.csv',
        },
        'legal_rights': {
            'taxonomy': f'{IMPORT_CSV_PATH}/DGA_LegalRights.csv',
        },
        'services': {
            'taxonomy': f'{IMPORT_CSV_PATH}/DGA_Services.csv',
        },
        'registers': {
            'taxonomy': f'{IMPORT_CSV_PATH}/DGA_Registers.csv',
        },
        'toms': {
            'taxonomy': f'{IMPORT_CSV_PATH}/DGA_TOMs.csv',
        },
        'entities': {
            'taxonomy': f'{IMPORT_CSV_PATH}/DGA_entities.csv',
            'properties': f'{IMPORT_CSV_PATH}/DGA_properties.csv',
        },
    },
    'tech': {
        'core': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-core.csv',
            'properties': f'{IMPORT_CSV_PATH}/tech-core-properties.csv',
        },
        'data': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-data.csv',
        },
        'ops': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-ops.csv',
        },
        'security': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-security.csv',
        },
        'surveillance': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-surveillance.csv',
        },
        'provision': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-provision.csv',
            'properties': f'{IMPORT_CSV_PATH}/tech-provision-properties.csv',
        },
        'actors': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-actors.csv',
            'properties': f'{IMPORT_CSV_PATH}/tech-actors-properties.csv',
        },
        'comms': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-comms.csv',
        },
        'provision': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-provision.csv',
            'properties': f'{IMPORT_CSV_PATH}/tech-provision-properties.csv',
        },
        'tools': {
            'taxonomy': f'{IMPORT_CSV_PATH}/tech-tools.csv',
        }, 
    },
    'risk': {
        'risk_consequences': {
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskConsequences.csv',
        },
        'risk_levels': {
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskLevels.csv',
        },
        'risk_matrix': {
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskMatrix.csv',
        },
        'risk_controls': {
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskControls.csv',
        },
        'risk_assessment': {
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskAssessmentTechniques.csv',
        },
        'risk_methodology': {
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskMethodology.csv',
        },
    },
    'eu-rights': {
        'fundamental': {
            'taxonomy': f'{IMPORT_CSV_PATH}/EUFundamentalRights.csv',
        },
    },

    # 'todo': {
    #     f'{IMPORT_CSV_PATH}/legal_Authorities.csv',
    #     f'{IMPORT_CSV_PATH}/legal_EU_Adequacy.csv',
    #     f'{IMPORT_CSV_PATH}/legal_EU_EEA.csv',
    #     f'{IMPORT_CSV_PATH}/legal_Laws.csv',
    #     f'{IMPORT_CSV_PATH}/legal_Locations.csv',
    #     f'{IMPORT_CSV_PATH}/legal_properties.csv',
    # }
}

EXPORTPATH = {
    'dpv': {
        'main': f'{EXPORT_PATH}/dpv',
        'modules': f'{EXPORT_PATH}/dpv/modules',
    },
    'pd': {
        'main': f'{EXPORT_PATH}/pd',
        'modules': f'{EXPORT_PATH}/pd/modules',
    },
    'tech': {
        'main': f'{EXPORT_PATH}/tech',
        'modules': f'{EXPORT_PATH}/tech/modules',
    },
    'risk': {
        'main': f'{EXPORT_PATH}/risk',
        'modules': f'{EXPORT_PATH}/risk/modules',
    },
    'eu-gdpr': {
        'main': f'{EXPORT_PATH}/legal/eu/gdpr',
        'modules': f'{EXPORT_PATH}/legal/eu/gdpr/modules',
    },
    'eu-dga': {
        'main': f'{EXPORT_PATH}/legal/eu/dga',
        'modules': f'{EXPORT_PATH}/legal/eu/dga/modules',
    },
    'eu-rights': {
        'main': f'{EXPORT_PATH}/legal/eu/rights',
        'modules': f'{EXPORT_PATH}/legal/eu/rights/modules',
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
            INFO(f'MODULE: {module} with schema: {schema_name}')
            header, csvdata = load_CSV(filepath)
            # clean data (dangling spaces)
            header = [x.strip() for x in header]
            # csvdata is a list of dicts containing column:value
            for row in csvdata:
                # clean data (dangling spaces)
                row = {x.strip():y.strip() for x,y in row.items()}
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
                    module_triples += func(item, row, namespace)
        INFO(f'Triples: {len(module_triples)} accepted, {len(PROPOSED[vocab][module])} proposed')
        # export module triples
        exportpath = EXPORTPATH[vocab]['modules']
        filepath = f'{exportpath}/{module}'
        serialize_graph(module_triples, filepath)
        vocab_triples += module_triples
    # export vocab triples
    exportpath = EXPORTPATH[vocab]['main']
    filepath = f'{exportpath}/{vocab}'
    serialize_graph(vocab_triples, filepath)
    INFO(f'VOCAB triples: {len(vocab_triples)} accepted, {sum((len(m) for m in PROPOSED[vocab].values()))} proposed')
    global_triples += vocab_triples
INFO('-'*40)
INFO(f'TOTAL triples: {len(global_triples)} accepted')
INFO('-'*40)
