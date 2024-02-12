# -*- coding: utf-8 -*-
{
    'name': 'State property',
    'version': '1.4',
    'description': """Tutorial, Demo2 Description 
        Property, proerty type, property offer, saleman...
    """,
    'summary': """ 
        Demo2 tutorial for to create un module en odoo 17.
        list, edit, create, search, sort...
    """,
    'author': 'Liban',
    'website': '',
    'category': 'Tutorials/State',
    'depends': ['base','web'],
    "data": [                
        "views/res_user_views.xml",
        "views/state_real_views.xml",
        "views/state_property_offer_views.xml",
        "views/state_property_tag_views.xml",
        "views/PropertyType_views.xml",
        "views/state_menu_view.xml",
        "security/ir.model.access.csv"
    ],'assets': {
    'web.assets_backend': [
        'state_property/static/src/**/*'
    ],
},
    'application': True,
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}