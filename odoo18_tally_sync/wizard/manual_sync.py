from odoo import models, fields, api, _

class TallyManualSync(models.TransientModel):
    _name = 'tally.manual.sync'
    _description = 'Tally Manual Sync Wizard'

    operation = fields.Selection([
        ('import', 'Import from Tally'),
        ('export', 'Export to Tally')
    ], string='Operation', required=True, default='export')

    sync_model = fields.Selection([
        ('customers', 'Customers'),
        ('vendors', 'Vendors')
    ], string='Model to Sync', required=True, default='customers')

    result_message = fields.Text(string='Result', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ], string='State', default='draft')

    def action_sync(self):
        self.ensure_one()
        from ..services.customer_service import CustomerService
        from ..services.vendor_service import VendorService

        success_count = 0
        failed_count = 0
        
        try:
            if self.sync_model == 'customers':
                service = CustomerService(self.env)
                if self.operation == 'export':
                    partners = self.env['res.partner'].search([('customer_rank', '>', 0)])
                    for p in partners:
                        success, resp, req = service.export_customer(p)
                        if success:
                            success_count += 1
                        else:
                            failed_count += 1
                else:
                    success, resp = service.import_customers()
                    if success:
                        success_count += 1 # placeholder

            elif self.sync_model == 'vendors':
                service = VendorService(self.env)
                if self.operation == 'export':
                    partners = self.env['res.partner'].search([('supplier_rank', '>', 0)])
                    for p in partners:
                        success, resp, req = service.export_vendor(p)
                        if success:
                            success_count += 1
                        else:
                            failed_count += 1
                else:
                    success, resp = service.import_vendors()
                    if success:
                        success_count += 1 # placeholder

            self.result_message = _("Sync Completed.\nSuccess: %d\nFailed: %d") % (success_count, failed_count)
            self.state = 'done'
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'tally.manual.sync',
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }

        except Exception as e:
            self.result_message = _("Error occurred during sync: %s") % str(e)
            self.state = 'done'
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'tally.manual.sync',
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }
