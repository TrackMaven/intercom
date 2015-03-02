import requests
import os
from . import IntercomError


class IntercomHTTPError(IntercomError):
    pass


class IntercomConnectionError(IntercomError):
    pass


class IntercomAPI(object):
    """
    API client for interacting with the intercom API
    """
    BASE_URL = 'https://api.intercom.io'

    try:
        from django.conf import settings
        api_key = settings.INTERCOM_API_KEY
        app_id = settings.INTERCOM_APP_ID
    except:
        api_key = os.environ.get('INTERCOM_API_KEY')
        app_id = os.environ.get('INTERCOM_APP_ID')

    @classmethod
    def request(cls, method, endpoint, params):
        url = '{}/{}'.format(cls.BASE_URL, endpoint)
        try:
            response = requests.request(method, url, params=params)
            try:
                response.raise_for_status()
                return response
            except requests.exceptions.HTTPError as e:
                raise IntercomHTTPError(e)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout) as e:
            raise IntercomConnectionError(e)
