{
    'name':'app one',
    'author': 'Mn3m',
    'category':'',
    'version':'17.0.0.1.0',
    'depends':[
        'base',
        'sale',
        'account',
        'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_inherited_view.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'app_one/static/src/css/property.css',

        ],
    },
    'application': True
}