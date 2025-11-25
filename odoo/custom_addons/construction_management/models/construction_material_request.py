from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ConstructionMaterialRequest(models.Model):
    _name = 'construction.material.request'
    _description = 'Construction Material Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Request Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    
    project_id = fields.Many2one('construction.project', string='Project', required=True, tracking=True)
    project_manager_id = fields.Many2one(related='project_id.project_manager_id', string='Project Manager', store=True)
    
    request_date = fields.Date(string='Request Date', default=fields.Date.today, required=True)
    requested_by = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user, tracking=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Done') # تم الشراء أو الصرف
    ], string='Status', default='draft', tracking=True)

    request_line_ids = fields.One2many('construction.material.request.line', 'request_id', string='Materials')

    description = fields.Text(string='Notes')



    purchase_order_ids = fields.One2many('purchase.order', 'material_request_id', string='Purchase Orders')
    purchase_count = fields.Integer(compute='_compute_purchase_count', string='PO Count')
    @api.depends('purchase_order_ids')
    def _compute_purchase_count(self):
        for rec in self:
            rec.purchase_count = len(rec.purchase_order_ids)

    def action_create_purchase_order(self):
        self.ensure_one()
        
        po_lines = []
        for line in self.request_line_ids:
            po_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.product_id.name,
                'product_qty': line.quantity,
                'product_uom': line.uom_id.id,
                'date_planned': line.date_required or fields.Date.today(),
                'price_unit': 0.0, # السعر لسه المشتريات هيحددوه
            }))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Purchase Order',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'context': {
                'default_project_id': self.project_id.id,
                'default_material_request_id': self.id,
                'default_order_line': po_lines,
                'default_origin': self.name,
            },
        }

    def action_view_purchase_orders(self):
        self.ensure_one()
        return {
            'name': 'Purchase Orders',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('material_request_id', '=', self.id)],
            'context': {'default_material_request_id': self.id},
        }

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('construction.material.request') or _('New')
        return super(ConstructionMaterialRequest, self).create(vals)

    def action_submit(self):
        for rec in self:
            if not rec.request_line_ids:
                raise ValidationError(_("You cannot submit an empty request. Please add lines."))
            rec.state = 'submitted'

    def action_approve(self):
        for rec in self:
            rec.state = 'approved'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'


class ConstructionMaterialRequestLine(models.Model):
    _name = 'construction.material.request.line'
    _description = 'Material Request Line'

    request_id = fields.Many2one('construction.material.request', string='Request Reference')
    
    product_id = fields.Many2one('product.product', string='Product', required=True)
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    
    # الوحدة بتيجي أوتوماتيك من المنتج بس ينفع نغيرها
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
    
    date_required = fields.Date(string='Date Required')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id
            self.description = self.product_id.name