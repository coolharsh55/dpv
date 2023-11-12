#!/usr/bin/env python3
#author: Harshvardhan J. Pandit 

'''Generates ReSpec documentation for DPV using RDF and SPARQL'''

# The vocabularies are modular

IMPORT_PATH = '..'
EXPORT_PATH = '..'
TEMPLATE_PATH = './jinja2_resources'

import json
from rdflib import Graph, Namespace
from rdflib import RDF, RDFS, OWL, SKOS
from rdflib import URIRef
from rdform import DataGraph, RDFS_Resource
import logging
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug

from vocab_management import generate_author_affiliation, NAMESPACES, NS
from vocab_management import prefix_from_iri


# What does HTML document require?
# per-vocab: modules and concepts/properties within the module
# dynamic content - number of subclasses/instances
# structured contents: prefixed form, term name from IRI

# How to do this?
# load all vocabulary files - create a global dict
VOCABS = {
    'dpv': {
        'vocab': f'{IMPORT_PATH}/dpv/dpv.ttl',
        'template': 'template_dpv.jinja2',
        'export': f'{EXPORT_PATH}/dpv',
        'modules': {
            # 'core': f'{IMPORT_PATH}/dpv/modules/core.ttl',
            'personal_data': f'{IMPORT_PATH}/dpv/modules/personal_data.ttl',
            'purposes': f'{IMPORT_PATH}/dpv/modules/purposes.ttl',
            'processing': f'{IMPORT_PATH}/dpv/modules/processing.ttl',
            'TOM': f'{IMPORT_PATH}/dpv/modules/TOM.ttl',
            'TOM-technical': f'{IMPORT_PATH}/dpv/modules/technical_measures.ttl',
            'TOM-organisational': f'{IMPORT_PATH}/dpv/modules/organisational_measures.ttl',
            'entities': f'{IMPORT_PATH}/dpv/modules/entities.ttl',
            'entities-authority': f'{IMPORT_PATH}/dpv/modules/entities_authority.ttl',
            'entities-legalrole': f'{IMPORT_PATH}/dpv/modules/entities_legalrole.ttl',
            'entities-organisation': f'{IMPORT_PATH}/dpv/modules/entities_organisation.ttl',
            'entities-datasubject': f'{IMPORT_PATH}/dpv/modules/entities_datasubject.ttl',
            'legal_basis': f'{IMPORT_PATH}/dpv/modules/legal_basis.ttl',
            'legal_basis-consent': f'{IMPORT_PATH}/dpv/modules/consent.ttl',
            'legal_basis-consent-types': f'{IMPORT_PATH}/dpv/modules/consent_types.ttl',
            'legal_basis-consent-status': f'{IMPORT_PATH}/dpv/modules/consent_status.ttl',
            'processing-context': f'{IMPORT_PATH}/dpv/modules/processing_context.ttl',
            'processing-scale': f'{IMPORT_PATH}/dpv/modules/processing_scale.ttl',
            'context': f'{IMPORT_PATH}/dpv/modules/context.ttl',
            'context-status': f'{IMPORT_PATH}/dpv/modules/status.ttl',
            'context-jurisdiction': f'{IMPORT_PATH}/dpv/modules/jurisdiction.ttl',
            'risk': f'{IMPORT_PATH}/dpv/modules/risk.ttl',
            'rights': f'{IMPORT_PATH}/dpv/modules/rights.ttl',
            'rules': f'{IMPORT_PATH}/dpv/modules/rules.ttl',
        },
        'module-template': {
            'entities': 'contents_dpv_entities.jinja2',
            'purposes': 'contents_dpv_purposes.jinja2',
            'processing': 'contents_dpv_processing.jinja2',
            'TOM': 'contents_dpv_TOM.jinja2',
            'legal_basis': 'contents_dpv_legal_basis.jinja2',
            'context': 'contents_dpv_context.jinja2',
            'risk': 'contents_dpv_risk.jinja2',
            'rights': 'contents_dpv_rights.jinja2',
            'rules': 'contents_dpv_rules.jinja2',
        },
    },
    'pd': {
        'vocab': f'{IMPORT_PATH}/pd/pd.ttl',
        'template': 'template_dpv_pd.jinja2',
        'export': f'{EXPORT_PATH}/pd',
        'modules': {
            'core': f'{IMPORT_PATH}/pd/modules/core.ttl',
            'extended': f'{IMPORT_PATH}/pd/modules/extended.ttl',
        },
    },
    'eu-gdpr': {
        'vocab': f'{IMPORT_PATH}/legal/eu/gdpr/eu-gdpr.ttl',
        'template': 'template_legal_eu_gdpr.jinja2',
        'export': f'{EXPORT_PATH}/legal/eu/gdpr',
        'modules': {
            'legal_basis': f'{IMPORT_PATH}/legal/eu/gdpr/modules/legal_basis.ttl',
            'legal_basis-special': f'{IMPORT_PATH}/legal/eu/gdpr/modules/legal_basis_special.ttl',
            'legal_basis-data_transfer': f'{IMPORT_PATH}/legal/eu/gdpr/modules/legal_basis_data_transfer.ttl',
            'rights': f'{IMPORT_PATH}/legal/eu/gdpr/modules/rights.ttl',
            'data_transfers': f'{IMPORT_PATH}/legal/eu/gdpr/modules/data_transfers.ttl',
            'dpia': f'{IMPORT_PATH}/legal/eu/gdpr/modules/dpia.ttl',
            'compliance': f'{IMPORT_PATH}/legal/eu/gdpr/modules/compliance.ttl',
        },
    },
    'eu-dga': {
        'vocab': f'{IMPORT_PATH}/legal/eu/dga/eu-dga.ttl',
        'template': 'template_legal_eu_dga.jinja2',
        'export': f'{EXPORT_PATH}/legal/eu/dga',
        'modules': {
            'entities': f'{IMPORT_PATH}/legal/eu/dga/modules/entities.ttl',
            'legal_basis': f'{IMPORT_PATH}/legal/eu/dga/modules/legal_basis.ttl',
            'legal_rights': f'{IMPORT_PATH}/legal/eu/dga/modules/legal_rights.ttl',
            'registers': f'{IMPORT_PATH}/legal/eu/dga/modules/registers.ttl',
            'services': f'{IMPORT_PATH}/legal/eu/dga/modules/services.ttl',
            'toms': f'{IMPORT_PATH}/legal/eu/dga/modules/toms.ttl',
        },
    },
}

