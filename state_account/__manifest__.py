# -*- coding: utf-8 -*-
{
    'name': 'State account',
    'version': '0.9',
    'description': """ State_account Description Invoice of property sold to partner 
    and contable journals update as necesary...  """,
    'summary': """
     State_account Summary 

     0.6: tratando de importar el modelo state_real en un modelo definido en state_account.
     
    
    """,
    'author': 'Liban',
    'website': '',
    'category': 'Tutorials/State',
    'depends': ['base', 'state_property','account',],
    "data": [    
        "views/state_real_views.xml"
    ],
    'application': True,
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
}
