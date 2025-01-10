import pandas as pd

def examine_excel(file_path):
    # Read all sheets from the Excel file
    excel_data = pd.read_excel(file_path, sheet_name=None)
    
    print("Available sheets:")
    for sheet_name in excel_data.keys():
        print(f"\n{sheet_name}:")
        print("Columns:", excel_data[sheet_name].columns.tolist())
        print("First few rows:")
        print(excel_data[sheet_name].head())
        print("-" * 80)

if __name__ == "__main__":
    examine_excel("HEAT_Tables_0422_am_1327.xlsx")
