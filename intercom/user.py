from . import IntercomError
from .client import IntercomAPI


class User(object):
    endpoint = 'users'
    attributes = ('user_id', 'email', 'id', 'signed_up_at', 'name',
                  'last_seen_ip', 'custom_attributes', 'last_seen_user_agent',
                  'companies', 'last_request_at', 'unsubscribed_from_emails')

    def _extract_companies(self, companies):
        result = []
        for comp in companies['companies']:
            result.append({'company_id': comp['company_id'],
                          'name': comp['name']})
            return result

    def __init__(self, **kwargs):
        for item in kwargs.keys():
            if item == 'companies':
                setattr(self, item, self._extract_companies(kwargs[item]))
                continue
            setattr(self, item, kwargs[item])

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
    def create(cls, user_id=None, email=None, new_session=False,
               update_last_request_at=False, **kwargs):
        data = cls._get_user_params(user_id, email)
        data['update_last_request_at'] = update_last_request_at
        data['new_session'] = new_session
        data.update(kwargs)
        return IntercomAPI.request('POST', cls.endpoint, data=data)

    @classmethod
    def update_last_seen(cls, user_id, last_request_at):
        data = {'user_id': user_id, 'last_request_at': last_request_at}
        return IntercomAPI.request('POST', cls.endpoint, data=data)

    @classmethod
    def bulk_create_users(cls, users):
        return IntercomAPI.request('POST', cls.endpoint,
                                   data={'users': users})

    @classmethod
    def list(cls, tag_id=None, segment_id=None):
        params = {'page': 1}
        if tag_id is not None:
            params['tag_id'] = tag_id
        if segment_id is not None:
            params['segment_id'] = segment_id
        data = IntercomAPI.request('GET', cls.endpoint, params=params)
        params['page'] += 1
        results = data['users']
        pages = int(data['pages']['total_pages'])

        while (params['page'] <= pages):
            data = IntercomAPI.request('GET', cls.endpoint, params=params)
            results += data['users']
            params['page'] += 1
        return [cls(**item) for item in results]

    @classmethod
    def get(cls, user_id=None, email=None):
        params = cls._get_user_params(user_id, email)
        data = IntercomAPI.request('GET', cls.endpoint, params=params)
        return cls(**data)

    @classmethod
    def delete_user(cls, user_id=None, email=None):
        params = cls._get_user_params(user_id, email)
        return IntercomAPI.request('DELETE', cls.endpoint, params=params)

    def save(self, update_last_request_at=False, new_session=False):
        data = {'new_session': new_session,
                'update_last_request_at': update_last_request_at}
        for attribute in self.attributes:
            if (hasattr(self, attribute) and
                    getattr(self, attribute) is not None):
                data[attribute] = getattr(self, attribute)
        new_data = IntercomAPI.request('POST', self.endpoint, data=data)
        self.__init__(**new_data)

    def delete(self):
        IntercomAPI.request('DELETE', self.endpoint,
                            params={'user_id': self.user_id})
