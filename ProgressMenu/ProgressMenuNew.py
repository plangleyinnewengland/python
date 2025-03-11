import tkinter as tk
import webbrowser
from tkinter import filedialog
import os
import re
import pandas as pd


def open_zoom_admin():
    webbrowser.open('https://progress-be-dev.zoominsoftware.io/admin/reindex')

def open_agile_board():
    webbrowser.open('https://progresssoftware.atlassian.net/jira/software/c/projects/MLE/boards/4190')

def open_github():
    webbrowser.open('https://github.com/prgs-caps/zoomin-md-marklogic-server-on-kubernetes')

def run_extract():
    folder_selected = filedialog.askdirectory()
    comments = []

    # Walk through the directory and subdirectories
    for root, dirs, files in os.walk(folder_selected):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract HTML comments
                    file_comments = re.findall(r'<!--(.*?)-->', content, re.DOTALL)
                    for comment in file_comments:
                        comments.append({'File': file_path, 'Comment': comment.strip()})

    # Create a DataFrame and save to an Excel file
    df = pd.DataFrame(comments)
    output_file = os.path.join(folder_selected, 'extracted_comments.xlsx')
    df.to_excel(output_file, index=False)
    tk.messagebox.showinfo("Extraction Complete", f"Comments extracted to {output_file}")
    # Open the Excel file after saving
    os.startfile(output_file)
    
    
# Create the main window
root = tk.Tk()
root.title("Progress Menu")
root.geometry("400x200")  # Set the window size to 400x200

# Create buttons
button_width = 20

zoom_button = tk.Button(root, text="Open Zoom Admin", command=open_zoom_admin, width=button_width, anchor='w')
agile_button = tk.Button(root, text="Open Agile Board", command=open_agile_board, width=button_width, anchor='w')
github_button = tk.Button(root, text="Open GitHub (Kubernetes)", command=open_github, width=button_width, anchor='w')
runapp_button = tk.Button(root, text="Extract HTML Comments", command=run_extract, width=button_width, anchor='w')

# Place buttons on the window
zoom_button.pack(pady=10)
agile_button.pack(pady=10)
github_button.pack(pady=10)
runapp_button.pack(pady=10)

# Run the application
root.mainloop()
