from odoo import models, fields, api, _

class EpmManagerReview(models.Model):
    _name = 'epm.manager.review'
    _description = 'Manager Review'
    _order = 'id desc'

    name = fields.Char(string='Reference', required=True, copy=False, default=lambda self: _('New'), readonly=True)
    self_review_id = fields.Many2one('epm.self.review', string='Self Review', required=True, ondelete='cascade')
    assignment_id = fields.Many2one('epm.employee.assignment', related='self_review_id.assignment_id', string='Assignment', store=True)
    employee_id = fields.Many2one('hr.employee', related='self_review_id.employee_id', string='Employee', store=True)
    manager_id = fields.Many2one('hr.employee', related='assignment_id.manager_id', string='Manager', store=True)
    
    manager_rating = fields.Float(string='Manager Rating')
    manager_remarks = fields.Text(string='Manager Remarks')
    suggested_improvement = fields.Text(string='Suggested Improvement')
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', required=True, tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('epm.manager.review') or _('New')
        return super().create(vals_list)

    def action_approve(self):
        self.write({'status': 'approved'})

    def action_reject(self):
        self.write({'status': 'rejected'})
