# Barcode Scanner - Sales

Barcode and QR code scanning integration for Sales Orders in Odoo 18.

---

# 條碼掃描 - 銷售模組

Odoo 18 銷售訂單條碼與 QR Code 掃描整合模組。

---

## Features / 功能特色

### English

- **Scan to Add Products**: Scan barcodes to add products to sales order lines
- **Auto-Increment**: Automatically increase quantity when scanning the same product
- **Stock Info Display**: Show on-hand quantity after scanning
- **State Validation**: Prevent scanning on cancelled or locked orders
- **GS1-128 Support**: Extract product info from GS1 barcodes

### 繁體中文

- **掃描新增產品**：掃描條碼將產品加入銷售訂單明細
- **自動累加**：掃描相同產品時自動增加數量
- **庫存資訊顯示**：掃描後顯示現有庫存數量
- **狀態驗證**：防止在已取消或鎖定的訂單上掃描
- **GS1-128 支援**：從 GS1 條碼擷取產品資訊

---

## Dependencies / 相依性

- `barcode_scanner_base`
- `sale_management`

---

## Installation / 安裝

### English

1. Install `barcode_scanner_base` first
2. Install this module from Apps menu
3. The scanner button will appear on Sales Order forms

### 繁體中文

1. 先安裝 `barcode_scanner_base`
2. 從應用程式選單安裝此模組
3. 掃描器按鈕將出現在銷售訂單表單上

---

## Usage / 使用方式

### Scanning Products / 掃描產品

**English:**

1. Create or open a Sales Order (must be in Draft or Quotation state)
2. Click the **Scan** button in the form header
3. Allow camera access when prompted
4. Point the camera at a product barcode
5. The product is automatically added to order lines with quantity 1
6. Scan the same barcode again to increment quantity
7. Click **Close** when done

**繁體中文：**

1. 建立或開啟銷售訂單（必須是草稿或報價單狀態）
2. 點擊表單標題列的 **掃描** 按鈕
3. 在提示時允許相機存取
4. 將相機對準產品條碼
5. 產品會自動加入訂單明細，數量為 1
6. 再次掃描相同條碼可增加數量
7. 完成後點擊 **關閉**

### Using USB Scanner / 使用 USB 掃描器

**English:**

The module also supports USB/Bluetooth barcode scanners. Simply focus on the Sales Order form and scan - the barcode will be processed automatically.

**繁體中文：**

此模組也支援 USB/藍牙條碼掃描器。只需將焦點放在銷售訂單表單上並掃描，條碼會自動處理。

---

## Notifications / 通知訊息

| Type | Message | 說明 |
|------|---------|------|
| Success | "Added to order" | 已加入訂單 |
| Success | "Quantity updated to X" | 數量已更新為 X |
| Warning | "Product Not Found" | 找不到產品 |
| Warning | "Order Cancelled" | 訂單已取消 |
| Warning | "Order Locked" | 訂單已鎖定 |

---

## API Reference / API 參考

### sale.order

| Method | Description | 說明 |
|--------|-------------|------|
| `on_barcode_scanned(barcode)` | Handle barcode scan event | 處理條碼掃描事件 |
| `action_open_barcode_scanner()` | Open scanner dialog | 開啟掃描器對話框 |

### sale.order.line

| Method | Description | 說明 |
|--------|-------------|------|
| `create_from_barcode(order_id, barcode)` | Create line from barcode | 從條碼建立明細 |

---

## Screenshots / 截圖

### Scanner Button Location / 掃描器按鈕位置

The scan button appears in the Sales Order form header next to the state buttons.

掃描按鈕出現在銷售訂單表單標題列，位於狀態按鈕旁邊。

---

## Troubleshooting / 疑難排解

### "Order Cancelled" error / 「訂單已取消」錯誤

**English:** You cannot add products to a cancelled order. Create a new quotation instead.

**繁體中文：** 無法將產品加入已取消的訂單。請改建立新的報價單。

### "Order Locked" error / 「訂單已鎖定」錯誤

**English:** The order has been confirmed and locked. Unlock it first or create a new order.

**繁體中文：** 訂單已確認並鎖定。請先解鎖訂單或建立新訂單。

---

## License / 授權

LGPL-3.0

---

**Author / 作者:** Woow Tech

**Version / 版本:** 18.0.1.0.0
