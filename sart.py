#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
############################### Import packages ###############################
###############################################################################

from psychopy import visual, core, event, data, gui
from psychopy.constants import NOT_STARTED, STARTED, FINISHED
import random
import pandas as pd
import os

###############################################################################
################################ Set variables ################################
###############################################################################

# Set number of trials
n_trials_train = 18     # Number of trails during the training block (default is 18)
n_trials_test  = 75     # Number of trails during ONE testing block (default is 75)

# Set keys
response_key     = 'space'     # Key with which users respond
exit_key         = 'escape'    # Key to stop the experiment at any time
experimenter_key = 'escape'    # Key experimenter uses to end the experiment on the last page

# General information about the experiment
experiment_info = {
    'experiment_name': 'sart', # Experiment name (relevant for data-file names)
    'participant' : '',
    'session'     : '001',     # Replace with '' to remove default value
    'training'    : 1,         # 1 = include training, 0 = no training
    'testing'     : 3,         # Number of testing blocks, 0 = no testing
    'rating'      : 1,         # 1 = include attention rating, 0 = no rating
    'date': data.getDateStr()  # Date and time of the beginning of the session 
}

# General information which should not be shown in the dialog
popped_keys = { 
    #'experiment_name': experiment_info.pop('experiment_name', 'sart'), # Remove first hashtag if you only run one experiment
    #'session': experiment_info.pop('session', '001'),      # Remove first hashtag if session number is always identical
    #'training': experiment_info.pop('training', 1),        # Remove first hashtag if sessions always or never include training
    #'testing': experiment_info.pop('testing', 1),          # Remove first hashtag if number of test block is always identical
    'date': experiment_info.pop('date', data.getDateStr()), # The date will not be displayed in the info dialog
    'rating': experiment_info.pop('rating', 1) # Comment out this line if you want to change rating settings in the info dialog
}

# Set stimulus-display times (in seconds)
digit_display_time    = .25  # Time the digit (stimulus) is displayed (default is .25)
mask_display_time     = .9   # Time the mask is displayed (default is white mask and .9)
feedback_display_time = 3.0  # Time feedback is displayed (default is green mask or reminder of the rules)

# Set stimuli layout
stimuli_font    = 'Arial' # Font of the stimuli
stimuli_scale   = 4  # Change scale to make stimuli numbers bigger or smaller
stimuli_heights = [height * stimuli_scale for height in [48, 72, 94, 100, 120]] # Stimuli will be randomly displayed with one of these heights

# Set stimulus digit range
digit_range = list(range(1, 10)) # 1-9 (upper bond is NOT included) 

# Set inhibition number
inhibition_number = 3 # Default is digit 3

# Set images size
image_rescale = (1.5, 1.5)

# Set image file names
title_screen        = 'img/title_screen.png'
intro1              = 'img/intro1.png'
intro2              = 'img/intro2.png' 
intro3              = 'img/intro3.png' 
intro_train         = 'img/intro_training.png'
intro_test          = 'img/intro_test.png'
end_training        = 'img/end_training.png'
end_test_block      = 'img/end_test_block.png'
end_experiment      = 'img/end_experiment.png'
countdown_images    = ['img/count_down3.png', 
                       'img/count_down2.png', 
                       'img/count_down1.png']
mask_correct        = 'img/mask_green.png'
mask                = 'img/mask_white.png'
feedback_inhibition = 'img/feedback_inhibition.png'
feedback_missed     = 'img/feedback_missed.png'
attention_check     = 'img/attention_check.png'

###############################################################################
############################### Define functions ##############################
###############################################################################

