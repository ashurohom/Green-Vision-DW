# Odoo 18 Shopify Connector (odoo18_shopify_sync)

A robust, one-way synchronization module that connects your Shopify store with Odoo 18. This module seamlessly imports Customers, Products, Sales Orders, and Payments from Shopify into Odoo, saving time and ensuring accurate data flow.

## Features

- **Customer Sync:** Automatically imports customers from Shopify. Prevents duplicates by matching via Shopify Customer ID, Email, or Phone.
- **Product Sync:** Dynamically creates or links products and variants during order import using SKU or Shopify Variant ID.
- **Order Sync:** Imports sales orders, including line items, discounts, shipping, and taxes. Accurately maps financial and fulfillment statuses.
- **Payment Sync:** Imports successful transaction histories for paid orders, creating corresponding payment records in Odoo without duplicates.
- **Manual & Auto Sync:** Trigger synchronizations manually via a Wizard, or let the scheduled daily cron job handle it automatically.
- **Detailed Sync Logs:** Comprehensive logging of all sync operations, including successes, partial failures, skipped records, and API errors.

## Installation

1. Copy the `odoo18_shopify_sync` folder into your Odoo 18 `addons` path.
2. Log into Odoo as an Administrator.
3. Enable **Developer Mode** (Settings -> scroll to bottom -> Activate the developer mode).
4. Go to the **Apps** menu.
5. Click **Update Apps List** in the top menu.
6. Search for `Odoo 18 Shopify Sync` and click **Install**.

## Configuration

Before synchronizing, you must configure your Shopify Instance in Odoo.

### 1. Generate a Shopify Admin API Access Token
To connect Odoo to Shopify, you need a custom app token from your Shopify Admin dashboard:
1. Log into your Shopify Admin dashboard.
2. Go to **Settings** > **Apps and sales channels** > **Develop apps**.
3. Click **Create an app** (e.g., name it "Odoo Integration").
4. Click **Configure Admin API scopes**.
5. Grant **Read** access for the following scopes (at minimum):
   - `read_customers`
   - `read_products`
   - `read_orders`
6. Click **Save** and then **Install app**.
7. **Reveal and copy the Admin API access token**. (Keep this safe, it only shows once).

### 2. Configure the Instance in Odoo
1. In Odoo, navigate to the new **Shopify** app from the main menu.
2. Go to **Configuration** > **Shopify Instances** and click **New**.
3. Fill in the required details:
   - **Name:** e.g., "My Shopify Store"
   - **Company:** Your Odoo Company
   - **Store URL:** Your full Shopify store URL (e.g., `https://your-store.myshopify.com`)
   - **API Version:** Use a supported version (e.g., `2023-10`)
   - **Admin API Access Token:** Paste the token you copied from Shopify.
4. Click the **Test Connection** button at the top to verify your credentials. If successful, the status will change to "Success".
5. Optionally, check the **Auto Sync** box to enable daily background synchronizations.

## How to Use

### Manual Synchronization
You can manually force a sync at any time:
1. Open your configured Shopify Instance in Odoo.
2. Use the buttons at the top of the form:
   - **Sync Customers**: Imports only customers.
   - **Sync Orders**: Imports only sales orders (and associated products).
   - **Sync Payments**: Imports payments for paid orders.
   - **Sync All**: Runs all synchronizations in sequence.

Alternatively, you can go to **Shopify > Operations > Sync Wizard** to trigger manual imports for specific instances.

### Monitoring Synchronizations
To monitor the health and history of your synchronizations:
1. Go to **Shopify > Operations > Sync Logs**.
2. Here you can see a list of all sync attempts, their duration, how many records were imported, skipped, or failed.
3. Click into a failed or partially successful log to view the exact **Error Message** or **API Response** for debugging.

## Technical Architecture

Designed following Odoo 18 best practices, this module uses a decoupled service layer:
- **Models**: Thin data layers (`shopify.instance`, `shopify.sync.log`, `shopify.payment`, plus extensions to core models).
- **Services**: Heavy lifting business logic is housed in the `services/` directory (`shopify_api`, `order_sync_service`, etc.) to ensure reusability and clean code.

## Future Extensibility
This module has been architected to easily support future upgrades, including Webhooks, Inventory Sync, Bidirectional Sync, and more, simply by expanding the existing Service classes.
