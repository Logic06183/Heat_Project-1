import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

def plot_stacked_bar_chart(df, title, save_path=None):
    """Create a stacked bar chart showing progress"""
    # Prepare the data
    df = df[df['Stage'] != 'Total'].copy()  # Remove Total row
    df = df.set_index('Stage').reindex(stage_order).reset_index()
    months = df.columns[1:]
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    ax = plt.gca()
    
    # Plot each stage
    bottom = np.zeros(len(months))
    for stage in df['Stage']:
        values = df[df['Stage'] == stage].iloc[:, 1:].values[0]
        ax.bar(range(len(months)), values, bottom=bottom, 
               label=stage, color=color_map.get(stage, '#333333'))
        
        # Add value labels for non-zero values
        for i, v in enumerate(values):
            if v > 0:
                ax.text(i, bottom[i] + v/2, f'{int(v)}',
                       ha='center', va='center')
        bottom += values
    
    # Calculate totals excluding ineligible
    monthly_totals = df[df['Stage'] != 'Ineligible/declined participation/data currently unavailable'].iloc[:, 1:].sum()
    ineligible = df[df['Stage'] == 'Ineligible/declined participation/data currently unavailable'].iloc[:, 1:].values[0]
    
    # Add N= and n= annotations
    for i, (total, excl) in enumerate(zip(monthly_totals, ineligible)):
        ax.text(i, total + excl + 3, f'N={int(total)}', ha='center', va='bottom')
        if excl > 0:
            ax.text(i, total + excl + 1, f'n={int(excl)}',
                   ha='center', va='bottom', color='red', fontsize=10)
    
    # Customize the plot
    plt.xticks(range(len(months)), months, rotation=45, ha='right')
    plt.title(title, pad=20)
    plt.ylabel('Number of Studies')
    
    # Add notes explaining N and n
    note_text = "Notes:\nN = Total number of eligible studies\nn = Number of ineligible/declined studies"
    plt.figtext(0.98, 0.02, note_text, ha='right', va='bottom', fontsize=10, style='italic')
    
    # Adjust legend
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.subplots_adjust(right=0.85, bottom=0.2)
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show()

def plot_final_month_summary(data_frames, title, output_file):
    """Create a summary visualization of the final month's data"""
    # Set total and excluded values
    total = 202  # Total number of studies
    excl = 40    # Number of excluded studies
    
    # Prepare data for plotting
    categories = [
        '1st or 2nd invites',
        '3rd or more invites',
        'Data sharing discussions and eligibility check',
        'DTA in progress',
        'DTA completed',
        'Data sets in hand',
        'Databases harmonised'
    ]
    
    values = [7, 10, 29, 36, 36, 64, 20]  # Your provided values
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Create stacked bar chart
    left = 0
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    
    for i, (value, color) in enumerate(zip(values, colors)):
        plt.barh(0, value, left=left, color=color, label=categories[i])
        # Add value label in the middle of each segment
        plt.text(left + value/2, 0, str(value), ha='center', va='center')
        left += value
    
    # Customize the plot
    plt.yticks([])  # Remove y-axis ticks since we only have one bar
    plt.xlabel('Number of Studies')
    
    # Add legend
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Add title
    plt.title(title)
    
    # Add total studies and excluded studies annotations
    plt.text(205, 0.1, f'N={total}', ha='left', va='center')
    plt.text(205, -0.1, f'n={excl}', ha='left', va='center')
    
    # Add notes at the bottom
    plt.figtext(0.02, 0.02, 'Notes:', ha='left')
    plt.figtext(0.02, -0.02, 'N = Total number of eligible studies', ha='left')
    plt.figtext(0.02, -0.06, 'n = Number of ineligible/declined studies', ha='left')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(output_file, bbox_inches='tight', dpi=300, pad_inches=0.5)
    plt.close()

def process_excel_data(excel_file):
    """Process the data and create visualizations"""
    # Read data files
    rp1_data = pd.read_csv('updated_heat_data.csv')
    abj_data = pd.read_csv('abidjan_data.csv')
    jhb_data = pd.read_csv('johannesburg_data.csv')
    
    # Create visualizations
    plot_stacked_bar_chart(rp1_data, 'RP1 Progress', 'Jan 2025/rp1_progress.png')
    plot_stacked_bar_chart(abj_data, 'Abidjan Progress', 'Jan 2025/abidjan_progress.png')
    plot_stacked_bar_chart(jhb_data, 'Johannesburg Progress', 'Jan 2025/johannesburg_progress.png')
    
    # Create overall summary
    plot_final_month_summary(
        [rp1_data, abj_data, jhb_data],
        'Overall Data Acquisition for the HE2AT Center - December 2024',
        'Jan 2025/overall_progress.png'
    )
    print("Generated all progress charts")

def main():
    process_excel_data(None)

if __name__ == "__main__":
    main()
