import pytest
import mock
import requests
import unittest
from intercom.client import (IntercomAPI, IntercomHTTPError,
                             IntercomConnectionError)


class IntercomAPITestCase(unittest.TestCase):

    def setUp(self):
        self.headers = {'Accept': 'application/json',
                        'Content-Type': 'application/json'}
        self.auth = (None, None)

    @mock.patch('intercom.client.requests.request')
    def test_request_success(self, mock_request):
        mock_response = mock.Mock()
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        IntercomAPI.request('GET', 'users', {'user_id': '8675309'})
        mock_request.assert_called_once_with(
            'GET', 'https://api.intercom.io/users',
            params={'user_id': '8675309'},
            headers=self.headers, auth=self.auth,
            data='null')
        mock_request.raise_for_status.assert_called_once()

    @mock.patch('intercom.client.requests.request')
    def test_request_http_error(self, mock_request):
        mock_response = mock.Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error
        mock_request.return_value = mock_response
        with pytest.raises(IntercomHTTPError):
            IntercomAPI.request('GET', 'users', {'user_id': 'TheRealJYD'})

    @mock.patch('intercom.client.requests.request')
    def test_request_connection_error(self, mock_request):
        mock_request.side_effect = requests.exceptions.ConnectionError()
        with pytest.raises(IntercomConnectionError):
            IntercomAPI.request('POST', 'users',
                                {'email': 'cambam@askjeeves.com'})
