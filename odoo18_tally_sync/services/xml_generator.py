import xml.etree.ElementTree as ET
import logging

_logger = logging.getLogger(__name__)

class XMLGenerator:
    """Generic XML Generator for Tally Requests."""

    @staticmethod
    def generate_partner_xml(partner, partner_type='Customer'):
        """Generates XML for a Customer or Vendor."""
        # Placeholder for actual Tally XML structure
        root = ET.Element("ENVELOPE")
        header = ET.SubElement(root, "HEADER")
        tally_request = ET.SubElement(header, "TALLYREQUEST")
        tally_request.text = "Import Data"
        
        body = ET.SubElement(root, "BODY")
        import_data = ET.SubElement(body, "IMPORTDATA")
        request_desc = ET.SubElement(import_data, "REQUESTDESC")
        report_name = ET.SubElement(request_desc, "REPORTNAME")
        report_name.text = "All Masters"
        
        request_data = ET.SubElement(import_data, "REQUESTDATA")
        tally_message = ET.SubElement(request_data, "TALLYMESSAGE", attrib={"xmlns:UDF": "TallyUDF"})
        ledger = ET.SubElement(tally_message, "LEDGER", attrib={"NAME": partner.name, "ACTION": "Create"})
        
        name = ET.SubElement(ledger, "NAME")
        name.text = partner.name
        
        group = ET.SubElement(ledger, "PARENT")
        group.text = "Sundry Debtors" if partner_type == 'Customer' else "Sundry Creditors"
        
        # Add more fields mapping as needed based on actual Tally structure
        
        return ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')
