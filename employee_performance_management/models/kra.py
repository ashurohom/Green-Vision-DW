from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EpmKra(models.Model):
    _name = 'epm.kra'
    _description = 'Key Result Area'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True, copy=False)
    code = fields.Char(string='Code', required=True, copy=False, default=lambda self: _('New'), readonly=True)
    description = fields.Text(string='Description')
    department_id = fields.Many2one('hr.department', string='Department')
    weightage = fields.Float(string='Weightage (%)', required=True, default=100.0)
    review_frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('half_yearly', 'Half Yearly'),
        ('yearly', 'Yearly'),
    ], string='Review Frequency', default='yearly', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(string='Active', default=True)

    kpa_ids = fields.One2many('epm.kpa', 'kra_id', string='KPAs')

    @api.constrains('weightage')
    def _check_weightage(self):
        for record in self:
            if record.weightage < 0.0 or record.weightage > 100.0:
                raise ValidationError(_("Weightage must be between 0 and 100."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('epm.kra') or _('New')
        return super().create(vals_list)

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'The Code of the KRA must be unique!')
    ]
