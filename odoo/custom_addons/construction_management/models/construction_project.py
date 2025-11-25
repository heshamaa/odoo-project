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
    warehouse_id = fields.Many2one('stock.warehouse', string='Site Warehouse',readonly=True,help="The dedicated warehouse automatically created for this construction site.")
    warehouse_name = fields.Char(
        string='Warehouse Name',
        related='warehouse_id.name',
        readonly=True
    )

    description = fields.Text(string='Description')

    @api.model
    def create(self, vals):
        projects = super(ConstructionProject, self).create(vals)
        for project in projects:
            project._create_project_warehouse()
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('construction.project') or 'New'
        return super(ConstructionProject, self).create(vals)
    

    def _create_project_warehouse(self):
        if not self.warehouse_id:
            warehouse_vals = {
                'name': ('Site: %s') % self.name,
                'code': self.name.replace(' ', '').upper()[:5] + '/' + str(self.id), 
                'project_id': self.id,
            }
            
            new_warehouse = self.env['stock.warehouse'].create(warehouse_vals)
            
            self.warehouse_id = new_warehouse.id
                        
        return True