{
    'name': 'Machinery Maintenance',
    'summary': 'Machines + maintenance logs with next-due tracking',
    'version': '17.0.1.0.0',
    'author': 'You',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/machinery_menu.xml',
        'views/machinery_machine_views.xml',
        'views/machinery_maintenance_views.xml',
        'data/machinery_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'machinery_maintenance/static/src/css/maintenance.css',
        ],
    },
    'demo': [
        'demo/machinery_demo.xml',
    ],
    'installable': True,
    'application': True,
}
