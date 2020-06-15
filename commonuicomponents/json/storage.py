from .json import Json

class Storage(Json):
   def __init__(self):
      super().__init__("storage.json", False)
