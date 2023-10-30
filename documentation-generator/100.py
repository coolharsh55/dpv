#!/usr/bin/env python3
#author: Harshvardhan J. Pandit

'''Downloads the DPV spreadsheets in CSV form'''
# REQUIRES xlsx2csv to be installed https://github.com/dilshod/xlsx2csv

import logging
# logging configuration for debugging to console
logging.basicConfig(
    level=logging.DEBUG, format='%(levelname)s - %(funcName)s :: %(lineno)d - %(message)s')
DEBUG = logging.debug
INFO = logging.info

# Google Export link for CSVs - NOT NEEDED
# GOOGLE_EXPORT_LINK = (
#     'https://docs.google.com/spreadsheets/d/'
#     '%s/gviz/tq?tqx=out:csv&sheet=%s')
# Google Excel Export link
GOOGLE_EXCEL_EXPORT_LINK = (
    'https://docs.google.com/spreadsheets/d/'
    '%s/export?exportFormat=xlsx&format=xlsx&title=%s')
DOCS_FOLDER = './vocab_csv'

DPV_FILES = (
    # Format of this data structure is 
    #   (DOCUMENT_NAME, ((DOCUMENT_ID, SHEET_NAME)+)
    # 
    ('base', '1x5Wfl-2Xp22R89lhNwNpYP0xN0zfQLFlNe3On6pwNM4',
        (
            'Namespaces', 
            'Namespaces_Other', 
            'BaseOntology', 
            'BaseOntology_properties',
            )),
    ('dpv-pd','1SI6gZh9-dq1rf_etfrlYHj0QZwq9Vd25f_OHPX5hbSQ',
        (
            'PersonalData', 
            'PersonalData_properties', 
            'pd-core',
            'pd-extended',
            )),
    ('purpose_processing', '1ePg6BU2Zp9fiSDuEnKuVi6dIRrFLEVdatbVxjHRk-8s',
       (
           'Purpose', 
           'Purpose_properties', 
           'Processing', 
           'Processing_properties', 
           'ProcessingContext', 
           'ProcessingContext_properties', 
           'ProcessingScale', 
           'ProcessingScale_properties',
           )),
    ('context_status', '1VPQW1DanprQhMwnhSqyKSGbEXdTmLHdc6UjpWJhyLMA', 
        (
            'Context', 
            'Context_properties', 
            'Status', 
            'Status_properties',
            )),
    ('toms', '16d0_k6ueoXxXRTgecih9Ny7NpeXYF8icm4QX99cPYJA', 
        (
            'TOM', 
            'TOM_properties', 
            'TechnicalMeasure', 
            'OrganisationalMeasure',
            )),
    ('entities', '1g6zLqVt5FlNlgsXq_NW2W9INv3KdGEFjJCyOd03UmOg', 
        (
            'Entities', 
            'Entities_properties', 
            'Entities_Authority', 
            'Entities_Authority_properties', 
            'Entities_LegalRole', 
            'Entities_LegalRole_properties', 
            'Entities_Organisation', 
            'Entities_DataSubject', 
            'Entities_DataSubject_properties',
            )),
    ('location_jurisdiction', '19exhY34jq6VDApRp2abHD-br6rpm6Q7BOP7H_pm5sKM',
       (
            'Jurisdiction', 
            'Jurisdiction_properties', 
            'legal_properties', 
            'legal_Locations', 
            'legal_Laws', 
            'legal_Authorities', 
            'legal_EU_EEA', 
            'legal_EU_Adequacy',
            )),
    ('legal_basis', '13Ub4LXHruocffYnd7JKCMvzi1MYv3Gy61d3UmQBhARc', 
        (
            'LegalBasis', 
            'LegalBasis_properties', 
            'ConsentTypes', 
            'ConsentStatus', 
            'Consent_properties',
            )),
    ('gdpr', '1lDJZpl0UND8Bm_4iWKVQtgmMUz0YwP2R63CgP7Gro-U',
       (
            'GDPR_LegalBasis', 
            'GDPR_LegalBasis_SpecialCategory', 
            'GDPR_LegalBasis_DataTransfer', 
            'GDPR_LegalRights', 
            'GDPR_LegalBasis_Rights_Mapping', 
            'GDPR_DataTransfers', 
            'GDPR_DPIA',
            'GDPR_DPIA_properties',
            'GDPR_compliance'
            )),
    ('dga', '1wKsf0Vqr0Gg1C91MqshtI5tjGXmQvXu4p4xF0yK0KaA',
        (
            'DGA_LegalBasis',
            'DGA_LegalRights',
            'DGA_Services',
            'DGA_Registers',
            'DGA_TOMs',
            'DGA_entities',
            'DGA_properties',
            )),
    ('dpv-tech', '1GVmF4c7b-9xMSs0TyT45kXoCLLUVs8bbW34tfcozbuA',
       (
            'tech-core',
            'tech-core-properties',
            'tech-data',
            'tech-ops',
            'tech-security',
            'tech-surveillance',
            'tech-provision',
            'tech-provision-properties',
            'tech-actors',
            'tech-actors-properties',
            'tech-comms',
            'tech-tools',
            'tech-algorithms',
            )),
    ('risk', '1y8r3Vk-_Gi1MqbyAM6Ot4DoNDJpa2ZVhCyCyFQkGBy0',
       (
            'Risk', 
            'Risk_properties', 
            'RiskConsequences', 
            'RiskLevels', 
            'RiskMatrix', 
            'RiskControls', 
            'RiskAssessment', 
            'RiskManagement', 
            'RiskMethodology',
            'Justifications',
            )),
    ('rights', '1XW-L6rGWbgGGp62q8eA22SWvh4wUWK5BpC0zfD6wAxM',
       (
            'Rights', 
            'Rights_properties', 
            'EUFundamentalRights',
            )),
    ('rules', '1SDmlzSo1Ax_35v754Jzx4oFGKvGo5nyNtEAL0vSBbM0', 
        (
            'Rules', 
            'Rules_properties',
            )),
    ('standards', '1z-qaB2m6lD1ROmPVf9yhfG05D68Z7H4glYLERj6ZCRk',
       (
            'Standards_ISO',
            )),
    ('ucr', '1__STWvOEZRc1u2J-8teOYjLpnTPlZ80_ebTytrUlWgQ',
        (
            'UseCase',
            'Requirement',
            'Example',
            )),
)


