from tkinter.ttk import LabelFrame
from .basecontainer import BaseContainer

class LabeledContainer(BaseContainer, LabelFrame):
   __DEFAULT_STYLE = BaseContainer._defaultStyle()

LabeledContainer.registerClass(LabeledContainer)
