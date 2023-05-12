from rich import print

from pipeline.collectInformation import collectInformation

# python main.py --path "C:\Users\benkl\Videos\please_convert_me"

def startConvertingFiles():
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
  startConvertingFiles()