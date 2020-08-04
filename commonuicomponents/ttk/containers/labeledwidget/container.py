from .basecontainer import inflateChildren
from .. import Container

class LabeledWidgetContainer(Container):
   def _inflateChildren(self):
      inflateChildren(self)
      
      super()._inflateChildren()
