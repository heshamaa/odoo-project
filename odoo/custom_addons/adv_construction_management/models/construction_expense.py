# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ConstructionExpense(models.Model):
    _name = 'construction.expense'
    _description = 'Construction Expense'
    _order = 'date desc'

    # Basic Fields
    name = fields.Char(string='Description', required=True)
    project_id = fields.Many2one(
        'construction.project',
        string='Project',
        required=True,
        ondelete='cascade'
    )
    stage_id = fields.Many2one(
        'construction.stage',
        string='Stage',
        domain="[('project_id', '=', project_id)]"
    )
    
    # Type and Amount
    type = fields.Selection(
        [('materials', 'Materials'),
         ('labor', 'Labor'),
         ('equipment', 'Equipment'),
         ('other', 'Other')],
        string='Type',
        required=True,
        default='materials'
    )
    amount = fields.Float(string='Amount', required=True)
    
    # Status
    approved = fields.Boolean(string='Approved', default=False, tracking=True)
    date = fields.Date(string='Expense Date', default=fields.Date.today)
    
    # Relations
    invoice_id = fields.Many2one(
        'account.invoice',
        string='Invoice'
    )
    
    notes = fields.Text(string='Notes')
    
    _sql_constraints = [
        ('amount_positive', 'CHECK(amount > 0)', 'Amount must be positive'),
    ]
    
    @api.onchange('approved')
    def _onchange_approved(self):
        """Trigger recomputation on project when approved status changes"""
        if self.project_id:
            self.project_id._compute_actual_costs()
