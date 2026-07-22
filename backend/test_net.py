import requests

try:
    print("Trying to ping Google...")
    response = requests.get("https://www.google.com", timeout=5)
    print("Success! Python has internet access.")
except Exception as e:
    print(f"Failed. Your computer is blocking Python: {e}")