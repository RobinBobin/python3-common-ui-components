class BaseStorage:
   __storage = dict()
   
   def __init__(self):
      version = self.__class__.__name__[7:].replace("_", ".")
      
      if version in BaseStorage.__storage:
         raise ValueError()
      
      BaseStorage.__storage[version] = self
   
   @staticmethod
   def get(version):
      return BaseStorage.__storage[version]
   
   @staticmethod
   def init():
      for storage in BaseStorage.__subclasses__():
         storage()
