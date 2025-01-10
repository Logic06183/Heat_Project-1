import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Define the stage order and color map
stage_order = [
    'Contact procedures not initiated',
    '1st or 2nd invites',
    '3rd or more invites',
    'Data sharing discussions and eligibility check',
    'DTA in progress',
    'DTA completed',
    'Data sets in hand',
    'Database harmonization',
    'Ineligible/declined participation/data currently unavailable'
]

color_map = {
    'Contact procedures not initiated': '#FFB6C1',    # Light pink
    '1st or 2nd invites': '#FFE4B5',                 # Light yellow
    '3rd or more invites': '#87CEEB',                # Light blue
    'Data sharing discussions and eligibility check': '#90EE90',  # Light green
    'DTA in progress': '#D3D3D3',                    # Light gray
    'DTA completed': '#98FB98',                      # Pale green
    'Data sets in hand': '#008000',                  # Dark green
    'Database harmonization': '#ADD8E6',             # Light blue
    'Ineligible/declined participation/data currently unavailable': '#FFFFFF'  # White
}

def plot_stacked_bar_chart(df, title, last_n_months=8, save_path=None):
    """
    Create a stacked bar chart showing progress
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the progress data
    title : str
        Title for the chart
    last_n_months : int
        Number of most recent months to show
    save_path : str, optional
        If provided, save the plot to this path instead of showing it
    """
    df = df.set_index('Stage').reindex(stage_order).reset_index()
    stages_df = df[~df['Stage'].str.contains("Total")]
    transposed_df = stages_df.set_index('Stage').transpose()
    transposed_df = transposed_df.iloc[-last_n_months:]

    # Exclude 'Ineligible/declined participation/data currently unavailable' from the plot
    plot_df = transposed_df.drop(columns=['Ineligible/declined participation/data currently unavailable'], errors='ignore')

    fig, ax = plt.subplots(figsize=(15, 7))
    bars = plot_df.plot(kind='bar', stacked=True, ax=ax, 
                       color=[color_map.get(x, '#333333') for x in stage_order if x in plot_df.columns])

    # Add value labels in the center of each bar segment
    for bar in bars.containers:
        labels = [f'{v.get_height():.0f}' if v.get_height() != 0 else '' for v in bar]
        ax.bar_label(bar, labels=labels, label_type='center', padding=3)

    # Add N= and n= annotations
    for i, month in enumerate(transposed_df.index):
        month_data = transposed_df.loc[month]
        cumulative_height = float(month_data.drop('Ineligible/declined participation/data currently unavailable', 
                                                errors='ignore').sum())
        excluded_height = float(month_data.get('Ineligible/declined participation/data currently unavailable', 0))

        x_position = i + 0.5
        # Adjust the positions of the N= and n= labels
        ax.text(i + 0.3, cumulative_height / 2, f"N={cumulative_height:.0f}", 
                ha='left', va='center')
        if excluded_height > 0:
            ax.text(i + 0.3, cumulative_height - (excluded_height), f"n={excluded_height:.0f}", 
                   ha='left', va='center', color='red', fontsize=10, fontweight='bold')

    # Customize the plot
    ax.set_xticklabels([x.strftime('%b %Y') if isinstance(x, datetime) else x 
                        for x in transposed_df.index], rotation=45)
    ax.legend(title='Stage', loc='upper center', bbox_to_anchor=(0.5, -0.3), 
             ncol=len(stage_order)//2, frameon=False)
    plt.subplots_adjust(bottom=0.3, right=1.3)
    ax.set_title(title)
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Studies')

    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show()

def plot_cumulative_stacked_bar_chart(dfs, title, last_n_months=8, save_path=None):
    """
    Create a cumulative stacked bar chart combining multiple DataFrames
    
    Parameters:
    -----------
    dfs : list of pandas.DataFrame
        List of DataFrames containing the progress data
    title : str
        Title for the chart
    last_n_months : int
        Number of most recent months to show
    save_path : str, optional
        If provided, save the plot to this path instead of showing it
    """
    combined_df = pd.DataFrame()
    for df in dfs:
        df = df.set_index('Stage').reindex(stage_order).reset_index()
        stages_df = df[~df['Stage'].str.contains("Total")]
        if combined_df.empty:
            combined_df = stages_df
        else:
            combined_df = combined_df.set_index('Stage').add(stages_df.set_index('Stage'), fill_value=0).reset_index()
    
    transposed_df = combined_df.set_index('Stage').transpose()
    transposed_df = transposed_df.iloc[-last_n_months:]

    # Exclude 'Ineligible/declined participation/data currently unavailable' from the plot
    plot_df = transposed_df.drop(columns=['Ineligible/declined participation/data currently unavailable'], errors='ignore')

    fig, ax = plt.subplots(figsize=(15, 7))
    bars = plot_df.plot(kind='bar', stacked=True, ax=ax, 
                       color=[color_map.get(x, '#333333') for x in stage_order if x in plot_df.columns])

    # Add value labels in the center of each bar segment
    for bar in bars.containers:
        labels = [f'{v.get_height():.0f}' if v.get_height() != 0 else '' for v in bar]
        ax.bar_label(bar, labels=labels, label_type='center', padding=3)

    # Add N= and n= annotations
    for i, month in enumerate(transposed_df.index):
        month_data = transposed_df.loc[month]
        cumulative_height = float(month_data.drop('Ineligible/declined participation/data currently unavailable', 
                                                errors='ignore').sum())
        excluded_height = float(month_data.get('Ineligible/declined participation/data currently unavailable', 0))

        x_position = i + 0.5
        # Adjust the positions of the N= and n= labels
        ax.text(i + 0.3, cumulative_height / 2, f"N={cumulative_height:.0f}", 
                ha='left', va='center')
        if excluded_height > 0:
            ax.text(i + 0.3, cumulative_height - (excluded_height / 2), f"n={excluded_height:.0f}", 
                   ha='left', va='center', color='red', fontsize=10, fontweight='bold')

    # Customize the plot
    ax.set_xticklabels([x.strftime('%b %Y') if isinstance(x, datetime) else x 
                        for x in transposed_df.index], rotation=45)
    ax.legend(title='Stage', loc='upper center', bbox_to_anchor=(0.5, -0.3), 
             ncol=len(stage_order)//2, frameon=False)
    plt.subplots_adjust(bottom=0.3, right=1.3)
    ax.set_title(title)
    ax.set_xlabel('Month')
    ax.set_ylabel('Number of Studies')

    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show()

def process_excel_data(excel_file):
    """
    Process the Excel file and create visualizations for each region and overall
    """
    # Read all sheets from the Excel file
    excel_data = pd.read_excel(excel_file, sheet_name=['RP1', 'Abj_outputs', 'Jhb_outputs'])
    
    # Create individual visualizations for each sheet
    for sheet_name, df in excel_data.items():
        if sheet_name == 'RP1':
            title = 'RP1 Progress'
        elif sheet_name == 'Abj_outputs':
            title = 'Abidjan Progress'
        elif sheet_name == 'Jhb_outputs':
            title = 'Johannesburg Progress'
        else:
            continue
            
        output_file = f"{sheet_name.lower()}_progress.png"
        plot_stacked_bar_chart(df, title, last_n_months=8, save_path=output_file)
        print(f"Generated {title} chart: {output_file}")
    
    # Create the cumulative visualization
    plot_cumulative_stacked_bar_chart(
        list(excel_data.values()),
        'Overall data acquisition for the HE2AT center',
        last_n_months=8,
        save_path='overall_progress.png'
    )
    print("Generated Overall Progress chart: overall_progress.png")

if __name__ == "__main__":
    excel_file = "HEAT_Tables_0422_am_1327.xlsx"
    process_excel_data(excel_file)
