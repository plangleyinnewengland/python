def extract():
   from tkinter import filedialog
    folder_path = tk.filedialog.askdirectory()
    if folder_path:
        extract_comments.extract_from_folder(folder_path)