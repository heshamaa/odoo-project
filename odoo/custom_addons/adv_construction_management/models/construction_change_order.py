# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ConstructionChangeOrder(models.Model):
    _name = 'construction.change.order'
    _description = 'Change Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Fields
    name = fields.Char(
        string='Change Order #',
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )
    project_id = fields.Many2one(
        'construction.project',
        string='Project',
        required=True,
        ondelete='cascade'
    )
    description = fields.Text(string='Description', required=True)
    
    # Changes
    additional_cost = fields.Float(
        string='Additional Cost',
        required=True
    )
    additional_days = fields.Integer(
        string='Additional Days',
        default=0
    )
    
    # Status
    approved = fields.Boolean(
        string='Approved',
        default=False,
        tracking=True
    )
    approval_date = fields.Date(
        string='Approval Date',
        readonly=True
    )
    
    _sql_constraints = [
        ('additional_cost_positive', 'CHECK(additional_cost > 0)', 
         'Additional cost must be positive'),
    ]
    
    @api.model
    def create(self, vals):
        """Auto-generate change order number"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'construction.change.order'
            ) or 'CO-001'
        return super().create(vals)
    
    @api.onchange('approved')
    def _onchange_approved(self):
        """Apply changes to project when approved"""
        if self.approved and self.project_id:
            self.approval_date = fields.Date.today()
            
            # Update project budget
            self.project_id.budget += self.additional_cost
            
            # Update project end date
            if self.additional_days:
                from datetime import timedelta
                self.project_id.end_date += timedelta(days=self.additional_days)
