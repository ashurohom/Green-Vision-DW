from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EpmRatingScale(models.Model):
    _name = 'epm.rating.scale'
    _description = 'Rating Scale'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    min_score = fields.Float(string='Minimum Score', required=True)
    max_score = fields.Float(string='Maximum Score', required=True)
    color = fields.Integer(string='Color')
    sequence = fields.Integer(string='Sequence', default=10)

    @api.constrains('min_score', 'max_score')
    def _check_score_limits(self):
        for record in self:
            if record.min_score >= record.max_score:
                raise ValidationError(_("Maximum Score must be strictly greater than Minimum Score."))
