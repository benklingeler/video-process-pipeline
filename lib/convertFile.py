from typing import Sequence

from moviepy.editor import ImageClip, VideoClip, VideoFileClip
from pipeline.basePipeline import BasePipeline
from pipeline.savePipeline import SavePipeline
from validators.validateFileType import validateFileType


def convertFile(
    file: str, steps: Sequence[BasePipeline], progress: any, stepSize: int
) -> VideoClip:
    subTaskStepSize = stepSize / (2 + len(steps))

    (isImage, _) = validateFileType(file)
    progress.update(subTaskStepSize)

    clip = prepareFileToClip(file, isImage)
    progress.update(subTaskStepSize)

    for step in steps:
        if isinstance(step, SavePipeline):
            clip = step.Process(clip, file)
        else:
            clip = step.Process(clip)
        progress.update(subTaskStepSize)

    return clip


def prepareFileToClip(file, isImage):
    return ImageClip(file) if isImage else VideoFileClip(file)
