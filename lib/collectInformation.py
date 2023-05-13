from os import listdir, mkdir, rmdir, path
from pathlib import Path
from shutil import rmtree

from rich.console import Console
import inquirer as iq
from lib.configuration import getConfiguration, saveConfiguration
from pipeline.zoomPipeline import ZoomPipeline
from validators.validateFileType import validateFileType

from validators.validatePath import validatePath


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

    (destPath, isDestAlreadyCreated) = getDestinationPath(sourcePath)

    if isDestAlreadyCreated:
        shouldKeepFiles = keepOldFiles()

        # Delete old dest folder, if user decides not to keep the old files
        if shouldKeepFiles is False:
            rmtree(destPath)

        mkdir(destPath)

    files = lookupFilesInSource(sourcePath)
    exitIfNotFilesAreThere(files)

    filteredFiles = filterOutUnwantedFiles(files)
    exitIfNotFilesAreThere(filteredFiles)

    userSelectedFiles = getSelectedFilesByUser(filteredFiles)
    exitIfNotFilesAreThere(userSelectedFiles)

    steps = getStepsForConversion()

    return (userSelectedFiles, steps, destPath)


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


def getDestinationPath(sourcePath):
    """
    Prompts the user to enter the destination path for the converted files.

    Args:
        sourcePath (str): The path of the source directory.

    Returns:
        tuple: A tuple containing the destination path and a flag indicating if the destination directory already exists.
    """

    lastUsedDestination = getConfiguration()["lastUsedDestination"]
    questions = [
        iq.Text(
            "destPath",
            "Where should we save the results?",
            default=(
                lastUsedDestination
                if len(lastUsedDestination) > 0
                else f"{sourcePath}\\results"
            ),
        )
    ]
    answers = iq.prompt(questions)
    destPath = answers["destPath"]
    return (destPath, validatePath(True, destPath))


def keepOldFiles():
    """
    Prompts the user to choose whether to keep or delete existing files in the target directory.

    Returns:
        bool: True if the user chooses to keep old files, False otherwise.
    """

    questions = [
        iq.List(
            "keepOldFiles",
            message="Do you want to delete existing files in the target directory?",
            choices=["no, keep old results", "yes, delete"],
        )
    ]
    answer = iq.prompt(questions)
    return answer["keepOldFiles"] == "no, keep old results"


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
            choices=["Zoom into clip", "Add watermark"],
            validate=lambda _, results: len(results) > 0,
        )
    ]
    answers = iq.prompt(questions)
    steps = []
    for answer in answers["steps"]:
        if answer == "Zoom into clip":
            steps.append(ZoomPipeline())
        # if answer == "Add watermark":
        #     steps.append("watermark")
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
