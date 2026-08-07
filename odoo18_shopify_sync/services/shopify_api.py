import requests
import logging
from odoo import models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ShopifyApiService(models.AbstractModel):
    _name = 'shopify.api.service'
    _description = 'Shopify API Service'

    def _get_headers(self, instance):
        return {
            'X-Shopify-Access-Token': instance.access_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def _build_url(self, instance, endpoint):
        base_url = instance.store_url.rstrip('/')
        api_version = instance.api_version
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        return f"{base_url}/admin/api/{api_version}{endpoint}"

    def test_connection(self, instance):
        url = self._build_url(instance, '/shop.json')
        try:
            response = requests.get(url, headers=self._get_headers(instance), timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            _logger.error("Shopify connection test failed: %s", str(e))
            return False

    def get(self, instance, endpoint, params=None):
        url = self._build_url(instance, endpoint)
        results = []
        try:
            while url:
                response = requests.get(url, headers=self._get_headers(instance), params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                # Find the main key which is typically the plural of the resource
                main_key = [k for k in data.keys() if k != 'errors']
                if main_key:
                    records = data.get(main_key[0], [])
                    if isinstance(records, list):
                        results.extend(records)
                    else:
                        results.append(records)
                
                # Pagination
                links = response.links
                if 'next' in links:
                    url = links['next']['url']
                    params = None # params are included in the next url
                else:
                    url = None
                    
            return results
        except requests.exceptions.RequestException as e:
            _logger.error("Shopify API GET error on %s: %s", endpoint, str(e))
            self._log_error(instance, 'API GET', str(e))
            raise UserError(_("Error communicating with Shopify: %s") % str(e))

    def _log_error(self, instance, sync_type, message):
        self.env['shopify.sync.log'].create({
            'instance_id': instance.id,
            'sync_type': 'order', # default, will be overridden by specific services if they log it directly
            'status': 'failed',
            'error_message': message,
        })
