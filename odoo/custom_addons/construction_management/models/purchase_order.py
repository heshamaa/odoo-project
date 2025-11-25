from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    
    material_request_id = fields.Many2one('construction.material.request', string='Source Material Request', readonly=True)