{
    'name':'todo management',
    'author': 'Mn3m',
    'category':'',
    'version':'17.0.0.1.0',
    'depends':[
        'base',

    ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/task_menu_view.xml'

    ],
    'assets': {
        'web.assets_backend': [
            'app_one/static/src/css/property.css',

        ],
    },
    'application': True
}