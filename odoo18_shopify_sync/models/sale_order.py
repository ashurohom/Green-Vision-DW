from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    shopify_order_id = fields.Char('Shopify Order ID', index=True, copy=False)
    shopify_financial_status = fields.Char('Shopify Financial Status', copy=False)
    shopify_fulfillment_status = fields.Char('Shopify Fulfillment Status', copy=False)
    shopify_raw_json = fields.Text('Shopify Raw JSON', copy=False)
