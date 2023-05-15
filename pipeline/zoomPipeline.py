import inquirer as iq
from moviepy.editor import VideoClip
from moviepy.video.fx.crop import crop
from validators.validateNumberInput import validateNumberInput

from pipeline.basePipeline import BasePipeline


class ZoomPipeline(BasePipeline):
    def Process(self, clip: VideoClip) -> VideoClip:
        zoomPercentModifier = 1 - (self.zoomPercent / 100)
        return clip.fx(
            crop,
            x_center=int(clip.w / 2),
            y_center=int(clip.h / 2),
            width=int(clip.w * zoomPercentModifier),
            height=int(clip.h * zoomPercentModifier),
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
