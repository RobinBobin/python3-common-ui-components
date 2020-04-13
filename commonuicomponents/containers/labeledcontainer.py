from tkinter.ttk import LabelFrame
from .basecontainer import BaseContainer
from .. import CommonUIComponents

class LabeledContainer(BaseContainer, LabelFrame):
   _DEFAULT_STYLE = BaseContainer._defaultStyle()
