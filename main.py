import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry, Calendar
import pandas as pd
from datetime import datetime

from util.general import get_df_from_excel, save_df_to_excel, set_GUI_size

# FIXME: put in config or parser parameter
FILE = 'entries/2024.xlsx' 
COLUMNS = ["Type", "Category", "Date", "Vendor", "Medium", "Amount", "Note"]
FONT = ("Arial", 14)
ENTRY_WIDTH = 30
# -------------------------------------------------------------------------------- #

# Load in dataframe. 
transactions_df: pd.DataFrame = get_df_from_excel(
    file=FILE,
    columns=COLUMNS
)

# Create main window
root = tk.Tk()
root.title("Finance Tracker")
set_GUI_size(root)

############################## TRANSACATION TYPE ##############################
transaction_type = tk.StringVar(root)
transaction_type.set("Expense")

# Dropdown menu for Transaction Type
transaction_type_label = tk.Label(root, text="Transaction Type:")
transaction_type_label.pack()
transaction_type_menu = tk.OptionMenu(root, transaction_type, "Income", "Expense")
transaction_type_menu.pack()
###############################################################################


################################### CATEGORY ##################################

# Sample lists of options
income_categories = [
    'Digital Payment', 
    'Extra Income', 
    'Gifts', 
    'Interest', 
    'Other', 
    'Salary']
expense_categories = [
    'Bills', 
    'Car Services', 
    'Entertainment', 
    'Food & Drink', 
    'Gas', 
    'Gifts', 
    'Groceries', 
    'Media & Subscriptions', 
    'Other', 
    'Rent & Utilities',
    'Retirement',
    'Services', 
    'Shopping', 
    'Student Loans', 
    'Transport', 
    'Travel']

# Variables to store selected options
category_options = tk.StringVar(root)
category_options.set(expense_categories[0])  # Default value

# Function to update Category dropdown based on Transaction Type
def update_categories(*args):
    selected_type = transaction_type.get()
    if selected_type == "Income":
        category_menu["menu"].delete(0, "end")  # Clear previous options
        for category in income_categories:
            category_menu["menu"].add_command(label=category, command=tk._setit(category_options, category))
        category_options.set(income_categories[0])  # Set default value for Income
    elif selected_type == "Expense":
        category_menu["menu"].delete(0, "end")  # Clear previous options
        for category in expense_categories:
            category_menu["menu"].add_command(label=category, command=tk._setit(category_options, category))
        category_options.set(expense_categories[0])  # Set default value for Expense

# Trace the changes in the Transaction Type variable and update the Category dropdown accordingly
transaction_type.trace("w", update_categories)

# Dropdown menu for Category
category_label = tk.Label(root, text="Category:")
category_label.pack()
category_menu = tk.OptionMenu(root, category_options, *expense_categories)
category_menu.pack()
###############################################################################


##################################### DATE ####################################
date_label = tk.Label(root, text="Date:")
date_label.pack()

# Create a DateEntry widget
date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2,)

date_entry = Calendar(root, selectmode = 'day',
                      year = 2023, month = 10,
                      day = 30)
date_entry.pack(padx=10, pady=10)
###############################################################################


#################################### VENDOR ###################################
vendor_label = tk.Label(root, text="Vendor:")
vendor_label.pack()
vendor_entry = tk.Entry(root, font=FONT, width=ENTRY_WIDTH)
vendor_entry.pack()
###############################################################################


################################### MEDIUM ####################################
medium_categories = [
    "Amex Credit",
    "Bilt Credit",
    "BoA Checking",
    "BoA Credit",
    "BoA Saving",
    "Capital One Saving",
    "Cash",
    "Chase Credit",
    "Venmo"
]

medium_entry = tk.StringVar(root)
medium_entry.set("Amex Credit")

medium_label = tk.Label(root, text="Medium:")
medium_label.pack()
medium_menu = tk.OptionMenu(root, medium_entry, *medium_categories)
medium_menu.pack()
###############################################################################


#################################### AMOUNT ###################################
amount_label = tk.Label(root, text="Amount:")
amount_label.pack()
amount_entry = tk.Entry(root, font=FONT, width=ENTRY_WIDTH)
amount_entry.pack()
###############################################################################


##################################### NOTE ####################################
note_label = tk.Label(root, text="Note:")
note_label.pack()
note_entry = tk.Entry(root, font=FONT, width=ENTRY_WIDTH)
note_entry.pack()
###############################################################################

# Function to handle adding transactions.
def add_transaction():
    global transactions_df

    date = date_entry.get_date()
    date = datetime.strptime(date, "%m/%d/%y")
    date = date.strftime("%m/%d/%Y")

    transaction_data = {
        "Type": transaction_type.get(),
        "Category": category_options.get(),
        "Date": date,
        "Vendor": vendor_entry.get(),
        "Medium": medium_entry.get(),
        "Amount": amount_entry.get(),
        "Note": note_entry.get()
    }

    transactions_df = pd.concat([transactions_df, pd.DataFrame(transaction_data, index=[0])], ignore_index=True)
    save_df_to_excel(df=transactions_df, file=FILE)
    messagebox.showinfo("Success", "Transaction added successfully!")

# Button to add transaction
add_button = tk.Button(root, text="Add Transaction", command=add_transaction)
add_button.pack()
###############################################################################

# Run the main loop
root.mainloop()