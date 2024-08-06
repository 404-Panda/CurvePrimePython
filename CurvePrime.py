import math
import random
import time
import requests
import json
import sys
from hashlib import sha256
from bitcoin import privtopub, pubtoaddr
from sympy import primerange
from concurrent.futures import ThreadPoolExecutor, as_completed

# Increase the limit for integer string conversion
sys.set_int_max_str_digits(10000)

prime_cache = {}

def generate_primes(start, end):
    """Generate primes using sympy's primerange and cache results for better performance."""
    if (start, end) not in prime_cache:
        prime_cache[(start, end)] = list(primerange(start, end))
    return prime_cache[(start, end)]

def calculate_merit(p, gap):
    """Calculate the merit of a prime gap."""
    return gap / math.log(p)

def calculate_difficulty(p, gap):
    """Calculate the difficulty of a prime gap."""
    rand_p = random.uniform(0, 1)
    return gap / math.log(p) + (2 / math.log(p)) * rand_p

def sieve_and_find_gaps(start, end):
    """Sieve for primes in the given range and find prime gaps."""
    primes = generate_primes(start, end)
    gaps = []
    for i in range(1, len(primes)):
        gap = primes[i] - primes[i-1]
        merit = calculate_merit(primes[i-1], gap)
        difficulty = calculate_difficulty(primes[i-1], gap)
        gaps.append((primes[i-1], gap, merit, difficulty))
    return gaps

def find_best_gap(gaps):
    """Find the prime gap with the highest merit."""
    return max(gaps, key=lambda x: x[2])

def generate_bitcoin_address(pvk_value):
    """Generate a Bitcoin address from a PVK value."""
    hex_pvk = format(pvk_value, '064x')  # Ensure the private key is 32 bytes (64 hex characters)
    pub_key = privtopub(hex_pvk)
    address = pubtoaddr(pub_key)
    return address, hex_pvk, pub_key

def check_balance(address):
    """Check the balance of a Bitcoin address using a local blockchain explorer API."""
    url = f"http://localhost:2760/chain/Bitcoin/q/getreceivedbyaddress/{address}"
    retry_count = 0
    status_message = "OK"
    while retry_count < 5:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return int(response.text), status_message
            else:
                status_message = "API Blocked"
                return 0, status_message
        except requests.RequestException:
            retry_count += 1
            time.sleep(2 ** retry_count)  # Exponential backoff
    status_message = "API Blocked"
    return 0, status_message

def hamming_distance(s1, s2):
    """Calculate the Hamming distance between two hexadecimal strings."""
    return bin(int(s1, 16) ^ int(s2, 16)).count('1')

def entropy(s):
    """Calculate the entropy of a hexadecimal string."""
    probabilities = [float(s.count(c)) / len(s) for c in set(s)]
    return - sum([p * math.log(p) / math.log(2.0) for p in probabilities])

def print_info(iteration, pvk, hex_pvk, address, balance, gap_start, gap_size, merit, difficulty, start_index, end_index, best_merit, best_difficulty, kangaroo_hops, best_prime, next_range, pub_key, prev_hex_pvk, api_status):
    range_searched = ((pvk - start_index) / (end_index - start_index)) * 100
    sha256_pvk = sha256(hex_pvk.encode()).hexdigest()
    sha256_pub_key = sha256(pub_key.encode()).hexdigest()
    hamming_dist = hamming_distance(hex_pvk, prev_hex_pvk) if prev_hex_pvk else 'N/A'
    pvk_entropy = entropy(hex_pvk)
    pub_key_entropy = entropy(pub_key)
    info = (
        f"\033[96mIteration: {iteration}\033[0m\n"
        f"  \033[92mPVK:\033[0m {pvk}\n"
        f"  \033[92mHex PVK:\033[0m {hex_pvk}\n"
        f"  \033[92mSHA-256 PVK:\033[0m {sha256_pvk}\n"
        f"  \033[92mAddress:\033[0m {address}\n"
        f"  \033[92mBalance:\033[0m {balance}\n"
        f"  \033[93mGap Start:\033[0m {gap_start}\n"
        f"  \033[93mGap Size:\033[0m {gap_size}\n"
        f"  \033[93mMerit:\033[0m {merit}\n"
        f"  \033[93mDifficulty:\033[0m {difficulty}\n"
        f"  \033[94mRange Searched:\033[0m {start_index} - {end_index}\n"
        f"  \033[94mRange Searched Percentage:\033[0m {range_searched:.2f}%\n"
        f"  \033[95mBest Merit Found:\033[0m {best_merit}\n"
        f"  \033[95mBest Difficulty Found:\033[0m {best_difficulty}\n"
        f"  \033[95mKangaroo Hops:\033[0m {kangaroo_hops}\n"
        f"  \033[95mBest Prime Found:\033[0m {best_prime}\n"
        f"  \033[95mNext Range:\033[0m {next_range}\n"
        f"  \033[92mPublic Key:\033[0m {pub_key}\n"
        f"  \033[92mSHA-256 Public Key:\033[0m {sha256_pub_key}\n"
        f"  \033[92mHamming Distance to Previous PVK:\033[0m {hamming_dist}\n"
        f"  \033[92mEntropy of PVK:\033[0m {pvk_entropy:.2f}\n"
        f"  \033[92mEntropy of Public Key:\033[0m {pub_key_entropy:.2f}\n"
        f"  \033[92mAPI Balance Request Status:\033[0m {api_status}\n"
    )
    sys.stdout.write("\033[H\033[J")  # Clear the terminal
    sys.stdout.write(info)
    sys.stdout.flush()

