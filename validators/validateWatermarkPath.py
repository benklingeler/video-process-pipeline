from pathlib import Path
from PIL import Image

allowedWatermarkExtensions = [".png", ".jpg", ".jpeg"]


def validateWatermarkPath(_, pathString):
    path = Path(pathString)

    if path.is_file() is False:
        return False

    if validateWatermarkFileType(pathString) is False:
        return False

    if validateWatermarkImageSize(pathString) is False:
        return False

    return True


def validateWatermarkFileType(path):
    return Path(path).suffix in allowedWatermarkExtensions


def validateWatermarkImageSize(path):
    img = Image.open(path)
    width, height = img.size

    return (width >= 10 and width <= 500) and (height >= 10 and height <= 500)


# answers = iq.prompt(questions)
# op.path.isfile(answers)
# if op.path.isfile == True:
#     pass
# else:
#     print("The given File does not exists")
