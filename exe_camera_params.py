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

def run_exe(work_directory, rig_path, color_path):
    exec_dir = r"C:\temp\DeviceParamsApp"  # Update this to the actual executable directory
    exe_path = os.path.join(exec_dir, "DeviceParameters.exe")
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
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Filter out the undesired error message
        filtered_output = result.stdout.replace("ERROR, the log config in C:\\Users\\user\\Desktop\\DeviceParamsApp\\Logs\\LogConfig.ecfg is invalid.\n", "")

        # Print the filtered output
        print(filtered_output)

        print("Execution successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def process_folders(base_directory, exe_path):
    log_paths = []
    pairs_found = False

    for root, dirs, files in os.walk(base_directory):
        colorrig_files = [file for file in files if file.lower().endswith('colorrig.txt')]

        for colorrig_file in colorrig_files:
            rig_file = colorrig_file.replace('colorrig.txt', 'rig.txt')
            rig_path = os.path.join(root, rig_file)
            colorrig_path = os.path.join(root, colorrig_file)

            print(f"Processing: {root}")
            print(f"{Fore.YELLOW}rig_path: {rig_path}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}colorrig_path: {colorrig_path}{Style.RESET_ALL}")


            run_exe(root, rig_path, colorrig_path)

            # Write new executable paths to DeviceParameters.log in each work directory
            log_path = os.path.join(root, "DeviceParameters.log")
            log_paths.append(log_path)
            with open(log_path, 'w') as file:
                file.write(f"Executable Path: {exe_path}\n")
                file.write(f"Work Directory: {root}\n")
                file.write(f"Rig Path: {rig_path}\n")
                file.write(f"ColorRig Path: {colorrig_path}\n")
                file.write("\n")

            pairs_found = True

    if not pairs_found:
        print(f"\n{Fore.YELLOW}No rig and colorrig pairs found in: {base_directory}{Style.RESET_ALL}")

    if pairs_found:
        print(f"\n{Fore.CYAN}New files of Device parameters are here:{Style.RESET_ALL}")
        for log_path in log_paths:
            print(f"{Fore.GREEN}{log_path}{Style.RESET_ALL}")

if __name__ == "__main__":
    # Ask the user for the base directory
    base_directory = input("Enter the base directory path: ")

    # Define the executable path
    exe_path = os.path.join(r"C:\Users\user\Desktop\DeviceParamsApp", "DeviceParameters.exe")

    # Process folders and find rig-colorrig pairs
    process_folders(base_directory, exe_path)

    # Add this line to keep the console window open until user input
    input("Press Enter to exit...")
