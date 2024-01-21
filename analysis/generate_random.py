from datetime import datetime, timedelta
import pandas as pd
import random
import sys

sys.path.append('..')
from util.general import get_df_from_excel, save_df_to_excel
from util.params import (
    FILE, COLUMNS, 
    income_categories, expense_categories, medium_categories,
)

LENGTH_RANDOM_DF = 1000

# -------------------------------------------------------------------------------- #
# Load in dataframe. 
transactions_df: pd.DataFrame = get_df_from_excel(
    file='../'+FILE,
    columns=COLUMNS,
)

for i in range(LENGTH_RANDOM_DF):
    # Generate` random type.
    type = random.choice(['Income', 'Expense'])

    # Generate random category.
    categories = income_categories if type == 'Income' else expense_categories
    category = random.choice(categories)

    # Generate random date.
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

    # Generate random vendor. 
    num_vendors = 5 if type == 'Income' else 25
    vendor = 'Vendor ' + str(random.randint(1, num_vendors))

    # Generate random medium.
    mediums = [i for i in medium_categories if 'Credit' not in i] if type == 'Income' else [i for i in medium_categories if 'Credit' in i]
    medium = random.choice(mediums)

    # Generate random amount.
    amount = random.randint(1, 1000)

    COLUMNS = ["Type", "Category", "Date", "Vendor", "Medium", "Amount", "Note"]

    row = {
        'Type': type,
        'Category': category,
        'Date': date,
        'Vendor': vendor,
        'Medium': medium,
        'Amount': amount,
        'Note': '',
    }

    transactions_df.loc[len(transactions_df)] = row

save_df_to_excel(df=transactions_df, file='../'+FILE)
