from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class ShopifyProductSyncService(models.AbstractModel):
    _name = 'shopify.product.sync.service'
    _description = 'Shopify Product Sync Service'

    def get_or_create_product(self, line_item):
        product_obj = self.env['product.product']
        variant_id = str(line_item.get('variant_id') or '')
        product_id = str(line_item.get('product_id') or '')
        sku = line_item.get('sku')
        
        domain = []
        if variant_id:
            domain = [('shopify_variant_id', '=', variant_id)]
        
        product = False
        if domain:
            product = product_obj.search(domain, limit=1)
            
        if not product and sku:
            product = product_obj.search([('default_code', '=', sku)], limit=1)
            
        # Optional: check barcode if available in line_item
        
        if product:
            if variant_id and not product.shopify_variant_id:
                product.shopify_variant_id = variant_id
            if product_id and not product.shopify_product_id:
                product.shopify_product_id = product_id
            return product
            
        # Create new product
        vals = {
            'name': line_item.get('title') or line_item.get('name') or 'Shopify Product',
            'type': 'consu', # Default to consumable or service to avoid stock issues if stock not installed/configured properly
            'list_price': float(line_item.get('price') or 0.0),
            'default_code': sku,
            'shopify_product_id': product_id,
            'shopify_variant_id': variant_id,
        }
        
        return product_obj.create(vals)
