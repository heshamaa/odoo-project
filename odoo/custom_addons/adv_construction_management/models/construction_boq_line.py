# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ConstructionBOQLine(models.Model):
    _name = 'construction.boq.line'
    _description = 'Bill of Quantities Line'
    _order = 'sequence'

    # Relations
    boq_id = fields.Many2one(
        'construction.boq',
        string='BOQ',
        required=True,
        ondelete='cascade'
    )
    
    # Description
    description = fields.Char(string='Description', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    
    # Planned
    quantity_planned = fields.Float(string='Planned Quantity', required=True)
    unit_cost_planned = fields.Float(string='Unit Cost (Planned)', required=True)
    total_planned = fields.Float(
        string='Total Planned',
        compute='_compute_planned_total',
        store=True
    )
    
    # Actual (computed from linked expenses)
    quantity_actual = fields.Float(
        string='Actual Quantity',
        compute='_compute_actual',
        store=True
    )
    total_actual = fields.Float(
        string='Total Actual',
        compute='_compute_actual',
        store=True
    )
    
    # Variance
    variance = fields.Float(
        string='Variance',
        compute='_compute_variance',
        store=True
    )
    variance_percentage = fields.Float(
        string='Variance %',
        compute='_compute_variance',
        store=True
    )
    
    # Relations
    linked_expenses = fields.Many2many(
        'construction.expense',
        'boq_line_expense_rel',
        'boq_line_id',
        'expense_id',
        string='Linked Expenses'
    )
    
    _sql_constraints = [
        ('quantity_planned_positive', 'CHECK(quantity_planned > 0)', 
         'Planned quantity must be positive'),
        ('unit_cost_positive', 'CHECK(unit_cost_planned > 0)', 
         'Unit cost must be positive'),
    ]
    
    @api.depends('quantity_planned', 'unit_cost_planned')
    def _compute_planned_total(self):
        """Compute total planned cost"""
        for line in self:
            line.total_planned = line.quantity_planned * line.unit_cost_planned
    
    @api.depends('linked_expenses.amount', 'linked_expenses.approved')
    def _compute_actual(self):
        """Compute actual quantity and total from linked expenses"""
        for line in self:
            approved_expenses = line.linked_expenses.filtered('approved')
            # For simplicity, we count quantity as number of expenses
            # In reality, you'd track quantity per expense
            line.quantity_actual = len(approved_expenses)
            line.total_actual = sum(approved_expenses.mapped('amount'))
    
    @api.depends('total_actual', 'total_planned')
    def _compute_variance(self):
        """Compute variance and variance percentage"""
        for line in self:
            line.variance = line.total_actual - line.total_planned
            
            if line.total_planned:
                line.variance_percentage = (
                    line.variance / line.total_planned * 100
                )
            else:
                line.variance_percentage = 0
