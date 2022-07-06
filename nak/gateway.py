import requests

from nak.conf import API_URL
from nak.decorator import check_error

# from ntk.decorator import check_error


class Gateway:
    def __init__(self, email, password, client_id):
        self.client_id = client_id
        self.email = email
        self.password = password

    def _request(self, request_type, url, payload={}, files=None):
        authenticate = requests.auth.HTTPBasicAuth(self.email, self.password)
        return requests.request(request_type, url, data=payload, files=files, auth=authenticate)

    @check_error(error_format='Uploading file to server failed.{error_msg}', response_json=True)
    def update_app(self, files):

        url = f"{API_URL}/api/apps/{self.client_id}/"
        return self._request("PATCH", url, files=files)
