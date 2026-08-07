from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    shopify_product_id = fields.Char('Shopify Product ID', index=True, copy=False)
    shopify_variant_id = fields.Char('Shopify Variant ID', index=True, copy=False)
