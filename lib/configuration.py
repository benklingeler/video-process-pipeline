from os import path
from pathlib import Path
import ujson

configuration = {}
# The configuration struct stores the current configuration settings.
# It is a dictionary that contains key-value pairs representing different configuration options.
# The structure of the configuration is as follows:
# {
#     "lastUsedSource": <str>,
#     "lastUsedDestination": <str>
# }
#
# - "lastUsedSource" represents the path of the last used source directory.
# - "lastUsedDestination" represents the path of the last used destination directory.
#
# The configuration variable is used to load and save configuration settings for the file conversion process.
# It is a global variable that can be accessed and modified by various functions within the program.


def loadConfiguration():
    """
    Loads the configuration from the configuration file.

    If the configuration file does not exist, a new configuration file is created with default values.
    The loaded configuration is stored in the global variable 'configuration'.
    """

    global configuration

    if Path(getConfigurationFilePath()).exists() is False:
        with open(getConfigurationFilePath(), "w+") as configFile:
            ujson.dump(getDefaultConfiguration(), configFile)

    with open(getConfigurationFilePath(), "r") as configFile:
        configuration = ujson.load(configFile)

    return True


def saveConfiguration():
    """
    Saves the configuration to the configuration file.

    The configuration is retrieved from the global variable 'configuration'.
    """

    global configuration
    with open(getConfigurationFilePath(), "w") as configFile:
        ujson.dump(configuration, configFile)

    return True


def getConfiguration():
    """
    Retrieves the current configuration.

    Returns:
        dict: The current configuration.
    """

    global configuration
    return configuration


def getUserDocumentsDirectory():
    """
    Returns the path of the user's documents directory.

    Creates the directory if it does not exist.

    Returns:
        str: The path of the user's documents directory.
    """

    pathString = path.expanduser("~/Documents/video-process-pipeline")
    pathObject = Path(pathString)
    if pathObject.exists() is False:
        pathObject.mkdir()
    return pathString


def getConfigurationFilePath():
    """
    Returns the file path of the configuration file.

    Returns:
        str: The file path of the configuration file.
    """

    return f"{getUserDocumentsDirectory()}/configuration.json"


def getDefaultConfiguration():
    """
    Returns the default configuration.

    Returns:
        dict: The default configuration.
    """

    return {"lastUsedSource": "", "lastUsedDestination": ""}
