import requests
import sys
import os
import time
import subprocess

def run_test():
    # Ensure server is running or start it (for the sake of this script, we assume running or start new)
    # Ideally, we start a fresh instance to ensure no pollution, but we can also test against running

    proc = subprocess.Popen(
        ["uv", "run", "uvicorn", "app.main:app", "--port", "8002"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    base_url = "http://localhost:8002"

    print("Waiting for server to start...")
    try:
        for _ in range(30):
            try:
                requests.get(base_url)
                print("Server ready.")
                break
            except requests.ConnectionError:
                time.sleep(1)
        else:
            print("Server failed to start.")
            proc.terminate()
            return False

        # Read test data
        data_file = os.path.join(os.path.dirname(__file__), "test_urls.txt")
        with open(data_file, "r") as f:
            lines = f.readlines()

        passed = 0
        failed = 0

        print(f"\n{'Expected':<15} | {'URL':<40} | {'Result':<10}")
        print("-" * 70)

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            category, url = line.split(",", 1)

            try:
                resp = requests.get(f"{base_url}/check", params={"url": url})
                data = resp.json()
                cats = data.get("categories", {})

                # Determine outcome
                is_hit = False

                if category == "safe":
                    # Expect all false
                    if not any(cats.values()):
                        is_hit = True
                else:
                    # Expect specific category true
                    # Handle adult/porn aliasing
                    check_cat = category
                    if category == "adult":
                         # API returns porn=True and adult=True for both
                         check_cat = "adult"

                    if cats.get(check_cat):
                        is_hit = True

                    # Fallback check for porn/adult equivalence if needed
                    # If expecting adult, but porn is set, that's valid as per my logic

                status = "PASS" if is_hit else "FAIL"
                if is_hit:
                    passed += 1
                else:
                    failed += 1

                print(f"{category:<15} | {url[:40]:<40} | {status:<10}")
                if not is_hit:
                    print(f"  Got: {cats}")

            except Exception as e:
                print(f"Error testing {url}: {e}")
                failed += 1

        print("-" * 70)
        print(f"Total: {passed + failed}, Passed: {passed}, Failed: {failed}")

        return failed == 0

    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
