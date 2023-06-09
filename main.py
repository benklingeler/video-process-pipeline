import logging
import time
from os import path
from pathlib import Path

import typer
from proglog import ProgressBarLogger
from rich import print

from lib.collectInformation import collectInformation
from lib.configuration import loadConfiguration
from lib.convertFile import convertFile

logger = logging.getLogger("moviepy")
logger.setLevel(logging.ERROR)


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

    (files, steps) = collectInformation()

    # Collect information for each assigned step, before converting files
    for step in steps:
        step.CollectRequiredInformation()
        step.PreparePipeline()

    # Initialize the progress bar with a length of 100 and a label
    with typer.progressbar(length=100, label="Processing videos") as progress:
        # Iterate over each file in the list
        for file in files:
            # Update the progress bar label to show the current file being processed
            progress.label = file

            # Convert the current file using the `convertFile` function,
            # passing the file, steps, progress, and progress update increment
            convertedVideoClip = convertFile(file, steps, progress, 100 / len(files))

        # Finish rendering the progress bar
        progress.render_finish()

    # Print the total number of files processed
    print(f"Processed {len(files)} Files.")

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
