from odoo import fields, models


class PurchaseDiscount(models.Model):
    _name = 'purchase.discount'
    _description = 'Purchase Discount'
    _order = 'name'

    name = fields.Char(required=True)
    discount_type = fields.Selection([
        ('percent', 'Percentage (%)'),
        ('fixed', 'Fixed Amount'),
    ], required=True, default='percent', string='Type')
    discount_value = fields.Float('Value', required=True, digits='Discount')

    def name_get(self):
        result = []
        for rec in self:
            if rec.discount_type == 'percent':
                label = f"{rec.name} ({rec.discount_value}%)"
            else:
                label = f"{rec.name} (-{rec.discount_value})"
            result.append((rec.id, label))
        return result
