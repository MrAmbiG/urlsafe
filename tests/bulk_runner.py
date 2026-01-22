import requests
import time
import sys

def check_url(url, expected_category):
    api_url = "http://localhost:8000/check"
    try:
        response = requests.get(api_url, params={"url": url})
        if response.status_code == 200:
            data = response.json()
            is_safe = data['is_safe']
            categories = data['categories']

            # Determine actual detected categories
            detected = [k for k, v in categories.items() if v]

            # Formatting output
            status = "SAFE" if is_safe else "UNSAFE"
            print(f"URL: {url:<30} | Expected: {expected_category:<10} | Detected: {','.join(detected):<20} | Status: {status}")
        else:
            print(f"Error checking {url}: {response.status_code}")
    except Exception as e:
        print(f"Failed to check {url}: {e}")

def main():
    try:
        with open("tests/test_urls.txt", "r") as f:
            lines = f.readlines()

        print(f"{'URL':<30} | {'Expected':<10} | {'Detected':<20} | {'Status'}")
        print("-" * 80)

        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) >= 2:
                category, url = parts[0], parts[1]
                check_url(url, category)

    except FileNotFoundError:
        print("tests/test_urls.txt not found")

if __name__ == "__main__":
    main()
