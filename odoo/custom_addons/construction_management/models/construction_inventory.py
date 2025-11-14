# models/construction_inventory.py
from odoo import models, fields, api

class ConstructionInventory(models.Model):
    _name = 'construction.inventory'
    _description = 'Construction Inventory'

    product_id = fields.Many2one(
        'product.product',
        string="Product",
        required=True
    )
    
    quantity = fields.Float(
        string="Quantity",
        required=True,
        default=1.0
    )

    location_id = fields.Many2one(
        'stock.location',
        string="Stock Location",
        required=True,
        default=lambda self: self.env.ref('stock.stock_location_stock')
    )

    available_qty = fields.Float(
        string="Available Quantity",
        compute='_compute_available_qty'
    )
    
    
    

    @api.depends('product_id')
    def _compute_available_qty(self):
        for record in self:
            record.available_qty = record.product_id.qty_available

    def action_add_to_stock(self):
        """لما المستخدم يضغط زر 'Add to Stock' يضيف الكمية للمخزون"""
        for record in self:
            self.env['stock.move'].create({
                'name': f'Construction Stock Update: {record.product_id.display_name}',
                'product_id': record.product_id.id,
                'product_uom': record.product_id.uom_id.id,
                'product_uom_qty': record.quantity,
                'location_id': self.env.ref('stock.stock_location_suppliers').id,
                'location_dest_id': record.location_id.id,
            })
