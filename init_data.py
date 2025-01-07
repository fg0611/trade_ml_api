import pandas as pd
from datetime import datetime

# Function to process timestamps
def process_time(data):
    result = []
    for record in data:
        try:
            # Convert Unix timestamp in milliseconds to a datetime object
            timestamp = record["time"] / 1000  # Convert milliseconds to seconds
            record["time"] = datetime.utcfromtimestamp(timestamp).isoformat()  # Convert to ISO format
        except (ValueError, OverflowError):
            record["time"] = None  # Handle out-of-bounds or invalid timestamps gracefully
        result.append(record)
    return result

def init_data(rates, global_st):

    processed_json = process_time(rates) # tiempo procesado

    # Convertir datos a DataFrame
    global_st["dfs"]["data"] = pd.DataFrame(processed_json)
    # global_st["dfs"]["data"]["time"] = pd.to_datetime(global_st["dfs"]["data"]["time"], unit="s")  # Convertir el tiempo UNIX a formato legible
    # Mostrar los datos
    # print(global_st["dfs"]["data"].tail(5))
