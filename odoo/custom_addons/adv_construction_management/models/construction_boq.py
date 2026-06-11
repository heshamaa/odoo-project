# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ConstructionBOQ(models.Model):
    _name = 'construction.boq'
    _description = 'Bill of Quantities'

    # Basic Fields
    name = fields.Char(
        string='BOQ Name',
        required=True,
        default='BOQ'
    )
    project_id = fields.Many2one(
        'construction.project',
        string='Project',
        required=True,
        ondelete='cascade'
    )
    
    # Totals (computed)
    total_planned = fields.Float(
        string='Total Planned Cost',
        compute='_compute_totals',
        store=True
    )
    total_actual = fields.Float(
        string='Total Actual Cost',
        compute='_compute_totals',
        store=True
    )
    total_variance = fields.Float(
        string='Total Variance',
        compute='_compute_totals',
        store=True
    )
    total_variance_percentage = fields.Float(
        string='Total Variance %',
        compute='_compute_totals',
        store=True
    )
    
    # Relations
    line_ids = fields.One2many(
        'construction.boq.line',
        'boq_id',
        string='BOQ Lines'
    )
    
    @api.depends('line_ids.total_planned', 'line_ids.total_actual')
    def _compute_totals(self):
        """Compute totals for all BOQ lines"""
        for boq in self:
            boq.total_planned = sum(boq.line_ids.mapped('total_planned'))
            boq.total_actual = sum(boq.line_ids.mapped('total_actual'))
            boq.total_variance = boq.total_actual - boq.total_planned
            
            if boq.total_planned:
                boq.total_variance_percentage = (
                    boq.total_variance / boq.total_planned * 100
                )
            else:
                boq.total_variance_percentage = 0
