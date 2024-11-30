# -*- coding: utf-8 -*-
{
    'name': "riders_warehouse_custom",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'website', 'board','portal','stock_picking_batch'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/res_config_settings_views.xml',
        'views/menu_actions.xml',
        'views/views.xml',
        'views/templates.xml',
        'reports/deliveryslip.xml',
        'reports/riders_report_batch.xml',
        'demo/scheduled_actions.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'rider_warehouse_cus/static/src/components/**/*.js',
            'rider_warehouse_cus/static/src/components/**/*.xml',
            'rider_warehouse_cus/static/src/components/**/*.scss',
        ],
    },
}
