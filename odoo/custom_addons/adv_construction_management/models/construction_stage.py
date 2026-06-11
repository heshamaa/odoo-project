# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ConstructionStage(models.Model):
    _name = 'construction.stage'
    _description = 'Construction Project Stage'
    _order = 'sequence, id'

    # Basic Fields
    name = fields.Char(string='Stage Name', required=True)
    project_id = fields.Many2one(
        'construction.project',
        string='Project',
        required=True,
        ondelete='cascade'
    )
    description = fields.Text(string='Description')
    
    # Cost
    planned_cost = fields.Float(string='Planned Cost')
    actual_cost = fields.Float(
        string='Actual Cost',
        compute='_compute_actual_cost',
        store=True
    )
    
    # Dates
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    
    # Progress
    progress = fields.Float(
        string='Progress %',
        default=0.0,
        help='0-100'
    )
    
    # Status
    state = fields.Selection(
        [('not_started', 'Not Started'),
         ('in_progress', 'In Progress'),
         ('completed', 'Completed'),
         ('delayed', 'Delayed')],
        string='State',
        default='not_started',
        compute='_compute_state',
        store=True
    )
    
    sequence = fields.Integer(string='Sequence', default=1)
    
    # Relations
    expense_ids = fields.One2many(
        'construction.expense',
        'stage_id',
        string='Expenses'
    )
    
    _sql_constraints = [
        ('planned_cost_positive', 'CHECK(planned_cost >= 0)', 
         'Planned cost must be positive'),
    ]
    
    @api.depends('expense_ids.amount', 'expense_ids.approved')
    def _compute_actual_cost(self):
        """Compute actual cost from approved expenses"""
        for stage in self:
            approved_expenses = stage.expense_ids.filtered('approved')
            stage.actual_cost = sum(approved_expenses.mapped('amount'))
    
    @api.depends('progress', 'start_date', 'end_date')
    def _compute_state(self):
        """Compute state based on progress and dates"""
        from datetime import datetime
        
        for stage in self:
            if stage.progress == 0:
                stage.state = 'not_started'
            elif stage.progress == 100:
                stage.state = 'completed'
            elif stage.progress > 0:
                if stage.end_date and datetime.now().date() > stage.end_date:
                    stage.state = 'delayed'
                else:
                    stage.state = 'in_progress'
