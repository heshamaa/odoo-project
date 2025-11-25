from odoo import fields,api,models


class ConstructionWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    project_id = fields.Many2one('construction.project',string="Construction Project",ondelete="restrict",help="The construction project this warehouse is linked to, if any.")