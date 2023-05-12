from rich import print
from lib.configuration import loadConfiguration
from pipeline.collectInformation import collectInformation


def startConvertingFiles():
    """
    Starts the file conversion process.

    - Collects user-selected files, conversion steps, and the destination path.
    - Prints the collected files, steps, and destination path (for demonstration purposes).

    The function represents the starting point of the file conversion process.
    It outlines the high-level steps involved in the conversion process, such as loading and processing files,
    applying conversion steps, saving results, and presenting the final output.

    Returns:
        None
    """

    (files, steps, destPath) = collectInformation()
    print(files, steps, destPath)

    # Start progress bar
    # Start the conversion pipeline
    # Load the images & videos
    # Process images & videos with steps
    # Save results
    # Show / present results

    # SUBTASK PIPELINE
    # Get additional information based on step
    return


if __name__ == "__main__":
    loadConfiguration()
    startConvertingFiles()
