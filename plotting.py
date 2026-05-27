import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_interactive_plot(df):
    """
    Create an interactive plot showing Power and Heart Rate over time.
    """
    if 'PowerOriginal' not in df.columns:
        return go.Figure()
    
    # Create secondary y-axis if HeartRate exists
    if 'HeartRate' in df.columns:
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{"secondary_y": True}]]
        )
        
        # Add Power trace
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['PowerOriginal'],
                name='Leistung (W)',
                line=dict(color='blue'),
                yaxis='y'
            ),
            secondary_y=False
        )
        
        # Add Heart Rate trace
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['HeartRate'],
                name='Herzfrequenz (bpm)',
                line=dict(color='red'),
                yaxis='y2'
            ),
            secondary_y=True
        )
        
        # Update layout
        fig.update_layout(
            title="Leistung und Herzfrequenz über Zeit",
            xaxis_title="Messpunkt",
            hovermode='x unified'
        )
        
        fig.update_yaxes(title_text="Leistung (W)", secondary_y=False)
        fig.update_yaxes(title_text="Herzfrequenz (bpm)", secondary_y=True)
    else:
        # Single plot if no heart rate data
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['PowerOriginal'],
                name='Leistung (W)',
                line=dict(color='blue')
            )
        )
        
        fig.update_layout(
            title="Leistung über Zeit",
            xaxis_title="Messpunkt",
            yaxis_title="Leistung (W)"
        )
    
    return fig
