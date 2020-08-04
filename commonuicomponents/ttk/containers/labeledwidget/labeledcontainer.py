from .basecontainer import inflateChildren
from .. import LabeledContainer

class LabeledWidgetLabeledContainer(LabeledContainer):
   def _inflateChildren(self):
      inflateChildren(self)
      
      super()._inflateChildren()
