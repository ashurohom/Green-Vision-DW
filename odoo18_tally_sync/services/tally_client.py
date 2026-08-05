import requests
import logging
from abc import ABC, abstractmethod

_logger = logging.getLogger(__name__)

class TallyClient(ABC):
    """Abstract Base Class for Tally API Communication."""

    def __init__(self, server_url, auth_type, username=None, password=None, token=None, timeout=30):
        self.server_url = server_url
        self.auth_type = auth_type
        self.username = username
        self.password = password
        self.token = token
        self.timeout = timeout

    @abstractmethod
    def test_connection(self):
        """Test the connection to the Tally Server."""
        pass

    @abstractmethod
    def send_request(self, payload):
        """Send a payload to Tally."""
        pass


class TallyAPIProvider(TallyClient):
    """Concrete Implementation of the Tally Client."""

    def _get_headers(self):
        headers = {'Content-Type': 'application/xml'}
        if self.auth_type == 'bearer' and self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def _get_auth(self):
        if self.auth_type == 'basic' and self.username and self.password:
            return (self.username, self.password)
        return None

    def test_connection(self):
        """Placeholder for test connection. Replace with actual logic when API is known."""
        try:
            # Using a generic GET or basic POST to check connection
            response = requests.get(
                self.server_url, 
                headers=self._get_headers(), 
                auth=self._get_auth(),
                timeout=self.timeout
            )
            response.raise_for_status()
            return True, "Connection successful."
        except Exception as e:
            _logger.error("Tally test connection failed: %s", str(e))
            return False, str(e)

    def send_request(self, payload):
        """Placeholder for sending request to Tally."""
        try:
            response = requests.post(
                self.server_url,
                data=payload,
                headers=self._get_headers(),
                auth=self._get_auth(),
                timeout=self.timeout
            )
            response.raise_for_status()
            return True, response.text
        except Exception as e:
            _logger.error("Tally send request failed: %s", str(e))
            return False, str(e)
