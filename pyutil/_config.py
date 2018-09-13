import os
import yaml
from typing import *


class Macros:
    HOME_DIR = os.getenv("HOME")
    THIS_DIR = os.path.dirname(os.path.realpath(__file__))
    PROJ_DIR = os.path.dirname(THIS_DIR)
    CONFIG_FILE = os.path.join(HOME_DIR, "pyutil_config.json")


def get_config(key: str) -> any:
    try:
        with open(Macros.CONFIG_FILE, "r") as f:
            configs = yaml.load(f)
            return configs[key]
        # end with
    except KeyError as e:
        raise KeyError("Config {} not available in the config file: {}".format(key, str(e)))
    except FileNotFoundError as e:
        return None
    # end try except
