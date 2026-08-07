from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    shopify_customer_id = fields.Char('Shopify Customer ID', index=True, copy=False)
