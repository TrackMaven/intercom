import requests
import os
import json
from . import IntercomError


class IntercomHTTPError(IntercomError):
    pass


class IntercomConnectionError(IntercomError):
    pass


class IntercomAPI(object):
    """
    API client for interacting with the intercom API
    """

    BASE_URL = "https://api.intercom.io"

    try:
        from django.conf import settings

        api_token = settings.INTERCOM_API_TOKEN
    except Exception:
        api_token = os.environ.get("INTERCOM_API_TOKEN", "test_token")

    @classmethod
    def request(cls, method, endpoint, params=None, data=None):
        url = "{}/{}".format(cls.BASE_URL, endpoint)
        try:
            response = requests.request(
                method,
                url,
                params=params,
                data=json.dumps(data),
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(cls.api_token),
                },
            )
            try:
                response.raise_for_status()
                print("HERE")
                return response.json()
            except requests.exceptions.HTTPError as e:
                raise IntercomHTTPError(e)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            raise IntercomConnectionError(e)
