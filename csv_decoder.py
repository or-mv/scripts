import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def read_and_process_csv(csv_path):
    # Adjust the CSV path if it contains double backslashes
    csv_path = csv_path.replace("\\\\", "\\")

    # Remove double quotes if present
    csv_path = csv_path.strip('"')

    df = pd.read_csv(csv_path)

    unique_stream_ids = df['StreamId'].unique()

    def plot_scale_figure(stream_id):
        stream_data_scale = df[(df['StreamId'] == stream_id) & (df['ScaleInMm'] != 0)]

        fig_scale = go.Figure()

        if not stream_data_scale.empty:
            average_scale = stream_data_scale['ScaleInMm'].mean()
            fig_scale.add_trace(go.Scatter(x=stream_data_scale.index, y=stream_data_scale['ScaleInMm'],
                                          mode='markers', marker=dict(size=10), name='ScaleInMm'))
            fig_scale.add_annotation(text=f'Average ScaleInMm: {average_scale:.2f}', x=0.5, y=0.9,
                                     xref='paper', yref='paper', showarrow=False, font=dict(size=14))

        fig_scale.update_layout(title=f'Stream {stream_id} - ScaleInMm', showlegend=True)

        return fig_scale

    def plot_error_figures(stream_id):
        stream_data = df[(df['StreamId'] == stream_id)]

        fig_errors = go.Figure()

        # Additional columns to include
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

        fig_errors.update_layout(title=f'Stream {stream_id} - Error Values', showlegend=True)

        return fig_errors

    def calculate_calibration_rate(average_scale, avg_error_col1, avg_error_col2, avg_error_c2c):
        rate = 100

        if abs(average_scale - 322) >= 2:
            rate -= 20

        for avg_error in [avg_error_col1, avg_error_col2, avg_error_c2c]:
            if avg_error > 2:
                rate -= 5 * ((avg_error - 2) // 0.5)

        return max(0, rate)

    # Iterate over unique_stream_ids after defining it
    for stream_id in unique_stream_ids:
        fig_scale = plot_scale_figure(stream_id)
        fig_errors = plot_error_figures(stream_id)

        fig_scale.show()
        fig_errors.show()

# Get the CSV file path from the user
csv_path = input("Please provide the path to the CSV file: ")
read_and_process_csv(csv_path)
