import pandas as pd 
def get_csv(return_type, title, initialdir, skip_blank_lines, skiprows):
    '''function for retrieving csv file and returning as indicated format'''
    import tkinter as tk
    from tkinter import filedialog
    import GeneralFunctions
    csvfile = tk.filedialog.askopenfilename(title=title, initialdir=initialdir, filetype=(("CSV files", ".csv"), ("all files", "*.*")))
    file = open(csvfile)
    if return_type == 'lines':
        file_lines = GeneralFunctions.get_file_lines(file)
        file.close()
        return(file_lines)
    elif return_type == 'df' :
        file_df = pd.read_csv(file, skip_blank_lines=skip_blank_lines, skiprows=skiprows)
        file.close()
        return(file_df)
    elif return_type == 'both':
        file_df = pd.read_csv(file, skip_blank_lines=skip_blank_lines, skiprows=skiprows)
        file.close()
        file = open(csvfile)
        file_lines = GeneralFunctions.get_file_lines(file)
        file.close()
        return(file_lines, file_df)
print("defined function for retrieving csv files")

def rename_duplicates(input_series):
    renamed_series = input_series
    series_list = []
    nduplicates = 0
    for item in input_series:
        counter = 1
        new_item = item
        while new_item in series_list:
            nduplicates += 1
            counter += 1
            new_item = item + '_' + str(counter)
        series_list.append(new_item)
    renamed_series_values = pd.Series(series_list)
    return renamed_series_values, nduplicates

