# -*- coding: utf-8 -*-
{
    'name': 'Barcode Scanner - Sales',
    'version': '18.0.1.0.0',
    'category': 'Sales/Barcode',
    'summary': 'Barcode and QR code scanning for Sales Orders',
    'description': """
Barcode Scanner for Sales Orders
================================

This module extends Sales Orders with barcode/QR scanning functionality:

* Scan products to add them to sales order lines
* Auto-increment quantity when scanning the same product
* Show on-hand quantity information
* State validation (block scanning on cancelled/locked orders)
* GS1-128 barcode support for product identification

Requires the Barcode Scanner Base module.
    """,
    'author': 'Woow Tech',
    'website': 'https://github.com/woowtech',
    'license': 'LGPL-3',
    'depends': [
        'barcode_scanner_base',
        'sale_management',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'barcode_scanner_sale/static/src/components/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
