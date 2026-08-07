from odoo import models, fields

class ShopifyManualSync(models.TransientModel):
    _name = 'shopify.manual.sync'
    _description = 'Shopify Manual Sync'

    instance_id = fields.Many2one('shopify.instance', string='Instance', required=True)
    
    def action_import_customers(self):
        self.ensure_one()
        self.instance_id.action_sync_customers()
        return {'type': 'ir.actions.act_window_close'}
        
    def action_import_orders(self):
        self.ensure_one()
        self.instance_id.action_sync_orders()
        return {'type': 'ir.actions.act_window_close'}
        
    def action_import_payments(self):
        self.ensure_one()
        self.instance_id.action_sync_payments()
        return {'type': 'ir.actions.act_window_close'}
        
    def action_import_all(self):
        self.ensure_one()
        self.instance_id.action_sync_all()
        return {'type': 'ir.actions.act_window_close'}
