import requests
import threading
import colorama
from colorama import Fore, Style
import time
import pyfiglet

colorama.init()

import pyfiglet

ascii_art = pyfiglet.figlet_format("Telegram Username Checker")
print(f"{Fore.CYAN}{ascii_art}{Style.RESET_ALL}")


def check_username(username, success_file, fail_file):
    url = f"https://fragment.com/?query={username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*"
    }

    try:
        response = requests.get(url, headers=headers)
        count_unavail = response.text.count("status-unavail\">Unavailable")
        count_avail = response.text.count("status-avail\">Available")
        count_taken = response.text.count("status-taken\">Taken")

        if count_unavail > 1:
            print(f"{Fore.GREEN}{username} is available{Style.RESET_ALL}")
            with open(success_file, "a") as f:
                f.write(username + '\n')
        elif count_avail > 1:
            print(f"{Fore.RED}{username} is not available{Style.RESET_ALL}")
            with open(fail_file, "a") as f:
                f.write(username + '\n')
        elif count_taken > 1:
            print(f"{Fore.RED}{username} is taken{Style.RESET_ALL}")
            with open(fail_file, "a") as f:
                f.write(username + '\n')
        else:
            print(f"{Fore.RED}{username} status could not be determined{Style.RESET_ALL}")
            with open(fail_file, "a") as f:
                f.write(username + '\n')
    except Exception:
            print(f"{Fore.RED}Error checking {username}: Check your Internet connection{Style.RESET_ALL}")


def main():
    username_file = input(f"{Fore.YELLOW}Enter .txt file containing username: {Style.RESET_ALL}")
    success_file = "available.txt"
    fail_file = "taken.txt"

    thread_count = int(input(f"{Fore.CYAN}Enter the number of threads (press 0 for default 10): {Style.RESET_ALL}") or 10)

    usernames = []
    with open(username_file, "r") as f:
        usernames = [line.strip() for line in f.readlines()]

    start_time = time.time()

    threads = []
    for username in usernames:
        thread = threading.Thread(target=check_username, args=(username, success_file, fail_file))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    total_time = round(end_time - start_time, 2)

    print(f"\n{len(usernames)} total checked")
    print(f"{Fore.GREEN}{len(open(success_file).readlines())} username are available{Style.RESET_ALL}")
    print(f"{Fore.RED}{len(open(fail_file).readlines())} username are not available{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{total_time} seconds total time took in checking{Style.RESET_ALL}")
    ascii_art = pyfiglet.figlet_format("Go Away Demon -_- ")
    print(f"{Fore.RED}{ascii_art}{Style.RESET_ALL}")

    input("Enter any key to exit..........")

if __name__ == "__main__":
    main()
