import os
import pathlib
import pandas as pd
import sys

# Get the absolute path to a directory in the users home dir
POLYCHRON_PROJECTS_DIR = (pathlib.Path.home() / "Documents/Pythonapp_tests/projects").resolve()
# Ensure the directory exists (this is a little aggressive)
POLYCHRON_PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
# Change into the projects dir
os.chdir(POLYCHRON_PROJECTS_DIR)
old_stdout = sys.stdout

# global variables
phase_true = 0
load_check = "not_loaded"
mcmc_check = "mcmc_notloaded"
proj_dir = ""
SCRIPT_DIR = pathlib.Path(__file__).parent  # Path to directory containing this script
CALIBRATION = pd.read_csv(SCRIPT_DIR / "linear_interpolation.txt")
# Vars not previously defined in global scope but set via globals keyword
FILE_INPUT = None 