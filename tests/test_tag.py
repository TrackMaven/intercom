import pytest
import unittest.mock as mock
from intercom import User, Tag
from intercom import IntercomError


def test_init():
    fields = {"name": "slurms mckenzie", "id": 2}
    tag = Tag(**fields)
    for item in fields.keys():
        assert getattr(tag, item) == fields[item]


def test_get_user_params_error():
    with pytest.raises(IntercomError):
        User._get_user_params(None, None)


@mock.patch("intercom.client.IntercomAPI.request")
def test_create(mock_request):
    mock_request.return_value = {"type": "tag", "name": "snood", "id": 3}
    tag = Tag.create("snood")
    assert tag.id == 3
    assert tag.name == "snood"
    mock_request.assert_called_once_with("POST", "tags", data={"name": "snood"})


@mock.patch("intercom.client.IntercomAPI.request")
def test_tag_users(mock_request):
    mock_request.return_value = {"type": "tag", "name": "silly", "id": "3"}
    users = [User(user_id="1"), User(user_id=2)]
    tag = Tag.tag_users("silly", users)
    mock_request.called_once_with(
        "POST", "tags", data={"users": [{"user_id": 1, "untag": False}, {"user_id": 2, "untag": False}]}
    )
    assert tag.name == "silly"


@mock.patch("intercom.client.IntercomAPI.request")
def test_untag_users(mock_request):
    mock_request.return_value = {"type": "tag", "name": "silly", "id": "3"}
    users = [User(user_id="1"), User(user_id=2)]
    tag = Tag.tag_users("silly", users, untag=True)
    mock_request.called_once_with(
        "POST", "tags", data={"users": [{"user_id": 1, "untag": True}, {"user_id": 2, "untag": True}]}
    )
    assert tag.name == "silly"


@mock.patch("intercom.client.IntercomAPI.request")
def test_tag_companies(mock_request):
    mock_request.return_value = {"type": "tag", "name": "silly", "id": "3"}
    companies = [{"id": 1}, {"id": 2}]
    tag = Tag.tag_companies("silly", companies)
    mock_request.called_once_with(
        "POST", "tags", data={"companies": [{"id": 1, "untag": False}, {"id": 2, "untag": False}]}
    )
    assert tag.name == "silly"


@mock.patch("intercom.client.IntercomAPI.request")
def test_list(mock_request):
    mock_request.return_value = [{"name": "red", "id": 1}, {"name": "blue", "id": 2}]
    tags = Tag.list()
    mock_request.assert_called_once_with("GET", "tags")
    assert len(tags) == 2
    assert tags[0].name == "red"
    assert tags[0].id == 1
    assert tags[1].name == "blue"
    assert tags[1].id == 2


@mock.patch("intercom.client.IntercomAPI.request")
def test_delete(mock_request):
    tag = Tag(id=1, name="silly")
    tag.delete()
    mock_request.assert_called_once_with("DELETE", "tags/1")
