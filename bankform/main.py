import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database setup
conn = sqlite3.connect('accounts.db')
c = conn.cursor()
c.execute('''
  CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    url TEXT NOT NULL,
    financial_institution TEXT NOT NULL
  )
''')

# Add financial_institution column if it doesn't exist (for existing databases)
try:
    c.execute('ALTER TABLE accounts ADD COLUMN financial_institution TEXT NOT NULL DEFAULT ""')
    conn.commit()
except sqlite3.OperationalError:
    # Column already exists
    pass

conn.commit()

# Save function
def save_account():
  name = entry_name.get()
  acc_type = entry_type.get()
  url = entry_url.get()
  financial_institution = entry_financial_institution.get()
  if not name or not acc_type or not url or not financial_institution:
    messagebox.showwarning("Input Error", "All fields are required.")
    return
  c.execute('INSERT INTO accounts (name, type, url, financial_institution) VALUES (?, ?, ?, ?)', (name, acc_type, url, financial_institution))
  conn.commit()
  messagebox.showinfo("Success", "Account saved successfully!")
  entry_name.delete(0, tk.END)
  entry_type.delete(0, tk.END)
  entry_url.delete(0, tk.END)
  entry_financial_institution.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Bank Account Form")

tk.Label(root, text="Account Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Account Type:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
entry_type = tk.Entry(root, width=30)
entry_type.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="URL:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
entry_url = tk.Entry(root, width=30)
entry_url.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Financial Institution:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
entry_financial_institution = tk.Entry(root, width=30)
entry_financial_institution.grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Save", command=save_account).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
conn.close()