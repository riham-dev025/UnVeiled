import requests
import socket

domains = [
    ("Hugging Face", "api-inference.huggingface.co", "https://api-inference.huggingface.co"),
    ("Groq", "api.groq.com", "https://api.groq.com")
]

for name, host, url in domains:
    print(f"\nInvestigating {name}...")
    try:
        # Step 1: Test DNS Translation
        ip = socket.gethostbyname(host)
        print(f"DNS Success: {host} translates to {ip}")
        
        # Step 2: Test Connection
        requests.get(url, timeout=5)
        print(f"Connection Success: Can reach {name}!")
    except Exception as e:
        print(f"FAILED to reach {name}: {e}")