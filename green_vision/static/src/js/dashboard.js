/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class GreenVisionDashboard extends Component {
    static template = "green_vision.Dashboard";

    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");

        this.state = useState({
            dashboardData: {
                total_sales_count: 0,
                so_pending_count: 0,
                total_revenue: 0,
                total_purchase_count: 0,
                po_pending_count: 0,
                total_receivable: 0,
                total_pending: 0,
                total_customers: 0,
                total_vendors: 0,
                total_products: 0,
                total_expenses: 0,
                recent_expenses: [],
            }
        });

        onWillStart(async () => {
            await this.fetchDashboardData();
        });
    }

    async fetchDashboardData() {
        const data = await this.orm.call("green.vision.dashboard", "get_dashboard_data", []);
        this.state.dashboardData = data;
    }

    // Example action opener if we want cards to be clickable
    openSalesOrders() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Sales Orders",
            res_model: "sale.order",
            views: [[false, "list"], [false, "form"]],
            domain: [['state', 'in', ['sale', 'done']]],
        });
    }

    openSOPending() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Sales Orders Pending",
            res_model: "sale.order",
            views: [[false, "list"], [false, "form"]],
            domain: [['state', 'in', ['draft', 'sent']]],
        });
    }

    openReceivables() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Total Receivables",
            res_model: "account.move",
            views: [[false, "list"], [false, "form"]],
            domain: [['move_type', '=', 'out_invoice'], ['state', '=', 'posted']],
        });
    }

    openPendingReceivables() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Pending Receivables",
            res_model: "account.move",
            views: [[false, "list"], [false, "form"]],
            domain: [['move_type', '=', 'out_invoice'], ['state', '=', 'posted'], ['payment_state', 'in', ['not_paid', 'partial']]],
        });
    }

    openPurchaseOrders() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Purchase Orders",
            res_model: "purchase.order",
            views: [[false, "list"], [false, "form"]],
            domain: [['state', 'in', ['purchase', 'done']]],
        });
    }

    openPOPending() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Purchase Orders Pending",
            res_model: "purchase.order",
            views: [[false, "list"], [false, "form"]],
            domain: [['state', 'in', ['draft', 'sent']]],
        });
    }

    openCustomers() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Customers",
            res_model: "res.partner",
            views: [[false, "list"], [false, "form"]],
            domain: [['customer_rank', '>', 0]],
        });
    }

    openVendors() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Vendors",
            res_model: "res.partner",
            views: [[false, "list"], [false, "form"]],
            domain: [['supplier_rank', '>', 0]],
        });
    }

    openProducts() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Products",
            res_model: "product.product",
            views: [[false, "list"], [false, "form"]],
            domain: [],
        });
    }

    openExpenses() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Expenses",
            res_model: "hr.expense",
            views: [[false, "list"], [false, "form"]],
            domain: [['state', 'in', ['approved', 'done']]],
        });
    }

    openAllExpenses() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "All Expenses",
            res_model: "hr.expense",
            views: [[false, "list"], [false, "form"]],
            domain: [],
        });
    }
}

registry.category("actions").add("green_vision.dashboard", GreenVisionDashboard);
