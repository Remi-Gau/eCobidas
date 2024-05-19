"""Build elements from data into MarkDown format for the specification text.

Functions decorated in "define_env()" are callable throughout the
specification and are run/rendered with the mkdocs plugin "macros".
"""

import sys
from pathlib import Path

from ecobidas import macros

code_path = Path(__file__).parent
sys.path.append(code_path)


def define_env(env):
    """Define variables, macros and filters for the mkdocs-macros plugin.

    Parameters
    ----------
    env : :obj:`macros.plugin.MacrosPlugin`
        An object in which to inject macros, variables, and filters.

    Notes
    -----
    "variables" are the dictionary that contains the environment variables
    "macro" is a decorator function, to declare a macro.

    Macro aliases must start with "MACROS___"
    """
    env.macro(macros.table_apps, "MACROS___table_apps")
    env.macro(macros.table_preset_responses, "MACROS___table_preset_responses")
    env.macro(macros.table_spreadsheets, "MACROS___table_spreadsheets")
    env.macro(macros.table_data_dictionary, "MACROS___table_data_dictionary")
