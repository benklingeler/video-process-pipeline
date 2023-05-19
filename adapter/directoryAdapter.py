from os import listdir
from pathlib import Path

import inquirer as iq
from lib.configuration import getConfiguration, saveConfiguration
from rich.console import Console
from validators.validateFileType import validateFileType
from validators.validatePath import validatePath

from adapter.baseAdapter import BaseAdapter


class DirectoryAdapter(BaseAdapter):
    def Process(self) -> list[str]:

        sourcePath = self.getPathOfSourceFiles()

        # Save the used sourcePath into the configuration
        getConfiguration()["lastUsedSource"] = sourcePath
        saveConfiguration()

        files = self.lookupFilesInSource(sourcePath)
        self.exitIfNotFilesAreThere(files)

        filteredFiles = self.filterOutUnwantedFiles(files)
        self.exitIfNotFilesAreThere(filteredFiles)

        userSelectedFiles: list[str] = self.getSelectedFilesByUser(filteredFiles)
        self.exitIfNotFilesAreThere(userSelectedFiles)

        return userSelectedFiles

    def getPathOfSourceFiles(self):
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

    def lookupFilesInSource(self, sourcePath):
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

    def filterOutUnwantedFiles(self, files):
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

    def getSelectedFilesByUser(self, files):
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

    def exitIfNotFilesAreThere(self, files):
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
