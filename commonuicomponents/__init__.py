from tkinter.ttk import Button, Label
from .smartwidget import SmartWidget

for tkinterBase in [Button, Label]:
   SmartWidget.wrapClass(tkinterBase)
