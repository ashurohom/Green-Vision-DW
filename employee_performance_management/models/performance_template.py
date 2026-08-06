from odoo import models, fields

class EpmPerformanceTemplate(models.Model):
    _name = 'epm.performance.template'
    _description = 'Performance Template'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(default=True)
    description = fields.Text(string='Description')

    kra_ids = fields.Many2many('epm.kra', string='KRAs')
    kpa_ids = fields.Many2many('epm.kpa', string='KPAs')
    kpi_ids = fields.Many2many('epm.kpi', string='KPIs')
