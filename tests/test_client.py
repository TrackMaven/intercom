import pytest
import unittest.mock as mock
import requests
import unittest
from intercom.client import IntercomAPI, IntercomHTTPError, IntercomConnectionError


class IntercomAPITestCase(unittest.TestCase):
    def setUp(self):
        self.headers = {
            "Accept": "application/json",
            "Authorization": "Bearer test_token",
            "Content-Type": "application/json",
        }

    @mock.patch("intercom.client.requests.request")
    def test_request_success(self, mock_request):
        mock_response = mock.Mock()
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        r = IntercomAPI.request("GET", "users", {"user_id": "8675309"})
        print(r)
        mock_request.assert_called_once_with(
            "GET", "https://api.intercom.io/users", params={"user_id": "8675309"}, data="null", headers=self.headers
        )
        mock_request.raise_for_status.assert_called_once()

    @mock.patch("intercom.client.requests.request")
    def test_request_http_error(self, mock_request):
        mock_response = mock.Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_request.return_value = mock_response
        with pytest.raises(IntercomHTTPError):
            IntercomAPI.request("GET", "users", {"user_id": "TheRealJYD"})

    @mock.patch("intercom.client.requests.request")
    def test_request_connection_error(self, mock_request):
        mock_request.side_effect = requests.exceptions.ConnectionError()
        with pytest.raises(IntercomConnectionError):
            IntercomAPI.request("POST", "users", {"email": "cambam@askjeeves.com"})
