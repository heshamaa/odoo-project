# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ConstructionEquipment(models.Model):
    _name = 'construction.equipment'
    _description = 'Construction Equipment'

    # Basic Fields
    name = fields.Char(string='Equipment Name', required=True)
    type = fields.Selection(
        [('machinery', 'Machinery'),
         ('tools', 'Tools'),
         ('vehicles', 'Vehicles'),
         ('other', 'Other')],
        string='Type',
        required=True,
        default='machinery'
    )
    
    # Ownership
    ownership = fields.Selection(
        [('owned', 'Owned'),
         ('rented', 'Rented')],
        string='Ownership',
        required=True,
        default='rented'
    )
    
    # Cost
    daily_cost = fields.Float(
        string='Daily Cost',
        required=True,
        help='Cost per day of usage'
    )
    
    # Details
    serial_number = fields.Char(string='Serial Number')
    acquisition_date = fields.Date(string='Acquisition Date')
    
    # Relations
    usage_ids = fields.One2many(
        'construction.equipment.usage',
        'equipment_id',
        string='Usage Records'
    )
    
    _sql_constraints = [
        ('daily_cost_positive', 'CHECK(daily_cost > 0)', 
         'Daily cost must be positive'),
    ]
