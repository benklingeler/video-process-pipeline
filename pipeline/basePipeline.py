from moviepy.editor import VideoClip


class BasePipeline:
    def Process(self, clip: VideoClip) -> VideoClip:
        raise NotImplemented

    def CollectRequiredInformation():
        return

    def FormatQuestion(self, message: str) -> str:
        return f"(\033[1m{self.__class__.__name__}\033[0m) {message}"
