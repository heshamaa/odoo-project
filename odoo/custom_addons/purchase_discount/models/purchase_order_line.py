from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    discount_ids = fields.Many2many(
        'purchase.discount',
        'purchase_order_line_discount_rel',
        'line_id',
        'discount_id',
        string='Discounts',
        context={'active_test': True},
    )


    price_unit_before_discount = fields.Float(
        string='Unit Price',
        digits='Product Price',
        store=True,
        copy=True,
        default=0.0,
    )

    # Hidden from UI. Computed from price_unit_before_discount + discount_ids.
    # Odoo uses this internally for subtotals, taxes, bills, and accounting.
    price_unit = fields.Float(
        string='Unit Price',
        digits='Product Price',
        compute='_compute_price_unit_and_date_planned_and_name',
        store=True,
        readonly=False,
    )

    @api.depends(
        'price_unit_before_discount',
        'discount_ids.discount_type',
        'discount_ids.discount_value',
        'product_qty',
    )
    def _compute_price_unit_and_date_planned_and_name(self):
        """
        1. super() runs native logic → populates price_unit from pricelist.
        2. We capture super's result into price_unit_before_discount
           (only when the user hasn't set it manually yet).
        3. Apply discount_ids against price_unit_before_discount.
        4. Store final discounted value in price_unit (hidden, used by Odoo).
        """
        super()._compute_price_unit_and_date_planned_and_name()

        for line in self:
            if not line.product_id:
                continue

            # Sync base from pricelist when super ran a fresh calculation.
            # super() always sets technical_price_unit == price_unit together.
            if line.technical_price_unit == line.price_unit and line.price_unit:
                line.price_unit_before_discount = line.price_unit

            base = line.price_unit_before_discount or line.price_unit
            if not base:
                continue

            if not line.discount_ids:
                line.price_unit = base
                continue

            qty = line.product_qty or 1.0
            total = base * qty

            for disc in line.discount_ids:
                if disc.discount_type == 'percent':
                    total *= (1.0 - disc.discount_value / 100.0)
                else:
                    total -= disc.discount_value

            line.price_unit = max(total, 0.0) / qty

    @api.onchange('price_unit_before_discount')
    def _onchange_price_unit_before_discount(self):
        """
        When user edits the base price field directly,
        ensure price_unit recomputes immediately in the UI.
        """
        for line in self:
            if not line.discount_ids:
                line.price_unit = line.price_unit_before_discount
