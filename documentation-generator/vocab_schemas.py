###################### schemas

import vocab_funcs

'''adds schemas for each CSV'''
SCHEMAS = {}
def get_schema(name):
    return SCHEMAS[name]

SCHEMAS['classes'] = {
    'Term': vocab_funcs.construct_class,
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
    'Term': vocab_funcs.construct_class,
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

SCHEMAS['properties'] = {
    'Term': vocab_funcs.construct_property,
    'Label': vocab_funcs.construct_label,
    'Description': vocab_funcs.contruct_description,
    'domain': vocab_funcs.construct_domain,
    'range': vocab_funcs.construct_range,
    'ParentProperty': vocab_funcs.construct_parent_property,
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

