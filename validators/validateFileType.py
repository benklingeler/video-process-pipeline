from pathlib import Path

allowedImageExtensions = [".png", ".jpg", ".jpeg", ".heic", ".webp", ".heif"]
allowedVideoExtensions = [".mp4", ".mov", ".3gp", ".hevc"]

def validateFileType(path):
    
    isImage = Path(path).suffix in allowedImageExtensions
    isVideo = Path(path).suffix in allowedVideoExtensions

    return (isImage, isVideo)