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
            'process': f'{IMPORT_PATH}/dpv/modules/process.ttl',
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
    # EXTENSIONS
    'pd': {
        'vocab': f'{IMPORT_PATH}/pd/pd.ttl',
        'template': 'template_pd.jinja2',
        'export': f'{EXPORT_PATH}/pd',
        'modules': {
            'core': f'{IMPORT_PATH}/pd/modules/core.ttl',
            'extended': f'{IMPORT_PATH}/pd/modules/extended.ttl',
        },
    },
    'tech': {
        'vocab': f'{IMPORT_PATH}/tech/tech.ttl',
        'template': 'template_tech.jinja2',
        'export': f'{EXPORT_PATH}/tech',
        'modules': {
            'core': f'{IMPORT_PATH}/tech/modules/core.ttl',
            'data': f'{IMPORT_PATH}/tech/modules/data.ttl',
            'ops': f'{IMPORT_PATH}/tech/modules/ops.ttl',
            'security': f'{IMPORT_PATH}/tech/modules/security.ttl',
            'surveillance': f'{IMPORT_PATH}/tech/modules/surveillance.ttl',
            'provision': f'{IMPORT_PATH}/tech/modules/provision.ttl',
            'actors': f'{IMPORT_PATH}/tech/modules/actors.ttl',
            'comms': f'{IMPORT_PATH}/tech/modules/comms.ttl',
            'provision': f'{IMPORT_PATH}/tech/modules/provision.ttl',
            'tools': f'{IMPORT_PATH}/tech/modules/tools.ttl',
        },
    },
    'risk': {
        'vocab': f'{IMPORT_PATH}/risk/risk.ttl',
        'template': 'template_risk.jinja2',
        'export': f'{EXPORT_PATH}/risk',
        'modules': {
            'risk_consequences': f'{IMPORT_PATH}/risk/modules/risk_consequences.ttl',
            'risk_levels': f'{IMPORT_PATH}/risk/modules/risk_levels.ttl',
            'risk_matrix': f'{IMPORT_PATH}/risk/modules/risk_matrix.ttl',
            'risk_controls': f'{IMPORT_PATH}/risk/modules/risk_controls.ttl',
            'risk_assessment': f'{IMPORT_PATH}/risk/modules/risk_assessment.ttl',
            'risk_methodology': f'{IMPORT_PATH}/risk/modules/risk_methodology.ttl',
        }
    },
    'loc': {
        'vocab': f'{IMPORT_PATH}/loc/loc.ttl',
        'template': 'template_locations.jinja2',
        'export': f'{EXPORT_PATH}/loc',
        'modules': {
            'locations': f'{IMPORT_PATH}/loc/modules/locations.ttl',
        },
    },
    # LEGAL VOCABS
    # 'legal-eu': {
    #     'vocab': f'{IMPORT_PATH}/legal/eu/legal-eu.ttl',
    #     'template': 'template_legal_jurisdiction.jinja2',
    #     'export': f'{EXPORT_PATH}/legal/eu',
    # },
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
            'legal_basis-rights_mapping': f'{IMPORT_PATH}/legal/eu/gdpr/modules/legal_basis_rights_mapping.ttl',
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
    'eu-rights': {
        'vocab': f'{IMPORT_PATH}/legal/eu/rights/eu-rights.ttl',
        'template': 'template_legal_eu_rights.jinja2',
        'export': f'{EXPORT_PATH}/legal/eu/rights',
        'modules': {},
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
    concepts_prefixed = {}
    

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
                    'prefix': term.split(':')[0],
                    'term': term.split(':')[1],
                    'vocab': vocab,
                    'namespace': s.replace(term.split(':')[1], ''),
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
                DATA.concepts_prefixed[obj] = DATA.concepts[o]
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
            if '_type' not in concept:
                concept['_type'] = 'notcp'
                # DEBUG(f"concept has no type {concept['prefixed']}")

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
            if 'module' not in DATA.data[vocab][term]:
                DATA.data[vocab][term]['module'] = []
            if module not in DATA.data[vocab][term]['module']:
                DATA.data[vocab][term]['module'].append(module)
        module_data = {
            'metadata': {'prefix': vocab, 'name': {module}},
            'classes': {},
            'properties': {},
            'schemes': {},
        }
        for k, v in module_data_temp.items():
            # DEBUG(v['iri'])
            # DEBUG(v.keys())
            if '_type' not in v:
                logging.warning(f"{v['iri']} has misconfigured information")
                continue
            if v['_type'] == 'class':
                module_data['classes'][k] = v
            elif v['_type'] == 'property':
                module_data['properties'][k] = v
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
        return


def get_concept_list(term):
    if not term:
        return []
    if not type(term) is list:
        term = [term]
    return sorted(
        [DATA.concepts[item] for item in term], 
        key=lambda x: x['iri'])


def get_parent_hierarchy(term):
    # DEBUG(f'getting parents for {term["prefixed"]}')
    if 'skos:broader' not in term: return []
    terms = term['skos:broader']
    if type(terms) is not list: terms = [terms]
    # DEBUG(f'parentlist: {terms}')

    ancestor_set = set()
    ancestory = []
    
    def _get_ancestor(term, ancestorlist):
        # if there are no parents, this is the ancestor
        # DEBUG(f'{term} :: {ancestorlist}')
        if 'skos:broader' not in DATA.concepts[term]:
            # DEBUG('path complete')
            ancestory.append(ancestorlist)
            return
        # there are parents, so find grandparents
        parents = DATA.concepts[term]['skos:broader']
        if type(parents) is list:
            for parent in parents:
                ancestor_set.add(parent)
                parentlist = ancestorlist.copy()
                parentlist.append(parent)
                _get_ancestor(parent, parentlist)
        else:
            ancestorlist.append(parents)
            ancestor_set.add(parents)
            _get_ancestor(parents, ancestorlist)
        return

    for parent in terms:
        _get_ancestor(parent, [parent])
    ancestorlist = [
        parentlist for parentlist in ancestory
        if parentlist[0] not in ancestor_set]    
    ancestory = []
    for parentlist in ancestorlist:
        ancestory.append([DATA.concepts[parent] for parent in parentlist])
    return ancestory


def get_children_hierarchy(term):
    # DEBUG(f'getting parents for {term["prefixed"]}')
    if 'skos:narrower' not in term: return []
    terms = term['skos:narrower']
    if type(terms) is not list: terms = [terms]
    # DEBUG(f'parentlist: {terms}')

    ancestor_set = set()
    ancestory = []
    
    def _get_ancestor(term, ancestorlist):
        # if there are no parents, this is the ancestor
        # DEBUG(f'{term} :: {ancestorlist}')
        if 'skos:narrower' not in DATA.concepts[term]:
            # DEBUG('path complete')
            ancestory.append(ancestorlist)
            return
        # there are parents, so find grandparents
        parents = DATA.concepts[term]['skos:narrower']
        if type(parents) is list:
            for parent in parents:
                ancestor_set.add(parent)
                parentlist = ancestorlist.copy()
                parentlist.append(parent)
                _get_ancestor(parent, parentlist)
        else:
            ancestorlist.append(parents)
            ancestor_set.add(parents)
            _get_ancestor(parents, ancestorlist)
        return

    for parent in terms:
        _get_ancestor(parent, [parent])
    ancestorlist = [
        parentlist for parentlist in ancestory
        if parentlist[0] not in ancestor_set]    
    ancestory = []
    for parentlist in ancestorlist:
        ancestory.append([DATA.concepts[parent] for parent in parentlist])
    return ancestory

def organise_hierarchy(terms, top=None):
    '''organise the given list of terms into a hierarchy
    returns { parent: { children: { children: { } } } }'''
    data = {}
    for term in terms:
        data[term] = { 'parents': [], 'children': [] }
    if 'prefix' in data:
        del data['prefix'] # this isn't a term
    for key, term in terms.items():
        if 'skos:broader' in term: # has parents
            parents = term['skos:broader'] # get parents
            if type(parents) is not list: # single parent
                parents = [parents]
            # DEBUG(f'{key} -> {parents}')
            for parent in parents: # check parents are not present in terms
                if prefix_from_iri(parent) in terms:
                    data[key]['parents'].append(prefix_from_iri(parent))
                    data[prefix_from_iri(parent)]['children'].append(key)
    
    if top is None:
        results = {k:terms[k] for k,v in data.items() if not v['parents']}
    else:
        results = {k:terms[k] for k,v in data.items() if top in v['parents']}
    return {k:results[k] for k in sorted(results.keys(), key=str.casefold)}


def get_sources(sourcestring):
    sourcestring = sourcestring.replace('(', '').replace(')', '').split(',')
    sources = []
    for i in range(1, len(sourcestring), 2):
        sources.append((sourcestring[i], sourcestring[i-1]))
    return sources


def ensure_list(item):
    if type(item) is not list:
        item = [item]
    return item


def filter_type(itemlist, itemtype, vocab=None):
    results = []
    # DEBUG(itemtype)
    # DEBUG(itemlist)
    for item in itemlist:
        if type(item) is dict:
            itemvocab = item['vocab']
        else:
            itemvocab = item.split(':')[0]
            # DEBUG(item)
            if itemvocab not in DATA.data:
                continue
            item = DATA.data[itemvocab][item]
        if not vocab or vocab != itemvocab or 'rdf:type' not in item:
            continue
        parents = item['rdf:type']
        if type(parents) is not list:
            parents = [parents]
        for p in parents:
            prefixed = prefix_from_iri(p)
            if prefixed == itemtype:
                results.append(item)
    return results


def get_prop_with_term_domain(term, vocab):
    props = []
    term_types = term['rdf:type']
    term_types = [str(x) for x in term_types]
    term_types.append(str(term['iri']))
    # DEBUG(term_types)
    for prop in DATA.concepts.values():
        # DEBUG(prop['prefixed'])
        if '_type' not in prop: continue
        if prop['_type'] != 'property': continue
        if 'dcam:domainIncludes' not in prop: continue
        domains = prop['dcam:domainIncludes']
        # DEBUG(f"{prop['prefixed']} - domains {domains}")
        if type(domains) is not list: domains = [domains]
        for domain in domains:
            for t in term_types:
                # DEBUG(type(domain))
                # DEBUG(f"{domain} x {t} = {domain == t}")
                if str(domain) == t:
                    props.append(prop)
                    # DEBUG(f"{term['prefixed']} range {prop['prefixed']}")
    return props


def get_prop_with_term_range(term, vocab):
    props = []
    term_types = term['rdf:type']
    term_types = [str(x) for x in term_types]
    term_types.append(str(term['iri']))
    # DEBUG(term_types)
    for prop in DATA.concepts.values():
        # DEBUG(prop['prefixed'])
        if '_type' not in prop: continue
        if prop['_type'] != 'property': continue
        if 'dcam:rangeIncludes' not in prop: continue
        domains = prop['dcam:rangeIncludes']
        # DEBUG(f"{prop['prefixed']} - domains {domains}")
        if type(domains) is not list: domains = [domains]
        for domain in domains:
            for t in term_types:
                # DEBUG(type(domain))
                # DEBUG(f"{domain} x {t} = {domain == t}")
                if str(domain) == t:
                    props.append(prop)
                    # DEBUG(f"{term['prefixed']} range {prop['prefixed']}")
    return props


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
    'get_parent_hierarchy': get_parent_hierarchy,
    'get_children_hierarchy': get_children_hierarchy,
    'organise_hierarchy': organise_hierarchy,
    'get_sources': get_sources,
    'ensure_list': ensure_list,
    'filter_type': filter_type,
    'get_prop_with_term_domain': get_prop_with_term_domain,
    'get_prop_with_term_range': get_prop_with_term_range,
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
            module_data[module_name]['prefix'] = vocab
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
