import pandas as pd
from typing import List

from util.params import PERCENT_SCREEN_WIDTH, PERCENT_SCREEN_HEIGHT

def get_df_from_excel(file: str, columns: List[str]) -> pd.DataFrame:
    # Load existing data from Excel file if it exists.
    try:
        transactions_df = pd.read_excel(file)
    except FileNotFoundError:
        transactions_df = pd.DataFrame(columns=columns)

    return transactions_df

def save_df_to_excel(df: pd.DataFrame, file: str) -> None:
    # Save to Excel file.
    df.to_excel(file, index=False)  
    return

def set_GUI_size(root) -> None:
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * PERCENT_SCREEN_WIDTH)  # % of the screen width
    window_height = int(screen_height * PERCENT_SCREEN_HEIGHT)  # % of the screen height
    root.geometry(f"{window_width}x{window_height}")
