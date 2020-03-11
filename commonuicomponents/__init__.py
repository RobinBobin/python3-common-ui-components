from .smartwidget import SmartWidget
from tkinter.ttk import Button, Frame, Label, LabelFrame, Style

def _styleName(base, name = None):
   return _styleName(base, base.__name__) if name == None else f"T{name}.T{base.__name__}"

_style = Style()

_containerCommon = {
   "grid": {
      "padx": [20, 0],
      "pady": [20, 0],
      "childPadx": [20, 0],
      "childPady": [20, 0]
   }
}

# = Container = #
_style.configure(_styleName(Frame, "Container"), **_containerCommon)

# = LabeledContainer = #
_style.configure(_styleName(LabelFrame, "LabeledContainer"), **_containerCommon)

_smartwidgets = [[t.__name__, t] for t in [Button, Label]]

_smartwidgets.extend([
   ["Container", Frame],
   ["LabeledContainer", LabelFrame]
])

for name, base in _smartwidgets:
   globals()[name] = type(name, (SmartWidget, base), {"STYLE": _styleName(base, name)})
