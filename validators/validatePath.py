from pathlib import Path


def validatePath(_, pathString):
  path = Path(pathString)
  if path.exists() is False:
    return False
  return True