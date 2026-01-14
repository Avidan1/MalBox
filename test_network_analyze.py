import socket
import urllib.request

print("--- MalBox Network Test ---")
try:
    # 1. DNS Lookup
    print("Resolving google.com...")
    ip = socket.gethostbyname("google.com")
    print(f"IP: {ip}")

    # 2. HTTP Request
    print("Fetching example.com...")
    with urllib.request.urlopen("http://example.com", timeout=5) as f:
        print(f"Status: {f.getcode()}")
except Exception as e:
    print(f"Network error: {e}")