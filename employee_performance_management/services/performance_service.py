from odoo import models, api

class EpmPerformanceService(models.AbstractModel):
    _name = 'epm.performance.service'
    _description = 'Performance Management Service'

    @api.model
    def generate_self_review_for_assignment(self, assignment):
        """
        Creates a draft self review for the given assignment, populating the KPIs from the template.
        """
        template = assignment.performance_template_id
        # Assuming the template has kpi_ids
        lines = []
        for kpi in template.kpi_ids:
            lines.append((0, 0, {
                'kpi_id': kpi.id,
                'target_value': kpi.target_value,
            }))
            
        self_review = self.env['epm.self.review'].create({
            'assignment_id': assignment.id,
            'line_ids': lines,
        })
        return self_review
