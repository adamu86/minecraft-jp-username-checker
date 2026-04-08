import sys
import os
import time
import concurrent.futures
import threading
import requests
from tqdm import tqdm

try:
    import requests
    from tqdm import tqdm
except ImportError:
    print("Installing required modules...\n")
    input("Press enter to continue...")
    for cmd in ["py", "python", "python3"]:
        os.system(f"{cmd} -m pip install requests tqdm")
    print("Done. Restart script.")
    sys.exit()



APP_INPUT_PATH  = "../input/"
APP_OUTPUT_PATH = "../output/"

MAN_OPTIMIZED   = "first_name_man_opti.csv"
MAN_ORIGINAL    = "first_name_man_org.csv"
WOMAN_OPTIMIZED = "first_name_woman_opti.csv"
WOMAN_ORIGINAL  = "first_name_woman_org.csv"


API = "https://api.mojang.com/users/profiles/minecraft/"
REQUEST_DELAY = 0.4
MAX_WORKERS   = 5

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"


lock            = threading.Lock()
last_request_time = 0
available_names = []
client          = requests.Session()


def rate_limited_request():
    global last_request_time
    with lock:
        now  = time.time()
        wait = REQUEST_DELAY - (now - last_request_time)
        if wait > 0:
            time.sleep(wait)
        last_request_time = time.time()


def check_username(username):
    retry = True
    while retry:
        retry = False
        rate_limited_request()

        try:
            res = client.get(f"{API}{username}", timeout=10)
        except requests.RequestException:
            tqdm.write(f"{YELLOW}⏺ {username}{RESET}")
            retry = True
            time.sleep(2)
            continue

        if res.status_code == 200:
            tqdm.write(f"{RED}⏺ {username}{RESET}")

        elif res.status_code in (204, 404):
            available_names.append(username)
            tqdm.write(f"{GREEN}⏺ {username}{RESET}")
            output_file = f"{APP_OUTPUT_PATH}{MAN_OPTIMIZED.split('.')[0]}_available.txt"
            with open(output_file, "a") as f:
                f.write(username + "\n")

        elif res.status_code == 429:
            time.sleep(15)
            retry = True

        else:
            retry = True
            time.sleep(5)



filepath = f"{APP_INPUT_PATH}{MAN_OPTIMIZED}"

with open(filepath) as f:
    username_list = [line.strip() for line in f if line.strip()]

if not username_list:
    print("File is empty.")
    sys.exit()

print(f"Checking {len(username_list)} usernames\n")

with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    list(tqdm(executor.map(check_username, username_list), total=len(username_list)))