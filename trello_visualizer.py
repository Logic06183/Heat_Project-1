import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import seaborn as sns

class TrelloVisualizer:
    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        # Define the stages and their colors
        self.stages = {
            'Contact procedures not initiated': '#FFB6C1',  # Pink
            '1st or 2nd invites': '#FFE4B5',              # Light yellow
            '3rd or more invites': '#ADD8E6',             # Light blue
            'Data sharing discussions and eligibility check': '#D3D3D3',  # Light gray
            'DTA in progress': '#98FB98',                 # Light green
            'DTA completed': '#228B22',                   # Dark green
            'Database harmonization': '#87CEEB'           # Sky blue
        }
        
        self.process_data()
    
    def process_data(self):
        """Process Trello JSON data into useful dataframes"""
        # Get all lists and cards
        lists = {lst['id']: lst['name'] for lst in self.data.get('lists', [])}
        cards = self.data.get('cards', [])
        
        # Create monthly snapshots
        snapshots = {}
        months = pd.date_range('2023-11-01', '2024-06-30', freq='M')
        
        for month in months:
            month_str = month.strftime('%Y-%m')
            stage_counts = {stage: 0 for stage in self.stages.keys()}
            
            for card in cards:
                card_date = datetime.strptime(card['dateLastActivity'], '%Y-%m-%dT%H:%M:%S.%fZ')
                if card_date <= month:
                    list_name = lists.get(card['idList'], 'Unknown')
                    # Map list name to stage
                    stage = self.map_list_to_stage(list_name)
                    if stage:
                        stage_counts[stage] += 1
            
            snapshots[month_str] = stage_counts
        
        self.monthly_data = snapshots
    
    def map_list_to_stage(self, list_name):
        """Map Trello list names to stages"""
        # Add your mapping logic here based on your Trello list names
        mapping = {
            'Initial Contact': 'Contact procedures not initiated',
            'First Invite': '1st or 2nd invites',
            'Second Invite': '1st or 2nd invites',
            'Third Invite': '3rd or more invites',
            'Data Sharing Discussion': 'Data sharing discussions and eligibility check',
            'DTA Process': 'DTA in progress',
            'DTA Signed': 'DTA completed',
            'Harmonization': 'Database harmonization'
        }
        
        # Try to match the list name with the mapping
        for key in mapping:
            if key.lower() in list_name.lower():
                return mapping[key]
        return None
    
    def plot_monthly_progression(self, output_file='data_acquisition_progress.png'):
        """Create a stacked bar chart showing monthly progression"""
        # Prepare data for plotting
        df = pd.DataFrame(self.monthly_data).T
        
        # Create the stacked bar chart
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Plot each stage
        bottoms = np.zeros(len(df))
        bars = []
        for stage, color in self.stages.items():
            values = df[stage].values
            bar = ax.bar(range(len(df)), values, bottom=bottoms, label=stage, color=color)
            bars.append(bar)
            
            # Add value labels in the middle of each segment
            for i, v in enumerate(values):
                if v > 0:  # Only add label if there's a value
                    height = bottoms[i] + v/2
                    ax.text(i, height, str(int(v)), ha='center', va='center')
            bottoms += values
        
        # Customize the plot
        ax.set_title('Overall data acquisition for the HE2AT center', pad=20)
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Studies')
        
        # Add total count
        totals = df.sum(axis=1)
        max_height = max(totals)
        
        # Add n=X at top
        for i, total in enumerate(totals):
            ax.annotate(f'n={int(total)}', 
                       xy=(i, total), 
                       xytext=(0, 5),
                       textcoords='offset points',
                       ha='center',
                       va='bottom',
                       color='red')
        
        # Add N=X at bottom
        for i, total in enumerate(totals):
            ax.annotate(f'N={int(total)}',
                       xy=(i, 0),
                       xytext=(0, -15),
                       textcoords='offset points',
                       ha='center',
                       va='top')
        
        # Set axis limits with padding
        ax.set_ylim(bottom=-max_height*0.1, top=max_height*1.1)
        
        # Set x-axis labels
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels([d.replace('-', ' ') for d in df.index], 
                          rotation=45, ha='right')
        
        # Add legend at the bottom
        ax.legend(bbox_to_anchor=(0.5, -0.2),
                 loc='upper center',
                 ncol=3,
                 title='Stage')
        
        # Adjust layout and save
        plt.subplots_adjust(bottom=0.25)
        plt.savefig(output_file, bbox_inches='tight', dpi=300)
        plt.close()

if __name__ == "__main__":
    visualizer = TrelloVisualizer("JSONS/ClS62fmQ - data-acquisition-rp1.json")
    visualizer.plot_monthly_progression()
