# -*- coding: utf-8 -*-
{
    "name": "H-source: Sale Purchase",
    "summary": """H-source: Sales Order Line Drop Shipping Customization""",
    "description": """
1. 2172054
""",
    "author": "Odoo Inc",
    "website": "http://odoo.com",
    "category": "Custom Development",
    "version": "0.1",
    "depends": ["sale_purchase", "sale_management", "stock_dropshipping"],
    "data": [
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
    ]
}
