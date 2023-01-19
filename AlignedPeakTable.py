print("Starting Script")
'''Install necessary packages'''
import os, sys
import pandas as pd

install_packages = False
if install_packages is True:
    import subprocess

    #implement pip as a subprocess:
    try:
        list_of_packages = ['numpy', 'pandas', 'tkinter']
        for package_name in list_of_packages:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
    except:
        print("error installing packages")

'''make sure python knows where to look for modules'''
designatemodules = True
if designatemodules is True:
    # print('designating module location')           
    pathname = os.path.dirname(sys.argv[0])        
    # print('full path =', os.path.abspath(pathname))
    test_modules_path = pathname + "/AlignedPeakTable"
    sys.path.insert(0, test_modules_path)
    print(f"Added {test_modules_path} as modules folder")

'''Old designation for modules'''
# designatemodules=False
# if designatemodules is True:
#     cwd = os.getcwd()
#     print(cwd)
#     modules_path = cwd + "\AlignedPeakTable"
#     sys.path.insert(0, modules_path)
#     print(f"Added {modules_path} as modules folder")



'''set up the working directory and folders'''
import InitialSetup
initial_setup_output = InitialSetup.initial_setup(withdate=False, get_input=True)
file_path_input, file_path_output=initial_setup_output[0]
spectra_scan_type, areas_scan_type, spectra_check_string = initial_setup_output[1]
print(f'{areas_scan_type} type selected')
print(f"Copy input files to {file_path_input}\n")
print("Initial setup complete")

'''Fetch profile in both formats'''
import GeneralFunctions
# profile_lines, profile_df = get_csv(return_type='both', title='Profile', initialdir=file_path_input)
profile_df = GeneralFunctions.get_csv(return_type='df', title='Profile', initialdir=file_path_input, skip_blank_lines=False, skiprows=None)
# can change the return type to lines once I add legacy functionality back in
print(f"profile file imported containing {max(profile_df.count())} features")

'''Check profile for duplicate features and rename them'''
input_series = profile_df['Peak']
profile_df['Peak'], nduplicates = GeneralFunctions.rename_duplicates(input_series)
# profile_df.head()
if nduplicates == 0:
    print("No duplicate feature names found in profile")
else:
    print(f'{nduplicates} duplicates found in list of profile features')

'''Get Peak Areas and align peak table according to profile'''
import PeakAreaFunctions
PeakAreaFunctions.process_areas(file_path_input, file_path_output, profile_df)
# areas_df = PeakAreasFunctions.get_areas_df(file_path_input)