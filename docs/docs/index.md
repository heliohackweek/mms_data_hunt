# MeMeS Docs

This is the documentation for the 2020 Heliophysics HackWeek to explore events noted by the SITL reports and within observations.

## Getting Set Up

In order for all of us to collaborate on a project together, we need to ensure that we all are able to contribute within the same environment. I recommend creating a virtual environment for such a reason and I will step you thru this process to do so on your local device.

!!! Note
    The reason I prefer using Miniconda over Anaconda or Enthought's Canopy is two-fold: Miniconda only installs the minimum amount of Python packages needed to run the distribution; Miniconda would have initally faster imports for several packages as the pycache has not been built whereas Anaconda will be slower for that initial import to compile more of those packages.

    I do not use Canopy as it is not freely available for all features (mainly to add/remove Python packages at will).

1. Obtain and Install Miniconda
    - Miniconda can be downloaded from here: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html).
        - For Linux/Mac Operating Systems, I recommend using the files that download a `.sh` file. This can then be run from the Terminal/Command Prompt.
        - For Windows, I will warn you to uninstall any prior installations of Python separate from ArcGIS and/or other self-contained installations. When installing packages, the exact location to install these gets clobbered within Windows installations that have multiple "Python"s. Miniconda, unlike Anaconda, will only install the Python `.exe` file. Ancaconda allows you to install the `Anaconda Navigator` which, in my experience, is confusing.
    - Follow the installation instructions:
        - Linux/Mac, at the end, be sure to allow the installer to run the init script which will place the proper lines in your shell's rc file. You can find which shell you are running by the command:

                echo $0

        - Windows, you will want to install from the `.exe` file and then use the `Anaconda Command Prompt` to use the modified environment that recognizes the proper Python installation.

2. Test your default installation.
    - In order to test your installation, type `python` from the Terminal/Anaconda Prompt and you should see something similar to:

            Python 3.8.3 
            [Clang 10.0.0 ] :: Anaconda, Inc.
            Type "help", "copyright", "credits" or "license" for more information.
             >>>

    - The `>>>` shows that you are actually running the Python interpreter. This is what we want to see. To exit, type `exit()` and hit enter.
    - Please refer to [this resource](https://github.com/edmondb/helio_info) for more links to get familiar with Python programming.

2. Set Up a Virtual Environment
    - I recommend doing the following step in order to update the installers and default environment from the Terminal/Anaconda Command Prompt:

            conda update conda
            conda install pip virtualenv

    - This updates the _conda_ installer as well as installs a separate installer (_pip_) and the Python package that allows us to create virtual environments (_virtualenv_).

3. Clone the GitHub Repository
    - Most Linux/Mac systems already come with Git installed. Windows, you will want to [download](https://git-scm.com/downloads) and install Git.
    - In order to clone the repository, you need to execute the following command (Windows, do this from the `Git Bash` which is separate from the `Anaconda Command Prompt`):

            git clone https://github.com/heliohackweek/mms_data_hunt.git

    - There might be some configuration needed in order to do this, but it will "copy" the code into the current directory that you are at. Windows, you will need to know where that is or `cd` to a location before cloning so that you can work with the copied files.
    - Please refer to [this resource](https://github.com/edmondb/helio_info) for more links to get familiar with Git.

4. Test environment on your local device.
    - In the files that you cloned, there is a `test` folder that contains a script that will allow one to ensure that their environment is setup properly. To run this:

            python /location/of/mms_data_hunt/test

    - It verifies that all the necessary imports are installed.

## Set Up for Remote Systems

On other systems, you will most likely be provided a Python installation that has been built or is customized for you. Here is my recommendations for getting started for those systems.

1. Log into the system.
2. Load Python environment using (module load; sourcing a module file).
    - Most remote systems are Linux OS-based. The administrators typically will allow the use of [modules](http://modules.sourceforge.net/) for environment/PATH modification.
    - In order to see what modules are available: `modules avail`.
    - Load a module: `module load module_name`.
3. Clone the GitHub Repository. (see #3 above)
4. Test environment on the remote system. (see #4 above)
