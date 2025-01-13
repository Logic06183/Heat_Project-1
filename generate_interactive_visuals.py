import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Create directory for interactive plots if it doesn't exist
os.makedirs('interactive_plots', exist_ok=True)

# Define the order of stages for consistent visualization
stage_order = [
    'Contact procedures not initiated',
    '1st or 2nd invites',
    '3rd or more invites',
    'Next steps/application sent',
    'Park',
    'Entering into DTA',
    'Batch to send to Ethics',
    'Transfer of data in progress',
    'Data sets in hand',
    'Health check in progress',
    'Harmonization in progress',
    'Geo-coding in progress',
    'Database finalized',
    'Data currently unavailable',
    'Declined Participation'
]

color_map = {
    'Contact procedures not initiated': '#1f77b4',  # Blue
    '1st or 2nd invites': '#ff7f0e',  # Orange
    '3rd or more invites': '#2ca02c',  # Green
    'Next steps/application sent': '#d62728',  # Red
    'Park': '#9467bd',  # Purple
    'Entering into DTA': '#8c564b',  # Brown
    'Batch to send to Ethics': '#e377c2',  # Pink
    'Transfer of data in progress': '#7f7f7f',  # Gray
    'Data sets in hand': '#bcbd22',  # Olive
    'Health check in progress': '#17becf',  # Cyan
    'Harmonization in progress': '#1a55FF',  # Blue
    'Geo-coding in progress': '#c49c94',  # Light brown
    'Database finalized': '#f7b6d2',  # Light pink
    'Data currently unavailable': '#c7c7c7',  # Light gray
    'Declined Participation': '#98df8a'  # Light green
}

def create_combined_plot(df, name):
    """Create a combined figure with both donut and bar charts"""
    # Create subplot figure
    fig = make_subplots(
        rows=2, cols=1,
        specs=[[{"type": "pie"}],
               [{"type": "bar"}]],
        vertical_spacing=0.1,
        subplot_titles=(f"{name} Latest Month Distribution", f"{name} Progress Over Time"),
        row_heights=[0.4, 0.6]
    )

    # Get latest month data for donut chart
    latest_month = df.columns[-1]
    latest_data = df[df['Stage'] != 'Total'].copy()
    latest_data = latest_data.set_index('Stage').reindex(stage_order)

    # Add donut chart
    fig.add_trace(
        go.Pie(
            labels=latest_data.index,
            values=latest_data[latest_month],
            hole=.4,
            marker_colors=[color_map[stage] for stage in latest_data.index],
            hovertemplate="Stage: %{label}<br>Studies: %{value}<extra></extra>",
            showlegend=True
        ),
        row=1, col=1
    )

    # Add bar chart traces
    months = df.columns[1:]  # Skip 'Stage' column
    for stage in stage_order:
        if stage in df['Stage'].values:
            fig.add_trace(
                go.Bar(
                    name=stage,
                    x=months,
                    y=df[df['Stage'] == stage].iloc[:, 1:].values[0],
                    marker_color=color_map[stage],
                    hovertemplate=f"Stage: {stage}<br>Month: %{{x}}<br>Studies: %{{y}}<extra></extra>"
                ),
                row=2, col=1
            )

    # Calculate monthly totals for annotations
    monthly_totals = df[months].sum()

    # Update layout
    fig.update_layout(
        title=f"{name} Data Acquisition Progress",
        barmode='stack',
        showlegend=True,
        legend_title_text='Stages',
        height=1000,
        margin=dict(t=100, b=50, l=50, r=50),
        annotations=[
            dict(
                x=month,
                y=total,
                text=f'N={int(total)}',
                showarrow=False,
                yshift=10,
                xref='x2',
                yref='y2'
            ) for month, total in monthly_totals.items()
        ] + [
            dict(
                text=f'N={int(latest_data[latest_month].sum())}',
                x=0.5, y=0.5,
                font_size=20,
                showarrow=False,
                xref='paper',
                yref='paper'
            )
        ]
    )

    # Update axes
    fig.update_xaxes(title_text="Month", row=2, col=1)
    fig.update_yaxes(title_text="Number of Studies", row=2, col=1)

    return fig

def process_data():
    """Process CSV data and create interactive visualizations"""
    # Read the CSV files
    johannesburg_df = pd.read_csv('johannesburg_data.csv')
    abidjan_df = pd.read_csv('abidjan_data.csv')
    rp1_df = pd.read_csv('rp1_data.csv')
    
    # Create visualizations for each dataset
    for df, name in [(rp1_df, 'RP1'), (johannesburg_df, 'Johannesburg'), (abidjan_df, 'Abidjan')]:
        # Create combined plot
        fig = create_combined_plot(df, name)
        
        # Save the figure with full HTML
        fig.write_html(
            f'interactive_plots/{name.lower()}_progress.html',
            include_plotlyjs=True,
            full_html=True,
            config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': f'{name.lower()}_progress',
                    'height': 1000,
                    'width': 1200,
                    'scale': 2
                }
            }
        )

def main():
    process_data()

if __name__ == "__main__":
    main()
