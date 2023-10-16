#!/usr/bin/env python3
#author: Harshvardhan J. Pandit 

'''Generates ReSpec documentation for DPV using RDF and SPARQL'''

# The vocabularies are modular

IMPORT_PATH = '..'
EXPORT_PATH = '..'
TEMPLATE_PATH = './jinja2_resources'

import json
from rdflib import Graph, Namespace
from rdflib import RDF, RDFS, OWL
from rdflib import URIRef
from rdform import DataGraph, RDFS_Resource
import logging
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug

from vocab_management import generate_author_affiliation, NAMESPACES, NS


# What does HTML document require?
# per-vocab: modules and concepts/properties within the module
# dynamic content - number of subclasses/instances
# structured contents: prefixed form, term name from IRI

# How to do this?
# load all vocabulary files - create a global dict
VOCABS = {
    'dpv': {
        'vocab': f'{IMPORT_PATH}/dpv/dpv.ttl',
        'modules': {
            'core': f'{IMPORT_PATH}/dpv/modules/core.ttl',
            'personal_data': f'{IMPORT_PATH}/dpv/modules/personal_data.ttl',
            'purposes': f'{IMPORT_PATH}/dpv/modules/purposes.ttl',
        },
        'template': 'template_dpv.jinja2'
    }
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
                    'term': term.split(':')[1]
                }
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
            else:
                obj = str(o)
        DATA.data[vocab] = vocab_data
        for concept in vocab_data.values():
            DATA.concepts[concept['iri']] = concept
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
        # TODO: sort module into classes and properties
        module_data = {
            'classes': {},
            'properties': {},
        }
        for k, v in module_data_temp.items():
            if v['term'][0].islower():
                module_data['properties'][k] = v
            else:
                module_data['classes'][k] = v
        if vocab not in DATA.modules:
            DATA.modules[vocab] = {}
        DATA.modules[vocab][module] = module_data
        return


def get_concept_list(term):
    if not term:
        return []
    if not type(term) is list:
        term = [term]
    return sorted(
        [DATA.concepts[item] for item in term], 
        key=lambda x: x['iri'])


from jinja2 import FileSystemLoader, Environment
template_loader = FileSystemLoader(searchpath=f'{TEMPLATE_PATH}')
template_env = Environment(
    loader=template_loader, 
    autoescape=True, trim_blocks=True, lstrip_blocks=True)

JINJA2_FILTERS = {
    'fragment_this': lambda x: x,
    'prefix_this': lambda x: x,
    'subclasses': lambda x: x,
    'saved_label': lambda x: x,
    'generate_author_affiliation': generate_author_affiliation,
    'get_example_title': lambda x: x,
    'get_namespace_reference': lambda x: x,
    'get_concept_list': get_concept_list,
}
template_env.filters.update(JINJA2_FILTERS)


if __name__ == '__main__':
    for vocab, vocab_data in VOCABS.items(): 
        DEBUG(f'VOCAB: {vocab}')
        DATA.load_vocab(vocab_data['vocab'], vocab)
        for module, filepath in vocab_data['modules'].items():
            DATA.load_module(filepath, module, vocab)

        template = template_env.get_template(vocab_data['template'])
        with open(f'{EXPORT_PATH}/{vocab}/index.html', 'w+') as fd:
            fd.write(template.render(
                data=DATA.data,
                vocab=DATA.data['dpv'],
                modules=DATA.modules['dpv']))
        DEBUG(f'wrote {vocab} spec at f{EXPORT_PATH}/{vocab}/index.html')
        with open(f'{EXPORT_PATH}/{vocab}/{vocab}.html', 'w+') as fd:
            fd.write(template.render(
                data=DATA.data,
                vocab=DATA.data['dpv'],
                modules=DATA.modules['dpv']))
        DEBUG(f'wrote {vocab} spec at f{EXPORT_PATH}/{vocab}/{vocab}.html')
# load a module file - create a dict with references to the global list

    # for k, v in DATA.data.items():
    #     for i, j in v.items():
    #         if not i.startswith("_module"):
    #             continue
    #         DEBUG(f"{i}")
    #         DEBUG(j.keys())
