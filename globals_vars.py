from dotenv import load_dotenv
import os
import pandas as pd


load_dotenv()

class Globals:
    def __init__(self):
        # Define your variables as a dictionary for flexibility
        self._data = {
            "chart_path": "chart.png",
            "tlg": {  # Telegram
                "chat": os.getenv("TLG_CHAT"),
                "token": os.getenv("TLG_TOKEN"),
            },
            "models": {"all": "", "lag": 4},
            "dfs": {
                "data": pd.DataFrame(),
                "score": pd.DataFrame(),
                "trained": pd.DataFrame(),
                "future": pd.DataFrame(),
            },
        }

    def __getitem__(self, key):
        # Allows dictionary-like access
        return self._data[key]

    def __setitem__(self, key, value):
        # Allows dictionary-like assignment
        self._data[key] = value


# Create a shared instance
global_state = Globals()
print(global_state["tlg"]["chat"])
