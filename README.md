# Summary
Working in collaboration with cancer research UK to automate the acquisition & analysis of
images used to monitor stem cell growth

---

## Instructions on setting up project:

#### On first run ever (when repo is cloned):
To set up your virtual environment and install the relevant packages
  * Run the command `source setup_linux.sh`, for Linux based systems
  * Run the command `setup_windows.bat`, for Windows based systems

#### On any subsequent run to set up virtual env:
  * On Linux run the command `source bin/activate`
  * `deactivate` will deactivate virtualenv environment

### Run project:

  * Run the project using `python AutoDAC.py`

#### General commands:
  * Generate HTML test coverage
    - `pytest --cov=ImageProcessing/src --cov=MicroscopeInterface/src --cov-report term --cov-report html ImageProcessing/tests MicroscopeInterface/tests`

  * Run tests
    - `pytest --cov=ImageProcessing/src --cov=MicroscopeInterface/src --cov-report term ImageProcessing/tests MicroscopeInterface/tests`


#### To view generated  html report on the browser:

One can run `python3 -m http.server` inside the **htmlcov** directory, this will launch a http server which you can access via the browser at **localhost:8000** (usually)

---

## General project structure:

The project is split into two major components: Microscope Interface and Image
Analysis

### Microscope Interface

  - Responsible for handling the interaction with the microscope
  - Clicks buttons on LASAF software
  - Extracts cells from microsocope images for analysis

### Image Analysis

  - Responsible for analysing extracted images
  - Segments images of cells
  - Scores segmented image of cell

## Documentation:

  - The source files have been annotated with comments describing the purpose of
the functions within them. These can be read directly from the source files or by running `pydoc <path-to-file>` from the *root level* directory
  - Documentation for each of the files can also be viewed as a webpage. For example, running `pydoc -w MicroscopeInterface/src/LeicaUI.py` from the *root level* directory will generate a LeicaUI.html file for the LeicaUI.py program file. The html file can be double clicked on to open, or can be opened via `open LeicaUI.html` on the terminal.

## Collaborators:
  - [Zubair Chowdhury](https://github.com/zubair100)
  - [Sarah Baka](https://github.com/sarahbaka)
  - [Harry Uglow](https://github.com/harry-uglow)
  - [Ioannis Gabrielides](https://github.com/YianniG)
  - [Andy Hume](https://github.com/monotypical)
