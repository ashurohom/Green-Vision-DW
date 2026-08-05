# Odoo 18 Tally Sync

A comprehensive, production-ready framework to synchronize data between Odoo 18 Enterprise and Tally.

## Features
- Tally Configuration
- Test Connection
- Customer Import / Export
- Vendor Import / Export
- Manual Sync Wizard
- Sync Logs
- Reusable Provider-based Service Architecture

## Architecture

This module implements a **Provider Pattern**.
The Odoo models do not contain API logic. They call the service layer which handles API communication and XML parsing/generation.

- `services/tally_client.py`: Abstract Base Class for API communication.
- `services/xml_parser.py`: Logic to parse Tally XML responses.
- `services/xml_generator.py`: Logic to generate Tally-compliant XML.
- `services/customer_service.py` & `vendor_service.py`: Business logic for mapping and orchestration.

## How to replace generic API
If a specific Tally API or middleware is introduced:
1. Subclass `TallyClient` or replace its `send_request` logic.
2. Update the `customer_service.py` and `vendor_service.py` mapping functions if required by the middleware.

## Installation
Just place the `odoo18_tally_sync` folder in your addons path and install it from the Apps menu.

## How to Use

### 1. Configure the API Connection
1. In the **Tally Integration** app, click on **Configuration** -> **Tally Configurations**.
2. Click **New** to create a new configuration record.
3. Fill in the details (Server URL, Company Name, Authentication Type, Credentials).
4. Make sure **Active** is checked.
5. Click **Test Connection** to verify connectivity.

### 2. Export / Import Individual Customers or Vendors
1. Navigate to the main **Contacts** app.
2. Open any Customer or Vendor record.
3. Click the new **Export to Tally** button at the top of the form.
4. Check the **Tally Integration** tab at the bottom to see sync status and Tally ID.

### 3. Run a Bulk Manual Sync
1. In the **Tally Integration** app, click the **Manual Sync** menu.
2. Select whether to sync **Customers** or **Vendors**.
3. Select **Import from Tally** or **Export to Tally**.
4. Click **Start Sync** to process the batch.

### 4. Check the Sync Logs
1. Click the **Sync Logs** menu to see a history of all API requests.
2. Open any log to see the exact XML request sent, response received, and errors (if any).
