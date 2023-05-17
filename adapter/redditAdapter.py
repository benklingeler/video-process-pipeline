from os import listdir
from pathlib import Path

import inquirer as iq
from lib.configuration import getConfiguration, saveConfiguration
from rich.console import Console
from validators.validateFileType import validateFileType
from validators.validatePath import validatePath

from adapter.baseAdapter import BaseAdapter


class RedditAdapter(BaseAdapter):
    def Process(self) -> list[str]:
        pass
