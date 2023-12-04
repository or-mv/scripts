def plot_figures(stream_id):
    stream_data = df[df['StreamId'] == stream_id]

    fig = go.Figure()

    if 'ScaleInMm' in stream_data.columns:
        scale_data = stream_data[stream_data['ScaleInMm'] != 0]
        average_scale = scale_data['ScaleInMm'].mean()
        fig.add_trace(go.Scatter(x=scale_data.index, y=scale_data['ScaleInMm'], mode='markers', marker=dict(color='blue', size=10, line=dict(width=2, color='DarkSlateGrey')), name='ScaleInMm')

    if 'Col1AvgError' in stream_data.columns:
        col1_data = stream_data[stream_data['Col1AvgError'] != 0]
        average_col1 = col1_data['Col1AvgError'].mean()
        fig.add_trace(go.Scatter(x=col1_data.index, y=col1_data['Col1AvgError'], mode='markers', marker=dict(color='red', size=10, line=dict(width=2, color='DarkSlateGrey')), name='Col1AvgError'))

    if 'Col2AvgError' in stream_data.columns:
        col2_data = stream_data[stream_data['Col2AvgError'] != 0]
        average_col2 = col2_data['Col2AvgError'].mean()
        fig.add_trace(go.Scatter(x=col2_data.index, y=col2_data['Col2AvgError'], mode='markers', marker=dict(color='green', size=10, line=dict(width=2, color='DarkSlateGrey')), name='Col2AvgError'))

    if 'C2CAvgError' in stream_data.columns:
        c2c_data = stream_data[stream_data['C2CAvgError'] != 0]
        average_c2c = c2c_data['C2CAvgError'].mean()
        fig.add_trace(go.Scatter(x=c2c_data.index, y=c2c_data['C2CAvgError'], mode='markers', marker=dict(color='purple', size=10, line=dict(width=2, color='DarkSlateGrey')), name='C2CAvgError'))

    fig.update_layout(title=f'Stream {stream_id} - Scale, Col1AvgError, Col2AvgError, C2CAvgError', xaxis_title='Data Point Index', showlegend=True)
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black')

    if 'ScaleInMm' in stream_data.columns:
        fig.add_annotation(text=f'Average Scale: {average_scale:.2f} mm', x=0.5, y=0.9, xref='paper', yref='paper', showarrow=False, font=dict(size=14, color='black'))

    if 'Col1AvgError' in stream_data.columns:
        fig.add_annotation(text=f'Average Col1AvgError: {average_col1:.2f}', x=0.5, y=0.8, xref='paper', yref='paper', showarrow=False, font=dict(size=14, color='black'))

    if 'Col2AvgError' in stream_data.columns:
        fig.add_annotation(text=f'Average Col2AvgError: {average_col2:.2f}', x=0.5, y=0.7, xref='paper', yref='paper', showarrow=False, font=dict(size=14, color='black'))

    if 'C2CAvgError' in stream_data.columns:
        fig.add_annotation(text=f'Average C2CAvgError: {average_c2c:.2f}', x=0.5, y=0.6, xref='paper', yref='paper', showarrow=False, font=dict(size=14, color='black'))

    fig.show()
