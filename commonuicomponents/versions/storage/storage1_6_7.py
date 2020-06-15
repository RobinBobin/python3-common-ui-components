from commonutils import StaticUtils
from .basestorage import BaseStorage

class Storage1_6_7(BaseStorage):
   # pylint: disable = no-self-use
   def getValueKeyInStorage(self, smartWidgetClassName):
      return "value" if smartWidgetClassName == "LabeledScale" else ""
   
   def getValueStorage(
      self,
      namePrefix,
      smartWidgetName,
      storage,
      topLevelContainer,
      valueDomains):
      for keys in (("values", ""), *valueDomains):
         for k in keys:
            storage = StaticUtils.setIfAbsentAndGet(storage, k, dict())
      
      for domain in valueDomains:
         storage = StaticUtils.setIfAbsentAndGet(storage, str(topLevelContainer.getSmartWidget(*domain).getValue()), dict())
      
      for name in (*namePrefix, smartWidgetName):
         storage = StaticUtils.setIfAbsentAndGet(storage, name, dict())
      
      return storage
   
   def processValueDomains(self, kw, namePrefix):
      domainPresent = "valueDomain" in kw
      
      if all((domainPresent, "valueDomains" in kw)):
         raise ValueError(f"Only one of {('valueDomain', 'valueDomains')} can be present")
      
      valueDomains = [kw.pop("valueDomain")] if domainPresent else kw.pop("valueDomains", [])
      
      # pylint: disable = consider-using-enumerate
      for i in range(len(valueDomains)):
         if isinstance(valueDomains[i], str) and valueDomains[i]:
            valueDomains[i] = valueDomains[i].split(".")
            
            if not valueDomains[i][0]:
               valueDomains[i][:1] = namePrefix
         
         elif not isinstance(valueDomains[i], list):
            raise ValueError()
      
      return valueDomains
