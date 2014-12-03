

class BaseModel(object):

    def __init__(self, client, raw_data):
        self._client = client
        self.raw_data = raw_data

    def __getattr__(self, item):
        try:
            return self.raw_data[item]
        except KeyError:
            raise AttributeError(
                "{} has no attribute or data under key '{}'".format(
                    self.__class__, item)
            )

    def __eq__(self, other):
        return self.raw_data == other.raw_data

class SearchResult(BaseModel):

    @property
    def full(self):
        return self._client.anime(self.id)

class Anime(BaseModel):

    @property
    def episodes(self):
        if "linked" not in self.raw_data:
            raise NotImplemented(
                "API V1 does not have episodes."
                "Register and app and set v2_token")

        return [Episode(self._client, self, ep)
                for ep in self.raw_data["linked"]["episodes"]]

class Episode(BaseModel):

    def __init__(self, client, anime, raw_data):
        self.anime = anime
        super(Episode, self).__init__(client, raw_data)

    def __eq__(self, other):
        return super(Episode, self).__eq__(other) and self.anime == other.anime
