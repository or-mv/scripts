import pandas as pd
import matplotlib.pyplot as plt

def read_and_process_csv():
    # Ask user for CSV file path
    csv_path = input("Enter the path to the CSV file: ")

    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Get unique values in the StreamId column
    unique_stream_ids = df['StreamId'].unique()

    # Process data for each unique StreamId
    for stream_id in unique_stream_ids:
        # Filter data for the current StreamId and ignore 0 values in ScaleInMm
        stream_data = df[(df['StreamId'] == stream_id) & (df['ScaleInMm'] != 0)]

        # Check calibration status based on ScaleInMm column
        calibration_status = 100  # Default to 100%
        if any(abs(stream_data['ScaleInMm'] - 322) > 0.3):
            calibration_status -= 10

        # Calculate the average of the "ScaleInMm" column
        average_scale = stream_data['ScaleInMm'].mean()

        # Visual representation (Scatter plot using "ScaleInMm" for X axis)
        plt.figure(figsize=(15, 8))  # Larger diagram and text area
        plt.scatter(range(len(stream_data)), stream_data['ScaleInMm'], c='turquoise', label=f'Stream {stream_id}')

        # Customize the plot as needed
        plt.xlabel('Data Point Index')
        plt.ylabel('ScaleInMm')

        # Set X-axis ticks at 0.50 intervals
        plt.xticks(range(0, len(stream_data), 50), [f'{i * 0.50:.2f}' for i in range(0, len(stream_data), 50)])

        # Set Y-axis ticks at 0.5 mm intervals
        min_scale = max(0, int(min(stream_data['ScaleInMm'])))
        max_scale = int(max(stream_data['ScaleInMm'])) + 1
        plt.yticks([i * 0.5 for i in range(min_scale * 2, max_scale * 2)])

        # Display calibration status and average scale two lines higher above the plot
        plt.text(0.1, 1.1, f'Average Scale: {average_scale:.2f} mm', ha='left', va='center', fontsize=14, transform=plt.gca().transAxes)
        plt.text(0.9, 1.1, f'Calibration status is {calibration_status}%', ha='right', va='center', fontsize=14, transform=plt.gca().transAxes)
        plt.text(0.5, 1.1, f'Stream {stream_id} Calibration Results', ha='center', va='center', fontsize=14, transform=plt.gca().transAxes)

        # Save or display the visual results for each StreamId
        plt.savefig(f'calibration_result_stream_{stream_id}.png', bbox_inches='tight')  # Save each plot with a unique filename
        plt.show()

# Call the function
read_and_process_csv()
