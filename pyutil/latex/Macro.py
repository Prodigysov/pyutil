from typing import *


class Macro:

    @classmethod
    def define(cls, key: str, value_fmt: Union[str, Any], *values, **values_items) -> str:
        key = key.replace("_", "-")

        if len(values) != 0 or len(values_items) != 0:
            value = value_fmt.format(*values, **values_items)
        else:
            value = str(value_fmt)
        # end if

        latex_line = "\\DefMacro{{{key}}}{{{value}}}".format(key=key, value=value)
        return latex_line

    @classmethod
    def use(cls, key: str) -> str:
        key = key.replace("_", "-")

        latex_line = "\\UseMacro{{{key}}}".format(key=key)
        return latex_line
