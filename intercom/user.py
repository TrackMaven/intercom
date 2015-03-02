from . import IntercomError
from .client import IntercomAPI


class User(object):
    endpoint = 'users'

    @classmethod
    def _get_user_params(cls, user_id, email):
        if not user_id and not email:
            raise IntercomError('Must specify either a user_id or email.')
        params = {}
        if user_id is not None:
            params['user_id'] = user_id
        if email is not None:
            params['email'] = email
        return params

    @classmethod
    def create_or_update_user(cls, user_id=None, email=None, name=None,
                              custom_attributes={}, new_session=False,
                              unsubscribed_from_emails=False, **kwargs):
        params = cls._get_user_params(user_id, email)
        for item in ['name', 'new_session', 'unsubscribed_from_emails',
                     'custom_attributes']:
            if eval(item):
                params[item] = eval(item)
        params.update(kwargs)
        return IntercomAPI.request('POST', cls.endpoint, params=params)

    @classmethod
    def update_last_seen(cls, user_id, last_request_at):
        params = {'user_id': user_id, 'last_request_at': last_request_at}
        return IntercomAPI.request('POST', cls.endpoint, params=params)

    @classmethod
    def bulk_create_users(cls, users):
        return IntercomAPI.request('POST', cls.endpoint,
                                   params={'users': users})

    @classmethod
    def get_users(cls, tag_id=None, segment_id=None):
        params = {'page': 1}
        if tag_id is not None:
            params['tag_id'] = tag_id
        if segment_id is not None:
            params['segment_id'] = segment_id
        data = IntercomAPI.request('GET', cls.endpoint, params=params)
        results = data['users']
        pages = int(data['total_pages'])
        while (params['page'] <= pages):
            data = IntercomAPI.request('GET', cls.endpoint, params=params)
            results += data['users']
            params['page'] += 1
        return results

    @classmethod
    def get_user(cls, user_id=None, email=None):
        params = cls._get_user_params(user_id, email)
        return IntercomAPI.request('GET', cls.endpoint, params=params)

    @classmethod
    def delete_user(cls, user_id=None, email=None):
        params = cls._get_user_params(user_id, email)
        return IntercomAPI.request('DELETE', cls.endpoint, params=params)
