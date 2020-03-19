import wtforms
from wtforms import SelectMultipleField


class MultiCheckboxField(SelectMultipleField):
    widget = wtforms.widgets.TableWidget()
    option_widget = wtforms.widgets.CheckboxInput()
