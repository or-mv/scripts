import pandas as pd
import matplotlib.pyplot as plt

def read_and_process_csv(csv_path):
    df = pd.read_csv(csv_path)
    calibration_status = 100
    average_scale = 0

    if 'StreamId' in df.columns and 'ScaleInMm' in df.columns and 'C2CErrVariance' in df.columns:
        unique_stream_ids = df['StreamId'].unique()
        
        def plot_scale_figures(stream_id):
            stream_data = df[(df['StreamId'] == stream_id) & (df['ScaleInMm'] != 0)]
            
            calibration_status = 100
            
            if any(abs(stream_data['ScaleInMm'] - 322) > 0.3):
                calibration_status -= 10

            average_scale = stream_data['ScaleInMm'].mean()
            
            plt.figure(figsize=(15, 8))
            plt.scatter(range(len(stream_data)), stream_data['ScaleInMm'], c='turquoise', label=f'ScaleInMm')
            plt.xlabel('Data Point Index')
            plt.ylabel('ScaleInMm')
            plt.title(f'Stream {stream_id} ScaleInMm')

            if len(stream_data) > 0:
                plt.text(0.5, 0.9, f'Average Scale: {average_scale:.2f} mm', ha='center', va='center', fontsize=14, transform=plt.gca().transAxes)
            
            plt.show()

        def plot_c2c_variance_figures(stream_id):
            stream_data = df[(df['StreamId'] == stream_id) & (df['ScaleInMm'] != 0)]
            c2c_err_variance = stream_data['C2CErrVariance']

            plt.figure(figsize=(15, 8))
            for i, val in enumerate(c2c_err_variance):
                if val > 2:
                    plt.scatter(i, val, c='red', label='C2CErrVariance')
                else:
                    plt.scatter(i, val, c='green', label='C2CErrVariance')

            plt.xlabel('Data Point Index')
            plt.ylabel('C2CErrVariance')
            plt.title(f'Stream {stream_id} C2CErrVariance')

            if len(c2c_err_variance) > 0:
                average_c2c = sum(c2c_err_variance) / len(c2c_err_variance)
                plt.text(0.5, 0.9, f'Average C2CErrVariance: {average_c2c:.2f}', ha='center', va='center', fontsize=14, transform=plt.gca().transAxes)
            
            plt.show()

        if len(unique_stream_ids) > 0:
            stream_id = unique_stream_ids[0]
            plot_scale_figures(stream_id)
            plot_c2c_variance_figures(stream_id)
        else:
            print("No valid data found.")
    else:
        print("Required columns (StreamId, ScaleInMm, C2CErrVariance) not found in the CSV.")

# Get the CSV file path from the user
csv_path = input("Please provide the path to the CSV file: ")
read_and_process_csv(csv_path)
