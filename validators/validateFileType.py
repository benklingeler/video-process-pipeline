from pathlib import Path

allowedImageExtensions = [".png", ".jpg", ".jpeg", ".heic", ".webp", ".heif"]
# List of allowed image file extensions.

allowedVideoExtensions = [".mp4", ".mov", ".3gp", ".hevc"]
# List of allowed video file extensions.


def validateFileType(path):
    """
    Validates the file type based on the file extension.

    Args:
        path (str): The path of the file to validate.

    Returns:
        tuple: A tuple containing a boolean value indicating if the file is an image,
            and a boolean value indicating if the file is a video.
    """

    isImage = Path(path).suffix in allowedImageExtensions
    isVideo = Path(path).suffix in allowedVideoExtensions

    return (isImage, isVideo)
