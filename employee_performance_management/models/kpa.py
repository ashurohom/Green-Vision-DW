from odoo import models, fields, api, _

class EpmKpa(models.Model):
    _name = 'epm.kpa'
    _description = 'Key Performance Area'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True, copy=False)
    code = fields.Char(string='Code', required=True, copy=False, default=lambda self: _('New'), readonly=True)
    kra_id = fields.Many2one('epm.kra', string='KRA', required=True, ondelete='cascade')
    description = fields.Text(string='Description')
    weightage = fields.Float(string='Weightage (%)', required=True, default=100.0)
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(string='Active', default=True)

    kpi_ids = fields.One2many('epm.kpi', 'kpa_id', string='KPIs')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('epm.kpa') or _('New')
        return super().create(vals_list)

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'The Code of the KPA must be unique!')
    ]
