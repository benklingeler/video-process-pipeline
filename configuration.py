from os import path
from pathlib import Path
import ujson

configuration = {}

def loadConfiguration():
  global configuration
  
  if Path(getConfigurationFilePath()).exists() is False:
    with open(getConfigurationFilePath(), 'w+') as configFile:
      ujson.dump(getDefaultConfiguration(), configFile)

  with open(getConfigurationFilePath(), 'r') as configFile:
    configuration = ujson.load(configFile)

def saveConfiguration():
  global configuration
  with open(getConfigurationFilePath(), 'w') as configFile:
    ujson.dump(configuration, configFile)

def getConfiguration():
  global configuration
  return configuration

def getUserDocumentsDirectory():
  pathString = path.expanduser("~/Documents/video-process-pipeline")
  pathObject = Path(pathString)
  if pathObject.exists() is False:
    pathObject.mkdir()
  return pathString

def getConfigurationFilePath():
  return f"{getUserDocumentsDirectory()}/configuration.json"

def getDefaultConfiguration():
  return {
    "lastUsedSource": "",
    "lastUsedDestination": ""
  }