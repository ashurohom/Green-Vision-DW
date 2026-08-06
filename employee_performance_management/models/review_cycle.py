from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EpmReviewCycle(models.Model):
    _name = 'epm.review.cycle'
    _description = 'Review Cycle'
    _order = 'start_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    cycle_type = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('half_yearly', 'Half Yearly'),
        ('yearly', 'Yearly'),
    ], string='Cycle Type', required=True, default='yearly')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', required=True, default='draft', copy=False, tracking=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("End Date cannot be earlier than Start Date."))

    def action_start(self):
        self.write({'status': 'running'})

    def action_complete(self):
        self.write({'status': 'completed'})

    def action_cancel(self):
        self.write({'status': 'cancelled'})

    def action_draft(self):
        self.write({'status': 'draft'})
