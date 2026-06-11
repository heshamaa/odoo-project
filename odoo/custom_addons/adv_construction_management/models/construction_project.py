# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ConstructionProject(models.Model):
    _name = 'construction.project'
    _description = 'Construction Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    # Basic Fields
    name = fields.Char(string='Project Name', required=True, tracking=True)
    client_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        domain=[('customer_rank', '>', 0)],
        tracking=True
    )
    description = fields.Text(string='Description')
    
    # Dates
    start_date = fields.Date(string='Start Date', tracking=True)
    end_date = fields.Date(string='End Date', tracking=True)
    
    # Budget
    budget = fields.Float(string='Total Budget', required=True, tracking=True)
    
    # Status
    state = fields.Selection(
        [('draft', 'Draft'),
         ('ongoing', 'Ongoing'),
         ('completed', 'Completed'),
         ('cancelled', 'Cancelled')],
        string='Status',
        default='draft',
        tracking=True
    )
    
    # Relations
    stage_ids = fields.One2many(
        'construction.stage',
        'project_id',
        string='Stages'
    )
    expense_ids = fields.One2many(
        'construction.expense',
        'project_id',
        string='Expenses'
    )
    timesheet_ids = fields.One2many(
        'construction.timesheet',
        'project_id',
        string='Timesheets'
    )
    subcontract_ids = fields.One2many(
        'construction.subcontract',
        'project_id',
        string='Subcontracts'
    )
    milestone_ids = fields.One2many(
        'construction.milestone',
        'project_id',
        string='Milestones'
    )
    boq_ids = fields.One2many(
        'construction.boq',
        'project_id',
        string='BOQs'
    )
    change_order_ids = fields.One2many(
        'construction.change.order',
        'project_id',
        string='Change Orders'
    )
    equipment_usage_ids = fields.One2many(
        'construction.equipment.usage',
        'project_id',
        string='Equipment Usage'
    )
    risk_ids = fields.One2many(
        'construction.risk',
        'project_id',
        string='Risks'
    )
    
    # Computed Cost Fields (CORE ENGINE)
    actual_expense_cost = fields.Float(
        string='Actual Expense Cost',
        compute='_compute_actual_costs',
        store=True,
        tracking=True
    )
    actual_labor_cost = fields.Float(
        string='Actual Labor Cost',
        compute='_compute_actual_costs',
        store=True,
        tracking=True
    )
    actual_subcontract_cost = fields.Float(
        string='Actual Subcontract Cost',
        compute='_compute_actual_costs',
        store=True,
        tracking=True
    )
    actual_cost = fields.Float(
        string='Total Actual Cost',
        compute='_compute_actual_costs',
        store=True,
        tracking=True
    )
    equipment_cost = fields.Float(
        string='Equipment Cost',
        compute='_compute_actual_costs',
        store=True,
        tracking=True
    )
    total_actual_cost = fields.Float(
        string='Total Actual Cost (with Equipment)',
        compute='_compute_actual_costs',
        store=True,
        tracking=True
    )
    profit = fields.Float(
        string='Profit',
        compute='_compute_profit',
        store=True,
        tracking=True
    )
    profit_margin = fields.Float(
        string='Profit Margin %',
        compute='_compute_profit_margin',
        store=True
    )
    progress = fields.Float(
        string='Overall Progress %',
        compute='_compute_progress',
        store=True
    )
    is_over_budget = fields.Boolean(
        string='Over Budget?',
        compute='_compute_is_over_budget',
        store=True
    )
    
    # Triggers for recomputation
    _sql_constraints = [
        ('budget_positive', 'CHECK(budget > 0)', 'Budget must be positive'),
    ]
    
    def action_start(self):
        """Change project state to ongoing"""
        self.state = 'ongoing'
    
    def action_complete(self):
        """Change project state to completed"""
        self.state = 'completed'
    
    def action_cancel(self):
        """Change project state to cancelled"""
        self.state = 'cancelled'
    
    # Core Compute Functions
    @api.depends(
        'expense_ids.amount',
        'expense_ids.approved',
        'timesheet_ids.cost',
        'subcontract_ids.paid_amount',
        'equipment_usage_ids.total_cost'
    )
    def _compute_actual_costs(self):
        """Compute all actual costs from all sources"""
        for project in self:
            # Approved expenses only
            approved_expenses = project.expense_ids.filtered('approved')
            project.actual_expense_cost = sum(approved_expenses.mapped('amount'))
            
            # Labor costs from timesheets
            project.actual_labor_cost = sum(project.timesheet_ids.mapped('cost'))
            
            # Subcontract paid amounts
            project.actual_subcontract_cost = sum(
                project.subcontract_ids.mapped('paid_amount')
            )
            
            # Equipment costs
            project.equipment_cost = sum(
                project.equipment_usage_ids.mapped('total_cost')
            )
            
            # Total actual cost (Core + Equipment)
            project.actual_cost = (
                project.actual_expense_cost +
                project.actual_labor_cost +
                project.actual_subcontract_cost
            )
            project.total_actual_cost = (
                project.actual_cost + project.equipment_cost
            )
    
    @api.depends('budget', 'total_actual_cost')
    def _compute_profit(self):
        """Compute profit"""
        for project in self:
            project.profit = project.budget - project.total_actual_cost
    
    @api.depends('profit', 'budget')
    def _compute_profit_margin(self):
        """Compute profit margin percentage"""
        for project in self:
            if project.budget:
                project.profit_margin = (project.profit / project.budget) * 100
            else:
                project.profit_margin = 0
    
    @api.depends('stage_ids.progress')
    def _compute_progress(self):
        """Compute overall progress from stages"""
        for project in self:
            if project.stage_ids:
                project.progress = sum(
                    project.stage_ids.mapped('progress')
                ) / len(project.stage_ids)
            else:
                project.progress = 0
    
    @api.depends('profit')
    def _compute_is_over_budget(self):
        """Check if project is over budget"""
        for project in self:
            project.is_over_budget = project.profit < 0
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """Validate start and end dates"""
        for project in self:
            if project.start_date and project.end_date:
                if project.start_date > project.end_date:
                    raise ValidationError(
                        'Start date must be before end date!'
                    )
