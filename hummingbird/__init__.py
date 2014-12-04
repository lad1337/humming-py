from __future__ import absolute_import
from requests import request
from .models import *

URL_V1 = "https://hummingbird.me/api/v1"
URL_V2 = "https://hummingbird.me/api/v2"


class Client(object):

    def __init__(self, user_name=None, password=None, v2_token=None):
        self._v2_token = v2_token
        self._user_name = user_name
        self._password = password

        self._user_auth_token = None

    @property
    def user_auth_token(self):
        if self._user_auth_token:
            return self._user_auth_token
        if self._user_name and self._password:
            self._user_auth_token = self._request(
                URL_V1,
                "post",
                "/users/authenticate",
                data={"username": self._user_name, "password": self._password}
            )
        return None

    def _request(self, url, method, path, params=None, data=None, set_auth=False):
        headers = {}
        if self._v2_token:
            headers["X-Client-Id"] = self._v2_token

        if set_auth and self.user_auth_token:
            data["user_auth_token"] = self.user_auth_token

        response = request(
            method,
            "{}{}".format(url, path),
            params=params,
            data=data,
            headers=headers
        )
        return response.json()

    def search(self, term):
        return [
            SearchResult(self, r)
            for r in self._request(
                URL_V1, "get", "/search/anime", {"query": term})
        ]

    def anime(self, id):
        """Get an Anime object.

        id: hummingbird internal id or myanimelist:<MAL-ID>

        """
        url = URL_V1
        if self._v2_token:
            url = URL_V2

        return Anime(self, self._request(url, "get", "/anime/{}".format(id)))
