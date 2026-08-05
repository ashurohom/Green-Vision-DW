import xml.etree.ElementTree as ET
import logging

_logger = logging.getLogger(__name__)

class XMLParser:
    """Generic XML Parser for Tally Responses."""

    @staticmethod
    def parse_response(xml_string):
        """Parses Tally XML response into a Python dictionary."""
        # This is a placeholder. Actual parsing logic depends on Tally's exact XML structure.
        try:
            if not xml_string:
                return {}
            
            root = ET.fromstring(xml_string)
            result = {}
            for child in root:
                result[child.tag] = child.text
            return result
        except ET.ParseError as e:
            _logger.error("Failed to parse XML response: %s", str(e))
            return {}