def display_puzzles(puzzles):
    """Display puzzles in a more readable format."""
    print("\nAvailable Puzzles:")
    for puzzle in puzzles:
        puzzle_num = puzzle["Puzzle"]
        key_range = puzzle["Key Range"]
        balance = puzzle["Address Balance"]
        status = "Solved" if "Solved" in puzzle["Balance"] else "Unsolved"
        print(f"Puzzle {puzzle_num}: Key Range {key_range}, Balance {balance}, Status {status}")
    print()

def main():
    # Load puzzle data from JSON file
    with open("output.json", "r") as json_file:
        puzzles = json.load(json_file)

    display_puzzles(puzzles)

    # Ask the user to select a puzzle range
    selected_puzzle_num = input("Enter the puzzle number to select the range: ")

    selected_puzzle = next((p for p in puzzles if p["Puzzle"] == selected_puzzle_num), None)
    if selected_puzzle:
        start_index = int(selected_puzzle["End Point"], 16)
        end_index = int(selected_puzzle["End Decimal"], 16)
    else:
        print("Invalid puzzle number selected. Exiting.")
        return

    pvk_values = [random.randint(start_index, end_index) for _ in range(10)]

    generated_addresses = []
    known_addresses = [
        "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so", "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9", "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ",
        "19vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG", "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU", "1JTK7s9YVYywfm5XUH7RNhHJH1LshCaRFR",
        "12VVRNPi4SJqUTsp6FmqDqY5sGosDtysn4", "1FWGcVDK3JGzCC3WtkYetULPszMaK2Jksv", "1DJh2eHFYQfACPmrvpyWc8MSTYKh7w9eRF",
        "1Bxk4CQdqL9p22JEtDfdXMsng1XacifUtE", "15qF6X51huDjqTmF9BJgxXdt1xcj46Jmhb", "1ARk8HWJMn8js8tQmGUJeQHjSE7KRkn2t8",
        "15qsCm78whspNQFydGJQk5rexzxTQopnHZ", "13zYrYhhJxp6Ui1VV7pqa5WDhNWM45ARAC", "14MdEb4eFcT3MVG5sPFG4jGLuHJSnt1Dk2",
        "1CMq3SvFcVEcpLMuuH8PUcNiqsK1oicG2D", "1K3x5L6G57Y494fDqBfrojD28UJv4s5JcK", "1PxH3K1Shdjb7gSEoTX7UPDZ6SH4qGPrvq",
        "16AbnZjZZipwHMkYKBSfswGWKDmXHjEpSf", "19QciEHbGVNY4hrhfKXmcBBCrJSBZ6TaVt", "1EzVHtmbN4fs4MiNk3ppEnKKhsmXYJ4s74",
        "1AE8NzzgKE7Yhz7BWtAcAAxiFMbPo82NB5", "17Q7tuG2JwFFU9rXVj3uZqRtioH3mx2Jad", "1K6xGMUbs6ZTXBnhw1pippqwK6wjBWtNpL",
        "15ANYzzCp5BFHcCnVFzXqyibpzgPLWaD8b", "18ywPwj39nGjqBrQJSzVq2izR12MDpDr8", "1CaBVPrwUxbQYYswu32w7Mj4HR4maNoJSX",
        "1JWnE6p6UN7ZJBN7TtcbNDoRcjFtuDWoNL", "1CKCVdbDJasYmhswB6HKZHEAnNaDpK7W4n", "1PXv28YxmYMaB8zxrKeZBW8dt2HK7RkRPX",
        "1AcAmB6jmtU6AiEcXkmiNE9TNVPsj9DULf", "1EQJvpsmhazYCcKX5Au6AZmZKRnzarMVZu", "18KsfuHuzQaBTNLASyj15hy4LuqPUo1FNB",
        "15EJFC5ZTs9nhsdvSUeBXjLAuYq3SWaxTc", "1HB1iKUqeffnVsvQsbpC6dNi1XKbyNuqao", "1GvgAXVCbA8FBjXfWiAms4ytFeJcKsoyhL",
        "1824ZJQ7nKJ9QFTRBqn7z7dHV5EGpzUpH3", "18A7NA9FTsnJxWgkoFfPAFbQzuQxpRtCos", "1NeGn21dUDDeqFQ63xb2SpgUuXuBLA4WT4",
        "174SNxfqpdMGYy5YQcfLbSTK3MRNZEePoy", "1MnJ6hdhvK37VLmqcdEwqC3iFxyWH2PHUV", "1KNRfGWw7Q9Rmwsc6NT5zsdvEb9M2Wkj5Z",
        "1PJZPzvGX19a7twf5HyD2VvNiPdHLzm9F6", "1GuBBhf61rnvRe4K8zu8vdQB3kHzwFqSy7", "1GDSuiThEV64c166LUFC9uDcVdGjqkxKyh",
        "1Me3ASYt5JCTAK2XaC32RMeH34PdprrfDx", "1CdufMQL892A69KXgv6UNBD17ywWqYpKut", "1BkkGsX9ZM6iwL3zbqs7HWBV7SvosR6m8N",
        "1PXAyUB8ZoH3WD8n5zoAthYjN15yN5CVq5", "1AWCLZAjKbV1P7AHvaPNCKiB7ZWVDMxFiz", "1G6EFyBRU86sThN3SSt3GrHu1sA7w7nzi4",
        "1MZ2L1gFrCtkkn6DnTT2e4PFUTHw9gNwaj", "1Hz3uv3nNZzBVMXLGadCucgjiCs5W9vaGz", "1Fo65aKq8s8iquMt6weF1rku1moWVEd5Ua",
        "16zRPnT8znwq42q7XeMkZUhb1bKqRogyy", "1KrU4dHE5WrW8rhWDsTRjR21r8t3dsrS3R", "17uDfp5r4n441xkgLFmhNoSW1KWp6xVLD",
        "13A3JrvXmvg5w9XGvyyR4JEJqiLz8ZySY3", "16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v", "1UDHPdovvR985NrWSkdWQDEQ1xuRiTALq",
        "15nf31J46iLuK1ZkTnqHo7WgN5cARFK3RA", "1Ab4vzG6wEQBDNQM1B2bvUz4fqXXdFk2WT", "1Fz63c775VV9fNyj25d9Xfw3YHE6sKCxbt",
        "1QKBaU6WAeycb3DbKbLBkX7vJiaS8r42Xo", "1CD91Vm97mLQvXhrnoMChhJx4TP9MaQkJo", "15MnK2jXPqTMURX4xC3h4mAZxyCcaWWEDD",
        "13N66gCzWWHEZBxhVxG18P8wyjEWF9Yoi1", "1NevxKDYuDcCh1ZMMi6ftmWwGrZKC6j7Ux", "19GpszRNUej5yYqxXoLnbZWKew3KdVLkXg",
        "1M7ipcdYHey2Y5RZM34MBbpugghmjaV89P", "18aNhurEAJsw6BAgtANpexk5ob1aGTwSeL", "1FwZXt6EpRT7Fkndzv6K4b4DFoT4trbMrV",
        "1CXvTzR6qv8wJ7eprzUKeWxyGcHwDYP1i2", "1MUJSJYtGPVGkBCTqGspnxyHahpt5Te8jy", "13Q84TNNvgcL3HJiqQPvyBb9m4hxjS3jkV",
        "1LuUHyrQr8PKSvbcY1v1PiuGuqFjWpDumN", "18192XpzzdDi2K11QVHR7td2HcPS6Qs5vg", "1NgVmsCCJaKLzGyKLFJfVequnFW9ZvnMLN",
        "1AoeP37TmHdFh8uN72fu9AqgtLrUwcv2wJ", "1FTpAbQa4h8trvhQXjXnmNhqdiGBd1oraE", "14JHoRAdmJg3XR4RjMDh6Wed6ft6hzbQe9",
        "19z6waranEf8CcP8FqNgdwUe1QRxvUNKBG", "14u4nA5sugaswb6SZgn5av2vuChdMnD9E5", "1NBC8uXJy1GiJ6drkiZa1WuKn51ps7EPTv"
    ]

    balance_log_file = "addresses_with_balances.txt"

    with open(balance_log_file, "w") as balance_file:
        balance_file.write("Address,Hex PVK,Balance\n")

    current_range = 10**5
    iteration = 0
    best_merit = 0
    best_difficulty = 0
    kangaroo_hops = 0
    best_prime = 0
    scan_time = 0

    prev_hex_pvk = None

    with ThreadPoolExecutor() as executor:
        while True:
            start_time = time.time()
            # Use Kangaroo Pollard's algorithm to skip ranges occasionally
            kangaroo = iteration % 10 == 0

            # Generate all primes in the current range
            primes = generate_primes(pvk_values[-1] + 1, min(pvk_values[-1] + current_range, end_index))
            
            for prime in primes:
                next_pvk_value = prime
                pvk_values.append(next_pvk_value)
                bitcoin_address, hex_pvk, pub_key = generate_bitcoin_address(next_pvk_value)
                generated_addresses.append((bitcoin_address, hex_pvk))

                # Submit check_balance task to ThreadPoolExecutor
                future = executor.submit(check_balance, bitcoin_address)
                balance, api_status = future.result()

                # Calculate merit and difficulty for logging purposes
                if len(pvk_values) > 1:
                    gap_start = pvk_values[-2]
                    gap_size = next_pvk_value - gap_start
                    merit = calculate_merit(gap_start, gap_size)
                    difficulty = calculate_difficulty(gap_start, gap_size)
                else:
                    gap_start = gap_size = merit = difficulty = 0

                if merit > best_merit:
                    best_merit = merit
                if difficulty > best_difficulty:
                    best_difficulty = difficulty
                if kangaroo:
                    kangaroo_hops += 1
                if pvk_values[-1] > best_prime:
                    best_prime = pvk_values[-1]

                iteration_time = time.time() - start_time
                scan_time = (scan_time * iteration + iteration_time) / (iteration + 1) * (current_range / len(primes))

                print_info(iteration, next_pvk_value, hex_pvk, bitcoin_address, balance, gap_start, gap_size, merit, difficulty, start_index, end_index, best_merit, best_difficulty, kangaroo_hops, best_prime, current_range, pub_key, prev_hex_pvk, api_status)

                # Check if the generated address is in the known list
                if bitcoin_address in known_addresses:
                    print(f"\033[91mFound known address! PVK: {next_pvk_value}, Address: {bitcoin_address}, Hex PVK: {hex_pvk}, Balance: {balance}\033[0m")

                if balance > 0:
                    with open(balance_log_file, "a") as balance_file:
                        balance_file.write(f"{bitcoin_address},{hex_pvk},{balance}\n")
                    # Show key and data on screen
                    print(f"\033[91mFound balance!\033[0m\n"
                          f"  \033[92mPVK:\033[0m {next_pvk_value}\n"
                          f"  \033[92mHex PVK:\033[0m {hex_pvk}\n"
                          f"  \033[92mAddress:\033[0m {bitcoin_address}\n"
                          f"  \033[92mBalance:\033[0m {balance}\n")

                prev_hex_pvk = hex_pvk
                iteration += 1

            # Increase the search range dynamically
            if iteration % 100 == 0:
                current_range *= 2
                print(f"\033[95mIncreasing search range to {current_range}\033[0m")

if __name__ == "__main__":
    main()
