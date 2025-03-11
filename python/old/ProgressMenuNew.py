
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import webbrowser

# Function to clone the selected repositories
def clone_repos(selected_repos):
    # Ask the user for the directory to clone to
    directory = filedialog.askdirectory()
    if directory:
        for repo_url in selected_repos:
            # Run the git clone command
            subprocess.run(["git", "clone", repo_url, directory])
        messagebox.showinfo("Success", f"Repositories cloned to {directory}")
        subprocess.run(["explorer", directory])

# Function to handle the Clone button click
def on_clone_button_click():
    selected_repos = [repo_urls[repo] for repo, var in repo_vars.items() if var.get()]
    if selected_repos:
        clone_repos(selected_repos)
    # Open Zoomin Admin if the checkbox is selected
    if open_zoomin_admin_var.get():
        webbrowser.open("https://progress-be-dev.zoominsoftware.io/admin/reindex")
        open_zoomin_admin_var.set(False)
        root.after(100, root.mainloop)
    
    # Open Agile Board if the checkbox is selected
    if open_agile_board_var.get():
        webbrowser.open("https://progresssoftware.atlassian.net/jira/software/c/projects/MLE/boards/4190")
    
    # Open GitHub if the checkbox is selected
    if open_github_var.get():
        webbrowser.open("https://github.com/prgs-caps/")

# Create the main window
root = tk.Tk()
root.title("Functions Menu")
root.geometry("400x300")

# Create a dictionary to store the repository URLs and their corresponding variables
repo_urls = {
    "Kubernetes": "https://plangleyprogress@github.com/prgs-caps/zoomin-md-marklogic-server-on-kubernetes.git",
    "SharepointOnline": "https://plangleyprogress@github.com/prgs-caps/zoomin-md-marklogic-server-on-sharepointonline.git",
    "PDC": "https://plangleyprogress@github.com/prgs-caps/zoomin-md-marklogic-server-on-pdc.git",
    "Zoomin Categories": "https://plangleyprogress@github.com/prgs-caps/zoomin-categories.git"
}

repo_vars = {repo: tk.BooleanVar() for repo in repo_urls}

# Create checkboxes for each repository
for repo, var in repo_vars.items():
    tk.Checkbutton(root, text=repo, variable=var).pack(anchor=tk.W)

# Create variables for the additional checkboxes
open_zoomin_admin_var = tk.BooleanVar()
open_agile_board_var = tk.BooleanVar()
open_github_var = tk.BooleanVar()

# Create the additional checkboxes
tk.Checkbutton(root, text="Open Zoomin Admin", variable=open_zoomin_admin_var).pack(anchor=tk.W)
tk.Checkbutton(root, text="Open Agile Board", variable=open_agile_board_var).pack(anchor=tk.W)
# Create a variable for the GitHub Kubernetes checkbox
open_github_kubernetes_var = tk.BooleanVar()

# Create the GitHub Kubernetes checkbox
tk.Checkbutton(root, text="Open GitHub Kubernetes", variable=open_github_kubernetes_var).pack(anchor=tk.W)

# Modify the on_clone_button_click function to handle the new checkbox
def on_clone_button_click():
    selected_repos = [repo_urls[repo] for repo, var in repo_vars.items() if var.get()]
    if selected_repos:
        clone_repos(selected_repos)
    # Open Zoomin Admin if the checkbox is selected
    if open_zoomin_admin_var.get():
        webbrowser.open("https://progress-be-dev.zoominsoftware.io/admin/reindex")
        open_zoomin_admin_var.set(False)
        root.after(100, root.mainloop)
    
    # Open Agile Board if the checkbox is selected
    if open_agile_board_var.get():
        webbrowser.open("https://progresssoftware.atlassian.net/jira/software/c/projects/MLE/boards/4190")
    
    # Open GitHub if the checkbox is selected
    if open_github_var.get():
        webbrowser.open("https://github.com/prgs-caps/")
    
    # Open GitHub Kubernetes if the checkbox is selected
    if open_github_kubernetes_var.get():
        webbrowser.open("https://github.com/prgs-caps/zoomin-md-marklogic-server-on-kubernetes")

# Create an OK button
clone_button = tk.Button(root, text="OK", command=on_clone_button_click)
clone_button.pack()


# Run the main event loop
root.mainloop()
