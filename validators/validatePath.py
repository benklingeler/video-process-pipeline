from pathlib import Path


def validatePath(_, pathString):
    """
    Validates the given path.

    Args:
        _: Unused argument (required for the validation function signature).
        pathString (str): The path to validate.

    Returns:
        bool: True if the path exists, False otherwise.
    """

    path = Path(pathString)
    if path.exists() is False:
        return False
    return True
