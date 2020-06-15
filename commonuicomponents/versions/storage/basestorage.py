from ...json import Config

class BaseStorage:
   __storage = dict()
   
   def __init__(self):
      version = self.__class__.__name__[7:].replace("_", ".")
      
      if version in BaseStorage.__storage:
         raise ValueError()
      
      BaseStorage.__storage[version] = self
   
   # pylint: disable = no-self-use
   def getValueKeyInStorage(self, _smartWidgetClassName):
      return "value"
   
   def getValueStorage(
      self,
      namePrefix,
      smartWidgetName,
      storage,
      topLevelContainer,
      valueDomains):
      pass
   
   def processValueDomains(self, kw, namePrefix):
      valueDomains = kw.pop("valueDomains", [])
      
      # pylint: disable = consider-using-enumerate
      for i in range(len(valueDomains)):
         valueDomains[i] = valueDomains[i].split(".")
         
         if not valueDomains[i][0]:
            valueDomains[i][:1] = namePrefix
      
      return valueDomains
   
   @staticmethod
   def addCurrentVersion():
      type(f"Storage{Config['version']}", (BaseStorage, ), dict())()
   
   @staticmethod
   def get():
      return BaseStorage.__storage[Config["version"]]
   
   @staticmethod
   def init():
      for storage in BaseStorage.__subclasses__():
         storage()
