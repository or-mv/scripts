import pandas as pd
import plotly.graph_objs as go

def read_and_process_csv(csv_path):
    df = pd.read_csv(csv_path)

    unique_stream_ids = df['StreamId'].unique()

    def plot_figures(stream_id):
        stream_data_scale = df[(df['StreamId'] == stream_id) & (df['ScaleInMm'] != 0)]

        # Additional columns to include
        additional_columns = ['ScaleInMm', 'Col1AvgError', 'Col2AvgError', 'C2CAvgError']

        fig = go.Figure()

        for col in additional_columns:
            stream_data_col = df[(df['StreamId'] == stream_id) & (df[col] != 0)]
            if not stream_data_col.empty:
                average_col = stream_data_col[col].mean()
                fig.add_trace(go.Scatter(x=stream_data_col.index, y=stream_data_col[col],
                                         mode='markers', marker=dict(size=10), name=col))
                fig.add_annotation(text=f'Average {col}: {average_col:.2f}', x=0.5, y=0.9 - additional_columns.index(col) * 0.1,
                                   xref='paper', yref='paper', showarrow=False, font=dict(size=14, color='black'))

        fig.update_layout(title=f'Stream {stream_id} - Additional Columns', xaxis_title='Data Point Index', showlegend=True)
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black')

        fig.show()

    for stream_id in unique_stream_ids:
        plot_figures(stream_id)

# Get the CSV file path from the user
csv_path = input("Please provide the path to the CSV file: ")
read_and_process_csv(csv_path)
