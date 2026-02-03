# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'barcodes.barcode_events_mixin']

    def on_barcode_scanned(self, barcode):
        """Handle barcode scan on sales order.

        This method is called by the barcode mixin when a barcode is scanned.
        It finds the product and adds/updates a sales order line.

        Args:
            barcode: The scanned barcode string

        Returns:
            dict: Action or notification to display
        """
        self.ensure_one()

        # Check order state
        if self.state == 'cancel':
            return {
                'warning': {
                    'title': _('Order Cancelled'),
                    'message': _('Cannot add products to a cancelled order.'),
                }
            }

        if self.state in ('done', 'sale') and self.locked:
            return {
                'warning': {
                    'title': _('Order Locked'),
                    'message': _('Cannot modify a locked order.'),
                }
            }

        # Find product by barcode
        product_info = self.env['product.product'].find_by_barcode_with_info(
            barcode,
            self.company_id.id
        )

        if not product_info.get('product'):
            return {
                'warning': {
                    'title': _('Product Not Found'),
                    'message': product_info.get('error', _('No product found for barcode: %s') % barcode),
                }
            }

        # product_info['product'] can be a dict (serialized) or recordset
        product_data = product_info['product']

        # Extract product_id from dict or recordset
        if isinstance(product_data, dict):
            product_id = product_data.get('id')
        elif hasattr(product_data, 'id'):
            product_id = product_data.id
        else:
            product_id = int(product_data)

        if not product_id:
            return {
                'warning': {
                    'title': _('Product Error'),
                    'message': _('Could not determine product ID'),
                }
            }

        # Check auto-increment setting
        auto_increment = self.env['ir.config_parameter'].sudo().get_param(
            'barcode_scanner.auto_increment', 'True'
        ) == 'True'

        # Look for existing line with this product
        existing_line = self.order_line.filtered(
            lambda l: l.product_id.id == product_id and not l.display_type
        )

        if existing_line and auto_increment:
            # Increment quantity on existing line
            existing_line = existing_line[0]
            existing_line.product_uom_qty += 1
            return self._get_scan_success_notification(product_id, existing_line, incremented=True)
        else:
            # Create new line
            new_line = self._add_product_line(product_id, product_info.get('gs1_data', {}))
            return self._get_scan_success_notification(product_id, new_line, incremented=False)

    def _add_product_line(self, product_id, gs1_data=None):
        """Add a new sales order line for the product.

        Args:
            product_id: int, product ID
            gs1_data: dict with parsed GS1 data (optional)

        Returns:
            sale.order.line record
        """
        self.ensure_one()

        # Prepare line values
        line_vals = {
            'order_id': self.id,
            'product_id': product_id,
            'product_uom_qty': gs1_data.get('quantity', 1) if gs1_data else 1,
        }

        # Create the line - this will trigger onchange to set name, price, etc.
        new_line = self.env['sale.order.line'].create(line_vals)

        return new_line

    def _get_scan_success_notification(self, product_id, line, incremented=False):
        """Generate success notification for scanned product.

        Args:
            product_id: int, product ID
            line: sale.order.line record
            incremented: bool, whether quantity was incremented

        Returns:
            dict: Notification data
        """
        # Get product record
        product = self.env['product.product'].browse(product_id)

        # Check if stock info should be shown
        show_stock = self.env['ir.config_parameter'].sudo().get_param(
            'barcode_scanner.show_stock_info', 'True'
        ) == 'True'

        message_parts = []

        if incremented:
            message_parts.append(_('Quantity updated to %s') % line.product_uom_qty)
        else:
            message_parts.append(_('Added to order'))

        if show_stock and product.type == 'product':
            # Get stock info
            qty_available = product.qty_available
            message_parts.append(_('On hand: %s %s') % (qty_available, product.uom_id.name))

        return {
            'success': {
                'title': product.display_name,
                'message': ' | '.join(message_parts),
            }
        }

    def action_open_barcode_scanner(self):
        """Open the barcode scanner dialog.

        This action is triggered from the button in the form view.
        It returns a client action to open the scanner dialog.
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'barcode_scanner_sale.scan_action',
            'target': 'new',
            'context': {
                'active_model': 'sale.order',
                'active_id': self.id,
            },
        }

    @api.model
    def get_barcode_scan_action(self, order_id):
        """Return action data for barcode scanning on a sales order.

        This method can be called from JavaScript to initiate scanning.

        Args:
            order_id: int, the sales order ID

        Returns:
            dict: Action configuration
        """
        order = self.browse(order_id)
        if not order.exists():
            return {'error': _('Order not found')}

        return {
            'model': 'sale.order',
            'res_id': order_id,
            'can_scan': order.state not in ('cancel', 'done') or not order.locked,
        }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create_from_barcode(self, order_id, barcode):
        """Create a sales order line from a barcode scan.

        This is an alternative method that can be called directly
        from JavaScript without going through the mixin.

        Args:
            order_id: int, the sales order ID
            barcode: str, the scanned barcode

        Returns:
            dict: Result with line data or error
        """
        order = self.env['sale.order'].browse(order_id)
        if not order.exists():
            return {'error': _('Order not found')}

        result = order.on_barcode_scanned(barcode)
        return result
