from tkinter.ttk import Frame
from .basecontainer import BaseContainer

class Container(BaseContainer, Frame):
   __DEFAULT_STYLE = BaseContainer._defaultStyle()

Container.registerClass(Container)
