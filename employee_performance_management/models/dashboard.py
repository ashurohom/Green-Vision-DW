from odoo import models, fields, api

class EpmDashboard(models.TransientModel):
    _name = 'epm.dashboard'
    _description = 'Performance Dashboard'

    total_employees = fields.Integer(compute='_compute_stats')
    active_kras = fields.Integer(compute='_compute_stats')
    active_kpas = fields.Integer(compute='_compute_stats')
    active_kpis = fields.Integer(compute='_compute_stats')
    pending_reviews = fields.Integer(compute='_compute_stats')
    completed_reviews = fields.Integer(compute='_compute_stats')
    average_score = fields.Float(compute='_compute_stats')

    def _compute_stats(self):
        for record in self:
            record.total_employees = self.env['hr.employee'].search_count([])
            record.active_kras = self.env['epm.kra'].search_count([('active', '=', True)])
            record.active_kpas = self.env['epm.kpa'].search_count([('active', '=', True)])
            record.active_kpis = self.env['epm.kpi'].search_count([('active', '=', True)])
            record.pending_reviews = self.env['epm.manager.review'].search_count([('status', '=', 'draft')])
            record.completed_reviews = self.env['epm.manager.review'].search_count([('status', '=', 'approved')])
            
            evaluations = self.env['epm.final.evaluation'].search([])
            if evaluations:
                total_score = sum(evaluations.mapped('overall_score'))
                record.average_score = total_score / len(evaluations)
            else:
                record.average_score = 0.0
