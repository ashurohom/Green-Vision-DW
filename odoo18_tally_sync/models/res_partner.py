from odoo import models, fields, api, _
from odoo.exceptions import UserError
import time

class ResPartner(models.Model):
    _inherit = 'res.partner'

    tally_id = fields.Char(string='Tally ID', help='Unique identifier from Tally.', copy=False)
    last_sync = fields.Datetime(string='Last Sync', readonly=True, copy=False)
    sync_status = fields.Selection([
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string='Sync Status', default='pending', copy=False)

    def action_export_to_tally(self):
        """Triggered by a button on the partner form."""
        from ..services.customer_service import CustomerService
        from ..services.vendor_service import VendorService
        
        for partner in self:
            start_time = time.time()
            success = False
            response = ""
            payload = ""
            error_msg = ""
            try:
                if partner.supplier_rank > 0:
                    service = VendorService(self.env)
                    success, response, payload = service.export_vendor(partner)
                else:
                    service = CustomerService(self.env)
                    success, response, payload = service.export_customer(partner)
                
                partner.sync_status = 'success' if success else 'failed'
                partner.last_sync = fields.Datetime.now()
            except Exception as e:
                error_msg = str(e)
                partner.sync_status = 'failed'
            
            duration = time.time() - start_time
            
            # Log the operation
            self.env['tally.sync.log'].create({
                'operation': 'export',
                'model': 'vendor' if partner.supplier_rank > 0 else 'customer',
                'status': 'success' if success else 'failed',
                'request': payload,
                'response': response,
                'error_message': error_msg,
                'duration': duration,
            })
            
            if not success:
                raise UserError(_("Failed to export to Tally: %s") % (error_msg or "Unknown Error"))
            
    def action_import_from_tally(self):
        """Action for importing from tally (usually a batch process, but can be a single refresh)."""
        # Placeholder implementation
        pass
