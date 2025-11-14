from odoo import models, fields


class ConstructionCategory(models.Model):
    _inherit = 'product.category'
    _description = 'Construction Category'

    description = fields.Text(string='Description')