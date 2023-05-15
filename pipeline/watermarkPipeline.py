import moviepy.editor as mp
from moviepy.editor import VideoClip
from pathlib import Path
import inquirer as iq
import os.path as op
from lib.configuration import getConfiguration, saveConfiguration

from pipeline.basePipeline import BasePipeline
from validators.validateWatermarkPath import validateWatermarkPath
from validators.validateNumberInput import validateNumberInput


class WatermarkPipeline(BasePipeline):
    def Process(self, clip: VideoClip) -> VideoClip:
        resizePercentModifier = self.watermarkPercentage / 100
        logo = (
            mp.ImageClip(self.watermarkPath)
            .set_duration(clip.duration)
            .resize(height=clip.h * resizePercentModifier)
            .resize(width=clip.w * resizePercentModifier)
            .margin(left=8, bottom=8, opacity=0)
            .set_pos(("left", "bottom"))
        )

        clipWithLogo = mp.CompositeVideoClip([clip, logo])

        return clipWithLogo

    def CollectRequiredInformation(self):
        lastUsedWatermarkPath = getConfiguration()["lastUsedWatermarkPath"]
        answers = iq.prompt(
            [
                iq.Text(
                    "watermark",
                    self.FormatQuestion(
                        "Please provide the path of your watermark file"
                    ),
                    default=lastUsedWatermarkPath,
                    validate=validateWatermarkPath,
                ),
                iq.Text(
                    "percentage",
                    self.FormatQuestion(
                        "How much percent of the video file show be used for the size of the watermark"
                    ),
                    default="10",
                    validate=validateNumberInput(1, 99),
                ),
            ]
        )

        self.watermarkPath = answers["watermark"]
        getConfiguration()["lastUsedWatermarkPath"] = self.watermarkPath
        saveConfiguration()
        self.watermarkPercentage = int(answers["percentage"])