class DATA(object):
    # data = {
    #     vocab: {
    #         term: { rel: obj },
    #         _module_name: { term: ref-to-term }
    #     }
    # }
    data = {}
    modules = {}
    schemes = {}
    concepts = {}
    

    @staticmethod
    def get_X(param):
        return

    @staticmethod
    def load_vocab(filepath, vocab):
        DEBUG(f'loading {vocab} data from {filepath}')
        graph = Graph()
        graph.parse(filepath)
        graph.ns = { k:v for k,v in NAMESPACES.items() }
        vocab_data = {}
        for s, p, o in graph:
            # DEBUG(f'{s} {p} {o}')
            # DEBUG(s.n3(graph.namespace_manager))
            # gets prefix:term using the n3 notation
            # convert s,p,o into prefixed terms and literals
            term = s.n3(graph.namespace_manager)
            rel = p.n3(graph.namespace_manager)
            # DEBUG(f"{term} {rel} {obj}")

            # if this is the first occurence, add to dict
            if term not in vocab_data:
                vocab_data[term] = {
                    'iri': s,
                    'prefixed': term,
                    'term': term.split(':')[1],
                    '_dpvterm': s.startswith('https://w3id.org/dpv'),
                }
                if not vocab_data[term]['_dpvterm']:
                    vocab_data[term]['term'] = term
            term = vocab_data[term]
            
            # add contents for p and o
            if p in term:
                if type(term[p]) is list:
                    term[p].append(o)
                    term[rel].append(o)
                else:
                    term[p] = [term[p], o]
                    term[rel] = [term[rel], o]
            else:
                term[p] = o
                term[rel] = o
            if o.startswith('http'):
                obj = o.n3(graph.namespace_manager)
                DATA.concepts[o] = {
                    'iri': o,
                    'prefixed': obj,
                    'term': obj.split(':')[1]
                }
                if p == RDF.type and o == RDFS.Class:
                    term['_type'] = "class"
                elif p == RDF.type and o == RDF.Property:
                    term['_type'] = "property" 
                elif p == SKOS.inScheme:
                    if prefix_from_iri(o) not in DATA.schemes:
                        DATA.schemes[prefix_from_iri(o)] = {}
                    DATA.schemes[prefix_from_iri(o)][term['prefixed']] = term
            else:
                obj = str(o)
        DATA.data[vocab] = vocab_data
        for concept in vocab_data.values():
            DATA.concepts[concept['iri']] = concept

        # for scheme in DATA.schemes:
        #     DEBUG(f'registered scheme {prefix_from_iri(scheme)}')
        return

    @staticmethod
    def hierarchical_classes(concepts):
        # TODO: produce hierarchical view of classes
        # to be used as nested lists in HTML
        hierarchy = []
        return hierarchy

    @staticmethod
    def load_module(filepath, module, vocab):
        DEBUG(f'loading {vocab}:{module} data from {filepath}')
        graph = Graph()
        graph.parse(filepath)
        graph.ns = { k:v for k,v in NAMESPACES.items() }
        module_data_temp = {}
        for s, _, _ in graph:
            term = s.n3(graph.namespace_manager)
            module_data_temp[term] = DATA.data[vocab][term]
        module_data = {
            'classes': {},
            'properties': {},
            'schemes': {}
        }
        for k, v in module_data_temp.items():
            if v['term'][0].islower():
                module_data['properties'][k] = v
            else:
                module_data['classes'][k] = v
        if vocab not in DATA.modules:
            DATA.modules[vocab] = {}
        DATA.modules[vocab][module] = module_data

        if f'{vocab}:{module}-classes' in DATA.schemes:
            scheme = DATA.schemes[f'{vocab}:{module}-classes']
            # DEBUG(f'{module} has scheme {vocab}:{module}-classes')
            module_data['schemes']['classes'] = scheme
        if f'{vocab}:{module}-properties' in DATA.schemes:
            scheme = DATA.schemes[f'{vocab}:{module}-properties']
            # DEBUG(f'{module} has scheme {vocab}:{module}-properties')
            module_data['schemes']['properties'] = scheme
        return


