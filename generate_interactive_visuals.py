import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

def process_data():
    """Process CSV data and create interactive visualizations"""
    # Read the CSV files
    johannesburg_df = pd.read_csv('johannesburg_data.csv')
    abidjan_df = pd.read_csv('abidjan_data.csv')
    rp1_df = pd.read_csv('rp1_data.csv')
    
    # Create visualizations for each dataset
    for df, name in [(rp1_df, 'rp1'), (johannesburg_df, 'johannesburg'), (abidjan_df, 'abidjan')]:
        # Get the latest month's data
        latest_month = df.columns[-1]
        latest_data = df[df['Stage'] != 'Total'].copy()
        latest_data = latest_data.set_index('Stage').reindex(stage_order)
        
        # Create donut chart
        donut = go.Figure(data=[go.Pie(
            labels=latest_data.index,
            values=latest_data[latest_month],
            hole=.4,
            marker_colors=[color_map[stage] for stage in latest_data.index],
            hovertemplate="Stage: %{label}<br>Studies: %{value}<extra></extra>"
        )])
        
        # Update donut layout
        donut.update_layout(
            title=f"{name.capitalize()} Distribution - {latest_month}",
            showlegend=True,
            legend_title_text='Stages',
            height=500,
            annotations=[dict(
                text=f'N={int(latest_data[latest_month].sum())}',
                x=0.5, y=0.5,
                font_size=20,
                showarrow=False
            )]
        )
        
        # Create stacked bar chart
        bar = go.Figure()
        months = df.columns[1:]  # Skip 'Stage' column
        
        for stage in stage_order:
            if stage in df['Stage'].values:
                bar.add_trace(go.Bar(
                    name=stage,
                    x=months,
                    y=df[df['Stage'] == stage].iloc[:, 1:].values[0],
                    marker_color=color_map[stage],
                    hovertemplate=f"Stage: {stage}<br>Month: %{{x}}<br>Studies: %{{y}}<extra></extra>"
                ))
        
        # Update bar layout
        monthly_totals = df[months].sum()
        bar.update_layout(
            title=f"{name.capitalize()} Progress Over Time",
            barmode='stack',
            showlegend=True,
            legend_title_text='Stages',
            xaxis_title='Month',
            yaxis_title='Number of Studies',
            height=600,
            hovermode='closest',
            annotations=[
                dict(
                    x=month,
                    y=total,
                    text=f'N={int(total)}',
                    showarrow=False,
                    yshift=10
                ) for month, total in monthly_totals.items()
            ]
        )
        
        # Save charts
        donut.write_html(f'interactive_plots/{name}_donut.html', include_plotlyjs='cdn', full_html=False)
        bar.write_html(f'interactive_plots/{name}_bar.html', include_plotlyjs='cdn', full_html=False)

def main():
    process_data()

if __name__ == "__main__":
    main()
