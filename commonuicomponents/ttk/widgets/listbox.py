from tkinter import Listbox as TListbox
from .smartwidget import SmartWidget

class Listbox(SmartWidget, TListbox):
   def __init__(self, master, **kw):
      SmartWidget._setFont(kw)
      
      SmartWidget.__init__(self, master, **kw)
