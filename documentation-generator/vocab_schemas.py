###################### schemas

import vocab_funcs

'''adds schemas for each CSV'''
SCHEMAS = {}
def get_schema(name):
    return SCHEMAS[name]

SCHEMAS['classes'] = {
    'Term': vocab_funcs.construct_iri,
    'Label': vocab_funcs.construct_label,
    'Description': vocab_funcs.contruct_description,
    'ParentTerm': vocab_funcs.construct_parent,
    'ParentType': None,
    'Value': vocab_funcs.construct_value,
    'RelatedTerms': vocab_funcs.construct_related_terms,
    'Relation': None,
    'Comment': vocab_funcs.construct_comment,
    'Source': vocab_funcs.construct_source,
    'Created': vocab_funcs.construct_date_created,
    'Modified': vocab_funcs.construct_date_modified,
    'Status': None,
    'Contributors': vocab_funcs.construct_contributors,
    'Resolution': vocab_funcs.construct_resolution, 
}

SCHEMAS['taxonomy'] = {
    'Term': vocab_funcs.construct_iri,
    'Label': vocab_funcs.construct_label,
    'Description': vocab_funcs.contruct_description,
    'ParentTerm': vocab_funcs.construct_parent_taxonomy,
    'ParentType': None,
    'Value': vocab_funcs.construct_value,
    'RelatedTerms': vocab_funcs.construct_related_terms,
    'Relation': None,
    'Comment': vocab_funcs.construct_comment,
    'Source': vocab_funcs.construct_source,
    'Created': vocab_funcs.construct_date_created,
    'Modified': vocab_funcs.construct_date_modified,
    'Status': None,
    'Contributors': vocab_funcs.construct_contributors,
    'Resolution': vocab_funcs.construct_resolution, 
}

SCHEMAS['properties'] = {}

