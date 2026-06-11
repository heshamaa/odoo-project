# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ConstructionTimesheet(models.Model):
    _name = 'construction.timesheet'
    _description = 'Construction Timesheet'
    _order = 'date desc'

    # Relations
    worker_id = fields.Many2one(
        'construction.worker',
        string='Worker',
        required=True,
        ondelete='cascade'
    )
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
    
    # Work Details
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    hours = fields.Float(string='Hours Worked', required=True, default=8.0)
    
    # Cost (computed)
    cost = fields.Float(
        string='Cost',
        compute='_compute_cost',
        store=True
    )
    
    notes = fields.Text(string='Notes')
    
    _sql_constraints = [
        ('hours_positive', 'CHECK(hours > 0)', 'Hours must be positive'),
    ]
    
    @api.depends('hours', 'worker_id.daily_rate')
    def _compute_cost(self):
        """Compute cost based on hours and worker daily rate"""
        for timesheet in self:
            if timesheet.worker_id and timesheet.hours:
                # Cost = (hours / 8) * daily_rate
                timesheet.cost = (
                    timesheet.hours / 8.0 * timesheet.worker_id.daily_rate
                )
            else:
                timesheet.cost = 0.0
