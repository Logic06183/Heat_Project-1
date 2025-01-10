import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class ProgressVisualizer:
    def __init__(self):
        # Define the stages and their colors
        self.stages = {
            'Contact procedures not initiated': '#FFB6C1',    # Light pink
            '1st or 2nd invites': '#FFE4B5',                 # Light yellow
            '3rd or more invites': '#87CEEB',                # Light blue
            'Data sharing discussions and eligibility check': '#90EE90',  # Light green
            'DTA in progress': '#D3D3D3',                    # Light gray
            'DTA completed': '#98FB98',                      # Pale green
            'Data sets in hand': '#008000',                  # Dark green
            'Database harmonization': '#ADD8E6'              # Light blue
        }
        
    def create_progress_chart(self, data, output_file, title="Progress Report"):
        """
        Create a stacked bar chart showing progress
        
        Parameters:
        -----------
        data : pandas.DataFrame or str
            DataFrame containing the progress data or path to CSV file
        output_file : str
            Path where the output image should be saved
        title : str
            Title for the chart
        """
        # Handle input data
        if isinstance(data, str):
            df = pd.read_csv(data)
        else:
            df = data
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Plot each stage
        bottoms = np.zeros(len(df))
        for stage, color in self.stages.items():
            if stage in df.columns:
                values = df[stage].values
                bar = ax.bar(range(len(df)), values, bottom=bottoms, 
                           label=stage, color=color)
                
                # Add value labels in the middle of each segment
                for i, v in enumerate(values):
                    if v > 0:  # Only add label if there's a value
                        height = bottoms[i] + v/2
                        ax.text(i, height, str(int(v)), ha='center', va='center')
                bottoms += values
        
        # Customize the plot
        ax.set_title(title, pad=20)
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Studies')
        
        # Set x-axis labels
        if 'Month' in df.columns:
            plt.xticks(range(len(df)), df['Month'], rotation=45)
        
        # Add n=8 and N=38 annotations
        for i in range(len(df)):
            ax.text(i, ax.get_ylim()[1], 'n=8', color='red', 
                   ha='center', va='bottom')
            ax.text(i, ax.get_ylim()[1]/2, 'N=38', color='black', 
                   ha='right', va='center')
        
        # Add legend
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(output_file, bbox_inches='tight', dpi=300)
        plt.close()

if __name__ == "__main__":
    visualizer = ProgressVisualizer()
    
    # Example usage with DataFrame
    data = pd.DataFrame({
        'Month': ['Nov 2023', 'Dec 2023', 'Jan 2024'],
        'Data sets in hand': [9, 9, 7],
        'DTA in progress': [12, 10, 10],
        'Data sharing discussions and eligibility check': [14, 14, 15]
    })
    
    visualizer.create_progress_chart(data, 'example_progress.png', 'Example Progress')
