from odoo import models, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self:
            # Check if it's a Delivery Order (outgoing)
            if picking.picking_type_id.code == 'outgoing':
                insufficient_products = []
                
                # Check lines
                for move in picking.move_ids:
                    if not move.product_id:
                        continue
                        
                    # Only check Goods (consu)
                    if move.product_id.type != 'consu':
                        continue

                    available_qty = move.product_id.qty_available
                    to_deliver_qty = move.product_uom_qty

                    if to_deliver_qty > available_qty:
                        insufficient_products.append(
                            _(
                                "%s\n"
                                "To Deliver: %s\n"
                                "Available: %s"
                            ) % (
                                move.product_id.display_name,
                                to_deliver_qty,
                                available_qty,
                            )
                        )

                if insufficient_products:
                    message = _(
                        "Cannot validate the delivery because the following products have insufficient stock:\n\n%s"
                    ) % ("\n\n".join(insufficient_products))
                    raise UserError(message)

        return super().button_validate()
