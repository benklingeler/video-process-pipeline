from validators.validateFileType import validateFileType
from validators.validatePath import validatePath


def test_validateFileType():
    """
    Test cases for the validateFileType function.

    - Test videos: Asserts that video file types return (False, True) indicating they are not images but are videos.
    - Test images: Asserts that image file types return (True, False) indicating they are images but not videos.
    - Test non-videos and non-images: Asserts that non-video and non-image file types return (False, False) indicating they are neither videos nor images.
    """

    assert validateFileType("video.mp4") == (False, True)
    assert validateFileType("video.mov") == (False, True)
    assert validateFileType("video.3gp") == (False, True)
    assert validateFileType("video.hevc") == (False, True)

    assert validateFileType("image.png") == (True, False)
    assert validateFileType("image.jpg") == (True, False)
    assert validateFileType("image.jpeg") == (True, False)
    assert validateFileType("image.heic") == (True, False)
    assert validateFileType("image.webp") == (True, False)
    assert validateFileType("image.heif") == (True, False)

    assert validateFileType("non-type.pdf") == (False, False)
    assert validateFileType("non-type.txt") == (False, False)
    assert validateFileType("non-type.docx") == (False, False)
    assert validateFileType("non-type.sql") == (False, False)


def test_validatePath():
    """
    Test cases for the validatePath function.

    - Test for valid path: Asserts that a valid path returns True.
    - Test for file: Asserts that a file path returns False.
    - Test for non-existing folders: Asserts that a non-existing folder path returns False.
    - Test for invalid paths: Asserts that an invalid path returns False.
    """

    assert validatePath(True, "C:\\Users\\benkl\\Videos\\please_convert_me") == True

    assert (
        validatePath(True, "C:\\Users\\benkl\\Videos\\please_convert_me\\video_1")
        == False
    )

    assert (
        validatePath(
            True, "C:\\Users\\benkl\\Videos\\please_convert_me\\non-existing-folder"
        )
        == False
    )

    assert validatePath(True, "invalid-path") == False
