{
    "name": "Machinery Maintenance",
    "summary": "Machines + maintenance logs with next-due tracking",
    "version": "17.0.1.0.0",
    "author": "You",
    "license": "LGPL-3",
    "depends": ["base"],


    "data": [
    "security/ir.model.access.csv",
    "views/machinery_menu.xml",
    "views/machinery_machine_views.xml",
    "views/machinery_machine_kanban.xml",
    "data/machinery_data.xml"
	],
    "installable": True,
    "application": True,
    'demo': [
    'demo/machinery_demo.xml',
	],

}


