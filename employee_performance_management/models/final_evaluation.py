from odoo import models, fields, api, _

class EpmFinalEvaluation(models.Model):
    _name = 'epm.final.evaluation'
    _description = 'Final Evaluation'
    _order = 'id desc'

    name = fields.Char(string='Reference', required=True, copy=False, default=lambda self: _('New'), readonly=True)
    assignment_id = fields.Many2one('epm.employee.assignment', string='Assignment', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', related='assignment_id.employee_id', string='Employee', store=True)
    
    overall_score = fields.Float(string='Overall Score (%)', compute='_compute_overall_score', store=True)
    performance_rating_id = fields.Many2one('epm.rating.scale', string='Performance Rating', compute='_compute_performance_rating', store=True)
    final_comment = fields.Text(string='Final Comment')

    line_ids = fields.One2many('epm.final.evaluation.line', 'evaluation_id', string='Evaluation Lines')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('epm.final.eval') or _('New')
        return super().create(vals_list)

    def action_calculate(self):
        self.env['epm.score.calculator'].calculate_final_evaluation(self)

    @api.depends('line_ids.score', 'line_ids.type')
    def _compute_overall_score(self):
        for record in self:
            kra_lines = record.line_ids.filtered(lambda l: l.type == 'kra')
            record.overall_score = sum(kra_lines.mapped('score'))

    @api.depends('overall_score')
    def _compute_performance_rating(self):
        Rating = self.env['epm.rating.scale']
        for record in self:
            rating = Rating.search([
                ('min_score', '<=', record.overall_score),
                ('max_score', '>=', record.overall_score)
            ], limit=1)
            record.performance_rating_id = rating.id if rating else False

class EpmFinalEvaluationLine(models.Model):
    _name = 'epm.final.evaluation.line'
    _description = 'Final Evaluation Line'

    evaluation_id = fields.Many2one('epm.final.evaluation', string='Evaluation', required=True, ondelete='cascade')
    type = fields.Selection([
        ('kpi', 'KPI'),
        ('kpa', 'KPA'),
        ('kra', 'KRA'),
    ], string='Type', required=True)
    reference_id = fields.Integer(string='Reference ID')
    name = fields.Char(string='Name')
    score = fields.Float(string='Calculated Score')
