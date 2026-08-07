from odoo import models, fields

class ShopifySyncLog(models.Model):
    _name = 'shopify.sync.log'
    _description = 'Shopify Sync Log'
    _order = 'date desc'

    instance_id = fields.Many2one('shopify.instance', string='Instance', required=True, ondelete='cascade')
    date = fields.Datetime('Date', default=fields.Datetime.now, required=True, readonly=True)
    sync_type = fields.Selection([
        ('customer', 'Customers'),
        ('product', 'Products'),
        ('order', 'Orders'),
        ('payment', 'Payments'),
    ], string='Sync Type', required=True, readonly=True)
    status = fields.Selection([
        ('success', 'Success'),
        ('partial', 'Partial Success'),
        ('failed', 'Failed'),
    ], string='Status', required=True, readonly=True)
    duration = fields.Float('Duration (seconds)', readonly=True)
    imported_count = fields.Integer('Imported', default=0, readonly=True)
    skipped_count = fields.Integer('Skipped', default=0, readonly=True)
    failed_count = fields.Integer('Failed', default=0, readonly=True)
    error_message = fields.Text('Error Message', readonly=True)
    api_response = fields.Text('API Response', readonly=True)
