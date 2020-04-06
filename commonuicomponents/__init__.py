from tkinter.ttk import Button, Label
from .containers import container, labeledcontainer
from .labeledscale import LabeledScale
from .smartwidget import SmartWidget

for tkinterBase in [Button, Label]:
   name, clazz = SmartWidget.wrapClass(tkinterBase)
   
   globals()[name] = clazz
