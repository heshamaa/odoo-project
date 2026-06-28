from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    purchase_discount_product_id = fields.Many2one(
        comodel_name='product.product',
        string="Purchase Discount Product",
        domain="[('type', '=', 'service')]",
    )
