{
    'name': 'Construction Management',
    'version': '1.0',
    'summary': 'Fully integrated materials construction management module',
    'description': """
    This module provides comprehensive materials construction management features,
    including inventory tracking, procurement, and supplier management.
    """,
    'category': 'Sales',
    'author': 'Hesham Ahmed',
    'website': 'https://example.com',
    'license': 'LGPL-3',
    'depends': ['base',"stock",'product', 'sale', 'purchase', 'account' ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu_view.xml',
        'views/category/category_menu_view.xml',
        'views/product/product_menu_view.xml',
        'views/project/construction_project_menu_view.xml',
        'views/project/construction_project_view.xml',
        'views/product/product_view.xml',
        'views/category/category_view.xml',
        'data/all_materials.xml',
        'data/construction_materials.xml',
        'data/building_materials.xml',
        'data/finishing_materials.xml',
        'data/electrical_materials.xml',
        'data/plumbing_materials.xml',
        'data/insulation_materials.xml',
        'data/metal_aluminum_materials.xml',
        'data/flooring_materials.xml',
        'data/hvac_materials.xml',
        'data/misc_materials.xml',     
    ],
    'assets': {
    'web.assets_backend': [
        'construction_management/static/src/js/category_tree_widget.js',
    ],
    },

    'installable': True,
    'application': True, 
    'auto_install': False,  
}
