#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

'''Extracts Namespaces from CSV and builds RDFLib objects'''

import csv
from rdflib import Namespace

import logging
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug
INFO = logging.info

###################### serializations 
# in the form of extention: rdflib name
RDF_SERIALIZATIONS = {
    'rdf': 'xml', 
    'ttl': 'turtle', 
    'n3': 'n3',
    'jsonld': 'json-ld'
    }


###################### vocab term statuses
VOCAB_TERM_ACCEPT = ('accepted', 'changed', 'modified', 'sunset')
VOCAB_TERM_REJECT = ('deprecated', 'removed')


###################### namespaces
NAMESPACE_CSV = (
	'vocab_csv/Namespaces.csv',
	'vocab_csv/Namespaces_Other.csv',
	)
NAMESPACES = {}
for csvfile in NAMESPACE_CSV:
	# DEBUG(f'Extracting namespaces from {csvfile}')
	with open(csvfile, 'r') as fd:
		csvreader = csv.reader(fd)
		next(csvreader)
		for row in csvreader:
			prefix, iri = row[0], row[1]
			variable = prefix.upper().replace('-', '_')
			namespace = Namespace(iri)
			globals()[variable] = namespace
			NAMESPACES[prefix] = namespace
			# DEBUG(f'{prefix} namespace with IRI {iri}')

from rdflib import Graph
NS = Graph()
NS.ns = { k:v for k,v in NAMESPACES.items() }

def prefix_from_iri(iri):
    # DEBUG(iri)
    for prefix, ns in NAMESPACES.items():
        if iri.startswith(ns):
            term = iri.replace(ns, '')
            # DEBUG(f'prefix: {prefix} :: term {term}')
            return f'{prefix}:{term}'
    return None


###################### CSV files
IMPORT_CSV_PATH = './vocab_csv'
CSVFILES = {
    'dpv': {
        'process': {
            'classes': f'{IMPORT_CSV_PATH}/Process.csv',
            'properties': f'{IMPORT_CSV_PATH}/Process_properties.csv',
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
            'taxonomy': f'{IMPORT_CSV_PATH}/TOM.csv',
            'properties': f'{IMPORT_CSV_PATH}/TOM_properties.csv',
        },
        'technical_measures': {
            'taxonomy': f'{IMPORT_CSV_PATH}/TechnicalMeasure.csv',
        },
        'organisational_measures': {
            'taxonomy': f'{IMPORT_CSV_PATH}/OrganisationalMeasure.csv',
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
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskAssessment.csv',
        },
        'risk_methodology': {
            'taxonomy': f'{IMPORT_CSV_PATH}/RiskMethodology.csv',
        },
    },
    'loc': {
        'locations': {
            'locations': f'{IMPORT_CSV_PATH}/location.csv',
            'properties': f'{IMPORT_CSV_PATH}/location_properties.csv',
        },
    },
    # Laws-Authorities
    # 'legal-eu': {
    #     'eu': {
    #         'law': f'{IMPORT_CSV_PATH}/legal-eu.csv',
    #     },
    # },
    # 'legal-de': {
    #     'de': {
    #         'law': f'{IMPORT_CSV_PATH}/legal-de.csv',
    #     },
    # },
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
        'legal_basis_rights_mapping': {
            'legal_basis_rights_mapping': f'{IMPORT_CSV_PATH}/GDPR_LegalBasis_Rights_Mapping.csv',
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

EXPORT_RDF_PATH = '..'
RDF_STRUCTURE = {
    'dpv': {
        'main': f'{EXPORT_RDF_PATH}/dpv',
        'modules': f'{EXPORT_RDF_PATH}/dpv/modules',
    },
    'pd': {
        'main': f'{EXPORT_RDF_PATH}/pd',
        'modules': f'{EXPORT_RDF_PATH}/pd/modules',
    },
    'tech': {
        'main': f'{EXPORT_RDF_PATH}/tech',
        'modules': f'{EXPORT_RDF_PATH}/tech/modules',
    },
    'risk': {
        'main': f'{EXPORT_RDF_PATH}/risk',
        'modules': f'{EXPORT_RDF_PATH}/risk/modules',
    },
    'loc': {
        'main': f'{EXPORT_RDF_PATH}/loc',
        'modules': f'{EXPORT_RDF_PATH}/loc/modules',
    },
    
    'legal-eu': {
        'main': f'{EXPORT_RDF_PATH}/legal/eu',
    },
    'legal-de': {
        'main': f'{EXPORT_RDF_PATH}/legal/de',
    },
    'eu-gdpr': {
        'main': f'{EXPORT_RDF_PATH}/legal/eu/gdpr',
        'modules': f'{EXPORT_RDF_PATH}/legal/eu/gdpr/modules',
    },
    'eu-dga': {
        'main': f'{EXPORT_RDF_PATH}/legal/eu/dga',
        'modules': f'{EXPORT_RDF_PATH}/legal/eu/dga/modules',
    },
    'eu-rights': {
        'main': f'{EXPORT_RDF_PATH}/legal/eu/rights',
        'modules': f'{EXPORT_RDF_PATH}/legal/eu/rights/modules',
    },
}

###################### contributors

'''A Jinja2 filter that takes author names and returns their affiliations'''

import json

with open('../contributors.json', 'r') as fd:
    contributors = json.load(fd)


def generate_author_affiliation(author):
    '''takes author name, returns affiliation'''
    if author in contributors:
        return contributors[author]
    else:
        return ''


def generate_authors_affiliations(authors):
    '''takes author name, returns affiliation'''
    authors = [contributors[author] for author in contributors]
    return authors