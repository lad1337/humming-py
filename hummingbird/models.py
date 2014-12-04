

class BaseModel(object):

    _repr_fields = []

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

    def __repr__(self):
        if not self._repr_fields:
            return super(BaseModel, self).__repr__()
        return "{}: {}".format(
            self.__class__.__name__, ("{}-" * len(self._repr_fields)).format(
                *[getattr(self, key) for key in self._repr_fields]
        )[:-1])

class SearchResult(BaseModel):

    @property
    def full(self):
        return self._client.anime(self.id)

class Anime(BaseModel):

    _repr_fields = ["title"]

    @property
    def title(self, lang=None):
        if lang is None:
            lang = "english"
        return self.titles[lang]

    def __getattr__(self, item):
        try:
            return self.raw_data["anime"][item]
        except KeyError:
            return super(Anime, self).__getattr__(item)

    @property
    def episodes(self):
        if "linked" not in self.raw_data:
            raise NotImplemented(
                "API V1 does not have episodes."
                "Register and app and set v2_token")
        episodes = [Episode(self._client, self, ep)
                    for ep in self.raw_data["linked"]["episodes"]]
        return sorted(episodes)

class Episode(BaseModel):

    _repr_fields = ["season_number", "number"]

    def __init__(self, client, anime, raw_data):
        self.anime = anime
        super(Episode, self).__init__(client, raw_data)

    def __eq__(self, other):
        return super(Episode, self).__eq__(other) and self.anime == other.anime

    def __cmp__(self, other):
        if self.season_number < other.season_number:
            return -1
        elif self.season_number > other.season_number:
            return 1
        else:
            if self.number < other.number:
                return -1
            return 1


# import hummingbird; c = hummingbird.Client(v2_token="9b737c2f9722bffbc39d"); d = c.search("space dandy")[0].full
