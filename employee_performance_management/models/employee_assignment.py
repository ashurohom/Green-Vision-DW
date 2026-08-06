from odoo import models, fields, api, _

class EpmEmployeeAssignment(models.Model):
    _name = 'epm.employee.assignment'
    _description = 'Employee Performance Assignment'
    _order = 'assignment_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, default=lambda self: _('New'), readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id', store=True)
    manager_id = fields.Many2one('hr.employee', string='Manager', related='employee_id.parent_id', store=True)
    review_cycle_id = fields.Many2one('epm.review.cycle', string='Review Cycle', required=True)
    performance_template_id = fields.Many2one('epm.performance.template', string='Performance Template', required=True)
    assignment_date = fields.Date(string='Assignment Date', default=fields.Date.context_today)
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('completed', 'Completed'),
    ], string='Status', required=True, default='draft', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('epm.assignment') or _('New')
        return super().create(vals_list)

    def action_run(self):
        self.write({'status': 'running'})

    def action_complete(self):
        self.write({'status': 'completed'})

    def action_draft(self):
        self.write({'status': 'draft'})
