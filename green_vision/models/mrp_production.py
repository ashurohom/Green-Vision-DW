from odoo import models, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def button_mark_done(self):
        for production in self:
            insufficient_products = []
            
            # move_raw_ids are the components to consume
            for move in production.move_raw_ids:
                if not move.product_id:
                    continue
                    
                # Only check Goods (consu)
                if move.product_id.type != 'consu':
                    continue

                available_qty = move.product_id.qty_available
                to_consume_qty = move.product_uom_qty

                if to_consume_qty > available_qty:
                    insufficient_products.append(
                        _(
                            "%s\n"
                            "To Consume: %s\n"
                            "Available: %s"
                        ) % (
                            move.product_id.display_name,
                            to_consume_qty,
                            available_qty,
                        )
                    )

            if insufficient_products:
                message = _(
                    "Cannot produce because the following components have insufficient stock:\n\n%s"
                ) % ("\n\n".join(insufficient_products))
                raise UserError(message)

        return super().button_mark_done()
