# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bike Rental Application',
    'version': '1.0',
    'category': 'Bike Rental Application',
    'sequence': 15,
    'summary': '',
    'description': "",
    'data':[
        'data/ir.model.access.csv',
        'views/bike_station_view.xml',
        'views/bike_bike_view.xml',
        'views/bike_rental_view.xml',
        'views/bike_menu_view.xml',
    ],
    'depends' : [
        'base',
    ],
    'application': True,
}