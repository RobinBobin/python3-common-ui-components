from commonutils import StaticUtils
from ...json import Config
from ...version import __version__

class BaseStorage:
   __storage = dict()
   
   def __init__(self):
      version = self.__class__.__name__[7:].replace("_", ".")
      
      if version in BaseStorage.__storage:
         raise ValueError(version)
      
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
      for domain in valueDomains:
         storage = StaticUtils.setIfAbsentAndGet(storage, f"{domain}={str(topLevelContainer.getSmartWidget(*domain).getValue())}", dict())
      
      for name in (*namePrefix, smartWidgetName):
         storage = StaticUtils.setIfAbsentAndGet(storage, name, dict())
      
      return storage
   
   def processValueDomains(self, kw, namePrefix):
      valueDomains = kw.pop("valueDomains", [])
      
      # pylint: disable = consider-using-enumerate
      for i in range(len(valueDomains)):
         valueDomains[i] = valueDomains[i].split(".")
         
         if not valueDomains[i][0]:
            valueDomains[i][:1] = namePrefix
      
      return valueDomains
   
   @staticmethod
   def get():
      return BaseStorage.__storage[Config["version"]]
   
   @staticmethod
   def init():
      type(f"Storage{__version__}", (BaseStorage, ), dict())
      
      for storage in BaseStorage.__subclasses__():
         storage()
