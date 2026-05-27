import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Zone definitions: (name, color, opacity)
ZONE_COLORS = {
    1: ("Zone 1 – Recovery",   "rgba(173, 216, 230, 0.25)"),  # light blue
    2: ("Zone 2 – Endurance",  "rgba(144, 238, 144, 0.25)"),  # light green
    3: ("Zone 3 – Tempo",      "rgba(255, 255, 102, 0.25)"),  # yellow
    4: ("Zone 4 – Threshold",  "rgba(255, 165,   0, 0.25)"),  # orange
    5: ("Zone 5 – VO2max",     "rgba(255,  80,  80, 0.25)"),  # red
}


def _add_zone_backgrounds(fig, df, max_hr):
    """Add colored horizontal bands for each HR zone onto the secondary y-axis."""
    zone_boundaries = [
        (1, 0,            max_hr * 0.60),
        (2, max_hr * 0.60, max_hr * 0.70),
        (3, max_hr * 0.70, max_hr * 0.80),
        (4, max_hr * 0.80, max_hr * 0.90),
        (5, max_hr * 0.90, max_hr * 1.00),
    ]

    shown_in_legend = set()
    for zone_num, y0, y1 in zone_boundaries:
        name, color = ZONE_COLORS[zone_num]
        show = zone_num not in shown_in_legend
        shown_in_legend.add(zone_num)

        fig.add_hrect(
            y0=y0, y1=y1,
            fillcolor=color,
            line_width=0,
            layer="below",
            annotation_text=name,
            annotation_position="top left",
            annotation=dict(font_size=10, font_color="gray"),
        )

    return fig


def create_interactive_plot(df, max_hr=190):
    """
    Create an interactive plot showing Power and Heart Rate over time,
    with coloured heart rate zone bands in the background.
    """
    if 'PowerOriginal' not in df.columns:
        return go.Figure()

    if 'HeartRate' in df.columns:
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{"secondary_y": True}]]
        )

        # --- Zone background bands (drawn on secondary y-axis / HR axis) ---
        zone_boundaries = [
            (1, 0,             max_hr * 0.60),
            (2, max_hr * 0.60, max_hr * 0.70),
            (3, max_hr * 0.70, max_hr * 0.80),
            (4, max_hr * 0.80, max_hr * 0.90),
            (5, max_hr * 0.90, max_hr * 1.00),
        ]

        for zone_num, y0, y1 in zone_boundaries:
            name, color = ZONE_COLORS[zone_num]
            # Invisible scatter on secondary axis to anchor the hrect to y2
            fig.add_trace(
                go.Scatter(
                    x=[None], y=[None],
                    mode="markers",
                    marker=dict(size=10, color=color.replace("0.25", "0.7")),
                    name=name,
                    showlegend=True,
                ),
                secondary_y=True,
            )

        # Add coloured background via shapes
        for zone_num, y0, y1 in zone_boundaries:
            name, color = ZONE_COLORS[zone_num]
            fig.add_shape(
                type="rect",
                xref="paper", yref="y2",
                x0=0, x1=1,
                y0=y0, y1=y1,
                fillcolor=color,
                line_width=0,
                layer="below",
            )

        # --- Power trace (primary y-axis) ---
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['PowerOriginal'],
                name='Leistung (W)',
                line=dict(color='royalblue', width=1.5),
            ),
            secondary_y=False,
        )

        # --- Heart Rate trace (secondary y-axis) ---
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['HeartRate'],
                name='Herzfrequenz (bpm)',
                line=dict(color='crimson', width=1.5),
            ),
            secondary_y=True,
        )

        fig.update_layout(
            title="Leistung und Herzfrequenz über Zeit (mit HF-Zonen)",
            xaxis_title="Zeit (Messpunkt)",
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )

        fig.update_yaxes(title_text="Leistung (W)", secondary_y=False)
        fig.update_yaxes(title_text="Herzfrequenz (bpm)", secondary_y=True)

    else:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['PowerOriginal'],
                name='Leistung (W)',
                line=dict(color='royalblue'),
            )
        )
        fig.update_layout(
            title="Leistung über Zeit",
            xaxis_title="Messpunkt",
            yaxis_title="Leistung (W)",
        )

    return fig
