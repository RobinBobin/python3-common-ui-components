from tkinter.ttk import Frame
from .basecontainer import BaseContainer

class Container(BaseContainer, Frame):
   _DEFAULT_STYLE = BaseContainer._defaultStyle()

Container.registerClass(Container)
