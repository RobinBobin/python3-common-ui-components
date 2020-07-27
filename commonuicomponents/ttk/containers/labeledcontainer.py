from tkinter.ttk import LabelFrame
from . import BaseContainer

class LabeledContainer(BaseContainer, LabelFrame):
   _DEFAULT_STYLE = BaseContainer._defaultStyle()