def check_for_quit(win, current_data= None, block=None, keys=None, exit_key=exit_key):
    """
    Quit experiment if exit key was pressed.
        
    Parameters:
    - win : visual.Window
        The window or screen instance where the experiment is displayed. This is closed if the exit key is detected.
    
    - current_data : list of dictionaries, optional
        Data of the current trial block. If provided, this data will be saved when exiting. Default is None.
    
    - block : int, optional
        Information or data about the current block in the experiment. Used for saving data on exit. Default is None.
    
    - keys : list of tuples, optional
        Information about pressed keys. The first element of the tuple is the key pressed, and the second element is the timestamp of the key press.
    
    - exit_key : str
        The key that, when pressed, triggers the exit and saving of data. Default is the global `exit_key` variable.

    Returns:
    - None

    Side Effects:
    - If the exit key was pressed, data up to that point is saved, the window is closed, and the experiment is terminated.
    """
    # Get keys
    if keys==None:
        keys = event.getKeys(timeStamped=True)

    # Quit experiment if exit key was pressed
    if len(keys)>0 and keys[len(keys)-1][0]==exit_key:
        save_data(current_data=current_data, block=block, exit_time = keys[0][1])
        
        win.close()
        core.quit()

def show_info_dialog(experiment_info, popped_keys):
    """
    Show info dialog, set and modify experiment information.

    Parameters:
    - experiment_info: dict
        Information about this experiment.
    - popped_keys: dict
        Information which should not be displayed in the dialog.
    
    Returns
    - experiment_info: dict
        Information about this experiment.
    """
    # Show participant info dialog
    dlg = gui.DlgFromDict(dictionary=experiment_info, sortKeys=False)#, title=expName)
    if dlg.OK == False: 
        core.quit()

    # Restore hidden keys
    experiment_info.update(popped_keys)

    return experiment_info

def display_instructions(win, instructions, continue_key=[response_key]):
    """
    Display a sequence of instruction screens.
    
    Parameters:
    - win : visual.Window
        The window or screen instance where the experiment is displayed.
    - instructions : list of str
        A list containing paths to image files that will be displayed as instruction screens.
    
    - continue_key : list of str, optional
        A list of keys that, when pressed, will move to the next instruction screen. The default is the global `response_key` variable.
        
    Returns:
    - None
    
    Side Effects:
    - Displays instruction images one by one in the provided window.
    - Waits for a key press from `continue_key` to move to the next instruction.
    - If the exit key is detected using the `check_for_quit` function, it will exit the experiment.
    
    """
    for instruction in instructions:
        # Load and display the instruction image
        instruction_stim = visual.ImageStim(win, image=instruction,
                                           size = image_rescale)
        #instruction_stim.size = 0.8
        #instruction_stim.height = 0.5
        instruction_stim.draw()
        win.flip()
        
        # Wait for a space-key press to move to the next instruction
        while True:
            keys = event.waitKeys(maxWait=0.05, keyList=continue_key)
            if keys is not None:
                break
            check_for_quit(win, keys=keys)

def display_ready_countdown(win):
    """
    Display a countdown sequence.
    
    Parameters:
    - win : visual.Window
        The window or screen instance where the countdown images are displayed.
    
    Returns:
    - None
    
    Notes:
    - This function assumes the existence of a global list 'countdown_images' containing paths to the countdown images.
    """
    for image_path in countdown_images:
        # Load and display the countdown image
        countdown_stim = visual.ImageStim(win, image=image_path, size = image_rescale)
        countdown_stim.draw()
        win.flip()
        
        # Wait for 1 second before showing the next countdown image
        if '1' in image_path:
            core.wait(.8)
        else:
            core.wait(1)
        check_for_quit(win)

