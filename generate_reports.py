import pandas as pd
from progress_visualizer import ProgressVisualizer

def process_excel_data(excel_file):
    """
    Read and process data from the Excel file
    """
    # Read the Excel file
    df = pd.read_excel(excel_file, sheet_name=None)
    
    # Initialize visualizer
    visualizer = ProgressVisualizer()
    
    # Process each sheet (assuming one sheet per region)
    for sheet_name, sheet_data in df.items():
        if not isinstance(sheet_data, pd.DataFrame):
            continue
            
        # Clean and prepare the data
        # Assuming the Excel structure matches our needs, adjust the column names as needed
        processed_data = sheet_data.copy()
        
        # Generate the visualization
        output_file = f"{sheet_name.replace(' ', '_')}_progress.png"
        visualizer.create_progress_chart(
            processed_data,
            output_file,
            f"{sheet_name} Progress"
        )
        print(f"Generated report for {sheet_name}: {output_file}")

if __name__ == "__main__":
    excel_file = "HEAT_Tables_0422_am_1327.xlsx"
    process_excel_data(excel_file)
