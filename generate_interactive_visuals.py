import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Define stage order and colors
stage_order = [
    '1st or 2nd invites',
    '3rd or more invites',
    'Data sharing discussions and eligibility check',
    'DTA in progress',
    'DTA completed',
    'Data sets in hand',
    'Databases harmonised',
    'Ineligible/declined participation/data currently unavailable'
]

color_map = {
    '1st or 2nd invites': '#1f77b4',
    '3rd or more invites': '#ff7f0e',
    'Data sharing discussions and eligibility check': '#2ca02c',
    'DTA in progress': '#d62728',
    'DTA completed': '#9467bd',
    'Data sets in hand': '#8c564b',
    'Databases harmonised': '#e377c2',
    'Ineligible/declined participation/data currently unavailable': '#7f7f7f'
}

def create_stacked_bar_chart(df, title):
    """Create an interactive stacked bar chart showing progress"""
    # Prepare the data
    df = df[df['Stage'] != 'Total'].copy()  # Remove Total row
    df = df.set_index('Stage').reindex(stage_order).reset_index()
    months = df.columns[1:]
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add traces for each stage
    for stage in df['Stage']:
        values = df[df['Stage'] == stage].iloc[:, 1:].values[0]
        
        # Create hover text
        hover_text = [f"{stage}<br>Count: {int(v)}" for v in values]
        
        # Only show text for values > 5 to reduce clutter
        text_values = []
        for v in values:
            if v > 5:
                text_values.append(str(int(v)))
            else:
                text_values.append('')
        
        fig.add_trace(go.Bar(
            name=stage,
            x=list(months),
            y=values,
            text=text_values,
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(size=11),
            hovertext=hover_text,
            marker_color=color_map.get(stage, '#333333'),
            width=0.8  # Adjust bar width
        ))
    
    # Calculate totals excluding ineligible
    monthly_totals = df[df['Stage'] != 'Ineligible/declined participation/data currently unavailable'].iloc[:, 1:].sum()
    ineligible = df[df['Stage'] == 'Ineligible/declined participation/data currently unavailable'].iloc[:, 1:].values[0]
    
    # Add annotations for N and n with improved positioning
    annotations = []
    max_y = max(monthly_totals + ineligible)
    padding = max_y * 0.08  # Dynamic padding based on chart height
    
    for i, (month, total, excl) in enumerate(zip(months, monthly_totals, ineligible)):
        # Position N and n with more spacing
        annotations.extend([
            dict(
                x=month,
                y=total + excl + padding,  # Dynamic padding
                text=f'N={int(total)}',
                showarrow=False,
                font=dict(size=12, color='black'),
                yanchor='bottom'
            ),
            dict(
                x=month,
                y=total + excl + (padding/2),  # Half padding for n
                text=f'n={int(excl)}',
                showarrow=False,
                font=dict(size=11, color='red'),
                yanchor='bottom'
            ) if excl > 0 else None
        ])
    annotations = [a for a in annotations if a is not None]
    
    # Update layout with improved spacing
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            y=0.98,
            font=dict(size=20)
        ),
        barmode='stack',
        xaxis=dict(
            title="Month",
            titlefont=dict(size=14),
            tickfont=dict(size=12),
            tickangle=0,
            showgrid=False,
            dtick=1  # Show all month labels
        ),
        yaxis=dict(
            title="Number of Studies",
            titlefont=dict(size=14),
            tickfont=dict(size=12),
            range=[0, max_y * 1.15]  # Add 15% padding for labels
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.45,  # More space for legend
            xanchor="center",
            x=0.5,
            font=dict(size=11),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1,
            itemsizing='constant'  # Consistent legend item sizes
        ),
        annotations=annotations,
        margin=dict(l=80, r=80, t=100, b=250),  # Increased bottom margin for legend
        height=900,
        width=1200,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        bargap=0.15,  # Increased gap between bar groups
        bargroupgap=0.1  # Gap between bars in a group
    )
    
    # Update axes lines and grid
    fig.update_xaxes(showline=True, linewidth=1, linecolor='gray', showgrid=False)
    fig.update_yaxes(
        showline=True, 
        linewidth=1, 
        linecolor='gray', 
        showgrid=True, 
        gridwidth=1, 
        gridcolor='lightgray',
        dtick=50  # Set y-axis tick interval to 50
    )
    
    return fig

def process_excel_data(excel_file):
    """Process Excel data and create interactive visualizations"""
    # Create directory for interactive plots if it doesn't exist
    import os
    os.makedirs('interactive_plots', exist_ok=True)
    
    # Read the Excel sheets
    df = pd.read_excel(excel_file)
    
    # Create sample data for demonstration
    sample_data = {
        'Stage': stage_order,
        'Jul 2024': [7, 10, 29, 36, 36, 64, 20, 40],
        'Aug 2024': [5, 8, 25, 38, 40, 68, 25, 35],
        'Sep 2024': [3, 6, 22, 40, 45, 72, 30, 32],
        'Oct 2024': [2, 4, 18, 42, 48, 75, 35, 30],
        'Nov 2024': [1, 2, 15, 44, 50, 78, 40, 28],
        'Dec 2024': [0, 0, 12, 46, 52, 80, 45, 25],
        'Jan 2025': [0, 0, 10, 48, 54, 82, 50, 22]
    }
    
    sample_df = pd.DataFrame(sample_data)
    
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
    
    plots = {
        'overall': create_stacked_bar_chart(sample_df, 'Overall Progress of Data Acquisition'),
        'rp1': create_stacked_bar_chart(sample_df, 'RP1 Progress of Data Acquisition'),
        'johannesburg': create_stacked_bar_chart(sample_df, 'Johannesburg Progress of Data Acquisition'),
        'abidjan': create_stacked_bar_chart(sample_df, 'Abidjan Progress of Data Acquisition')
    }
    
    # Save each plot as an HTML file
    for name, fig in plots.items():
        fig.write_html(f'interactive_plots/{name}_progress.html',
                      config=config,
                      include_plotlyjs='cdn',
                      full_html=False)

def main():
    excel_file = "HEAT_Tables_0517_am.xlsx"  # Update with your Excel file path
    process_excel_data(excel_file)

if __name__ == "__main__":
    main()
