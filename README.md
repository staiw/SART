# SART for PsychoPy

This repository provides a PsychoPy implementation of the **Sustained Attention to Response Task (SART)** [1] with feedback after each trial  and an optional attention rating. Designed with psychological researchers and students in mind, this implementation aims to be user-friendly even for those with limited programming experience. 

Robertson et al. (1997) designed the SART in order to measure sustained attention and response inhibition. Participants are asked to respond to frequent "go" stimuli (typically all digits except or '3') while withholding their response to rare "no-go" stimuli (display of '3's), with their performance indicating levels of attention and impulsivity. Gijsbert Stoet suggested intoduced a modification of the task where each person ranks their attention on the task during the experiment.

You can change the general settings of the experiment (number of trials and blocks, stimuli characteristics, whether training and/or attention rating is included etc.) in the section `Set variables` of the `sart.py` script. The **default settings** are, among other things, as follows:
- 1 training block with 18 trials
- 3 test blocks with 75 trials each
- attention rating from 1 (on task) to 6 (off task) after each test block
- stimulus display: 250 milliseconds
- mask display: 900 milliseconds
- feedback display: 3 seconds
- users respond with the `space` key
- the experiment may be quitted with `escape` key

Getting Started:

- Prerequisites: Ensure you have PsychoPy installed on your system.
- Download: Clone or download this repository to your local machine.
- Run: Navigate to the repository folder in PsychoPy and run the 'sart.py' script to start the task.
- Data analysis: The results are saved as one CSV file per session/participant. The script ``data_analysis/read_in_data_in_R`` merges all data from a study.

Repository Structure:

- ``sart``.py: The main script to run the SART task, containing of the following three main three sections:
  - ``Set variables``: You may change the general settings of the experiment here.
  - ``Define functions``: Code for defining the experimental procedure and how the data will be save.
  - ``Run experiment``: This section calls the previously defined function to run the experiment.
- ``img``: Directory with images used in the task (instructions, feedback etc.).
- ``instructions``: Presentation with the instructions for the task.
- ``data_analysis``: Folder containing scripts and tools for analyzing the results.
  - ``read_in_data_in_R.R``: Script to read in and merge data from all participants of a study.
  - ``codebook_data.txt``: Explainations of all variables that are saved.

References:
[1] Robertson, I. H., Manly, T., Andrade, J., Baddeley, B. T., & Yiend, J. (1997). Sustained Attention to Response Task (SART) [Database record]. APA PsycTests. https://doi.org/10.1037/t28308-000

[2] Stoet, G. (2021). Sustained Attention to Response Task (SART) with response feedback (SART 2). PsyToolkit. 