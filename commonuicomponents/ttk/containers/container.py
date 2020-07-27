from tkinter.ttk import Frame
from . import BaseContainer

class Container(BaseContainer, Frame):
   _DEFAULT_STYLE = BaseContainer._defaultStyle()
   
   def __init__(self, master, **kw):
      BaseContainer.__init__(self, master, padAllChildren = False, **kw)
