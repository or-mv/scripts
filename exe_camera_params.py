import os
import subprocess
from colorama import Fore, Style, init

# Initialize colorama
init()

def find_rig_colorrig_pairs(directory):
    rig_colorrig_pairs = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('rig.txt') or file.lower().endswith('colorrig.txt'):
                rig_colorrig_pairs.append((root, file))
                break  # Break to ensure only one pair is added per directory
    return rig_colorrig_pairs

def run_exe(work_directory, rig_path, color_path, exe_path):
    print(f"PATHS are: {color_path} and {rig_path}")

    # Construct the command to run the executable
    command = [
        exe_path,
        "-printVersion", "All",
        "-workDirectoryName", work_directory,
        "-rig", rig_path,
        "-colorRig", color_path
    ]

    try:
        # Call the executable with the provided arguments
        subprocess.run(command, check=True)

        print("Execution successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def process_folders(base_directory, exe_path):
    log_paths = []
    only_rig_paths = []

    for root, dirs, files in os.walk(base_directory):
        colorrig_files = [file for file in files if file.lower().endswith('colorrig.txt')]

        for colorrig_file in colorrig_files:
            rig_file = colorrig_file.replace('colorrig.txt', 'rig.txt')
            rig_path = os.path.join(root, rig_file)
            colorrig_path = os.path.join(root, colorrig_file)

            print(f"Processing: {root}")
            print(f"{Fore.YELLOW}rig_path: {rig_path}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}colorrig_path: {colorrig_path}{Style.RESET_ALL}")

            run_exe(root, rig_path, colorrig_path, exe_path)

            # Add the log path to the list
            log_path = os.path.join(root, "DeviceParameters.log")
            log_paths.append(log_path)

        # Check if no colorrig suffix is found and work only with rig file
        if not colorrig_files:
            rig_files = [file for file in files if file.lower().endswith('rig.txt')]
            for rig_file in rig_files:
                rig_path = os.path.join(root, rig_file)
                print(f"{Fore.YELLOW}Working with only rig file: {rig_path}{Style.RESET_ALL}")
                run_exe(root, rig_path, "", exe_path)

                # Add the log path to the list
                log_path = os.path.join(root, "DeviceParameters.log")
                only_rig_paths.append(log_path)

    # Print all DeviceParameters.log paths from rig and colorrig pairs
    if log_paths:
        print(f"\n{Fore.CYAN}New files of Device parameters from rig and colorrig are here:{Style.RESET_ALL}")
        unique_log_paths = list(set(log_paths))  # Remove duplicates
        for log_path in unique_log_paths:
            print(f"{Fore.GREEN}{log_path}{Style.RESET_ALL}")

    # Print only rig paths if they are present
    if only_rig_paths:
        print(f"\n{Fore.YELLOW}Working with only rig file:{Style.RESET_ALL}")
        unique_rig_paths = list(set(only_rig_paths))  # Remove duplicates
        for rig_path in unique_rig_paths:
            print(f"{Fore.GREEN}{rig_path}{Style.RESET_ALL}")


if __name__ == "__main__":
    # Ask the user for the base directory
    base_directory = input("Enter the base directory path: ")

    # Define the executable path
    exe_path = os.path.join(r"C:\Users\user\Desktop\DeviceParamsApp", "DeviceParameters.exe")

    # Process folders and find rig-colorrig pairs
    process_folders(base_directory, exe_path)

    # Add this line to keep the console window open until user input
    input("Press Enter to exit...")
