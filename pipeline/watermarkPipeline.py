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

            if answers["watermarkPosition"] == "Left Top":
                logo = (
                    mp.ImageClip(self.watermarkPath)
                    .set_duration(clip.duration)
                    .resize(height=clip.h * resizePercentModifier)
                    .resize(width=clip.w * resizePercentModifier)
                    .margin(left=8, top=8, opacity=0)
                    .set_pos(("left", "top"))
                )
                clips.append(logo)

            if answers["watermarkPosition"] == "Left Middle":
                logo = (
                    mp.ImageClip(self.watermarkPath)
                    .set_duration(clip.duration)
                    .resize(height=clip.h * resizePercentModifier)
                    .resize(width=clip.w * resizePercentModifier)
                    .margin(left=8, opacity=0)
                    .set_pos(("left", "middle"))
                )
                clips.append(logo)

            if answers["watermarkPosition"] == "Left Bottom":
                logo = (
                    mp.ImageClip(self.watermarkPath)
                    .set_duration(clip.duration)
                    .resize(height=clip.h * resizePercentModifier)
                    .resize(width=clip.w * resizePercentModifier)
                    .margin(left=8, bottom=8, opacity=0)
                    .set_pos(("left", "bottom"))
                )
                clips.append(logo)

            if answers["watermarkPosition"] == "Center Top":
                logo = (
                    mp.ImageClip(self.watermarkPath)
                    .set_duration(clip.duration)
                    .resize(height=clip.h * resizePercentModifier)
                    .resize(width=clip.w * resizePercentModifier)
                    .margin(top=8, opacity=0)
                    .set_pos(("top"))
                )
                clips.append(logo)

            if answers["watermarkPosition"] == "Center Middle":
                logo = (
                    mp.ImageClip(self.watermarkPath)
                    .set_duration(clip.duration)
                    .resize(height=clip.h * resizePercentModifier)
                    .resize(width=clip.w * resizePercentModifier)
                    .margin(opacity=0)
                    .set_pos(("center"))
                )
                clips.append(logo)

            if answers["watermarkPosition"] == "Center Bottom":
                logo = (
                    mp.ImageClip(self.watermarkPath)
                    .set_duration(clip.duration)
                    .resize(height=clip.h * resizePercentModifier)
                    .resize(width=clip.w * resizePercentModifier)
                    .margin(bottom=8, opacity=0)
                    .set_pos(("bottom"))
                )
                clips.append(logo)

            if answers["watermarkPosition"] == "Right Top":
                logo = (
                    mp.ImageClip(self.watermarkPath)
                    .set_duration(clip.duration)
                    .resize(height=clip.h * resizePercentModifier)
                    .resize(width=clip.w * resizePercentModifier)
                    .margin(right=8, top=8, opacity=0)
                    .set_pos(("right", "top"))
                )
                clips.append(logo)

            if answers["watermarkPosition"] == "Right Middle":
                logo = (
                    mp.ImageClip(self.watermarkPath)
                    .set_duration(clip.duration)
                    .resize(height=clip.h * resizePercentModifier)
                    .resize(width=clip.w * resizePercentModifier)
                    .margin(right=8, opacity=0)
                    .set_pos(("right"))
                )
                clips.append(logo)

            if answers["watermarkPosition"] == "Right Bottom":
                logo = (
                    mp.ImageClip(self.watermarkPath)
                    .set_duration(clip.duration)
                    .resize(height=clip.h * resizePercentModifier)
                    .resize(width=clip.w * resizePercentModifier)
                    .margin(right=8, bottom=8, opacity=0)
                    .set_pos(("right", "bottom"))
                )
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

                if positionCounter == 0:
                    watermark = watermark.margin(
                        right=8, bottom=8, opacity=0
                    ).set_position(("right", "bottom"))
                elif positionCounter == 1:
                    watermark = watermark.margin(left=8, top=8, opacity=0).set_position(
                        ("left", "top")
                    )
                elif positionCounter == 2:
                    watermark = watermark.margin(right=8, opacity=0).set_position(
                        ("right", "center")
                    )

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

        self.watermarkPath = answers["watermark"]
        getConfiguration()["lastUsedWatermarkPath"] = self.watermarkPath
        saveConfiguration()
        self.watermarkPercentage = int(answers["percentage"])
        self.watermarkTypeIsNormal = answers["watermarkType"] == "Normal watermark"
        self.watermarkPosition = answers["watermarkPosition"] == "Right Bottom"

    # def SettingsPipeline(self, t):
    #     if self.watermarkTypeIsNormal is False:
    #         resizePercentModifier = self.watermarkPercentage / 100

    #         watermark_duration = 3

    #         positions = [
    #             (self.w - t * (self.w / 3), self.h - t * (self.h / 3)),
    #             (t * (self.w / 6), t * (self.h / 6)),
    #             (self.w - t * (self.w / 9), self.h / 2),
    #         ]

    #         position_index = int(t // watermark_duration) % len(positions)
    #         x, y = positions[position_index]

    #         watermark = watermark(self, watermark_duration)
    #         watermark = watermark.set_position((x, y)).set_duration(watermark_duration)

    #         final_clip = self.set_opacity(0).set_duration(self.duration)

    #         for t in range(int(self.duration // watermark_duration)):
    #             watermark_clip = SettingsPipeline(t * watermark_duration)
    #             final_clip = final_clip.overlay(watermark_clip)

    #         return watermark_clip
