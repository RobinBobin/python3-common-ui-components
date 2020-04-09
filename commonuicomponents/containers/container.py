from tkinter.ttk import Frame
from .basecontainer import BaseContainer
from .. import CommonUIComponents

class Container(BaseContainer, Frame):
   _DEFAULT_STYLE = BaseContainer._defaultStyle({
      "background": "lightgreen"
    } if CommonUIComponents.DEBUG else None)
   
   def __init__(self, master = None, **kw):
      BaseContainer.__init__(self, master, padAllChildren = False, **kw)
