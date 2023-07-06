# Copyright 2023 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Fieldservice Rating',
    'summary': """
        This module enable field service order rating""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/field-service',
    'depends': [
        'fieldservice',
        'rating',
    ],
    'data': [
        'data/fieldservice_data.xml',
        'views/fsm_order.xml',
        'views/fsm_stage.xml',
    ],
    'demo': [
        'demo/fsm_order.xml',
        'demo/fsm_stage.xml',
    ],
}
