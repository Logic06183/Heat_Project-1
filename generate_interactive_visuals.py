import pandas as pd
import plotly.graph_objects as go
import os

# Create directory for interactive plots if it doesn't exist
os.makedirs('interactive_plots', exist_ok=True)

# Define the order of stages for consistent visualization (in reverse order for stacking)
stage_order = [
    'Ineligible/declined participation/data currently unavailable',  # Final outcomes at top
    'Database harmonization',
    'Data sets in hand',
    'DTA completed',
    'DTA in progress',
    'Data sharing discussions and eligibility check',
    '3rd or more invites',
    '1st or 2nd invites',
    'Contact procedures not initiated'  # Initial stage at bottom
]

# Define colors for each stage
color_map = {
    'Contact procedures not initiated': '#1f77b4',  # Blue
    '1st or 2nd invites': '#ff7f0e',  # Orange
    '3rd or more invites': '#2ca02c',  # Green
    'Data sharing discussions and eligibility check': '#d62728',  # Red
    'DTA in progress': '#9467bd',  # Purple
    'DTA completed': '#8c564b',  # Brown
    'Data sets in hand': '#bcbd22',  # Olive
    'Database harmonization': '#17becf',  # Cyan
    'Ineligible/declined participation/data currently unavailable': '#e377c2'  # Pink
}

def create_donut_chart(df, name):
    """Create a donut chart for the latest month's data"""
    # Get latest month data
    latest_month = df.columns[-1]
    latest_data = df.copy()
    
    # Filter out stages with zero values and sort by stage_order
    latest_data = latest_data[latest_data[latest_month] > 0]
    latest_data = latest_data.reindex(stage_order)
    latest_data = latest_data.dropna()
    
    # Create donut chart
    fig = go.Figure(data=[go.Pie(
        labels=latest_data.index,
        values=latest_data[latest_month],
        hole=.5,
        marker_colors=[color_map[stage] for stage in latest_data.index],
        hovertemplate="Stage: %{label}<br>Studies: %{value}<extra></extra>",
        textinfo='value+percent',
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
        margin=dict(t=100, b=150),
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
    
    # Add traces for each stage in reverse order (for proper stacking)
    for stage in reversed(stage_order):
        if stage in df.index:
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
    monthly_totals = df.sum()
    
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
        margin=dict(t=100, b=150),
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
                include_plotlyjs='cdn',
                full_html=True,
                config={
                    'displayModeBar': False,
                    'responsive': True
                }
            )
            
            # Create and save bar chart
            bar_fig = create_stacked_bar_chart(df, site_name)
            bar_fig.write_html(
                f'interactive_plots/{site_name.lower()}_bar.html',
                include_plotlyjs='cdn',
                full_html=True,
                config={
                    'displayModeBar': False,
                    'responsive': True
                }
            )

if __name__ == "__main__":
    main()
