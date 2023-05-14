from moviepy.editor import VideoClip


class BasePipeline:
    """
    Base class for video processing pipelines.
    """

    def Process(self, clip: VideoClip) -> VideoClip:
        """
        Process the given video clip.

        Args:
            clip (VideoClip): The input video clip to be processed.

        Returns:
            VideoClip: The processed video clip.
        """

        raise NotImplemented

    def CollectRequiredInformation():
        """
        Collect any required information for the pipeline.

        This method should be implemented in derived classes to gather any necessary
        information before processing the video clip.
        """

        return

    def FormatQuestion(self, message: str) -> str:
        """
        Format a question with the class name included.

        Args:
            message (str): The question message to be formatted.

        Returns:
            str: The formatted question string.
        """

        return f"(\033[1m{self.__class__.__name__}\033[0m) {message}"

    def PreparePipeline(self):
        """
        Prepare the pipeline for video processing.

        This method should be implemented in derived classes to perform any necessary
        setup or initialization steps before processing the video clip.
        """
        pass
