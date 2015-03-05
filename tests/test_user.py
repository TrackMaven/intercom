import pytest
import mock
from intercom import User
from intercom import IntercomError


def test_extract_companies():
    user = User()
    companies = {'companies': [{'company_id': 123,
                                'name': "Jon and Cam's house of mirrors",
                                'type': 'company', 'price': '3 doll hairs'}]}

    output = user._extract_companies(companies)
    assert output == [{'company_id': 123,
                      'name': "Jon and Cam's house of mirrors"}]

def test_init():
    fields = {'name' : 'slurms mckenzie', 'status': 'partying'}
    user = User(**fields)
    for item in fields.keys():
        assert getattr(user, item) == fields[item]

@mock.patch('intercom.user.User._extract_companies')
def test_init_with_companies(mock_extract):
    fields = {'companies': 'stuff'}
    user = User(**fields)
    mock_extract.assert_called_once_with('stuff')

def test_get_user_params_both():
    user_id = '1337'
    email = 'joshthemagic@finnie.com'
    params = User._get_user_params(user_id, email)
    assert {'user_id': user_id, 'email': email} == params


def test_get_user_params_email():
    email = 'joshthemagic@finnie.com'
    params = User._get_user_params(None, email)
    assert {'email': email} == params


def test_get_user_params_user_id():
    user_id = '1337'
    params = User._get_user_params(user_id, None)
    assert {'user_id': user_id} == params


def test_get_user_params_error():
    with pytest.raises(IntercomError):
        User._get_user_params(None, None)


@mock.patch('intercom.user.User._get_user_params')
@mock.patch('intercom.client.IntercomAPI.request')
def test_create_user(mock_request, mock_params):
    email = 'noobs@leagueofcasuals.com'
    name = 'Slurms McKenzie'
    expected = {'name': name, 'email': email, 'update_last_request_at': False,
                'new_session': False}
    mock_params.return_value = {'email': email}
    User.create(user_id='stuff', name=name)
    mock_params.assert_called_once_with('stuff', None)
    mock_request.assert_called_once_with('POST', 'users', data=expected)


@mock.patch('intercom.client.IntercomAPI.request')
def test_update_last_seen(mock_request):
    user_id = '123'
    last_request_at = '12345678'
    User.update_last_seen(user_id, last_request_at)
    mock_request.assert_called_once_with(
        'POST', 'users', data={'user_id': user_id,
                               'last_request_at': last_request_at})


@mock.patch('intercom.client.IntercomAPI.request')
def test_bulk_create_users(mock_request):
    users = [{'name': 'Donald Duck', 'email': 'whatthequack@yahoo.com'}]
    User.bulk_create_users(users)
    mock_request.assert_called_once_with('POST', 'users',
                                         data={'users': users})


@mock.patch('intercom.client.IntercomAPI.request')
def test_list(mock_request):
    tag_id, segment_id = ('123', '456')
    mock_request.side_effect = [
        {'users': [{'name': 'Tom'}], 'pages':{'total_pages': 2}},
        {'users': [{'name': 'Jerry'}], 'pages':{'total_pages': 2}},
    ]
    users = User.list(tag_id, segment_id)
    assert [user.name for user in users] == ['Tom', 'Jerry']
    assert mock_request.call_count == 2


@mock.patch('intercom.client.IntercomAPI.request')
def test_get(mock_request):
    mock_request.return_value = {'name': 'Spock'}
    user = User.get(email='youvulcant@yahoo.com')
    assert user.name == 'Spock'
    mock_request.assert_called_once_with(
        'GET', 'users', params={'email': 'youvulcant@yahoo.com'})


@mock.patch('intercom.user.User._get_user_params')
@mock.patch('intercom.client.IntercomAPI.request')
def test_delete_user(mock_request, mock_params):
    mock_params.return_value = {'email': 'yaherd@perd.com'}
    User.delete_user(email='yaherd@perd.com')
    mock_params.assert_called_once_with(None, 'yaherd@perd.com')
    mock_request.assert_called_once_with('DELETE', 'users',
                                         params={'email': 'yaherd@perd.com'})


@mock.patch('intercom.client.IntercomAPI.request')
def test_save(mock_request):
    user = User(name='Bender Rodriguez', color='saffron', email=None)
    user.save()
    mock_request.assert_called_once_with(
        'POST', 'users', data={'name': 'Bender Rodriguez',
                               'update_last_request_at': False,
                               'new_session': False})


@mock.patch('intercom.client.IntercomAPI.request')
def test_delete(mock_request):
    user = User(user_id='123')
    user.delete()
    mock_request.assert_called_once_with(
        'DELETE', 'users', params={'user_id': '123'})

