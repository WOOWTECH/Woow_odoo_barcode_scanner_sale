/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

/**
 * Sale Order Barcode Scanner Action
 *
 * Client action for scanning barcodes into sales orders.
 * Opens the scanner dialog and handles product addition to SO lines.
 */
export class SaleBarcodeScannerAction extends Component {
    static template = "barcode_scanner_sale.ScannerAction";
    static props = {
        action: { type: Object, optional: true },
        actionId: { type: Number, optional: true },
        "*": true,
    };

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.barcodeScanner = useService("barcodeScanner");
        this.actionService = useService("action");

        this.state = useState({
            orderId: null,
            orderName: "",
            isLoading: true,
            scannedProducts: [],
        });

        onWillStart(async () => {
            await this.loadOrderInfo();
        });
    }

    async loadOrderInfo() {
        const context = this.props.action?.context || {};
        this.state.orderId = context.active_id;

        if (this.state.orderId) {
            const orders = await this.orm.read(
                "sale.order",
                [this.state.orderId],
                ["name", "state", "partner_id"]
            );
            if (orders.length > 0) {
                this.state.orderName = orders[0].name;
            }
        }
        this.state.isLoading = false;
    }

    /**
     * Open the barcode scanner dialog
     */
    async openScanner() {
        this.barcodeScanner.scanForProduct({
            onProduct: async (result) => {
                await this.addProductToOrder(result);
            },
            onNotFound: (result) => {
                this.notification.add(
                    _t("Product not found: %s", result.barcode),
                    { type: "danger" }
                );
            },
            keepOpen: true, // Keep scanner open for multiple scans
        });
    }

    /**
     * Add scanned product to the sales order
     */
    async addProductToOrder(productResult) {
        if (!this.state.orderId) {
            this.notification.add(_t("No order selected"), { type: "danger" });
            return;
        }

        try {
            const result = await this.orm.call(
                "sale.order.line",
                "create_from_barcode",
                [this.state.orderId, productResult.scanResult.barcode]
            );

            if (result.success) {
                this.notification.add(result.success.message, {
                    title: result.success.title,
                    type: "success",
                });

                // Add to scanned list
                this.state.scannedProducts.push({
                    name: result.success.title,
                    barcode: productResult.scanResult.barcode,
                    timestamp: new Date().toLocaleTimeString(),
                });
            } else if (result.warning) {
                this.notification.add(result.warning.message, {
                    title: result.warning.title,
                    type: "warning",
                });
            } else if (result.error) {
                this.notification.add(result.error, { type: "danger" });
            }
        } catch (error) {
            console.error("Error adding product to order:", error);
            this.notification.add(_t("Error adding product to order"), {
                type: "danger",
            });
        }
    }

    /**
     * Close the scanner and return to the order
     */
    close() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: "sale.order",
            res_id: this.state.orderId,
            views: [[false, "form"]],
            target: "current",
        });
    }
}

SaleBarcodeScannerAction.template = "barcode_scanner_sale.ScannerAction";

// Register the client action
registry.category("actions").add("barcode_scanner_sale.scan_action", SaleBarcodeScannerAction);
