from odoo import models, fields
import logging
import time

_logger = logging.getLogger(__name__)

class ShopifyCustomerSyncService(models.AbstractModel):
    _name = 'shopify.customer.sync.service'
    _description = 'Shopify Customer Sync Service'

    def sync_customers(self, instance):
        log_vals = {
            'instance_id': instance.id,
            'sync_type': 'customer',
            'status': 'success',
        }
        start_time = time.time()
        imported = 0
        skipped = 0
        failed = 0
        error_msg = ""
        
        api_service = self.env['shopify.api.service']
        
        params = {}
        if instance.last_sync_datetime:
            # Format datetime to ISO 8601 for Shopify
            params['updated_at_min'] = instance.last_sync_datetime.isoformat()

        try:
            customers = api_service.get(instance, '/customers.json', params=params)
            for cust in customers:
                try:
                    self._sync_single_customer(cust)
                    imported += 1
                except Exception as e:
                    _logger.error("Failed to sync customer %s: %s", cust.get('id'), str(e))
                    failed += 1
                    error_msg += f"Customer {cust.get('id')}: {str(e)}\n"
        except Exception as e:
            log_vals['status'] = 'failed'
            error_msg = str(e)
            
        if failed > 0 and log_vals['status'] == 'success':
            log_vals['status'] = 'partial'
            
        log_vals.update({
            'duration': time.time() - start_time,
            'imported_count': imported,
            'skipped_count': skipped,
            'failed_count': failed,
            'error_message': error_msg,
        })
        self.env['shopify.sync.log'].create(log_vals)

    def _sync_single_customer(self, cust_data):
        partner_obj = self.env['res.partner']
        shopify_id = str(cust_data.get('id'))
        email = cust_data.get('email')
        phone = cust_data.get('phone')
        
        domain = [('shopify_customer_id', '=', shopify_id)]
        partner = partner_obj.search(domain, limit=1)
        
        if not partner and email:
            partner = partner_obj.search([('email', '=', email)], limit=1)
        if not partner and phone:
            partner = partner_obj.search([('phone', '=', phone)], limit=1)
            
        vals = {
            'shopify_customer_id': shopify_id,
            'name': f"{cust_data.get('first_name', '')} {cust_data.get('last_name', '')}".strip() or email or shopify_id,
            'email': email,
            'phone': phone,
        }
        
        if partner:
            partner.write(vals)
        else:
            partner_obj.create(vals)
