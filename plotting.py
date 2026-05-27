import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


# Solid line colors per zone
ZONE_LINE_COLORS = {
    1: ("Zone 1 – Recovery",  "#5B9BD5"),  # blue
    2: ("Zone 2 – Endurance", "#70AD47"),  # green
    3: ("Zone 3 – Tempo",     "#FFD966"),  # yellow
    4: ("Zone 4 – Threshold", "#F4932F"),  # orange
    5: ("Zone 5 – VO2max",    "#FF3333"),  # red
}

# Background fill colors per zone (semi-transparent)
ZONE_BG_COLORS = {
    1: "rgba( 91, 155, 213, 0.12)",
    2: "rgba(112, 173,  71, 0.12)",
    3: "rgba(255, 217, 102, 0.15)",
    4: "rgba(244, 147,  47, 0.15)",
    5: "rgba(255,  51,  51, 0.18)",
}


def _zone_segments(df):
    """Split df into contiguous segments where Zone is constant."""
    segments = []
    if 'Zone' not in df.columns:
        return segments
    current_zone = None
    start = 0
    for i, row in enumerate(df.itertuples()):
        z = row.Zone
        if z != current_zone:
            if current_zone is not None:
                # include one overlap point for continuity
                segments.append((current_zone, df.iloc[start: i + 1]))
            current_zone = z
            start = i
    if current_zone is not None:
        segments.append((current_zone, df.iloc[start:]))
    return segments


def create_interactive_plot(df, max_hr=190):
    """
    Interactive plot: Power (primary y) and Heart Rate (secondary y).
    The HR line is coloured per zone. Zone bands appear in the background.
    """
    if 'PowerOriginal' not in df.columns:
        return go.Figure()

    if 'HeartRate' not in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index, y=df['PowerOriginal'],
            name='Leistung (W)', line=dict(color='royalblue'),
        ))
        fig.update_layout(title="Leistung über Zeit",
                          xaxis_title="Messpunkt",
                          yaxis_title="Leistung (W)")
        return fig

    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])

    # --- Background zone bands (on secondary / HR axis) ---
    zone_boundaries = [
        (1,  0,              max_hr * 0.60),
        (2,  max_hr * 0.60,  max_hr * 0.70),
        (3,  max_hr * 0.70,  max_hr * 0.80),
        (4,  max_hr * 0.80,  max_hr * 0.90),
        (5,  max_hr * 0.90,  max_hr * 1.05),  # a bit above max so band fills
    ]
    for zone_num, y0, y1 in zone_boundaries:
        fig.add_shape(
            type="rect",
            xref="paper", yref="y2",
            x0=0, x1=1, y0=y0, y1=y1,
            fillcolor=ZONE_BG_COLORS[zone_num],
            line_width=0,
            layer="below",
        )

    # --- Legend entries for zones (invisible markers) ---
    legend_added = set()
    for zone_num, (name, color) in ZONE_LINE_COLORS.items():
        fig.add_trace(
            go.Scatter(x=[None], y=[None], mode="markers",
                       marker=dict(size=10, color=color),
                       name=name, showlegend=True),
            secondary_y=True,
        )
        legend_added.add(zone_num)

    # --- Power trace (primary axis, single color) ---
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df['PowerOriginal'],
            name='Leistung (W)',
            line=dict(color='royalblue', width=1.5),
            showlegend=True,
        ),
        secondary_y=False,
    )

    # --- HR line coloured per zone segment ---
    segments = _zone_segments(df)
    first_hr = True
    for zone_num, seg in segments:
        name, color = ZONE_LINE_COLORS.get(zone_num, (f"Zone {zone_num}", "gray"))
        fig.add_trace(
            go.Scatter(
                x=seg.index,
                y=seg['HeartRate'],
                mode='lines',
                line=dict(color=color, width=2),
                name='Herzfrequenz (bpm)' if first_hr else None,
                legendgroup='hr',
                showlegend=first_hr,
                hovertemplate="HF: %{y} bpm<extra>" + name + "</extra>",
            ),
            secondary_y=True,
        )
        first_hr = False

    fig.update_layout(
        title="Leistung & Herzfrequenz über Zeit – eingefärbt nach HF-Zone",
        xaxis_title="Zeit (Messpunkt)",
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_yaxes(title_text="Leistung (W)", secondary_y=False)
    fig.update_yaxes(title_text="Herzfrequenz (bpm)", secondary_y=True)

    return fig
