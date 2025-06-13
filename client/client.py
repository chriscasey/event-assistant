import requests
import time

SERVER_URL = "http://app-server:8000/ask"
MAX_RETRIES = 10
RETRY_DELAY = 2

def wait_for_server():
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(SERVER_URL, json={"question": "ping"})
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(RETRY_DELAY)
    print("Failed to connect to server.")
    return False

def main():
    if not wait_for_server():
        return

    print("Ask the event assistant (type 'exit' to quit):")
    while True:
        try:
            q = input("> ").strip()
            if q.lower() == "exit":
                break
            response = requests.post(SERVER_URL, json={"question": q})
            if response.status_code == 200:
                print("Assistant:", response.json().get("answer"))
            else:
                print("Error:", response.status_code, response.text)
        except EOFError:
            break
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
