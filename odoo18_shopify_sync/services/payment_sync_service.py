from odoo import models, fields
import logging
import time

_logger = logging.getLogger(__name__)

class ShopifyPaymentSyncService(models.AbstractModel):
    _name = 'shopify.payment.sync.service'
    _description = 'Shopify Payment Sync Service'

    def sync_payments(self, instance):
        log_vals = {
            'instance_id': instance.id,
            'sync_type': 'payment',
            'status': 'success',
        }
        start_time = time.time()
        imported = 0
        skipped = 0
        failed = 0
        error_msg = ""
        
        api_service = self.env['shopify.api.service']
        
        # Only import payments for paid orders or partially paid
        params = {'financial_status': 'paid'}
        if instance.last_sync_datetime:
            params['updated_at_min'] = instance.last_sync_datetime.isoformat()

        try:
            # First fetch orders that are paid
            orders = api_service.get(instance, '/orders.json', params=params)
            for order in orders:
                try:
                    # Then fetch transactions for these orders
                    order_id = str(order.get('id'))
                    transactions = api_service.get(instance, f'/orders/{order_id}/transactions.json')
                    for trans in transactions:
                        if trans.get('status') == 'success' and trans.get('kind') in ['sale', 'capture']:
                            res = self._sync_single_payment(instance, order_id, trans)
                            if res == 'imported':
                                imported += 1
                            else:
                                skipped += 1
                except Exception as e:
                    _logger.error("Failed to sync payments for order %s: %s", order.get('id'), str(e))
                    failed += 1
                    error_msg += f"Payment for Order {order.get('id')}: {str(e)}\n"
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

    def _sync_single_payment(self, instance, order_id, trans_data):
        payment_obj = self.env['shopify.payment']
        trans_id = str(trans_data.get('id'))
        
        existing = payment_obj.search([('transaction_id', '=', trans_id)], limit=1)
        if existing:
            return 'skipped'
            
        # Find the sale order in Odoo
        so = self.env['sale.order'].search([('shopify_order_id', '=', order_id)], limit=1)
        
        date_trans = trans_data.get('created_at')
        if date_trans:
            date_trans = date_trans[:19].replace('T', ' ')
            
        currency = self.env['res.currency'].search([('name', '=', trans_data.get('currency'))], limit=1)
            
        vals = {
            'transaction_id': trans_id,
            'payment_gateway': trans_data.get('gateway'),
            'amount': float(trans_data.get('amount') or 0.0),
            'currency_id': currency.id if currency else False,
            'payment_date': date_trans or fields.Datetime.now(),
            'payment_status': trans_data.get('status'),
            'sale_order_id': so.id if so else False,
            'company_id': instance.company_id.id,
        }
        
        payment_obj.create(vals)
        return 'imported'
