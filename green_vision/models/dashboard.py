from odoo import models, api

class GreenVisionDashboard(models.AbstractModel):
    _name = 'green.vision.dashboard'
    _description = 'Green Vision Dashboard Model'

    @api.model
    def get_dashboard_data(self):
        # Total Sales Order
        total_sales_count = self.env['sale.order'].search_count([('state', 'in', ['sale', 'done'])])

        # Sales Order Approval Pending
        so_pending_count = self.env['sale.order'].search_count([('state', 'in', ['draft', 'sent'])])

        # Total Revenue (Using Sales for simplicity)
        sales = self.env['sale.order'].search([('state', 'in', ['sale', 'done'])])
        total_revenue = sum(sales.mapped('amount_total'))

        # Total Purchase Orders
        total_purchase_count = self.env['purchase.order'].search_count([('state', 'in', ['purchase', 'done'])])

        # Purchase Order Approval Pending
        po_pending_count = self.env['purchase.order'].search_count([('state', 'in', ['draft', 'sent'])])

        # Outstanding Receivable Amount (Pending Customer Invoices)
        out_invoices = self.env['account.move'].search([('move_type', '=', 'out_invoice'), ('state', '=', 'posted')])
        outstanding_receivable = sum(out_invoices.mapped('amount_residual'))

        # Outstanding Payable Amount (Pending Vendor Bills)
        in_invoices = self.env['account.move'].search([('move_type', '=', 'in_invoice'), ('state', '=', 'posted')])
        outstanding_payable = sum(in_invoices.mapped('amount_residual'))

        # Total Customers & Vendors
        total_customers = self.env['res.partner'].search_count([('customer_rank', '>', 0)])
        total_vendors = self.env['res.partner'].search_count([('supplier_rank', '>', 0)])

        # Total Products
        total_products = self.env['product.product'].search_count([])

        # Total Expenses
        total_expenses = sum(self.env['hr.expense'].search([('state', 'in', ['approved', 'done'])]).mapped('total_amount_currency'))

        # Recent Expenses
        expenses = self.env['hr.expense'].search_read(
            [], 
            ['name', 'total_amount_currency', 'state', 'date'], 
            limit=5, 
            order='id desc'
        )

        return {
            'total_sales_count': total_sales_count,
            'so_pending_count': so_pending_count,
            'total_revenue': total_revenue,
            'total_purchase_count': total_purchase_count,
            'po_pending_count': po_pending_count,
            'outstanding_receivable': outstanding_receivable,
            'outstanding_payable': outstanding_payable,
            'total_customers': total_customers,
            'total_vendors': total_vendors,
            'total_products': total_products,
            'total_expenses': total_expenses,
            'recent_expenses': expenses,
        }
