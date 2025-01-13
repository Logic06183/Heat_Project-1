import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Define color scheme for stages
color_map = {
    'Contact procedures not initiated': '#1f77b4',  # Blue
    '1st or 2nd invites': '#ff7f0e',  # Orange
    '3rd or more invites': '#2ca02c',  # Green
    'Next steps/application sent': '#d62728',  # Red
    'Data currently unavailable': '#9467bd',  # Purple
    'Data sets in hand': '#8c564b',  # Brown
    'Transfer of data in progress': '#e377c2',  # Pink
    'Health check in progress': '#7f7f7f',  # Gray
    'Harmonization in progress': '#bcbd22',  # Yellow-green
    'Geo-coding in progress': '#17becf',  # Cyan
    'Database finalized': '#aec7e8',  # Light blue
    'Batch to send to Ethics': '#ffbb78',  # Light orange
    'Entering into DTA': '#98df8a',  # Light green
    'Park': '#ff9896',  # Light red
    'Declined Participation': '#c5b0d5'  # Light purple
}

def load_data(file_path):
    """Load and process CSV data"""
    # Read CSV with 'Stage' as index
    df = pd.read_csv(file_path, index_col='Stage')
    
    # Convert month columns to datetime
    df.columns = pd.to_datetime(df.columns)
    
    # Get the latest month's data
    latest_month = df.columns[-1]
    
    return df

def create_donut_chart(df, site_name):
    """Create a donut chart for the latest month's data"""
    # Get the latest month's data
    latest_month = df.columns[-1]
    latest_data = df[latest_month]
    
    # Define the logical order of stages
    stage_order = [
        'Contact procedures not initiated',
        '1st or 2nd invites',
        '3rd or more invites',
        'Next steps/application sent',
        'Data currently unavailable',
        'Entering into DTA',
        'Data sets in hand',
        'Transfer of data in progress',
        'Health check in progress',
        'Harmonization in progress',
        'Geo-coding in progress',
        'Database finalized',
        'Batch to send to Ethics',
        'Park',
        'Declined Participation'
    ]
    
    # Filter out stages with zero values and maintain the logical order
    non_zero_stages = []
    values = []
    colors = []
    
    for stage in stage_order:
        if stage in latest_data.index and latest_data[stage] > 0:
            non_zero_stages.append(stage)
            values.append(latest_data[stage])
            colors.append(color_map[stage])
    
    # Calculate percentages
    total = sum(values)
    
    if total == 0:
        # If no data, create an empty donut
        fig = go.Figure(data=[go.Pie(
            labels=['No Data'],
            values=[1],
            hole=0.6,
            textinfo='none',
            showlegend=False,
            marker_colors=['#f0f0f0']
        )])
        fig.update_layout(
            title=f"{site_name} Latest Month Distribution",
            annotations=[dict(text='No Data', x=0.5, y=0.5, font_size=20, showarrow=False)],
            showlegend=False,
            height=600
        )
    else:
        # Create the donut chart with data
        fig = go.Figure(data=[go.Pie(
            labels=non_zero_stages,
            values=values,
            hole=0.6,
            textinfo='percent+value',
            textposition='inside',
            hovertemplate="%{label}<br>%{value} studies<br>%{percent}<extra></extra>",
            direction='clockwise',
            sort=False,  # Prevent automatic sorting to maintain our order
            marker_colors=colors
        )])
        
        # Update layout
        fig.update_layout(
            title=f"{site_name} Latest Month Distribution",
            annotations=[dict(text=f'N={total}', x=0.5, y=0.5, font_size=20, showarrow=False)],
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="right",
                x=1.1
            ),
            margin=dict(t=60, l=20, r=150, b=20),
            height=600
        )
    
    return fig

def create_bar_chart(df, site_name):
    """Create a stacked bar chart showing progress over time"""
    # Create the stacked bar chart
    fig = go.Figure()
    
    # Add bars for each stage in the defined order
    for stage in color_map.keys():
        if stage in df.index:
            fig.add_trace(go.Bar(
                name=stage,
                x=df.columns,
                y=df.loc[stage],
                marker_color=color_map[stage]
            ))
    
    # Update layout
    fig.update_layout(
        title=f"{site_name} Progress Over Time",
        barmode='stack',
        xaxis_title="Month",
        yaxis_title="Number of Studies",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.1
        ),
        margin=dict(r=150),
        showlegend=True,
        height=600
    )
    
    return fig

def main():
    # Create output directory if it doesn't exist
    if not os.path.exists('interactive_plots'):
        os.makedirs('interactive_plots')
    
    # Process each dataset
    datasets = {
        'RP1': 'rp1_data.csv',
        'Johannesburg': 'johannesburg_data.csv',
        'Abidjan': 'abidjan_data.csv'
    }
    
    for site_name, file_name in datasets.items():
        if os.path.exists(file_name):
            # Load data
            df = load_data(file_name)
            
            # Create and save donut chart
            donut_fig = create_donut_chart(df, site_name)
            donut_fig.write_html(f'interactive_plots/{site_name.lower()}_donut.html')
            
            # Create and save bar chart
            bar_fig = create_bar_chart(df, site_name)
            bar_fig.write_html(f'interactive_plots/{site_name.lower()}_bar.html')

if __name__ == "__main__":
    main()
