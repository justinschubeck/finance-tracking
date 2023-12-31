import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry, Calendar
import pandas as pd
from datetime import datetime, date

from util.general import get_df_from_excel, save_df_to_excel, set_GUI_size

# FIXME: put in config or parser parameter
FILE = 'entries/2024.xlsx' 
COLUMNS = ["Type", "Category", "Date", "Vendor", "Medium", "Amount", "Note"]
FONT = ("Arial", 12)
ENTRY_WIDTH = 20

selected_color_bg = "#E0E0E0"  # Selected Button Background Color (Green)
selected_color_fg = "#000000"  # Selected Button Text Color (White)

non_selected_color_bg = "#E0E0E0"  # Non-Selected Button Background Color (Light Gray)
non_selected_color_fg = "#000000"  # Non-Selected Button Text Color (Black)
# -------------------------------------------------------------------------------- #

# Load in dataframe. 
transactions_df: pd.DataFrame = get_df_from_excel(
    file=FILE,
    columns=COLUMNS,
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
transaction_type_label.grid(row=1, column=1, columnspan=2, rowspan=1)

# RadioButtons for Income and Expense
income_radio = tk.Radiobutton(root, text="Income", variable=transaction_type, value="Income", 
                              indicator=0, bg=selected_color_bg, fg=selected_color_fg, width=20)
income_radio.grid(row=2, column=1, rowspan=2)
expense_radio = tk.Radiobutton(root, text="Expense", variable=transaction_type, value="Expense", 
                               indicator=0, bg=selected_color_bg, fg=selected_color_fg, width=20)
expense_radio.grid(row=2, column=2, rowspan=2)
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

# Dropdown menu for Category
category_label = tk.Label(root, text="Category:")
category_label.grid(row=4, column=1, columnspan=2, rowspan=2)

# Function to update Category based on Transaction Type
def update_categories(*args):
    selected_type = transaction_type.get()

    if selected_type == "Income":
        categories = income_categories
    else:
        categories = expense_categories
    category_options.set(categories[0])
        
    # Clear existing Radiobuttons
    for widget in category_frame.winfo_children():
        widget.destroy()
    
    # Create new Radiobuttons
    for i, category in enumerate(categories):
        tk.Radiobutton(category_frame, text=category, variable=category_options, value=category,
                       indicator=0, bg=selected_color_bg, fg=selected_color_fg, width=20).grid(row=6+i, column=1, columnspan=2)

# Frame to hold the category Radiobuttons
category_frame = tk.Frame(root)
category_frame.grid(row=6, column=1, columnspan=2)
update_categories()

# Trace the changes in the Transaction Type variable and update the Category accordingly
transaction_type.trace("w", update_categories)
###############################################################################


##################################### DATE ####################################
date_label = tk.Label(root, text="Date:")
date_label.grid(row=0, column=0)
root.columnconfigure(0, minsize=275)

# Create a DateEntry widget
date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2,)

# Extract year, month, and day from today's date
today = date.today()
year = today.year
month = today.month
day = today.day
date_entry = Calendar(root, selectmode = 'day',
                      year = year, month = month,
                      day = day)
date_entry.place(x=10, y=25)
###############################################################################


#################################### VENDOR ###################################
vendor_label = tk.Label(root, text="Vendor:")
vendor_label.grid(row=0, column=3, padx=5)
vendor_entry = tk.Entry(root, font=FONT, width=ENTRY_WIDTH)
vendor_entry.grid(row=1, column=3, padx=5)
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
medium_label.grid(row=4, column=3)
medium_menu = tk.OptionMenu(root, medium_entry, *medium_categories)
medium_menu.grid(row=5, column=3)
###############################################################################


#################################### AMOUNT ###################################
amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=2, column=3, padx=5)
amount_entry = tk.Entry(root, font=FONT, width=ENTRY_WIDTH)
amount_entry.grid(row=3, column=3, padx=5)

def format_currency(event):
    entry_content = amount_entry.get()
    
    # Remove any non-digit characters from the input content
    digits = [char for char in entry_content if char.isdigit()]

    try:
        # Convert the parsed digits to a float and format as currency
        value = float("".join(digits)) / 100
        formatted_value = "${:.2f}".format(value)
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, formatted_value)
    except ValueError:
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, "$0.00")

def handle_keypress(event):
    # Allow only digits, backspace, and the decimal point
    allowed_keys = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "\b"}
    if event.char not in allowed_keys:
        return 'break'
amount_entry.bind("<KeyRelease>", format_currency)
amount_entry.bind("<KeyPress>", handle_keypress)

###############################################################################


##################################### NOTE ####################################
note_label = tk.Label(root, text="Note:")
note_label.grid(row=0, column=4)
note_entry = tk.Text(root, font=FONT, width=ENTRY_WIDTH, wrap="word")
note_entry.place(x=770, y=20)
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
        "Amount": amount_entry.get().replace('$', ''),
        "Note": note_entry.get("1.0", tk.END)
    }

    if(vendor_entry.get() == ''):
        messagebox.showinfo("ERROR", "Missing vendor!")
    elif(amount_entry.get() == '' or amount_entry.get() == '$0.00'):
        messagebox.showinfo("ERROR", "Missing amount!")
    else:
        vendor_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        note_entry.delete(1.0, tk.END)

        transactions_df = pd.concat([transactions_df, pd.DataFrame(transaction_data, index=[0])], ignore_index=True)
        save_df_to_excel(df=transactions_df, file=FILE)
        messagebox.showinfo("Success", "Transaction added successfully!")

# Button to add transaction
add_button = tk.Button(root, text="Add Transaction", command=add_transaction, width=30, height=10, bg="green", fg="white")
add_button.place(x=25, y=225)
###############################################################################

# Run the main loop
root.mainloop()