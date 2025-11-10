class SpotifyArtist:
    def __init__(self, id:str, name, genres:list[str]):
        self.id = id
        self.name = name
        self.genres = genres

    @property
    def id(self):
      return getattr(self, "_id", None)

    @id.setter
    def id(self, value):
      self._id = value

    @property
    def name(self):
      return getattr(self, "_name", None)

    @name.setter
    def name(self, value):
      self._name = value

    