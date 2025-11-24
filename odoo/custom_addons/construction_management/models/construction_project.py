from odoo import models, fields, api

class ConstructionProject(models.Model):
    _name = 'construction.project'
    _description = 'Construction Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Project Name', required=True, tracking=True)
    code = fields.Char(string='Project Code', required=True, copy=False, default='New')
    
    project_type = fields.Selection([
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('infrastructure', 'Infrastructure'),
        ('industrial', 'Industrial')
    ], string='Project Type', required=True)
    
    site_location = fields.Char(string='Site Location')
    

    site_engineer_id = fields.Many2one('res.users', string='Site Engineer', tracking=True)
    project_manager_id = fields.Many2one('res.users', string='Project Manager', tracking=True)
    
  
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'In Progress'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='Expected End Date')
    
    
    budget = fields.Float(string='Total Budget', tracking=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Site Warehouse')
    

    description = fields.Text(string='Description')

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('construction.project') or 'New'
        return super(ConstructionProject, self).create(vals)