from os import listdir, rmdir
from pathlib import Path

from rich.console import Console
import inquirer as iq
from validators.validateFileType import validateFileType

from validators.validatePath import validatePath 

def collectInformation():
  sourcePath = getPathOfSourceFiles()
  (destPath, isDestAlreadyCreated) = getDestinationPath(sourcePath)
  
  if isDestAlreadyCreated:
    shouldKeepFiles = keepOldFiles()

    # Delete old dest folder, if user decides not to keep the old files
    if shouldKeepFiles is False:
      rmdir(destPath)

  files = lookupFilesInSource(sourcePath)
  exitIfNotFilesAreThere(files)

  filteredFiles = filterOutUnwantedFiles(files)
  exitIfNotFilesAreThere(filteredFiles)

  userSelectedFiles = getSelectedFilesByUser(filteredFiles)
  exitIfNotFilesAreThere(userSelectedFiles)

  steps = getStepsForConversion()

  return (userSelectedFiles, steps, destPath)

def getPathOfSourceFiles():
  # TODO: Delete default value later
  questions = [
    iq.Text('sourcePath', 'What is your source directory path?', default="C:\\Users\\benkl\\Videos\\please_convert_me", validate=validatePath)
  ]
  answers = iq.prompt(questions)
  return answers["sourcePath"]

def getDestinationPath(sourcePath):
  questions = [
    iq.Text('destPath', 'Where should we save the results?', default=f"{sourcePath}\\results")
  ]
  answers = iq.prompt(questions)
  destPath = answers["destPath"]
  return (destPath, validatePath(True, destPath))

def keepOldFiles():
  questions = [
      iq.List(
        'keepOldFiles',
        message="Do you want to delete existing files in the target directory?",
        choices=["no, keep old results", "yes, delete"]
      )
  ]
  answer = iq.prompt(questions)
  return answer["keepOldFiles"] == "no, keep old results"

def lookupFilesInSource(sourcePath):
  files = [f"{sourcePath}\\{file}" for file in listdir(sourcePath) if Path(f"{sourcePath}\\{file}").is_file()]
  return files

def filterOutUnwantedFiles(files):
  questions = [
    iq.Checkbox(
    'allowedFileTypes',
    message='Select the allowed file types',
    choices=['Images', 'Videos'],
    default=['Images', 'Videos']
    )
  ]
  answers = iq.prompt(questions)

  filteredFiles = []
  for file in files:
    (isImage, isVideo) = validateFileType(file)

    if isImage and 'Images' in answers["allowedFileTypes"]:
      filteredFiles.append(file)

    if isVideo and 'Videos' in answers["allowedFileTypes"]:
      filteredFiles.append(file)

  return filteredFiles

def getSelectedFilesByUser(files):
  questions = [
    iq.Checkbox(
    'selectedFiles',
    message='Choose your files for conversion',
    choices=files,
    default=files
    )
  ]
  answers = iq.prompt(questions)
  return answers["selectedFiles"]

def getStepsForConversion():
  questions = [
    iq.Checkbox(
    'steps',
    message='Steps take in conversion',
    choices=['Zoom into video/image (10% centered)', 'Add watermark'],
    validate=lambda _, results: len(results) > 0
    )
  ]
  answers = iq.prompt(questions)
  steps = []
  for answer in answers["steps"]:
    if answer == 'Zoom into video/image (10% centered)':
      steps.append("zoom_10")
    if answer == 'Add watermark':
      steps.append("watermark")
  return steps

def exitIfNotFilesAreThere(files):
  if len(files) == 0:
    console = Console()
    console.print(':warning: There are no files left.', style="bold red")
    exit(0)