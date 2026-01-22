import requests
import sys

# Usage: python simple_test.py "url"

def check_single_url(url):
    # Endpoint
    api_url = "http://localhost:8000/check"

    print(f"Checking URL: {url}")
    try:
        # GET request
        response = requests.get(api_url, params={"url": url})

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(f"Error: Status Code {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to localhost:8000. Is the server running?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Default to 007win.com if no argument provided
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://007win.com"
    check_single_url(target_url)
