import pandas as pd
import tkinter as tk
from tkinter import filedialog

def main():
  # Prompt user for Excel file
  root = tk.Tk()
  root.withdraw()
  file_path = filedialog.askopenfilename(
    title="Select Excel File",
    filetypes=[("Excel files", "*.xlsx *.xls")]
  )
  if not file_path:
    print("No file selected.")
    return

  # Read Excel file
  df = pd.read_excel(file_path)

  # Ensure required columns exist
  required_cols = ['Issue Type', 'Status', 'Story Points', 'Program Increment']
  for col in required_cols:
    if col not in df.columns:
      print(f"Missing required column: {col}")
      return

  # Group and aggregate
  grouped = df.groupby(['Issue Type', 'Status', 'Program Increment']).agg(
    Total_Story_Points=pd.NamedAgg(column='Story Points', aggfunc='sum'),
    Records_Without_Story_Points=pd.NamedAgg(
      column='Story Points', aggfunc=lambda x: x.isna().sum() + (x == 0).sum()
    ),
    Total_Records=pd.NamedAgg(column='Story Points', aggfunc='count')
  ).reset_index()

  print(grouped)

  # Prompt user for output file name
  output_path = filedialog.asksaveasfilename(
    title="Save Report As",
    defaultextension=".xlsx",
    filetypes=[("Excel files", "*.xlsx *.xls")]
  )
  if output_path:
    grouped.to_excel(output_path, index=False)
    print(f"Report saved to {output_path}")
  else:
    print("No output file selected. Report not saved.")


if __name__ == "__main__":
  main()