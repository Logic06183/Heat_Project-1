import pandas as pd
import plotly.graph_objects as go
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

def create_donut_chart(df, name):
    """Create a donut chart for the latest month's data"""
    # Get latest month data
    latest_month = df.columns[-1]
    latest_data = df[df.index != 'Total'].copy()
    
    # Filter out stages with zero values
    latest_data = latest_data[latest_data[latest_month] > 0]
    
    # Create donut chart
    fig = go.Figure(data=[go.Pie(
        labels=latest_data.index,
        values=latest_data[latest_month],
        hole=.5,  # Increased hole size
        marker_colors=[color_map[stage] for stage in latest_data.index],
        hovertemplate="Stage: %{label}<br>Studies: %{value}<extra></extra>",
        textinfo='value+percent',  # Show values and percentages
        textposition='inside'
    )])
    
    # Update layout
    fig.update_layout(
        showlegend=True,
        title=dict(
            text=f"{name} Distribution - {latest_month}",
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=20)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5
        ),
        height=600,
        margin=dict(t=100, b=150),  # Increased bottom margin for legend
        annotations=[dict(
            text=f'Total Studies: {int(latest_data[latest_month].sum())}',
            x=0.5, y=0.5,
            font_size=16,
            showarrow=False
        )]
    )
    
    return fig

def create_stacked_bar_chart(df, name):
    """Create an interactive stacked bar chart showing progress"""
    # Create figure
    fig = go.Figure()
    
    # Add traces for each stage
    for stage in stage_order:
        if stage in df.index and stage != 'Total':
            stage_data = df.loc[stage]
            if any(stage_data > 0):  # Only add trace if there's non-zero data
                fig.add_trace(go.Bar(
                    name=stage,
                    x=df.columns,
                    y=stage_data,
                    marker_color=color_map[stage],
                    hovertemplate=f"Stage: {stage}<br>Month: %{{x}}<br>Studies: %{{y}}<extra></extra>"
                ))
    
    # Calculate monthly totals
    monthly_totals = df[df.index != 'Total'].sum()
    
    # Update layout
    fig.update_layout(
        barmode='stack',
        title=dict(
            text=f"{name} Progress Over Time",
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=20)
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5
        ),
        xaxis_title="Month",
        yaxis_title="Number of Studies",
        height=600,
        margin=dict(t=100, b=150),  # Increased bottom margin for legend
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
    
    return fig

def main():
    # Process each dataset
    datasets = {
        'RP1': 'rp1_data.csv',
        'Johannesburg': 'johannesburg_data.csv',
        'Abidjan': 'abidjan_data.csv'
    }
    
    # Remove old files
    for file in os.listdir('interactive_plots'):
        os.remove(os.path.join('interactive_plots', file))
    
    for site_name, file_name in datasets.items():
        if os.path.exists(file_name):
            # Load data
            df = pd.read_csv(file_name, index_col='Stage')
            
            # Create and save donut chart
            donut_fig = create_donut_chart(df, site_name)
            donut_fig.write_html(
                f'interactive_plots/{site_name.lower()}_donut.html',
                include_plotlyjs='cdn',  # Use CDN for plotly.js
                full_html=True,
                config={
                    'displayModeBar': False,  # Hide the modebar
                    'responsive': True  # Make the plot responsive
                }
            )
            
            # Create and save bar chart
            bar_fig = create_stacked_bar_chart(df, site_name)
            bar_fig.write_html(
                f'interactive_plots/{site_name.lower()}_bar.html',
                include_plotlyjs='cdn',  # Use CDN for plotly.js
                full_html=True,
                config={
                    'displayModeBar': False,  # Hide the modebar
                    'responsive': True  # Make the plot responsive
                }
            )

if __name__ == "__main__":
    main()
