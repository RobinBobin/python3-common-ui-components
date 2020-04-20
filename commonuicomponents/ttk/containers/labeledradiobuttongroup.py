from .labeledcontainer import LabeledContainer

class LabeledRadioButtonGroup(LabeledContainer):
   def __init__(self, master = None, **kw):
      LabeledContainer._setVariable(kw, "IntVar")
      
      super().__init__(master, **kw)
      
      self._initValueAndTraceAdd()
   
   def _inflateChildren(self):
      for child in self._baseContainerChildren:
         if "type" not in child:
            child["type"] = "Radiobutton"
      
      LabeledContainer._inflateChildren(self)
      
      for index, proxy in enumerate(self._baseContainerChildren.values()):
         proxy.value.configure(value = index, variable = self.value)
