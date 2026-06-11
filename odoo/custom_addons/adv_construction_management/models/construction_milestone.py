# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ConstructionMilestone(models.Model):
    _name = 'construction.milestone'
    _description = 'Construction Milestone'
    _order = 'sequence'

    # Basic Fields
    name = fields.Char(string='Milestone Name', required=True)
    project_id = fields.Many2one(
        'construction.project',
        string='Project',
        required=True,
        ondelete='cascade'
    )
    
    # Percentage and Amount
    percentage = fields.Float(
        string='% of Project',
        required=True,
        default=25.0,
        help='Percentage of project completion (0-100)'
    )
    amount = fields.Float(
        string='Milestone Amount',
        compute='_compute_amount',
        store=True
    )
    
    # Status
    approved = fields.Boolean(string='Approved', default=False, tracking=True)
    sequence = fields.Integer(string='Sequence', default=1)
    
    # Relations
    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice'
    )
    
    _sql_constraints = [
        ('percentage_range', 'CHECK(percentage > 0 AND percentage <= 100)', 
         'Percentage must be between 0 and 100'),
    ]
    
    @api.depends('project_id.budget', 'percentage')
    def _compute_amount(self):
        """Compute milestone amount based on percentage of budget"""
        for milestone in self:
            if milestone.project_id:
                milestone.amount = (
                    milestone.percentage / 100.0 * milestone.project_id.budget
                )
            else:
                milestone.amount = 0.0
