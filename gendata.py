import json
import time
import random

def generate_data():
  """Generates a list of 50 dictionaries, 
     each containing 'close' (random int between 100 and 150) 
     and 'time' (unix timestamp with 5-minute intervals)."""

  data = []
  start_time = int(time.mktime(time.strptime("01/01/2025 10:00:00", "%d/%m/%Y %H:%M:%S")))
  for i in range(50):
    close_price = random.randint(100, 150)
    data.append({
      "close": close_price,
      "time": start_time + (i * 5 * 60)  # Add 5 minutes (in seconds) for each interval
    })
  return data

if __name__ == "__main__":
  data = generate_data()
  with open("data.json", "w") as f:
    json.dump(data, f, indent=2)