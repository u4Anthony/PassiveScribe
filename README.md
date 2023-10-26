# PassiveScribe


## Idea
Create Passive Income through the use of prepackaged AI, bots, or other programs.  Specifically these should be put into a pipeline that creates some sort of end product that can be "sold" for money.  Minimal amount of actual human work should need to be utilized during the actual work flow.

## Flow
Download Video -> Pull Audio from Video -> Pipe Video through AI/program that will automatically transcribe video -> Upload Video for Profit

## Technology Needed
* Something to pull audio from video
* Something to transcribe video
* DevOps pipeline to automate everything
* Hardware for everything



## Development Setup

### Cloning PassiveScribe
* To get PassiveScribe on your local machine you must have Git installed. See the GitHub guide for Git if you are unsure of the availability on your machine, found here https://github.com/git-guides/install-git .
* Simply clone PassiveScribe to the desired location on your directy through the following command:
`git clone git@github.com:u4Anthony/PassiveScribe.git`

### Installing Miniconda
* Download the appropriate installer for your device from https://docs.conda.io/projects/miniconda/en/latest/ .
* Install Miniconda, accept default options.
* (On Windows) Open the newly installed Anaconda Prompt (Miniconda 3) command line program.
* Run `conda update conda` within the Miniconda command line terminal.
* Run `conda create --name passivescribe python=3.11.5` to create a new Python 3.11.5 environment for Python development.
* Run `conda activate passivescribe` to access the new environment.
* To ensure everything is working as intended, run `python --version`, you should get a response of "Python 3.11.5" within the terminal window.

### Installing Dependencies
* Open an Anaconda Prompt (Miniconda 3) command line program
* Run `conda activate passivescribe` to access the PassiveScribe environment.  If this does not work, refer back to the "Installing Miniconda" instructions, otherwise continue to the next step.
* If not already there, navigate to the PassiveScribe directory. If you do not already have the PassiveScribe project cloned onto your local machine, refer back to the "Cloning PassiveScribe" section before continuing. 
* Once in the PassiveScribe directory, run `python -m pip install requirements.txt`

### Maintaining and Auditing the Dependency List
* To check for outdated dependency versions:
`python -m pip list --outdated`
* To upgrade a dependency (replace the word "dependency" with your desired dependency for updates):
`python -m pip install -U dependency`
* Regenerate the requirements.txt file after updating or adding a dependency:
`python -m pip freeze > requirements.txt`

Note: all of these commands should be done within the PassiveScribe miniconda environment and within the PassiveScribe project directory.

### Installing FFmpeg
FFmpeg is a multimedia framework that is required for PassiveScribe to work properly.  Unfortunately, we cannot install correctly through pip and so these steps must be done for any new machine (not Miniconda environement) that PassiveScribe will be run on.
* Download the zip file of the latest FFmpeg (on windows) using this link: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
* If you are not on Windows, find the correct package for you through the FFmpeg site here: https://ffmpeg.org/download.html
* Unzip the downloaded file using a file archiver such as Winrar or 7z.
* Rename the extracted file to "ffmpeg" and move it to the root of the C: drive
* Open a command prompt (cmd) as an administrator and set the encironment path variable for ffmpeg utilzing the command: `setx /m PATH "C:\ffmpeg\bin;%PATH%"`
* Open a new command prompt and verify that the installtion was succesfuly with the command `ffmpeg -version`, a computer restart might be necessary

### Installing CUDA
NVIDIA describes CUDA as "a parallel computing platform and programming model...It enables dramatic increases in computing performance by harnessing the power of the graphics processing unit (HGPU)."  PassiveScribe utilizes CUDA to ensure that the transcription processing time is within profitable timeframes.  Like FFmpeg, CUDA is not something we can setup through pip and it must be done for any new machine (not Miniconda environment) that PassiveScribe will be run on.
<br>
Because CUDA is a proprietary API for NVIDIA cards, PassiveScribe currently only works with NVIDIA GPUs or on your CPU.  If an NVIDIA GPU is not available, and you plan to utilize PassiveScribe on CPU, note that processing times will be affected.

* First navigate to https://developer.nvidia.com/cuda-downloads and select all the options that match to your local machine's platform.
* Download the associated CUDA installer matched to your platform and follow the installation steps