def run_block(win, n_trials, digits=digit_range, block=None):
    """
    Run the SART (Sustained Attention to Response Task) for a specified number of trials.

    Parameters:
    - win : visual.Window
        The window or screen instance where the experiment is displayed.
    
    - n_trials : int
        Number of trials to run.
    
    - digits : list of ints, optional
        List of digits to use as stimuli. Default is the global 'digit_range' variable.
    
    - block : int or None, optional
        Number of current block. Used to save data if block is exited earlier. Default is None.
    
    Returns:
    - trial_data : list of dictionaries
        A list of dictionaries, where each dictionary contains data for a trial. This includes:
        - 'digit': The digit displayed in the trial (stimulus).
        - 'stimulus_size': The index of the stimulus size.
        - 'go_trial': A binary indicator indicating if it's a go-trial (1) or not (0).
        - 'key': The response key pressed that may be pressed by the participant.
        - 'stimulus_time': The timestamp when the stimulus was displayed.
        - 'reaction_time': The timestamp when the participant responded.
        - 'reaction_duration': The duration between stimulus display and participant's response.
        - 'status': An indicator of whether the participant's response was correct (1) or incorrect (0).

    Side Effects:
    - Displays digits one by one in the provided window and waits for participant's response.
    - Shows feedback if there was an error in response.
    - Checks for the exit key using the `check_for_quit` function, and if detected, it will exit the experiment.
    
    Notes:
    - This function assumes the existence of global variables like 'countdown_images', 'mask', 'mask_correct', 'feedback_inhibition', 'feedback_missed', etc. 
      Adjustments to the function might be needed if these globals are not defined elsewhere.
    """
    trial_data = []
    
    # Replicate digits to meet the number of trials and shuffle their order
    stimuli = (digits * (n_trials // len(digits) + 1))[:n_trials]
    random.shuffle(stimuli)

    # Load images before the loop to prevent time delays
    mask_stim_default = visual.ImageStim(win, image=mask, size = image_rescale)
    mask_stim_correct = visual.ImageStim(win, image=mask_correct, size = image_rescale)
    feedback_stim_inhibition = visual.ImageStim(win, image=feedback_inhibition, size = image_rescale)
    feedback_stim_missed = visual.ImageStim(win, image=feedback_missed, size = image_rescale)
    
    for trial in stimuli:

        # Clear (saved) reaction time
        reaction_time = None

        # Display the digit in a random font size 
        stimulus_height_index = random.choice(range(len(stimuli_heights)))
        digit_stim = visual.TextStim(win, text=str(trial), 
                                     height=stimuli_heights[stimulus_height_index]*0.001, 
                                     font=stimuli_font)
        digit_stim.draw()
        stimulus_time = win.flip()

        # Wait for a response
        keys = event.waitKeys(maxWait=0.25, keyList=[response_key], timeStamped=True)
        check_for_quit(win, current_data = trial_data, block=block, keys=keys)

        # Handle response
        if keys is not None: # Do not merge these two if statements (otherwise false gos arent covered)
            if trial != inhibition_number:
                # If a key was pressed in a go-trial, display green mask
                reaction_time = keys[0][1]
                mask_stim = mask_stim_correct
        else:
            # If no key was pressed while the digit was displayed, display mask and wait
            mask_stim = mask_stim_default
            mask_stim.draw()
            win.flip()
            keys = event.waitKeys(maxWait=0.9, keyList=[response_key], timeStamped=True)

            check_for_quit(win, current_data = trial_data, block=block, keys=keys)

            if keys:
                reaction_time = keys[0][1]
                if trial != inhibition_number:
                    mask_stim = mask_stim_correct
        
        mask_stim.draw()
        win.flip()

        # Determine feedback and status
        if trial == inhibition_number and keys:
            # Incorrect press on a no-go trial
            feedback_stim = feedback_stim_inhibition
            status = 0
        elif trial != inhibition_number and not keys:
            # Missed a go trial
            feedback_stim = feedback_stim_missed
            status = 0
        else:
            # Correct response
            status = 1

        # Show feedback if there was an error
        if status == 0:
            feedback_stim.draw()
            win.flip()
            core.wait(feedback_display_time)
        
        # Calculate duration of reaction
        if reaction_time and stimulus_time:
            reaction_duration = reaction_time - stimulus_time
        else: 
            reaction_duration = None
        
        # Get response key
        if (keys !=  None):
            key = keys[0][0]
        else:
            key = None

        # Check whether trial is a go-trial  
        go_trial = 0 if trial == inhibition_number else 1

        # Save trial data
        trial_data.append({
            'digit': trial,
            'stimulus_size': stimulus_height_index + 1,
            'go_trial': go_trial,
            'key': key,
            'stimulus_time': stimulus_time,
            'reaction_time': reaction_time,
            'reaction_duration': reaction_duration,
            'status': status
        })
        
        # Wait before starting the next trial
        core.wait(1)
        check_for_quit(win, current_data = trial_data, block=block,keys=keys)
    
    # Get rating of attention on the task
    if experiment_info['rating'] == 1:
        attention_rating = rate_attention(win, attention_check, trial_data = trial_data, block=block)
        trial_data.extend(attention_rating)     

    return trial_data

def rate_attention(win, image_name, trial_data, block, min_val=1, max_val=6):
    """
    Display attention-rating scale and let user rate attention during the trial.

    Parameters:
    - win : visual.Window
        The window or screen instance where the experiment is displayed.
    
    - image_name : str
        The path to the image file with instructions and the scale.
        
    - trial_data : list of dict
        List of dictionaries containing data for each trial up to this point.
    
    - block : int or None
        Number of current block. Used to save data if block is exited earlier. Default is None.
    
    - min_val : int, optional
        Minimum possible value for the rating. Default is 1.
    
    - max_val : int, optional
        Maximum possible value for the rating. Default is 6.

    Returns:
    - rating_data : list of dict
        A list of dictionaries, where each dictionary contains:
        - 'attention_rating': The rating provided by the participant.
        - 'reaction_time': The timestamp when the participant provided the rating.
        - 'stimulus_time': The timestamp when the rating scale was displayed.
        - 'reaction_duration': The duration between the image display and participant's response.

    Side Effects:
    - Display the attention scale and wait for the participant's rating.
    - Checks for the exit key using the `check_for_quit` function, and if detected, it will exit the experiment.

    Notes:
    - The function assumes that the user's inputs are limited to number keys '1' through '6' and the 'escape' key.
    """
    # Display attention scale
    img = visual.ImageStim(win, image=image_name, size = image_rescale)
    img.draw()
    stimulus_time = win.flip()
    
    # Wait for user input
    rating = None
    while True:
        keys = event.getKeys(keyList=['1', '2', '3', '4', '5', '6', "escape"], timeStamped=True)
        check_for_quit(win, current_data = trial_data, block=block, keys=keys)
        if keys:
            rating = keys
            if min_val <= int(rating[len(rating)-1][0]) <= max_val:
                break
    
    # Save data
    rating_data = []
    for response in rating:
        rating_data.append({'attention_rating': response[0], 
                            'reaction_time': response[1],
                            'stimulus_time': stimulus_time,
                            'reaction_duration': response[1] - stimulus_time})
    
    return rating_data

def run_training_block(win, n_trials):
    """
    Run the training block of the experiment.

    Parameters:
    - win : visual.Window
        The window or screen instance where the experiment is displayed.
    
    - n_trials : int
        Number of training trials to run.
    
    Returns:
    - trial_data: List of dictionaries containing data for each trial in the training block.
    """
    # Display instructions
    display_instructions(win, [intro_train])

    # Show ready countdown
    display_ready_countdown(win)

    # Run the 'sart' task for all training trials
    trial_data = run_block(win, n_trials, digits=digit_range, block=0)

    # Display feedback
    display_instructions(win, [end_training])

    save_data(training_data=trial_data)
    #return trial_data


def run_test_block(win, n_trials, block):
    """
    Run the real test block of the experiment.

    Parameters:
    - win : visual.Window
        The window or screen instance where the experiment is displayed.
    
    - n_trials : int
        Number of testing trials to run.
    
    - block : int or None
        Number of current block. Used to save data if block is exited earlier.

    Returns:
    - trial_data: List of dictionaries containing data for each trial in the testing block.
    """
    # Display instructions
    display_instructions(win, [intro_test])

    # Show ready countdown
    display_ready_countdown(win)

    # Run the 'sart' task for all test trials
    trial_data = run_block(win, n_trials, digits=digit_range, block=block)

    # Display feedback
    display_instructions(win, [end_test_block])

    # Save data
    save_data(test_data=trial_data, block=block)

def save_data(training_data=None, test_data=None, current_data=None, block=None, exit_time = None):
    """
    Save experimental data into a CSV file. The CSV file is named based on the task name, 
    participant ID and the date, and if the file already exists, the new data is appended to it.

    Parameters:
    - training_data: list of dict, optional
        A list of dictionaries containing data from the training phase.
    - test_data: list of dict, optional
        A list of dictionaries containing data from the testing phase.
    - current_data: list of dict, optional
        A list of dictionaries containing data from the currently running block.
    - block: int, optional
        The block number. Not required for the training block.
    - exit_time: float, optional
        The timestamp indicating the exit time, if applicable.

    CSV Structure:
    The resulting CSV file will have columns for:
    - experiment_name: Name of the experiment.
    - participant: The participant ID.
    - session: The session number.
    - block: The block number (0 for training).
    - date: The date and time when the experiment started.
    - training: A flag indicating if the data is from the training phase (1 for yes, 0 for no).
    - test: A flag indicating if the data is from the testing phase (1 for yes, 0 for no).
    - rating: A flag indicating if row contains attention-rating data (1 for yes, otherwise None).
    - digit: The digit displayed in the trial (stimulus).
    - stimulus_size: The size of the stimulus.
    - go_trial: A binary indicator indicating if it's a go-trial (1) or not (0).
    - key: The response key pressed that may be pressed by the participant.
    - status: A binary indicator indicating if the participant's response was correct (1) or not (0).
    - stimulus_time: The timestamp when the stimulus or the rating scale was displayed.
    - reaction_time: The timestamp when the participant responded.
    - reaction_duration: The duration between stimulus display and participant's response.
    - attention_rating: The attention rating given by the participant.

    Side effects:
    - The function writes data to a CSV file.

    Note:
    - The function assumes the presence of a global variable 'experiment_info' that provides metadata 
      about the experiment, including participant ID, session number, date, etc.
    - The function also assumes the existence of a 'data/' directory where the CSV file is saved.

    Returns:
    - None. 
    """
    # Get general information about the session
    experiment_name = experiment_info['experiment_name']
    participant     = experiment_info['participant']
    session         = experiment_info['session']
    date            = experiment_info['date']

    all_data = []

    # Get data from training
    if training_data !=None:
        for data in training_data:
            row = {
                'experiment_name': experiment_name,
                'participant': participant,
                'session': session,
                'block': 0,
                'date': date,
                'training': 1,
                'test': 0,
                'rating': 1 if data.get('attention_rating', None) else None,
                'digit': data.get('digit', None),
                'stimulus_size': data.get('stimulus_size', None),
                'go_trial': data.get('go_trial', None),
                'key': data.get('key', None),
                'status': data.get('status', None),
                'stimulus_time': data.get('stimulus_time', None),
                'reaction_time': data.get('reaction_time', None),
                'reaction_duration': data.get('reaction_duration', None),
                'attention_rating': data.get('attention_rating', None),
            }
            all_data.append(row)
    
    # Get data from test
    if test_data != None:
        for data in test_data:
            row = {
                'experiment_name': experiment_name,
                'participant': participant,
                'session': session,
                'block': block,
                'date': date,
                'training': 0,
                'test': 1,
                'rating': 1 if data.get('attention_rating', None) else None,
                'digit': data.get('digit', None),
                'stimulus_size': data.get('stimulus_size', None),
                'go_trial': data.get('go_trial', None),
                'key': data.get('key', None),
                'status': data.get('status', None),
                'stimulus_time': data.get('stimulus_time', None),
                'reaction_time': data.get('reaction_time', None),
                'reaction_duration': data.get('reaction_duration', None),
                'attention_rating': data.get('attention_rating', None)               
            }
            all_data.append(row)
    
    # Get data from currently running block
    if current_data !=None:
        for data in current_data:
            row = {
                'experiment_name': experiment_name,
                'participant': participant,
                'session': session,
                'block': block,
                'date': date,
                'training': 1 if block==0 else 0,
                'test': 0 if block==0 else 1,
                'rating': 1 if data.get('attention_rating', None) else None,
                'digit': data.get('digit', None),
                'stimulus_size': data.get('stimulus_size', None),
                'go_trial': data.get('go_trial', None),
                'key': data.get('key', None),
                'status': data.get('status', None),
                'stimulus_time': data.get('stimulus_time', None),
                'reaction_time': data.get('reaction_time', None),
                'reaction_duration': data.get('reaction_duration', None),
                'attention_rating': data.get('attention_rating', None)
            }
            all_data.append(row)
    
    # If participant
    if exit_time !=None:  
        exit_row = {
            'experiment_name': experiment_name,
            'participant': participant,
            'session': session,
            'block': None,
            'date': date,
            'training': None,
            'test': None,
            'rating': None,
            'digit': None,
            'stimulus_size': None,
            'go_trial': None,
            'key': exit_key,
            'status': None,
            'stimulus_time': None,
            'reaction_time': exit_time,
            'reaction_duration': None,
            'attention_rating': None
        }
        all_data.append(exit_row)

    # Save data in csv file
    filename = f"sart2_{participant}_{date}.csv"
    path = "data/" + filename
    df = pd.DataFrame(all_data)
    if os.path.exists(path):
        df.to_csv(path, mode='a', header=False, index=False)
    else:
        df.to_csv(path, mode='w', header=True, index=False)

def main_experiment(experiment_info):
    """
    Run the experiment.

    Parameters:
    - experiment_info (dict): 
        A dictionary containing metadata and settings for the experiment. Expected keys include:
        - 'training': Boolean indicating if a training block should be run.
        - 'testing': Integer indicating the number of test blocks to run.
    
    Workflow:
    1. Show an information dialog with general information.
    2. Set up the main experiment window.
    3. Display introductory instructions.
    4. If indicated in 'experiment_info', run a training block.
    5. Run the actual testing blocks as specified in 'experiment_info'.
    6. Display a concluding message and await a keypress from the experimenter.
    7. Close the experiment window and end the experiment.

    Note:
    - The function assumes the presence of several global variables ('title_screen', 'intro1', 'intro2', 'end_experiment', 
      'n_trials_train', 'n_trials_test', and 'experimenter_key', etc.) and helper functions ()'show_info_dialog', 
      'display_instructions', 'run_training_block', and 'run_test_block', etc.)
    
    Returns:
    -None. 
    """
    # Show experiment info dialog
    experiment_info = show_info_dialog(experiment_info, popped_keys)

    # Set up the experiment window
    win = visual.Window(fullscr=True, color="black", units="norm")
    win.mouseVisible = False

    # Display introduction and task instructions
    display_instructions(win, [title_screen, intro1, intro2])

    # Run the training block
    if experiment_info['training']:
        run_training_block(win, n_trials_train)

    # Run the real test block
    n_blocks = experiment_info['testing']
    if n_blocks:
        for block in range(1, n_blocks + 1):
            run_test_block(win, n_trials_test, block)
    
    # Display end-of-experiment slide
    display_instructions(win, [end_experiment], continue_key=experimenter_key)

    # End the experiment
    win.close()

###############################################################################
################################ Run experiment ###############################
###############################################################################

if __name__ == '__main__':
    main_experiment(experiment_info)
