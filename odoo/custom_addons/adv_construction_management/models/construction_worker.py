# -*- coding: utf-8 -*-
from odoo import models, fields


class ConstructionWorker(models.Model):
    _name = 'construction.worker'
    _description = 'Construction Worker'
    _order = 'name'

    # Basic Fields
    name = fields.Char(string='Worker Name', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    
    # Rate
    daily_rate = fields.Float(
        string='Daily Rate (per 8 hours)',
        required=True,
        help='Cost per day (8 working hours)'
    )
    
    # Status
    active = fields.Boolean(string='Active', default=True)
    
    # Relations
    timesheet_ids = fields.One2many(
        'construction.timesheet',
        'worker_id',
        string='Timesheets'
    )
    
    _sql_constraints = [
        ('daily_rate_positive', 'CHECK(daily_rate > 0)', 
         'Daily rate must be positive'),
    ]
