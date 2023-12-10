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

DPV_FILES = {
    # Format of this data structure is 
    #   (DOCUMENT_NAME, ((DOCUMENT_ID, SHEET_NAME)+)
    # 
    'process': {
        'name': 'process',
        'doc_id': '1x5Wfl-2Xp22R89lhNwNpYP0xN0zfQLFlNe3On6pwNM4',
        'sheets': (
            'Namespaces', 
            'Namespaces_Other', 
            'Process', 
            'Process_properties',
            ),
    },
    'dpv-pd': {
        'name': 'dpv-pd',
        'doc_id': '1SI6gZh9-dq1rf_etfrlYHj0QZwq9Vd25f_OHPX5hbSQ',
        'sheets': (
            'PersonalData', 
            'PersonalData_properties', 
            'pd-core',
            'pd-extended',
            ),
    },
    'purpose_processing': {
        'name': 'purpose_processing',
        'doc_id': '1ePg6BU2Zp9fiSDuEnKuVi6dIRrFLEVdatbVxjHRk-8s',
        'sheets': (
           'Purpose', 
           'Purpose_properties', 
           'Processing', 
           'Processing_properties', 
           'ProcessingContext', 
           'ProcessingContext_properties', 
           'ProcessingScale', 
           'ProcessingScale_properties',
           ),
    },
    'context_status': {
        'name': 'context_status',
        'doc_id':  '1VPQW1DanprQhMwnhSqyKSGbEXdTmLHdc6UjpWJhyLMA', 
        'sheets': (
            'Context', 
            'Context_properties', 
            'Status', 
            'Status_properties',
            ),
    },
    'toms': {
        'name': 'toms',
        'doc_id':  '16d0_k6ueoXxXRTgecih9Ny7NpeXYF8icm4QX99cPYJA', 
        'sheets': (
            'TOM', 
            'TOM_properties', 
            'TechnicalMeasure', 
            'OrganisationalMeasure',
            ),
    },
    'entities': {
        'name': 'entities',
        'doc_id':  '1g6zLqVt5FlNlgsXq_NW2W9INv3KdGEFjJCyOd03UmOg', 
        'sheets': (
            'Entities', 
            'Entities_properties', 
            'Entities_Authority', 
            'Entities_Authority_properties', 
            'Entities_LegalRole', 
            'Entities_LegalRole_properties', 
            'Entities_Organisation', 
            'Entities_DataSubject', 
            'Entities_DataSubject_properties',
            ),
    },
    'location_jurisdiction': {
        'name': 'location_jurisdiction',
        'doc_id': '19exhY34jq6VDApRp2abHD-br6rpm6Q7BOP7H_pm5sKM',
        'sheets': (
            'Jurisdiction', 
            'Jurisdiction_properties', 
            'legal_properties', 
            'legal_Locations', 
            'legal_Laws', 
            'legal_Authorities', 
            'legal_EU_EEA', 
            'legal_EU_Adequacy',
            ),
    },
    'legal_basis': {
        'name': 'legal_basis',
        'doc_id':  '13Ub4LXHruocffYnd7JKCMvzi1MYv3Gy61d3UmQBhARc', 
        'sheets': (
            'LegalBasis', 
            'LegalBasis_properties', 
            'ConsentTypes', 
            'ConsentStatus', 
            'Consent_properties',
            ),
    },
    'gdpr': {
        'name': 'gdpr',
        'doc_id': '1lDJZpl0UND8Bm_4iWKVQtgmMUz0YwP2R63CgP7Gro-U',
        'sheets': (
            'GDPR_LegalBasis', 
            'GDPR_LegalBasis_SpecialCategory', 
            'GDPR_LegalBasis_DataTransfer', 
            'GDPR_LegalRights', 
            'GDPR_LegalBasis_Rights_Mapping', 
            'GDPR_DataTransfers', 
            'GDPR_DPIA',
            'GDPR_DPIA_properties',
            'GDPR_compliance'
            ),
    },
    'dga': {
        'name': 'dga',
        'doc_id':  '1wKsf0Vqr0Gg1C91MqshtI5tjGXmQvXu4p4xF0yK0KaA',
        'sheets': (
            'DGA_LegalBasis',
            'DGA_LegalRights',
            'DGA_Services',
            'DGA_Registers',
            'DGA_TOMs',
            'DGA_entities',
            'DGA_properties',
            ),
    },
    'dpv-tech': {
        'name': 'dpv-tech',
        'doc_id': '1GVmF4c7b-9xMSs0TyT45kXoCLLUVs8bbW34tfcozbuA',
        'sheets': (
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
            ),
    },
    'risk': {
        'name': 'risk',
        'doc_id': '1y8r3Vk-_Gi1MqbyAM6Ot4DoNDJpa2ZVhCyCyFQkGBy0',
        'sheets': (
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
            ),
    },
    'rights': {
        'name': 'rights',
        'doc_id': '1XW-L6rGWbgGGp62q8eA22SWvh4wUWK5BpC0zfD6wAxM',
        'sheets': (
            'Rights', 
            'Rights_properties', 
            'EUFundamentalRights',
            ),
    },
    'rules': {
        'name': 'rules',
        'doc_id':  '1SDmlzSo1Ax_35v754Jzx4oFGKvGo5nyNtEAL0vSBbM0', 
        'sheets': (
            'Rules', 
            'Rules_properties',
            ),
    },
    'standards': {
        'name': 'standards',
        'doc_id': '1z-qaB2m6lD1ROmPVf9yhfG05D68Z7H4glYLERj6ZCRk',
        'sheets': (
            'Standards_ISO',
            ),
    },
    'ucr': {
        'name': 'ucr',
        'doc_id': '1__STWvOEZRc1u2J-8teOYjLpnTPlZ80_ebTytrUlWgQ',
        'sheets': (
            'UseCase',
            'Requirement',
            'Example',
            ),
    },
}


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


