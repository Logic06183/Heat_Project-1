import pandas as pd
import plotly.graph_objects as go
import os

# Create directory for interactive plots if it doesn't exist
os.makedirs('interactive_plots', exist_ok=True)

# Define the order of stages for consistent visualization
stage_order = [
    'Ineligible/declined participation/data currently unavailable',  # Start with ineligible
    'Contact procedures not initiated',
    '1st or 2nd invites',
    '3rd or more invites',
    'Data sharing discussions and eligibility check',
    'DTA in progress',
    'DTA completed',
    'Data sets in hand',
    'Database harmonization',  # End with the final process
    'Database ready for analysis'
]

# Define colors for each stage
color_map = {
    'Database ready for analysis': '#e377c2',  # Pink
    'Database harmonization': '#17becf',  # Cyan
    'Data sets in hand': '#bcbd22',  # Olive
    'DTA completed': '#8c564b',  # Brown
    'DTA in progress': '#9467bd',  # Purple
    'Data sharing discussions and eligibility check': '#d62728',  # Red
    '3rd or more invites': '#2ca02c',  # Green
    '1st or 2nd invites': '#ff7f0e',  # Orange
    'Contact procedures not initiated': '#1f77b4',  # Blue
    'Ineligible/declined participation/data currently unavailable': '#7f7f7f'  # Gray
}

def create_donut_chart(df, name):
    """Create a donut chart for the latest month's data"""
    # Get latest month data
    latest_month = df.columns[-1]
    latest_data = df[~df.index.isin(['Total'])].copy()  # Exclude Total row
    
    # Filter out stages with zero values
    latest_data = latest_data[latest_data[latest_month] > 0]
    
    # Sort stages according to stage_order
    sorted_stages = [stage for stage in stage_order if stage in latest_data.index]
    sorted_values = [latest_data.loc[stage, latest_month] for stage in sorted_stages]
    
    # Create donut chart
    fig = go.Figure(data=[go.Pie(
        labels=sorted_stages,
        values=sorted_values,
        hole=.5,
        marker_colors=[color_map[stage] for stage in sorted_stages],
        hovertemplate="Stage: %{label}<br>Studies: %{value}<extra></extra>",
        textinfo='value+percent',
        textposition='inside'
    )])
    
    # Get total from the Total row if it exists, otherwise calculate it
    total = df.loc['Total', latest_month] if 'Total' in df.index else sum(sorted_values)
    
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
            text=f'Total Studies: {int(total)}',
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
    
    # Remove Total row if it exists
    df_no_total = df[~df.index.isin(['Total'])]
    
    # Add traces for each stage in reverse order for proper stacking
    # First add ineligible at bottom
    if 'Ineligible/declined participation/data currently unavailable' in df_no_total.index:
        stage_data = df_no_total.loc['Ineligible/declined participation/data currently unavailable']
        if any(stage_data > 0):
            fig.add_trace(go.Bar(
                name='Ineligible/declined participation/data currently unavailable',
                x=df_no_total.columns,
                y=stage_data,
                marker_color=color_map['Ineligible/declined participation/data currently unavailable'],
                hovertemplate="Stage: Ineligible/declined participation/data currently unavailable<br>Month: %{x}<br>Studies: %{y}<extra></extra>"
            ))
    
    # Then add other stages in reverse order (excluding ineligible)
    other_stages = [s for s in reversed(stage_order) if s != 'Ineligible/declined participation/data currently unavailable']
    for stage in other_stages:
        if stage in df_no_total.index:
            stage_data = df_no_total.loc[stage]
            if any(stage_data > 0):  # Only add trace if there's non-zero data
                fig.add_trace(go.Bar(
                    name=stage,
                    x=df_no_total.columns,
                    y=stage_data,
                    marker_color=color_map[stage],
                    hovertemplate=f"Stage: {stage}<br>Month: %{{x}}<br>Studies: %{{y}}<extra></extra>"
                ))
    
    # Get monthly totals from Total row if it exists, otherwise calculate
    if 'Total' in df.index:
        monthly_totals = df.loc['Total']
    else:
        monthly_totals = df_no_total.sum()
    
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
            traceorder='normal',  # Normal order to match stage_order
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

def create_combined_donut_chart(datasets):
    """Create a combined donut chart showing the latest distribution across all datasets"""
    # Combine the latest month data from all datasets
    combined_data = {}
    total_studies = 0
    
    for site_name, file_name in datasets.items():
        if os.path.exists(file_name):
            df = pd.read_csv(file_name, index_col='Stage')
            latest_month = df.columns[-1]
            
            # Get data excluding Total row
            latest_data = df[~df.index.isin(['Total'])].copy()
            
            # Add data to combined dictionary
            for stage in latest_data.index:
                if stage not in combined_data:
                    combined_data[stage] = 0
                combined_data[stage] += latest_data.loc[stage, latest_month]
            
            # Add to total studies
            if 'Total' in df.index:
                total_studies += df.loc['Total', latest_month]
            else:
                total_studies += latest_data[latest_month].sum()
    
    # Filter out stages with zero values and prepare for plotting
    plot_data = {stage: count for stage, count in combined_data.items() if count > 0}
    
    # Sort stages according to stage_order
    sorted_stages = [stage for stage in stage_order if stage in plot_data]
    sorted_values = [plot_data[stage] for stage in sorted_stages]
    
    # Create donut chart
    fig = go.Figure(data=[go.Pie(
        labels=sorted_stages,
        values=sorted_values,
        hole=.5,
        marker_colors=[color_map[stage] for stage in sorted_stages],
        hovertemplate="Stage: %{label}<br>Studies: %{value}<extra></extra>",
        textinfo='value+percent',
        textposition='inside'
    )])
    
    # Update layout
    fig.update_layout(
        showlegend=True,
        title=dict(
            text=f"Combined Distribution - Latest Data",
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
            text=f'Total Studies: {int(total_studies)}',
            x=0.5, y=0.5,
            font_size=16,
            showarrow=False
        )]
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
    
    # Create and save combined donut chart
    combined_donut = create_combined_donut_chart(datasets)
    combined_donut.write_html(
        'interactive_plots/combined_donut.html',
        include_plotlyjs='cdn',
        full_html=True,
        config={
            'displayModeBar': False,
            'responsive': True
        }
    )

if __name__ == "__main__":
    main()
