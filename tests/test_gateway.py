from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from requests.auth import HTTPBasicAuth

from nak.conf import API_URL
from nak.gateway import Gateway


class TestGateway(TestCase):
    def setUp(self):
        self.client_id = 'ABCD1234'
        self.user_email = 'test@test.com'
        self.password = 'password'

        self.gateway = Gateway(self.client_id, self.password, self.client_id)
        self.mock_zip_file = MagicMock()

    ####
    # _request
    ####
    @patch('nak.gateway.requests', autospec=True)
    def test_request_should_call_requests_correctly(self, mock_requests):
        mock_requests.auth.HTTPBasicAuth.return_value = authenticate = HTTPBasicAuth(
            self.user_email, self.password)

        request_type = 'POST'
        url = 'test.com'
        payload = {}
        files = {'file': ('tmp/test.zip', self.mock_zip_file)}

        self.gateway._request(request_type, url, payload=payload, files=files)

        expected_calls = [call(
            'POST', 'test.com',
            data={},
            files=files,
            auth=authenticate)
        ]
        assert mock_requests.request.mock_calls == expected_calls

    @patch('nak.gateway.requests')
    def test_gateway_update_app_success_should_call_request_correctly(self, mock_requests):
        mock_requests.request.return_value.json.return_value = {"a": "b"}
        mock_requests.request.return_value.ok = True
        mock_requests.request.return_value.headers = {'content-type': 'application/json'}
        mock_requests.auth.HTTPBasicAuth.return_value = authenticate = HTTPBasicAuth(
            self.user_email, self.password)

        self.gateway.update_app(self.mock_zip_file)

        assert mock_requests.request.mock_calls == [
            # call request
            call(
                'PATCH', f'{API_URL}/api/apps/ABCD1234/',
                data={}, files=self.mock_zip_file, auth=authenticate),
        ]

    @patch('nak.gateway.requests')
    def test_gateway_update_app_failed_should_call_request_correctly(self, mock_requests):
        mock_requests.request.return_value.json.return_value = {"error": "file size limit"}
        mock_requests.request.return_value.ok = False
        mock_requests.request.return_value.headers = {'content-type': 'application/json'}
        mock_requests.auth.HTTPBasicAuth.return_value = authenticate = HTTPBasicAuth(
            self.user_email, self.password)

        with self.assertLogs(level='INFO') as log:
            self.gateway.update_app(self.mock_zip_file)

            assert mock_requests.request.mock_calls == [
                # call request
                call(
                    'PATCH', f'{API_URL}/api/apps/ABCD1234/',
                    data={}, files=self.mock_zip_file, auth=authenticate),
                call().json()
            ]

        assert log.output == ['INFO:root:Uploading file to server failed. -> file size limit']
