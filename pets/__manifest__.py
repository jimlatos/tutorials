# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Pets',
    'version': '0.1',
    'category': 'Tools',
    'summary': 'Summary: Pets management',
    'description': """
        Description: Module to manage pets
    """,
    'author': 'Jim Latos',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/pets_animal_views.xml',
        'views/pets_species_views.xml',
        'views/pets_feeding_views.xml',
        'views/pets_weight_views.xml',
        'views/pets_menus.xml',
    ],
    'application': True,
}