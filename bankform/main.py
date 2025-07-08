import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

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

# Create balance tracking table
c.execute('''
  CREATE TABLE IF NOT EXISTS balances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    bank_balance REAL NOT NULL,
    quicken_balance REAL NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts (id)
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

# View accounts function
def view_accounts():
  # Create a new window
  view_window = tk.Toplevel(root)
  view_window.title("View Accounts")
  view_window.geometry("800x400")
  
  # Create a text widget with scrollbar
  text_frame = tk.Frame(view_window)
  text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
  
  scrollbar = tk.Scrollbar(text_frame)
  scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
  
  text_widget = tk.Text(text_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD)
  text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
  
  scrollbar.config(command=text_widget.yview)
  
  # Fetch and display accounts
  c.execute('SELECT id, name, type, url, financial_institution FROM accounts ORDER BY id')
  accounts = c.fetchall()
  
  if not accounts:
    text_widget.insert(tk.END, "No accounts found in the database.")
  else:
    text_widget.insert(tk.END, "SAVED ACCOUNTS:\n")
    text_widget.insert(tk.END, "=" * 80 + "\n\n")
    
    for account in accounts:
      account_id, name, acc_type, url, financial_institution = account
      text_widget.insert(tk.END, f"ID: {account_id}\n")
      text_widget.insert(tk.END, f"Account Name: {name}\n")
      text_widget.insert(tk.END, f"Account Type: {acc_type}\n")
      text_widget.insert(tk.END, f"URL: {url}\n")
      text_widget.insert(tk.END, f"Financial Institution: {financial_institution}\n")
      text_widget.insert(tk.END, "-" * 50 + "\n\n")
  
  # Make text widget read-only
  text_widget.config(state=tk.DISABLED)

# Balance tracking function
def track_balance():
  # Create a new window
  balance_window = tk.Toplevel(root)
  balance_window.title("Track Account Balance")
  balance_window.geometry("400x300")
  
  # Get accounts for dropdown
  c.execute('SELECT id, name, financial_institution FROM accounts ORDER BY name')
  accounts = c.fetchall()
  
  if not accounts:
    messagebox.showwarning("No Accounts", "Please add at least one account before tracking balances.")
    balance_window.destroy()
    return
  
  # Create account selection dropdown
  tk.Label(balance_window, text="Select Account:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
  account_var = tk.StringVar()
  account_dropdown = ttk.Combobox(balance_window, textvariable=account_var, state="readonly", width=40)
  account_dropdown['values'] = [f"{acc[1]} - {acc[2]}" for acc in accounts]
  account_dropdown.grid(row=0, column=1, padx=10, pady=5)
  
  # Date entry
  tk.Label(balance_window, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky='e')
  entry_date = tk.Entry(balance_window, width=30)
  entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Default to today
  entry_date.grid(row=1, column=1, padx=10, pady=5)
  
  # Bank balance entry
  tk.Label(balance_window, text="Bank Balance:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
  entry_bank_balance = tk.Entry(balance_window, width=30)
  entry_bank_balance.grid(row=2, column=1, padx=10, pady=5)
  
  # Quicken balance entry
  tk.Label(balance_window, text="Quicken Balance:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
  entry_quicken_balance = tk.Entry(balance_window, width=30)
  entry_quicken_balance.grid(row=3, column=1, padx=10, pady=5)
  
  # Save balance function
  def save_balance():
    if not account_var.get():
      messagebox.showwarning("Input Error", "Please select an account.")
      return
    
    date = entry_date.get()
    bank_balance = entry_bank_balance.get()
    quicken_balance = entry_quicken_balance.get()
    
    if not date or not bank_balance or not quicken_balance:
      messagebox.showwarning("Input Error", "All fields are required.")
      return
    
    try:
      bank_balance = float(bank_balance)
      quicken_balance = float(quicken_balance)
      datetime.strptime(date, "%Y-%m-%d")  # Validate date format
    except ValueError:
      messagebox.showwarning("Input Error", "Please enter valid numbers for balances and date in YYYY-MM-DD format.")
      return
    
    # Get selected account ID
    selected_index = account_dropdown.current()
    account_id = accounts[selected_index][0]
    
    # Save to database
    c.execute('INSERT INTO balances (account_id, date, bank_balance, quicken_balance) VALUES (?, ?, ?, ?)', 
              (account_id, date, bank_balance, quicken_balance))
    conn.commit()
    
    messagebox.showinfo("Success", "Balance record saved successfully!")
    entry_date.delete(0, tk.END)
    entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
    entry_bank_balance.delete(0, tk.END)
    entry_quicken_balance.delete(0, tk.END)
    account_dropdown.set("")
  
  # Save button
  tk.Button(balance_window, text="Save Balance", command=save_balance).grid(row=4, column=0, columnspan=2, pady=20)

# View balance records function
def view_balances():
  # Create a new window
  balance_view_window = tk.Toplevel(root)
  balance_view_window.title("View Balance Records")
  balance_view_window.geometry("900x500")
  
  # Create a text widget with scrollbar
  text_frame = tk.Frame(balance_view_window)
  text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
  
  scrollbar = tk.Scrollbar(text_frame)
  scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
  
  text_widget = tk.Text(text_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD)
  text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
  
  scrollbar.config(command=text_widget.yview)
  
  # Fetch and display balance records
  c.execute('''
    SELECT b.id, a.name, a.financial_institution, b.date, b.bank_balance, b.quicken_balance
    FROM balances b
    JOIN accounts a ON b.account_id = a.id
    ORDER BY b.date DESC, a.name
  ''')
  balance_records = c.fetchall()
  
  if not balance_records:
    text_widget.insert(tk.END, "No balance records found in the database.")
  else:
    text_widget.insert(tk.END, "BALANCE TRACKING RECORDS:\n")
    text_widget.insert(tk.END, "=" * 90 + "\n\n")
    
    for record in balance_records:
      record_id, account_name, financial_institution, date, bank_balance, quicken_balance = record
      difference = bank_balance - quicken_balance
      
      text_widget.insert(tk.END, f"Record ID: {record_id}\n")
      text_widget.insert(tk.END, f"Account: {account_name} ({financial_institution})\n")
      text_widget.insert(tk.END, f"Date: {date}\n")
      text_widget.insert(tk.END, f"Bank Balance: ${bank_balance:,.2f}\n")
      text_widget.insert(tk.END, f"Quicken Balance: ${quicken_balance:,.2f}\n")
      text_widget.insert(tk.END, f"Difference: ${difference:,.2f}")
      if difference != 0:
        text_widget.insert(tk.END, " ⚠️" if abs(difference) > 0.01 else "")
      text_widget.insert(tk.END, "\n")
      text_widget.insert(tk.END, "-" * 60 + "\n\n")
  
  # Make text widget read-only
  text_widget.config(state=tk.DISABLED)

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
tk.Button(root, text="View Accounts", command=view_accounts).grid(row=5, column=0, columnspan=2, pady=5)
tk.Button(root, text="Track Balance", command=track_balance).grid(row=6, column=0, columnspan=2, pady=5)
tk.Button(root, text="View Balances", command=view_balances).grid(row=7, column=0, columnspan=2, pady=5)
tk.Button(root, text="View Balances", command=view_balances).grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()
conn.close()