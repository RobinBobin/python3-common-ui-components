from . import LabeledContainer

class LabeledRadioButtonGroup(LabeledContainer):
   def __init__(self, master, **kw):
      LabeledContainer._setVariable(kw, "IntVar")
      
      super().__init__(master, **kw)
      
      self._initValueAndTraceAdd()
   
   def getValueText(self):
      return self.getSmartWidget((self.getValue(), 0))["text"]
   
   def _inflateChildren(self):
      for child in self._baseContainerChildren:
         if "type" not in child:
            child["type"] = "Radiobutton"
      
      LabeledContainer._inflateChildren(self)
      
      for index, widget in enumerate(self._baseContainerChildren.values()):
         widget.configure(value = index, variable = self.getRawValue())
