from pipeline.basePipeline import BasePipeline
from moviepy.editor import VideoClip
from moviepy.video.fx.crop import crop
import inquirer as iq

from validators.validateNumberInput import validateNumberInput


class ZoomPipeline(BasePipeline):
    def __init__(self, percent=10):
        self.zoomPercent = percent

    def Process(self, clip: VideoClip) -> VideoClip:
        zoomPercentModifier = 1 - (self.zoomPercent / 100)
        return clip.fx(
            crop,
            x_center=clip.w / 2,
            y_center=clip.h / 2,
            width=clip.w * zoomPercentModifier,
            height=clip.h * zoomPercentModifier,
        )

    def CollectRequiredInformation(self):
        answers = iq.prompt(
            [
                iq.Text(
                    "percent",
                    self.FormatQuestion(
                        "How much percent you want to zoom in? (0-100)"
                    ),
                    default="10",
                    validate=validateNumberInput(1, 99),
                )
            ]
        )

        self.zoomPercent = int(answers["percent"])
        print(self.zoomPercent)
