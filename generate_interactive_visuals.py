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
    'Contact procedures not initiated': '#1f77b4',
    '1st or 2nd invites': '#ff7f0e',
    '3rd or more invites': '#2ca02c',
    'Next steps/application sent': '#d62728',
    'Park': '#9467bd',
    'Entering into DTA': '#8c564b',
    'Batch to send to Ethics': '#e377c2',
    'Transfer of data in progress': '#7f7f7f',
    'Data sets in hand': '#bcbd22',
    'Health check in progress': '#17becf',
    'Harmonization in progress': '#1a55FF',
    'Geo-coding in progress': '#c49c94',
    'Database finalized': '#f7b6d2',
    'Data currently unavailable': '#c7c7c7',
    'Declined Participation': '#98df8a'
}

def create_stacked_bar_chart(df, title):
    """Create an interactive stacked bar chart showing progress"""
    # Only keep the last 6 months of data
    df_subset = df.copy()
    if len(df.columns) > 7:  # If we have more than 6 months + Stage column
        df_subset = df_subset[['Stage'] + list(df.columns[-6:])]
    
    # Prepare the data
    df_subset = df_subset[df_subset['Stage'] != 'Total'].copy()  # Remove Total row
    df_subset = df_subset.set_index('Stage').reindex(stage_order).reset_index()
    months = df_subset.columns[1:]
    
    # Fill NaN values with 0
    df_subset = df_subset.fillna(0)
    
    # Create figure
    fig = go.Figure()
    
    # Add traces for each stage
    for stage in stage_order:
        if stage in df_subset['Stage'].values:
            fig.add_trace(go.Bar(
                name=stage,
                x=df_subset.columns[1:],  # Skip 'Stage' column
                y=df_subset[df_subset['Stage'] == stage].iloc[:, 1:].values[0],
                marker_color=color_map.get(stage, '#000000')
            ))
    
    # Calculate totals excluding declined participation
    monthly_totals = df_subset[df_subset['Stage'] != 'Declined Participation'].iloc[:, 1:].sum()
    declined = df_subset[df_subset['Stage'] == 'Declined Participation'].iloc[:, 1:].values[0]
    
    # Add annotations for N only
    annotations = []
    for i, (total, declined_val) in enumerate(zip(monthly_totals, declined)):
        annotations.append(dict(
            x=df_subset.columns[i+1],
            y=total + declined_val,
            text=f'N={int(total + declined_val)}',
            showarrow=False,
            yshift=10
        ))
    
    # Update layout
    fig.update_layout(
        title=title,
        barmode='stack',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5
        ),
        annotations=annotations,
        height=600,
        margin=dict(t=100, b=200)  # Increase bottom margin for legend
    )
    
    return fig

def standardize_data(df, data_type='standard'):
    """Standardize the data format across different CSV files"""
    if data_type == 'sample':
        # For sample_data.csv format
        # Rename columns to match the standard format
        df = df.rename(columns={
            'Contact procedures not initiated': 'Contact procedures not initiated',
            'Database harmonization': 'Batch to send to Ethics',
            'Month': 'Stage'  # Temporarily rename for processing
        })
        
        # Convert wide format to long format
        df_long = df.melt(id_vars=['Stage'], var_name='Month', value_name='Value')
        
        # Handle duplicates by taking the latest value for each Stage-Month combination
        df_pivot = df_long.sort_values('Value').drop_duplicates(['Stage', 'Month'], keep='last')
        
        # Convert back to wide format
        df = df_pivot.pivot(index='Month', columns='Stage', values='Value').reset_index()
        df = df.rename(columns={'Month': 'Stage'})  # Fix the column name back
        
        # Add missing categories with zeros
        for stage in stage_order:
            if stage not in df.columns:
                df[stage] = 0
        
        # Reorder columns to match stage_order
        df = df[['Stage'] + stage_order]
        
        # Fill NaN values with 0
        df = df.fillna(0)
    else:
        # Remove Total row if present
        if 'Total' in df['Stage'].values:
            df = df[df['Stage'] != 'Total']
        
        # Ensure all required stages are present
        missing_stages = [s for s in stage_order if s not in df['Stage'].values]
        for stage in missing_stages:
            new_row = pd.DataFrame({'Stage': [stage], **{col: 0 for col in df.columns if col != 'Stage'}})
            df = pd.concat([df, new_row], ignore_index=True)
        
        # Reorder rows to match stage_order
        df['Stage_order'] = df['Stage'].map({stage: i for i, stage in enumerate(stage_order)})
        df = df.sort_values('Stage_order').drop('Stage_order', axis=1)
    
    return df

def process_data():
    """Process CSV data and create interactive visualizations"""
    # Create directory for interactive plots if it doesn't exist
    import os
    os.makedirs('interactive_plots', exist_ok=True)
    
    # Define CSV files and their types for each plot
    data_sources = {
        'overall': ('sample_data.csv', 'standard'),
        'rp1': ('rp1_data.csv', 'standard'),
        'johannesburg': ('johannesburg_data.csv', 'standard'),
        'abidjan': ('abidjan_data.csv', 'standard')
    }
    
    # Create and save interactive plots with config options
    config = {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'chart',
            'height': 900,
            'width': 1200,
            'scale': 2
        }
    }
    
    plots = {}
    for name, (csv_file, data_type) in data_sources.items():
        try:
            # Read CSV file
            df = pd.read_csv(csv_file)
            
            # Standardize the data format
            df = standardize_data(df, data_type)
            
            # Create plot title
            title = f'{name.title()} Progress of Data Acquisition'
            if name == 'rp1':
                title = 'RP1 Progress of Data Acquisition'
            
            # Create plot
            plots[name] = create_stacked_bar_chart(df, title)
            
        except FileNotFoundError:
            print(f"Warning: {csv_file} not found. Using sample data for {name}.")
            # Create sample data as fallback
            sample_data = {
                'Stage': stage_order,
                'Jul 2024': [7, 10, 29, 36, 36, 64, 20, 40, 15, 10, 0, 0, 0, 0, 0],
                'Aug 2024': [5, 8, 25, 38, 40, 68, 25, 35, 12, 8, 0, 0, 0, 0, 0],
                'Sep 2024': [3, 6, 22, 40, 45, 72, 30, 32, 10, 6, 0, 0, 0, 0, 0],
                'Oct 2024': [2, 4, 18, 42, 48, 75, 35, 30, 8, 4, 0, 0, 0, 0, 0],
                'Nov 2024': [1, 2, 15, 44, 50, 78, 40, 28, 6, 2, 0, 0, 0, 0, 0],
                'Dec 2024': [0, 0, 12, 46, 52, 80, 45, 25, 4, 0, 0, 0, 0, 0, 0],
                'Jan 2025': [0, 0, 10, 48, 54, 82, 50, 22, 2, 0, 0, 0, 0, 0, 0]
            }
            sample_df = pd.DataFrame(sample_data)
            plots[name] = create_stacked_bar_chart(sample_df, f'{name.title()} Progress of Data Acquisition')
    
    # Save each plot as an HTML file
    for name, fig in plots.items():
        fig.write_html(f'interactive_plots/{name}_progress.html',
                      config=config,
                      include_plotlyjs='cdn',
                      full_html=False)

def main():
    process_data()

if __name__ == "__main__":
    main()
