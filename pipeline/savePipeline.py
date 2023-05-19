from os import mkdir
from pathlib import Path
from shutil import rmtree

import inquirer as iq
import proglog
from lib.configuration import getConfiguration, saveConfiguration
from moviepy.editor import VideoClip
from validators.validateNumberInput import validateNumberInput
from validators.validatePath import validatePath

from pipeline.basePipeline import BasePipeline


class SavePipeline(BasePipeline):
    """
    Video processing pipeline for saving video clips to a specified destination.

    This pipeline extends the BasePipeline class and provides methods to process
    and save video clips.
    """

    def Process(self, clip: VideoClip, sourceFilepath: str) -> VideoClip:
        destFilePath = f"{self.destinationFolderPath}\\{Path(sourceFilepath).stem}.mp4"

        clip.write_videofile(
            destFilePath,
            codec="libx264",
            verbose=False,
            threads=4,
            bitrate=f"{self.videoQuality}000k",
            logger=proglog.TqdmProgressBarLogger(print_messages=False),
        )
        clip.close()

        return clip

    def CollectRequiredInformation(self):
        lastUsedDestination = getConfiguration()["lastUsedDestination"]
        answers = iq.prompt(
            [
                iq.Text(
                    "destPath",
                    self.FormatQuestion("Save destination"),
                    default=(
                        lastUsedDestination if len(lastUsedDestination) > 0 else None
                    ),
                ),
                iq.List(
                    "keepOldFiles",
                    message=self.FormatQuestion("Delete old results?"),
                    choices=["no", "yes, delete"],
                ),
                iq.Text(
                    "quality",
                    self.FormatQuestion("Video quality (1-10)"),
                    default="5",
                    validate=validateNumberInput(1, 10),
                ),
                iq.List(
                    "GIF-Converter",
                    message=self.FormatQuestion("Convert to GIF?"),
                    choices=["yes", "no"],
                ),
            ]
        )
        self.destinationFolderPath = answers["destPath"]
        self.destinationFolderExists = validatePath(None, self.destinationFolderPath)
        self.keepOldFiles = answers["keepOldFiles"] == "no"
        self.videoQuality = answers["quality"]

        getConfiguration()["lastUsedDestination"] = self.destinationFolderPath
        saveConfiguration()

    def PreparePipeline(self):
        if self.keepOldFiles is False and self.destinationFolderExists:
            rmtree(self.destinationFolderPath)

        mkdir(self.destinationFolderPath)
