from .client import IntercomAPI


class Tag(object):
    endpoint = "tags"
    attributes = ("id", "name")

    def __init__(self, **kwargs):
        for item in kwargs.keys():
            setattr(self, item, kwargs[item])

    @classmethod
    def create(cls, name):
        data = IntercomAPI.request("POST", cls.endpoint, data={"name": name})
        return cls(**data)

    @classmethod
    def tag_users(cls, name, users, untag=False):
        list_of_users = [{"user_id": user.user_id, "untag": untag} for user in users]
        data = IntercomAPI.request("POST", cls.endpoint, data={"name": name, "users": list_of_users})
        return cls(**data)

    @classmethod
    def tag_companies(cls, name, companies, untag=False):
        company_list = [{"id": company.get("id"), "untag": untag} for company in companies]
        data = IntercomAPI.request("POST", cls.endpoint, data={"name": name, "companies": company_list})
        return cls(**data)

    @classmethod
    def list(cls):
        return [cls(**data) for data in IntercomAPI.request("GET", cls.endpoint)]

    def delete(self):
        IntercomAPI.request("DELETE", "{}/{}".format(self.endpoint, self.id))
