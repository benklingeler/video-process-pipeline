from os import listdir, mkdir, path, rmdir
from pathlib import Path
from shutil import rmtree

import inquirer as iq
from pipeline.basePipeline import BasePipeline
from pipeline.savePipeline import SavePipeline
from pipeline.watermarkPipeline import WatermarkPipeline
from pipeline.zoomPipeline import ZoomPipeline
from rich.console import Console
from validators.validateFileType import validateFileType
from validators.validatePath import validatePath

from lib.configuration import getConfiguration, saveConfiguration


def collectInformation():
    """
    Collects information for file conversion.

    Returns:
        tuple: A tuple containing the user-selected files, conversion steps, and destination path.
    """

    sourcePath = getPathOfSourceFiles()

    # Save the used sourcePath into the configuration
    getConfiguration()["lastUsedSource"] = sourcePath
    saveConfiguration()

    # (destPath, isDestAlreadyCreated) = getDestinationPath(sourcePath)

    # if isDestAlreadyCreated:
    #     shouldKeepFiles = keepOldFiles()

    #     # Delete old dest folder, if user decides not to keep the old files
    #     if shouldKeepFiles is False:
    #         rmtree(destPath)

    # mkdir(destPath)

    files = lookupFilesInSource(sourcePath)
    exitIfNotFilesAreThere(files)

    filteredFiles = filterOutUnwantedFiles(files)
    exitIfNotFilesAreThere(filteredFiles)

    userSelectedFiles = getSelectedFilesByUser(filteredFiles)
    exitIfNotFilesAreThere(userSelectedFiles)

    steps: list[BasePipeline] = getStepsForConversion()

    return (userSelectedFiles, steps)


def getPathOfSourceFiles():
    """
    Prompts the user to enter the path of the source directory.

    Returns:
        str: The path of the source directory entered by the user.
    """

    lastUsedSource = getConfiguration()["lastUsedSource"]
    questions = [
        iq.Text(
            "sourcePath",
            "What is your source directory path?",
            default=lastUsedSource,
            validate=validatePath,
        )
    ]
    answers = iq.prompt(questions)
    return answers["sourcePath"]


def lookupFilesInSource(sourcePath):
    """
    Looks up and returns the list of files in the specified source directory.

    Args:
        sourcePath (str): The path of the source directory.

    Returns:
        list: A list of file paths in the source directory.
    """

    files = [
        f"{sourcePath}\\{file}"
        for file in listdir(sourcePath)
        if Path(f"{sourcePath}\\{file}").is_file()
    ]
    return files


def filterOutUnwantedFiles(files):
    """
    Filters out unwanted files based on the user-selected allowed file types.

    Args:
        files (list): A list of file paths to be filtered.

    Returns:
        list: A filtered list of files containing only the allowed file types.
    """

    questions = [
        iq.Checkbox(
            "allowedFileTypes",
            message="Select the allowed file types",
            choices=["Images", "Videos"],
            default=["Images", "Videos"],
        )
    ]
    answers = iq.prompt(questions)

    filteredFiles = []
    for file in files:
        (isImage, isVideo) = validateFileType(file)

        if isImage and "Images" in answers["allowedFileTypes"]:
            filteredFiles.append(file)

        if isVideo and "Videos" in answers["allowedFileTypes"]:
            filteredFiles.append(file)

    return filteredFiles


def getSelectedFilesByUser(files):
    """
    Prompts the user to choose files for conversion from a list of available files.

    Args:
        files (list): A list of available file paths.

    Returns:
        list: A list of user-selected file paths.
    """

    questions = [
        iq.Checkbox(
            "selectedFiles",
            message="Choose your files for conversion",
            choices=files,
            default=files,
        )
    ]
    answers = iq.prompt(questions)
    return answers["selectedFiles"]


def getStepsForConversion():
    """
    Prompts the user to select steps for the conversion process.

    Returns:
        list: A list of selected conversion steps.
    """

    questions = [
        iq.Checkbox(
            "steps",
            message="Steps take in conversion",
            choices=["Zoom into clip", "Add watermark", "Save Files"],
            default=["Save Files"],
            validate=lambda _, results: len(results) > 1,
        )
    ]
    answers = iq.prompt(questions)["steps"]
    steps = []

    if "Zoom into clip" in answers:
        steps.append(ZoomPipeline())
    if "Add watermark" in answers:
        steps.append(WatermarkPipeline())
    if "Save Files" in answers:
        steps.append(SavePipeline())

    return steps


def exitIfNotFilesAreThere(files):
    """
    Exits the program if there are no files available.

    Args:
        files (list): A list of files.

    Raises:
        SystemExit: If the list of files is empty.
    """

    if len(files) == 0:
        console = Console()
        console.print(":warning: There are no files left.", style="bold red")
        exit(0)