from urllib import request
def download_document(
    document_id, document_name, export_link, ext='xlsx'):
    '''Download the sheet and save to specified path in specified format'''
    url = export_link % (document_id, document_name)
    try:
        request.urlretrieve(url, f'{DOCS_FOLDER}/{document_name}.{ext}')
        INFO(f'Downloaded {document_name}.{ext}')
    except Exception as E:
        logging.error(f'ERROR :: {E}')


def _download_spreadsheets():
    INFO('-'*40)
    INFO('Downloading spreadsheets...')
    INFO('-'*40)
    # TODO: uncomment below
    for document_name, document_id, sheets in DPV_FILES:
        download_document(
            document_id=document_id,
            document_name=document_name,
            export_link=GOOGLE_EXCEL_EXPORT_LINK,
        ext='xlsx')


def _extract_CSVs():
    INFO('-'*40)
    INFO('Extracting CSVs...')
    INFO('-'*40)
    for document_name, _, sheets in DPV_FILES:
        INFO(document_name)
        for sheet_name in sheets:
            # Extract CSV
            with open(f'{DOCS_FOLDER}/{sheet_name}.csv', 'w') as outfile:
                subprocess.run(["xlsx2csv", f"{DOCS_FOLDER}/{document_name}.xlsx", "-n", f"{sheet_name}"], stdout=outfile)
            INFO(f'Wrote {sheet_name}.csv from {document_name}.xlsx')
        INFO('-'*40)


# MAIN
import subprocess
if __name__ == '__main__':
    _download_spreadsheets()
    _extract_CSVs()
