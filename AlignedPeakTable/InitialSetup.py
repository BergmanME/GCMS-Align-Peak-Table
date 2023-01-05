def directory():
    '''asks user to select the working directory'''
    from tkinter import filedialog
    filepath=filedialog.askdirectory(initialdir=r"Documents", title="Select working directory")
    return(filepath)

'''get working directory'''
directory_path = directory()
counter = 0
while directory_path is None and counter < 3:
    '''ask for folder 3 times'''
    print("please select a folder")
    directory_path = directory()
    counter = counter + 1
print(f'Working directory selected:\n{directory_path}')

def get_folders(withdate):
    '''makes the input and output folders if they do not exist, and returns the paths'''
    import os
    if withdate is True: # adds the data to the folder name
        from datetime import datetime
        date = datetime.date(datetime.now())
        input_folder = "Input_Data_" + str(date)
        output_folder = "Output_Data_" + str(date)
    else: # more general folder names
        input_folder = "Input_Data"
        output_folder = "Output_Data"
    # file_path_input = os.path.join(input_folder)
    # file_path_output = os.path.join(output_folder)
    file_path_input = f'{directory_path}/{input_folder}'
    file_path_output = f'{directory_path}/{output_folder}'
    os.makedirs(file_path_input, exist_ok=True)
    os.makedirs(file_path_output, exist_ok=True)
    return ([file_path_input, file_path_output])

def scan_settings_error():
    '''prints error information and quits code'''
    print("Unexpected scan settings.\nAcceptable ionization_mode = +CI or +EI.\nAcceptable scan_mode = Scan or SIM\nScript will now close")
    return quit()

class Question:
    def __init__(self, prompt, acceptable_answers):
        self.prompt = prompt
        self.acceptable_answers = acceptable_answers
def ask_questions(questions, return_type):
    answers = []
    indeces = []
    for question in questions:
        valid_response = False
        while valid_response != True:
            answer = input(question.prompt)
            if answer in question.acceptable_answers:
                print("\n")
                index = question.acceptable_answers.index(answer)
                valid_response = True
            else:
                print("Please choose a valid response ", question.acceptable_answers, "\n")
        answers.append(answer)
        indeces.append(index)
    if return_type == 'index':
        return indeces
    else:
        return answers  

def configure_scan_settings(ionization_mode, scan_mode): # sets up the ionization and scan settings for later functions
    if ionization_mode == '+CI':
        if scan_mode == 'Scan':
            areas_scan_type = '+CI TIC Scan'
            spectra_scan_type = '+CI Scan'
        elif scan_mode == 'SIM':
            areas_scan_type = '+CI TIC SIM'
            spectra_scan_type = '+CI SIM'
        else:
            return scan_settings_error()
    elif ionization_mode == '+EI':
        if scan_mode == 'Scan':
            areas_scan_type = '+EI TIC Scan'
            spectra_scan_type = '+EI Scan'
        elif scan_mode == 'SIM':
            areas_scan_type = '+EI TIC SIM'
            spectra_scan_type = '+EI SIM'
        else:
            return scan_settings_error()
    else:
        return scan_settings_error()
    spectra_check_string = f"{ionization_mode} {scan_mode}"
    settings = [spectra_scan_type, areas_scan_type, spectra_check_string]
    return settings

def get_data_type(get_input):
    if get_input is True:
        ionization_modes = [
            "+EI", "+CI NH3", "+CI CH4", "-CI NH3", "-CI CH4"
        ]
        scan_modes = [
            "Scan", "SIM"
        ]
        question_prompts = [
            f"Select the ionization mode\n(a) {ionization_modes[0]}\n(b) {ionization_modes[1]}\n(c) {ionization_modes[2]}\n(d) {ionization_modes[3]}\n(e) {ionization_modes[4]}\nYour choice: ",
            f"Select the scan mode\n(a) {scan_modes[0]}\n(b) {scan_modes[1]}\nYour choice: "
        ]
        questions = [
            Question(question_prompts[0],['a','b','c','d','e']),
            Question(question_prompts[1],['a','b'])
        ]
        answers_as_indeces = ask_questions(questions=questions, return_type='index')
        chosen_ionization_mode = ionization_modes[answers_as_indeces[0]]
        chosen_scan_mode = scan_modes[answers_as_indeces[1]]
        spectra_scan_type = f"{chosen_ionization_mode} {chosen_scan_mode}"
        areas_scan_type = f"{chosen_ionization_mode} TIC {chosen_scan_mode}"
        simple_ionization_modes = [
            "+EI", "+CI", "-CI"
        ]
        chosen_simple_ionization_mode = simple_ionization_modes[answers_as_indeces[0]]
        if chosen_scan_mode == "SIM":
            spectra_check_string = "SIM"
        else:
            spectra_check_string = f"{chosen_simple_ionization_mode} {chosen_scan_mode}"
        settings = [spectra_scan_type, areas_scan_type, spectra_check_string]
    else:
        ionization_mode = get_input[0]
        scan_mode = get_input[1]
        settings = configure_scan_settings(ionization_mode, scan_mode)
    return settings

def initial_setup(withdate, get_input):
    input_output_folders = get_folders(withdate)
    #withdate can be True to have a separate folder each day
    settings = get_data_type(get_input)
    #Requires user input for data type, if False default is +EI
    return(input_output_folders, settings)