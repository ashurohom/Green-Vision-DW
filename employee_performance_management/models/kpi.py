from odoo import models, fields, api, _

class EpmKpi(models.Model):
    _name = 'epm.kpi'
    _description = 'Key Performance Indicator'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True, copy=False)
    code = fields.Char(string='Code', required=True, copy=False, default=lambda self: _('New'), readonly=True)
    kpa_id = fields.Many2one('epm.kpa', string='KPA', required=True, ondelete='cascade')
    description = fields.Text(string='Description')
    measurement_type = fields.Selection([
        ('number', 'Number'),
        ('percentage', 'Percentage'),
        ('currency', 'Currency'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('manual', 'Manual'),
    ], string='Measurement Type', required=True, default='number')
    
    target_value = fields.Float(string='Target Value', required=True, default=100.0)
    minimum_value = fields.Float(string='Minimum Value', default=0.0)
    maximum_value = fields.Float(string='Maximum Value', default=100.0)
    weightage = fields.Float(string='Weightage (%)', required=True, default=100.0)
    
    calculation_method = fields.Selection([
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ], string='Calculation Method', required=True, default='manual')
    
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(string='Active', default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code('epm.kpi') or _('New')
        return super().create(vals_list)

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'The Code of the KPI must be unique!')
    ]
