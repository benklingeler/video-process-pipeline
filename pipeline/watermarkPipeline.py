import os.path as op
from pathlib import Path
import random

import inquirer as iq
import moviepy.editor as mp
from lib.configuration import getConfiguration, saveConfiguration
from moviepy.editor import VideoClip
from validators.validateNumberInput import validateNumberInput
from validators.validateWatermarkPath import validateWatermarkPath

from pipeline.basePipeline import BasePipeline


class WatermarkPipeline(BasePipeline):
    def Process(self, clip: VideoClip) -> VideoClip:
        resizePercentModifier = self.watermarkPercentage / 100

        clips = [clip]

        if self.watermarkTypeIsNormal:
            answers = iq.prompt(
                [
                    iq.List(
                        "watermarkPosition",
                        message=self.FormatQuestion(
                            "Where do you want to place the watermark?"
                        ),
                        choices=[
                            "Left Top",
                            "Left Middle",
                            "Left Bottom",
                            "Center Top",
                            "Center Middle",
                            "Center Bottom",
                            "Right Top",
                            "Right Middle",
                            "Right Bottom",
                        ],
                    ),
                ]
            )

            imageClip = (
                mp.ImageClip(self.watermarkPath)
                .set_duration(clip.duration)
                .resize(height=clip.h * resizePercentModifier)
                .resize(width=clip.w * resizePercentModifier)
            )
            logo = self.ApplyPositionOnClip(imageClip, answers["watermarkPosition"])
            clips.append(logo)

        else:
            positionCounter = 0

            watermarkDuration = 3
            startTime = 0
            clipDuration = clip.duration

            while clipDuration > 0:
                applyingDuration = (
                    watermarkDuration
                    if clipDuration >= watermarkDuration
                    else clipDuration
                )

                watermark = (
                    mp.ImageClip(self.watermarkPath)
                    .set_duration(applyingDuration)
                    .resize(height=clip.h * resizePercentModifier)
                    .resize(width=clip.w * resizePercentModifier)
                )

                possiblePositions = [
                    "Left Top",
                    "Left Middle",
                    "Left Bottom",
                    "Center Top",
                    "Center Middle",
                    "Center Bottom",
                    "Right Top",
                    "Right Middle",
                    "Right Bottom",
                ]
                watermark = self.ApplyPositionOnClip(
                    watermark,
                    possiblePositions[random.randint(0, len(possiblePositions) - 1)],
                )

                # if positionCounter == 0:
                #     watermark = watermark.margin(
                #         right=8, bottom=8, opacity=0
                #     ).set_position(("right", "bottom"))
                # elif positionCounter == 1:
                #     watermark = watermark.margin(left=8, top=8, opacity=0).set_position(
                #         ("left", "top")
                #     )
                # elif positionCounter == 2:
                #     watermark = watermark.margin(right=8, opacity=0).set_position(
                #         ("right", "center")
                #     )

                clips.append(watermark.set_start(startTime))

                clipDuration = clipDuration - applyingDuration
                startTime = startTime + applyingDuration
                positionCounter = positionCounter + 1 if positionCounter < 2 else 0

        clipWithLogo = mp.CompositeVideoClip(clips)

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
                iq.List(
                    "watermarkType",
                    message=self.FormatQuestion(
                        "Do you want a normal or extra safe watermark?"
                    ),
                    choices=["Normal watermark", "Safe watermark"],
                ),
            ]
        )

        self.watermarkPath = answers["watermark"]
        getConfiguration()["lastUsedWatermarkPath"] = self.watermarkPath
        saveConfiguration()
        self.watermarkPercentage = int(answers["percentage"])
        self.watermarkTypeIsNormal = answers["watermarkType"] == "Normal watermark"

    def ApplyPositionOnClip(self, clip, position):
        if position == "Left Top":
            return clip.margin(left=8, top=8, opacity=0).set_pos(("left", "top"))
        if position == "Left Middle":
            return clip.margin(left=8, opacity=0).set_pos(("left"))
        if position == "Left Bottom":
            return clip.margin(left=8, bottom=8, opacity=0).set_pos(("left", "bottom"))
        if position == "Center Top":
            return clip.margin(top=8, opacity=0).set_pos(("top"))
        if position == "Center Middle":
            return clip.margin(opacity=0).set_pos(("center"))
        if position == "Center Bottom":
            return clip.margin(bottom=8, opacity=0).set_pos(("bottom"))
        if position == "Right Top":
            return clip.margin(right=8, top=8, opacity=0).set_pos(("right", "top"))
        if position == "Right Middle":
            return clip.margin(right=8, opacity=0).set_pos(("right"))
        if position == "Right Bottom":
            return clip.margin(right=8, bottom=8, opacity=0).set_pos(
                ("right", "bottom")
            )
