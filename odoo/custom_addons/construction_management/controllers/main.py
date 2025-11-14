from odoo import http
from odoo.http import request

class CustomViewController(http.Controller):

    @http.route('/my_custom_view', type='http', auth='user', website=True)
    def my_custom_view(self, **kwargs):
        categories = request.env['product.category'].sudo().search([])
        return request.render('construction_management.my_custom_template', {
            'categories': categories
        })
