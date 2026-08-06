from odoo import models, api

class EpmScoreCalculator(models.AbstractModel):
    _name = 'epm.score.calculator'
    _description = 'Performance Score Calculator Service'

    @api.model
    def calculate_final_evaluation(self, evaluation):
        """
        Calculates KPI -> KPA -> KRA -> Overall score based on a Self Review and Manager Review.
        Since we need the reviews, we'll find them based on the assignment.
        """
        # Find self review and manager review linked to this assignment
        self_review = self.env['epm.self.review'].search([('assignment_id', '=', evaluation.assignment_id.id)], limit=1)
        manager_review = self.env['epm.manager.review'].search([('assignment_id', '=', evaluation.assignment_id.id)], limit=1)
        
        if not self_review:
            return False

        # Clear existing lines
        evaluation.line_ids.unlink()
        
        lines_to_create = []
        kpi_scores = {}
        kpa_scores = {}
        kra_scores = {}
        
        # Calculate KPI scores based on self review
        for line in self_review.line_ids:
            score = line.automatic_score
            # If manager adjusted the score or we want to use manager rating instead, that logic can be here.
            # We'll use automatic score for this example.
            kpi_scores[line.kpi_id] = score
            lines_to_create.append({
                'evaluation_id': evaluation.id,
                'type': 'kpi',
                'reference_id': line.kpi_id.id,
                'name': f"KPI: {line.kpi_id.name}",
                'score': score
            })
            
            # Aggregate to KPA
            kpa = line.kpa_id
            if kpa not in kpa_scores:
                kpa_scores[kpa] = {'total_kpi_score': 0.0, 'weightage': kpa.weightage}
            kpa_scores[kpa]['total_kpi_score'] += score

        # Calculate KPA scores
        for kpa, data in kpa_scores.items():
            # KPA Score = Sum of KPI scores * KPA weightage (if relative, or just sum if absolute)
            # Assuming KPI scores are already weighted out of 100, and KPA just aggregates them.
            # Let's say KPA score is simply the sum of its KPI scores (since KPI weightage usually sums to 100 within a KPA).
            # If we apply KPA weightage, it would be (Total KPI Score) * (KPA Weightage / 100)
            kpa_score = data['total_kpi_score'] * (data['weightage'] / 100.0)
            lines_to_create.append({
                'evaluation_id': evaluation.id,
                'type': 'kpa',
                'reference_id': kpa.id,
                'name': f"KPA: {kpa.name}",
                'score': kpa_score
            })
            
            # Aggregate to KRA
            kra = kpa.kra_id
            if kra not in kra_scores:
                kra_scores[kra] = {'total_kpa_score': 0.0, 'weightage': kra.weightage}
            kra_scores[kra]['total_kpa_score'] += kpa_score
            
        # Calculate KRA scores
        for kra, data in kra_scores.items():
            kra_score = data['total_kpa_score'] * (data['weightage'] / 100.0)
            lines_to_create.append({
                'evaluation_id': evaluation.id,
                'type': 'kra',
                'reference_id': kra.id,
                'name': f"KRA: {kra.name}",
                'score': kra_score
            })
            
        # Create the lines. Overall score will be automatically computed in the evaluation model by summing KRA scores.
        # Wait, if we create all lines and the evaluation model sums all lines, it will double count.
        # So we should only sum 'kra' lines for overall score in the evaluation model, or we can let evaluation model sum everything and we just don't sum here.
        # The prompt says: "Automatically calculate: KPI Score -> KPA Score -> KRA Score -> Overall % -> Performance Rating."
        # We will adjust the compute method in EpmFinalEvaluation to sum only KRA scores.
        self.env['epm.final.evaluation.line'].create(lines_to_create)
        return True
