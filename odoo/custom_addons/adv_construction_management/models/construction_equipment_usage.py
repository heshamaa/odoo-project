# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class ConstructionEquipmentUsage(models.Model):
    _name = 'construction.equipment.usage'
    _description = 'Equipment Usage in Project'

    # Relations
    equipment_id = fields.Many2one(
        'construction.equipment',
        string='Equipment',
        required=True,
        ondelete='cascade'
    )
    project_id = fields.Many2one(
        'construction.project',
        string='Project',
        required=True,
        ondelete='cascade'
    )
    
    # Dates
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    
    # Computed
    days = fields.Float(
        string='Days Used',
        compute='_compute_days',
        store=True
    )
    total_cost = fields.Float(
        string='Total Cost',
        compute='_compute_total_cost',
        store=True
    )
    
    _sql_constraints = [
        ('start_before_end', 'CHECK(start_date <= end_date)', 
         'Start date must be before or equal to end date'),
    ]
    
    @api.depends('start_date', 'end_date')
    def _compute_days(self):
        """Compute number of days equipment was used"""
        for usage in self:
            if usage.start_date and usage.end_date:
                delta = usage.end_date - usage.start_date
                usage.days = delta.days + 1  # Include both start and end dates
            else:
                usage.days = 0
    
    @api.depends('days', 'equipment_id.daily_cost')
    def _compute_total_cost(self):
        """Compute total cost of equipment usage"""
        for usage in self:
            if usage.equipment_id:
                usage.total_cost = usage.days * usage.equipment_id.daily_cost
            else:
                usage.total_cost = 0
