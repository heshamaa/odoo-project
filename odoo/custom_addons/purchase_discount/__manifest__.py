{
    'name': 'Purchase Multi-Discount',
    'version': '19.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Multi-discount support for Purchase Order lines',
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/discount_template_views.xml',
        'views/purchase_order_views.xml',
        'wizard/purchase_order_discount_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
