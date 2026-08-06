from odoo import models, fields, api, _

class EpmSelfReview(models.Model):
    _name = 'epm.self.review'
    _description = 'Self Review'
    _order = 'id desc'

    name = fields.Char(string='Reference', required=True, copy=False, default=lambda self: _('New'), readonly=True)
    assignment_id = fields.Many2one('epm.employee.assignment', string='Assignment', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', related='assignment_id.employee_id', string='Employee', store=True)
    review_cycle_id = fields.Many2one('epm.review.cycle', related='assignment_id.review_cycle_id', string='Review Cycle', store=True)
    
    line_ids = fields.One2many('epm.self.review.line', 'review_id', string='Review Lines')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('epm.self.review') or _('New')
        return super().create(vals_list)

class EpmSelfReviewLine(models.Model):
    _name = 'epm.self.review.line'
    _description = 'Self Review Line'

    review_id = fields.Many2one('epm.self.review', string='Review', required=True, ondelete='cascade')
    kpi_id = fields.Many2one('epm.kpi', string='KPI', required=True)
    kpa_id = fields.Many2one('epm.kpa', related='kpi_id.kpa_id', string='KPA', store=True)
    kra_id = fields.Many2one('epm.kra', related='kpa_id.kra_id', string='KRA', store=True)
    
    target_value = fields.Float(related='kpi_id.target_value', string='Target Value')
    
    achievement = fields.Text(string='Achievement')
    completed_value = fields.Float(string='Completed Value')
    remarks = fields.Text(string='Remarks')
    attachment = fields.Binary(string='Attachment')
    progress_percentage = fields.Float(string='Progress %', compute='_compute_progress', store=True)
    automatic_score = fields.Float(string='Automatic Score', compute='_compute_score', store=True)

    @api.depends('completed_value', 'target_value')
    def _compute_progress(self):
        for record in self:
            if record.target_value and record.completed_value:
                progress = (record.completed_value / record.target_value) * 100
                record.progress_percentage = min(progress, 100.0)
            else:
                record.progress_percentage = 0.0

    @api.depends('progress_percentage', 'kpi_id.weightage')
    def _compute_score(self):
        for record in self:
            record.automatic_score = (record.progress_percentage * record.kpi_id.weightage) / 100.0 if record.kpi_id.weightage else 0.0
