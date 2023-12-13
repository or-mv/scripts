import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt



def read_and_process_csv(csv_path):
    csv_path = csv_path.replace("\\\\", "\\")
    csv_path = csv_path.strip('"')
    df = pd.read_csv(csv_path)
    unique_stream_ids = df['StreamId'].unique()
    return df, unique_stream_ids

def plot_scale_figure(df, stream_id):
    stream_data_scale = df[(df['StreamId'] == stream_id) & (df['ScaleInMm'] != 0)]
    fig_scale = go.Figure()

    if not stream_data_scale.empty:
        average_scale = stream_data_scale['ScaleInMm'].mean()
        fig_scale.add_trace(go.Scatter(x=stream_data_scale.index, y=stream_data_scale['ScaleInMm'],
                                      mode='markers', marker=dict(size=10), name='ScaleInMm'))
        fig_scale.add_annotation(text=f'Average ScaleInMm: {average_scale:.2f}', x=0.5, y=0.9,
                                 xref='paper', yref='paper', showarrow=False, font=dict(size=14))

    fig_scale.update_layout(title=f'Stream {stream_id} - ScaleInMm',
                            xaxis_title='Frames',
                            yaxis_title='Millimeters',
                            showlegend=True)

    return fig_scale

def plot_error_figures(df, stream_id):
    stream_data = df[(df['StreamId'] == stream_id)]
    fig_errors = go.Figure()

    additional_columns = ['Col1AvgError', 'Col2AvgError', 'C2CAvgError']

    for col in additional_columns:
        stream_data_col = stream_data[(stream_data[col] != 0)]
        if not stream_data_col.empty:
            average_col = stream_data_col[col].mean()
            fig_errors.add_trace(go.Scatter(x=stream_data_col.index, y=stream_data_col[col],
                                           mode='markers', marker=dict(size=10), name=col))
            fig_errors.add_annotation(text=f'Average {col}: {average_col:.2f}', x=0.5,
                                      y=0.9 - additional_columns.index(col) * 0.1,
                                      xref='paper', yref='paper', showarrow=False, font=dict(size=14))

    calibration_rate = calculate_calibration_rate(stream_data['ScaleInMm'].mean(),
                                                  stream_data['Col1AvgError'].mean(),
                                                  stream_data['Col2AvgError'].mean(),
                                                  stream_data['C2CAvgError'].mean())

    fig_errors.add_annotation(text=f'<b style="color: green;"> Calibration Rate: {calibration_rate:.2f}</b>',
                              x=0.5, y=1, xref='paper', yref='paper', showarrow=False, font=dict(size=16))

    fig_errors.update_layout(title=f'Stream {stream_id} - Error Values',
                             xaxis_title='Frames',
                             yaxis_title='Pixels',
                             showlegend=True)

    return fig_errors

def calculate_calibration_rate(average_scale, avg_error_col1, avg_error_col2, avg_error_c2c):
    rate = 100

    if abs(average_scale - 322) >= 2:
        rate -= 20

    for avg_error in [avg_error_col1, avg_error_col2, avg_error_c2c]:
        if avg_error > 2:
            rate -= 5 * ((avg_error - 2) // 0.5)

    return max(0, rate)

# Get the CSV file path from the user
csv_path = input("Please provide the path to the CSV file: ")

# Call the function and get df, unique_stream_ids
df, unique_stream_ids = read_and_process_csv(csv_path)

# Iterate over unique_stream_ids after defining it
for stream_id in unique_stream_ids:
    fig_scale = plot_scale_figure(df, stream_id)
    fig_errors = plot_error_figures(df, stream_id)

    fig_scale.show()
    fig_errors.show()

    # # Check if the required columns exist in the DataFrame
    # if 'FrameID' not in df.columns:
    #     print("Error: 'FrameID' column is missing in the DataFrame.")
    # if 'MedianEpiDist' not in df.columns:
    #     print("Error: 'MedianEpiDist' column is missing in the DataFrame.")
    # if 'spreadEpiDist' not in df.columns:
    #     print("Error: 'spreadEpiDist' column is missing in the DataFrame.")

    # Create a new figure for FrameID, medianEpiDist, spreadEpiDist
    fig_epi = go.Figure()

    # Check if the new columns exist in the DataFrame
    if 'FrameID' in df.columns and 'medianEpiDist' in df.columns and 'spreadEpiDist' in df.columns:
        # Plot medianEpiDist
        fig_epi.add_trace(go.Scatter(x=df['FrameID'], y=df['medianEpiDist'], mode='lines+markers',
                                    marker=dict(color='pink', size=8), name='MedianEpiDist'))

        # Plot spreadEpiDist
        fig_epi.add_trace(go.Scatter(x=df['FrameID'], y=df['spreadEpiDist'], mode='lines',
                                    line=dict(color='turquoise', dash='dash'), name='SpreadEpiDist'))

        # Annotate average value for medianEpiDist
        average_median = df['medianEpiDist'].mean()
        fig_epi.add_annotation(text=f'Average MedianEpiDist: {average_median:.2f}', x=0.5, y=0.9,
                                xref='paper', yref='paper', showarrow=False, font=dict(size=14),
                                bgcolor='rgba(255, 255, 255, 0.5)')

        # Annotate average value for spreadEpiDist
        average_spread = df['spreadEpiDist'].mean()
        fig_epi.add_annotation(text=f'Average SpreadEpiDist: {average_spread:.2f}', x=0.5, y=0.8,
                                xref='paper', yref='paper', showarrow=False, font=dict(size=14),
                                bgcolor='rgba(255, 255, 255, 0.5)')

        # Calculate rates for medianEpiDist and spreadEpiDist
        rate_median = int((average_median - 0.18) / 0.01)
        rate_spread = int((average_spread - 0.30) / 0.01)
        overall_rate = 100 - (rate_median + rate_spread)


        # Annotate the rate at the top of the plot
        fig_epi.add_annotation(text=f'<b style="color: green;"> Rate: {overall_rate}</b>',
                                x=0.5, y=1, xref='paper', yref='paper', showarrow=False, font=dict(size=16))

        fig_epi.update_layout(title=f'Stream {stream_id} - Epi Values',
                            xaxis_title='Frame',
                            yaxis_title='Pixels',
                            showlegend=True)

        fig_epi.show()
    else:
        print("One or more columns (FrameID, MedianEpiDist, SpreadEpiDist) are missing in the DataFrame.")