def _download_spreadsheets(document_id, document_name, export_link):
    download_document(
        document_id=document_id,
        document_name=document_name,
        export_link=GOOGLE_EXCEL_EXPORT_LINK,
        ext='xlsx')


def _extract_CSVs(document_name, sheets):
    INFO(document_name)
    for sheet_name in sheets:
        # Extract CSV
        with open(f'{DOCS_FOLDER}/{sheet_name}.csv', 'w') as outfile:
            subprocess.run(["xlsx2csv", f"{DOCS_FOLDER}/{document_name}.xlsx", "-n", f"{sheet_name}"], stdout=outfile)
        INFO(f'Wrote {sheet_name}.csv from {document_name}.xlsx')


def _download_all_spreadsheets():
    for data in DPV_FILES.values():
        doc_id = data['doc_id']
        document_name = data['name']
        _download_spreadsheets(
            doc_id, document_name, GOOGLE_EXCEL_EXPORT_LINK)


def _extract_all_CSVs():
    for data in DPV_FILES.values():
        document_name = data['name']
        sheets = data['sheets']
        _extract_CSVs(document_name, sheets)


# MAIN
import subprocess
if __name__ == '__main__':
    # Setup argument parser
    # Default is to NOT download any file, and extract ALL CSVs
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--d', action='store_true', help="download data files")
    parser.add_argument('-x', '--x', action='store_true', default=True, help="extract CSVs from all data files")
    parser.add_argument('--ds', nargs='+', default=False, help="download only indicated data files")
    parser.add_argument('--xs', nargs='+', default=False, help="extract CSVs from indicated data files")
    args = parser.parse_args()

    # DEBUG(args)
    # Handle arguments
    # File Downloaded
    if args.d or args.ds: # Download files
        INFO('-'*40)
        INFO('Downloading spreadsheets...')
        INFO('-'*40)
        if not args.ds: # download all files
            _download_all_spreadsheets()
            args.x = True
        else: # download only indicated files
            if not args.ds:
                args.ds = []
            for document_name in args.ds:
                if document_name not in DPV_FILES:
                    raise NameError(f'{document_name} is not a DPV File')
                if not document_name in args.ds:
                    args.xs.append(document_name)
                _download_spreadsheets(
                    DPV_FILES[document_name]['doc_id'],
                    document_name, GOOGLE_EXCEL_EXPORT_LINK)
            args.xs = args.ds
        INFO('-'*40)
    # Extracting CSVs
    if args.x is True:
        INFO('-'*40)
        INFO('Extracting CSVs...')
        INFO('-'*40)
        if not args.xs:
            _extract_all_CSVs()
        else:
            if not args.xs:
                args.xs = []
            for document_name in args.xs:
                if document_name not in DPV_FILES:
                    raise NameError(f'{document_name} is not a DPV File')
                _extract_CSVs(
                    document_name, DPV_FILES[document_name]['sheets'])
        INFO('-'*40)
