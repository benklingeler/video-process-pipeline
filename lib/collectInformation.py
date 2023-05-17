from os import listdir, mkdir, path, rmdir
from pathlib import Path
from shutil import rmtree

import inquirer as iq
from adapter.baseAdapter import BaseAdapter
from adapter.directoryAdapter import DirectoryAdapter
from adapter.redditAdapter import RedditAdapter
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

    files: list[str] = getFilesForConversion()
    steps: list[BasePipeline] = getStepsForConversion()

    return (files, steps)


def getFilesForConversion():
    answers = iq.prompt(
        [
            iq.List(
                "adapter",
                message="Select the source of your files",
                choices=["Directory", "Reddit"],
                default=["Directory"],
            )
        ]
    )
    source = answers["adapter"]

    adapter = None

    if source == "Directory":
        adapter = DirectoryAdapter()

    if source == "Reddit":
        adapter = RedditAdapter()

    return adapter.Process()


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
