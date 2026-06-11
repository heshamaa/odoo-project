# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ConstructionRisk(models.Model):
    _name = 'construction.risk'
    _description = 'Construction Risk Register'

    # Basic Fields
    name = fields.Char(string='Risk Description', required=True)
    project_id = fields.Many2one(
        'construction.project',
        string='Project',
        required=True,
        ondelete='cascade'
    )
    
    description = fields.Text(string='Detailed Description')
    
    # Risk Assessment
    probability = fields.Selection(
        [('low', 'Low (20%)'),
         ('medium', 'Medium (50%)'),
         ('high', 'High (80%)')],
        string='Probability',
        required=True,
        default='medium'
    )
    impact = fields.Selection(
        [('low', 'Low (20%)'),
         ('medium', 'Medium (50%)'),
         ('high', 'High (80%)')],
        string='Impact',
        required=True,
        default='medium'
    )
    
    # Risk Score (computed)
    risk_score = fields.Float(
        string='Risk Score',
        compute='_compute_risk_score',
        store=True,
        help='Probability × Impact'
    )
    
    # Mitigation
    mitigation_plan = fields.Text(string='Mitigation Plan')
    
    # Status
    status = fields.Selection(
        [('identified', 'Identified'),
         ('mitigated', 'Mitigated'),
         ('resolved', 'Resolved')],
        string='Status',
        default='identified',
        tracking=True
    )
    
    # Ownership
    owner_id = fields.Many2one(
        'res.users',
        string='Risk Owner'
    )
    
    _probability_values = {'low': 0.2, 'medium': 0.5, 'high': 0.8}
    _impact_values = {'low': 0.2, 'medium': 0.5, 'high': 0.8}
    
    @api.depends('probability', 'impact')
    def _compute_risk_score(self):
        """Compute risk score as probability × impact"""
        for risk in self:
            prob_value = self._probability_values.get(risk.probability, 0.5)
            impact_value = self._impact_values.get(risk.impact, 0.5)
            risk.risk_score = prob_value * impact_value
