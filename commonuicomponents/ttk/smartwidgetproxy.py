class SmartWidgetProxy:
   def __init__(self, smartWidget):
      self.__value = smartWidget
   
   @property
   def value(self):
      return self.__value
   
   def __getitem__(self, key):
      return self.__value._baseContainerChildren[key]
   
   def __iter__(self):
      return iter(self.__value._baseContainerChildren.items())
