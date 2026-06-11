# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ConstructionSubcontract(models.Model):
    _name = 'construction.subcontract'
    _description = 'Construction Subcontract'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Fields
    name = fields.Char(string='Subcontract Name', required=True)
    project_id = fields.Many2one(
        'construction.project',
        string='Project',
        required=True,
        ondelete='cascade'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Subcontractor',
        required=True,
        domain=[('supplier_rank', '>', 0)]
    )
    
    # Contract Value
    contract_value = fields.Float(string='Contract Value', required=True)
    retention_percentage = fields.Float(
        string='Retention %',
        default=10.0,
        help='Percentage to retain from payment'
    )
    
    # Computed Fields
    paid_amount = fields.Float(
        string='Paid Amount',
        compute='_compute_paid_amount',
        store=True
    )
    remaining_amount = fields.Float(
        string='Remaining Amount',
        compute='_compute_remaining_amount',
        store=True
    )
    
    # Status
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('invoiced', 'Invoiced'),
         ('paid', 'Paid')],
        string='State',
        default='draft',
        tracking=True
    )
    
    # Relations
    invoice_ids = fields.Many2many(
        'account.move',
        string='Invoices',
        domain="[('move_type', 'in', ['in_invoice', 'in_refund']), ('state', '=', 'posted')]"
    )
    
    _sql_constraints = [
        ('contract_value_positive', 'CHECK(contract_value > 0)', 
         'Contract value must be positive'),
        ('retention_positive', 'CHECK(retention_percentage >= 0)', 
         'Retention percentage must be positive'),
    ]
    
    @api.depends('invoice_ids.amount_total', 'invoice_ids.payment_state', 'contract_value', 'retention_percentage')
    def _compute_paid_amount(self):
        """Compute paid amount from paid invoices only (Odoo 17)"""
        for subcontract in self:
            # Only consider invoices that are posted and fully paid
            paid_invoices = subcontract.invoice_ids.filtered(lambda inv: inv.state == 'posted' and inv.payment_state == 'paid')
            total_paid = sum(paid_invoices.mapped('amount_total'))
            # Deduct retention
            retention = (subcontract.contract_value * subcontract.retention_percentage / 100)
            subcontract.paid_amount = total_paid - retention
    
    @api.depends('contract_value', 'paid_amount')
    def _compute_remaining_amount(self):
        """Compute remaining amount to pay"""
        for subcontract in self:
            subcontract.remaining_amount = (
                subcontract.contract_value - subcontract.paid_amount
            )