def get_concept_list(term):
    if not term:
        return []
    if not type(term) is list:
        term = [term]
    return sorted(
        [DATA.concepts[item] for item in term], 
        key=lambda x: x['iri'])


def organise_hierarchy(terms, top=None):
    '''organise the given list of terms into a hierarchy
    returns { parent: { children: {} } }'''
    data = {}
    for term in terms:
        data[term] = { 'parents': [], 'children': [] }

    for key, term in terms.items():
        if 'skos:broader' in term: # has parents
            parents = term['skos:broader'] # get parents
            if type(parents) is not list: # single parent
                parents = [parents]
            for parent in parents: # check parents are not present in terms
                if prefix_from_iri(parent) in terms:
                    data[key]['parents'].append(prefix_from_iri(parent))
                    data[prefix_from_iri(parent)]['children'].append(key)
    
    if top is None:
        results = {k:terms[k] for k,v in data.items() if not v['parents']}
    else:
        results = {k:terms[k] for k,v in data.items() if top in v['parents']}
    return {k:results[k] for k in sorted(results.keys(), key=str.casefold)}


from jinja2 import FileSystemLoader, Environment
template_loader = FileSystemLoader(searchpath=f'{TEMPLATE_PATH}')
template_env = Environment(
    loader=template_loader, 
    autoescape=True, trim_blocks=True, lstrip_blocks=True)

JINJA2_FILTERS = {
    'fragment_this': lambda x: x,
    'prefix_this': prefix_from_iri,
    'subclasses': lambda x: x,
    'saved_label': lambda x: x,
    'generate_author_affiliation': generate_author_affiliation,
    'get_example_title': lambda x: x,
    'get_namespace_reference': lambda x: x,
    'get_concept_list': get_concept_list,
    'organise_hierarchy': organise_hierarchy,
}
template_env.filters.update(JINJA2_FILTERS)


if __name__ == '__main__':
    for vocab, vocab_data in VOCABS.items(): 
        DEBUG(f'VOCAB: {vocab}')
        DATA.load_vocab(vocab_data['vocab'], vocab)
        module_data = {}
        DATA.modules[vocab] = {}
        for module, filepath in vocab_data['modules'].items():
            DATA.load_module(filepath, module, vocab)
            # create collection to generate module pages
            module_name = module.split('-')[0] # e.g. consent-type = consent
            if module_name not in module_data:
                module_data[module_name] = {}
                module_data[module_name]['index'] = {}
            module_data[module_name][module] = DATA.modules[vocab][module]
            for data in DATA.modules[vocab][module].values():
                for k, v in data.items():
                    module_data[module_name]['index'][k] = v
        # else:
        #     DATA.modules[vocab] = []
        template = template_env.get_template(vocab_data['template'])
        with open(f'{vocab_data["export"]}/index.html', 'w+') as fd:
            fd.write(template.render(
                data=DATA.data,
                vocab=DATA.data[vocab],
                modules=DATA.modules[vocab]))
        DEBUG(f'wrote {vocab} spec at {vocab_data["export"]}/index.html')
        # TODO: replace duplicate code with filecopy
        with open(f'{vocab_data["export"]}/{vocab}.html', 'w+') as fd:
            fd.write(template.render(
                data=DATA.data,
                vocab=DATA.data[vocab],
                modules=DATA.modules[vocab]))
        DEBUG(f'wrote {vocab} spec at {vocab_data["export"]}/{vocab}.html')

        if 'module-template' not in vocab_data:
            continue # this vocab doesn't have module specific docs
        # generate module docs
        for module, data in module_data.items():
            if module not in vocab_data['module-template']:
                DEBUG(f'{module} has no template associated - skipping')
                continue
            DEBUG(f'exporting {module} page')
            template = template_env.get_template(vocab_data['module-template'][module])
            with open(f'{vocab_data["export"]}/modules/{module}.html', 'w+') as fd:
                fd.write(template.render(
                    data=data,
                    vocab=DATA.data[vocab],
                    modules=DATA.modules[vocab]))
                DEBUG(f'wrote {vocab}/{module} docs at {vocab_data["export"]}/modules/{module}.html')
