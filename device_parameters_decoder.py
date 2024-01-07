import sys
import os
import matplotlib.pyplot as plt
import re
import mplcursors

def is_valid_path(path):
    """
    Check if the given path is a valid file path.
    """
    return os.path.isfile(path)

# Check if log file path is provided as a command-line argument
if len(sys.argv) == 2:
    log_file = sys.argv[1]
    if not is_valid_path(log_file):
        print("Invalid path. Please enter a valid file path.")
        sys.exit(1)
else:
    # Ask the user for the log file path if not provided or invalid
    try:
        log_file = input("Enter the path to your log file: ")
        while not is_valid_path(log_file):
            print("Invalid path. Please enter a valid file path.")
            log_file = input("Enter the path to your log file: ")
    except EOFError:
        sys.exit(1)

# Read the log file and parse the data using regular expressions
data = {}
with open(log_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        match = re.match(r'\s*([\d.-]+)\s*:\s*(.*)', line)
        if match:
            value = float(match.group(1))
            key = match.group(2).strip()
            data[key] = value

# Define the parameter ranges
ranges = {
    'Baseline [mm]': (1, 2),
    'NeighborDist [pix]': (2, 3),
    'Camera focal length [pix]': (2, 3),
    'Camera Center of Projection (X) [pix]': (400, 600),
    'Camera Center of Projection (Y) [pix]': (500, 700),
    'Projector focal length [pix]': (300, 400),
    'Projector Center of Projection (X) [pix]': (50, 100),
    'Projector Center of Projection (Y) [pix]': (40, 80),
    'Angle of epipolar line in camera [°]': (-2, 2),
    'Angle of epipolar line in projector [°]': (-15, -10),
    'Projector pattern angle in camera [°]': (-15, -10),
    'Projector x tilt [°]': (-2, 2),
    'Camera y tilt [°]': (-2, 2),
    'Projector y tilt [°]': (-2, 2),
    'Projector x-angle [°]': (-2, 2),
    'Projector y-angle [°]': (-2, 2),
    'Projector z-angle [°]': (-15, -10),
    'Projector x-translation [mm]': (-1, 1),
    'Projector y-translation [mm]': (-1, 1),
    'Projector z-translation [mm]': (-5, 5),
    'RGB Camera x-angle [°]': (-5, 5),
    'RGB Camera y-angle [°]': (-5, 5),
    'RGB Camera z-angle [°]': (-5, 5),
    'RGB Camera x-translation [mm]': (-50, 50),
    'RGB Camera y-translation [mm]': (-50, 50),
    'RGB Camera z-translation [mm]': (-5, 5),
    'IR Camera FOV-x [°]': (50, 60),
    'IR Camera FOV-y [°]': (60, 70),
}

# Plotting and evaluation
fig, ax = plt.subplots(figsize=(10, 12))
bar_colors = ['green' if ranges[param][0] <= value <= ranges[param][1] else 'red' for param, value in data.items()]
bar_heights = list(range(len(data)))

bars = ax.barh(bar_heights, data.values(), color=bar_colors, edgecolor='black')

# Function to display the value when a bar is clicked
def on_bar_click(sel):
    index = sel.target.index
    bar = sel.artist[index]
    x = bar.get_x() + bar.get_width() / 2  # Extract x-coordinate of the bar
    param = list(data.keys())[index]
    plt.gca().text(0.5, -0.1, f'Selected Bar: {param}, Value: {x:.2f}', ha='center', va='top', transform=ax.transAxes, color='white')

# Attach the cursor to the bars
cursor = mplcursors.cursor(hover=True)
cursor.connect("add", on_bar_click)

# Count successes and failures
failures = sum(1 for color in bar_colors if color == 'red')
successes = len(bar_colors) - failures

# Set up the plot details
ax.set_yticks(bar_heights)
ax.set_yticklabels(data.keys())
ax.set_xlabel('Values')

# Set the main title
title = f'Successes: {successes} (Within Range), Failures: {failures} (Out of Range)'
ax.set_title(title, pad=30, color='black')  # Adjust title color here

# Display the input at the top right corner
plt.annotate(f'Input: {log_file}', xy=(1, 1), xytext=(-10, -10), ha='right', va='top', color='black', xycoords='axes fraction', textcoords='offset points')

# Display the plot
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
