from odoo import models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):

        for order in self:

            insufficient_products = []

            for line in order.order_line:

                # Ignore section/note lines
                if not line.product_id:
                    continue

                # Only check products of type 'Goods' (consu)
                if line.product_id.type != "consu":
                    continue

                available_qty = line.product_id.free_qty
                requested_qty = line.product_uom_qty

                if requested_qty > available_qty:

                    insufficient_products.append(
                        _(
                            "%s\n"
                            "Requested: %s\n"
                            "Available: %s"
                        )
                        % (
                            line.product_id.display_name,
                            requested_qty,
                            available_qty,
                        )
                    )

            if insufficient_products:

                message = _(
                    "Cannot confirm the quotation because the following products have insufficient stock:\n\n%s"
                ) % ("\n\n".join(insufficient_products))

                raise UserError(message)

        return super().action_confirm()