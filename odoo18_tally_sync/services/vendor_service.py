from .tally_client import TallyAPIProvider
from .xml_generator import XMLGenerator
from .xml_parser import XMLParser
from odoo import _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class VendorService:
    """Service to handle vendor synchronization."""

    def __init__(self, env):
        self.env = env
        config = self.env['tally.configuration'].search([('active', '=', True)], limit=1)
        if not config:
            raise UserError(_("No active Tally configuration found."))
        
        self.client = TallyAPIProvider(
            server_url=config.server_url,
            auth_type=config.auth_type,
            username=config.username,
            password=config.password,
            token=config.api_token,
            timeout=config.connection_timeout
        )

    def export_vendor(self, partner):
        """Exports a single vendor to Tally."""
        payload = XMLGenerator.generate_partner_xml(partner, partner_type='Vendor')
        success, response = self.client.send_request(payload)
        
        # Parse response here
        parsed_response = XMLParser.parse_response(response) if success else {}
        
        return success, response, payload

    def import_vendors(self):
        """Imports vendors from Tally."""
        # Placeholder payload for fetching vendors
        payload = "<ENVELOPE><HEADER><TALLYREQUEST>Export Data</TALLYREQUEST></HEADER><BODY><EXPORTDATA><REQUESTDESC><REPORTNAME>List of Accounts</REPORTNAME></REQUESTDESC></EXPORTDATA></BODY></ENVELOPE>"
        success, response = self.client.send_request(payload)
        
        if success:
            parsed_response = XMLParser.parse_response(response)
            # Logic to create or update res.partner
            # ...
        
        return success, response
