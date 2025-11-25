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
        'views/material_request/construction_material_request_menu_view.xml',
        'views/warehouse/construction_warehouse_menu_view.xml',
        'views/material_request/construction_material_request_view.xml',
        'views/material_request/purchase_order_view.xml',
        'views/project/construction_project_view.xml',
        'views/product/product_view.xml',
        'views/category/category_view.xml',
        'data/categories/all_materials.xml',
        'data/categories/construction_materials.xml',
        'data/categories/building_materials.xml',
        'data/categories/finishing_materials.xml',
        'data/categories/electrical_materials.xml',
        'data/categories/plumbing_materials.xml',
        'data/categories/insulation_materials.xml',
        'data/categories/metal_aluminum_materials.xml',
        'data/categories/flooring_materials.xml',
        'data/categories/hvac_materials.xml',
        'data/categories/misc_materials.xml',
        'data/products/products_data.xml'     
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
