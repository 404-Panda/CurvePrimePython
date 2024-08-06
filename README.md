# Python Script for Cryptographic Bitcoin Puzzles

<p align="center">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" width="40" height="40"/>
  <img src="https://github.com/spothq/cryptocurrency-icons/blob/master/32%402x/color/btc%402x.png" alt="Bitcoin" width="40" height="40"/>
</p>

As the architect of this multifaceted Python script, I designed it to delve into cryptographic puzzles associated with Bitcoin. This tool not only generates Bitcoin addresses from private keys derived within specific numerical ranges but also explores prime gaps and their properties extensively.

<p align="center">
  <img src="https://github.com/DaCryptoRaccoon/CurvePrimePython/blob/main/video.gif" alt="KeyTools">
</p>



## How To Install

## Setup Guide

This project requires a fully synchronized Bitcoin node and a local instance of the Bitcoin ABE explorer, which will use a MySQL database for queries. The setup process is tailored for users with a basic understanding of Bitcoin's infrastructure and experience with Python, specifically Python 2.7.18.

### Prerequisites
- ** Ubuntu 22.04.4 LTS **: Build enviro
- **Python 2.7.18**: The project is compatible with Python 2.7.18, and it is crucial to use this version to avoid compatibility issues with Bitcoin ABE.
- **Bitcoin Core Node**: A running Bitcoin node is required for the Bitcoin ABE to access blockchain data.
- **MySQL Database**: Bitcoin ABE will use a MySQL database to store and query blockchain data.

### Step 1: Install Python 2.7.18

Ensure that Python 2.7.18 is installed on your system. You can download it from the [official Python archives](https://www.python.org/downloads/release/python-2718/). 

Follow the installation instructions specific to your operating system for this guide we will be building everything in Ubuntu 22.04.4 LTS

### Step 2: Set Up a Bitcoin Node

1. **Download Bitcoin Core**: You can download the latest version of Bitcoin Core from the [official repository](https://github.com/bitcoin/bitcoin). It's recommended to review the [build instructions for Unix](https://github.com/bitcoin/bitcoin/blob/master/doc/build-unix.md) if you are running on a Unix-based system.

2. **Installation**: Follow the detailed instructions in the link provided to compile and install Bitcoin Core.

3. **Blockchain Synchronization**: Run the Bitcoin Core client to start downloading the blockchain. This process can take a significant amount of time, depending on your internet connection and the hardware specifications of your system.

## Step 3: Setup MYSQL DB

Quick Guide to Create a MySQL Database for Bitcoin ABE
Access MySQL Command Line by opening your terminal or command prompt.

Connect to your MySQL server as the root user (or another user with sufficient privileges to create databases and users):
```
mysql -u root -p
```

You'll be prompted to enter the root user's password.

Step 2: Create the Database

Once you’re connected to MySQL, create a new database named BitcoinABE:
```
CREATE DATABASE BitcoinABE;
```
Step 3: Create a New User

Create a new user and grant it access to the newly created database. This user will have the credentials specified in your connect-args. Adjust the credentials as necessary based on your security practices:
```
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON BitcoinABE.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```
admin is the username.
admin is the password. 

(USE A SECURE PASSWORD JUST MAKE SURE YOU NOTE THIS DOWN YOU NEED IT FOR YOUR ABE CONF LATER IN THE SETUP.)

localhost means this user can only connect from the local machine. 
Change this if the user needs to connect from other hosts. (NOT ADVISED) 

Step 4: Verify the Database and User
To ensure the database and user are set up correctly, log in as the new user:
```
mysql -u admin -p
```
Once logged in, try accessing the BitcoinABE database:
```
USE BitcoinABE;
```
If there are no errors, the database and user are set up correctly.

### Step 4: Set Up Bitcoin ABE

1. **Clone Bitcoin ABE**: Bitcoin ABE is an open-source block explorer that reads the Bitcoin block file, transforms, and loads the data into a database. Clone the repository from GitHub:

   ```bash
   git clone https://github.com/bitcoin-abe/bitcoin-abe

Move into the Bitcoin ABE directory and run

python setup.py install

This will install abe to your system. After you set up the config file and database (see below and README-.txt) 

https://github.com/bitcoin-abe/bitcoin-abe/blob/master/README-MYSQL.txt

next open the abe.conf file and add your MySQL config

MySQL example; see also README-MYSQL.txt:
```
dbtype = MySQLdb
connect-args = {"user":"admin", "passwd":"admin", "db":"BitcoinABE"}
```

Specify port and/or host to serve HTTP instead of FastCGI: <-- Used to show the ABE front end.
```
port 2760
host localhost
```

New coins typically need a new "address_version", see doc/FAQ.html.
```
datadir += [{
    "dirname": "/path/to/.bitcoin",
    "loader": "rpc",    # See the comments for default-loader below.
    "chain": "Bitcoin",
    "rpcuser": "Administrator",
    "rpcpassword": "YourBitc0indRPCPa44wordSh0u3ldG0Here-Sec3ur3:Sup3RP@SSw0RdsOn1y"
}]
```
Filesystem location of static content, if served by Abe.
```
document-root = Abe/htdocs
```

Uncomment "auto-agpl" to add a "Source" link to each page pointing
to a "/download" URL that streams the directory containing abe.py
and all subdirectories as a compressed TAR archive.  This exposes
files outside of the htdocs directory to the client, so use it with
caution.
```
auto-agpl
```

Directory name and tarfile name prefix for auto-agpl source
download.
```
download-name = abe
```

One you have added the above settings you can then ensure your Bitcoind is running and run the following command.
```
python -m Abe.abe --config myconf.conf --commit-bytes 100000 --no-serve
```
You should start to see scroling output : 

    block_tx 1 1
    block_tx 2 2
    ...

This step may take several WEEKS OR MONTHS!!!! depending on chain size and hardware and config settings used..

Please ensure you read about the abe.conf setting before running the command to start the data import. 

You should now be able to access your ABE frontend and API via :
```
https://127.0.0.1:2760
```
<p align="center">
  <img src="https://github.com/DaCryptoRaccoon/CurvePrimePython/blob/main/2.jpg" alt="Abe Front End & API">
</p>

## Puzzle Selection Mechanism

### Overview
The script includes a user-interactive mechanism that allows users to select from a range of cryptographic puzzles related to Bitcoin. Each puzzle represents a unique cryptographic challenge involving the generation and evaluation of Bitcoin addresses within specified numerical ranges.

### How It Works
Upon execution, the script presents a list of available puzzles, each defined by its unique parameters including key ranges and current balance status. Users can select a puzzle by entering the corresponding puzzle number, and the script will focus its computational efforts on this selected range.

### Puzzle Details
Each puzzle is defined by several key parameters:
- **Puzzle Number**: A unique identifier for the puzzle.
- **Key Range**: The numeric range within which the script will generate private keys and derive Bitcoin addresses.
- **Address Balance**: Displays the current balance of the Bitcoin address associated with the puzzle, providing insights into whether the puzzle has been 'solved' or if the reward remains unclaimed.

### Interaction
Users interact with the puzzle selection mechanism via a simple command-line interface. Upon launching the script, the system displays the list of puzzles along with their details. Users are prompted to input the number of the puzzle they wish to explore. Here's what happens next:

1. **Puzzle Selection**: The user inputs the number corresponding to their selected puzzle.
2. **Range Setting**: The script sets the internal parameters to focus on the selected puzzle's key range.
3. **Address Generation and Checking**: The script generates Bitcoin addresses within the specified range and checks their balances against a blockchain explorer to determine if any contain a balance, which would indicate a 'solved' puzzle.

### Example of Available Puzzles
When the user runs the script, they might see a display similar to this:
```
Available Puzzles:
Puzzle 1: Key Range 0x1B03... to 0x1B0A..., Balance 0.00 BTC, Status Unsolved
Puzzle 2: Key Range 0x1B0B... to 0x1B10..., Balance 0.50 BTC, Status Solved
Puzzle 3: Key Range 0x1B11... to 0x1B16..., Balance 0.00 BTC, Status Unsolved
```
## Overview

### Prime Number Generation
- **Tool Used**: sympy library's `primerange` function.
- **Optimization**: Results are cached to prevent recalculating primes for previously queried ranges.

### Bitcoin Address Generation
- **Process**:
  - Convert each generated prime number (treated as a private key, PVK) to hexadecimal format.
  - Generate the corresponding public key.
  - Compute the Bitcoin address from the public key.

### Merit and Difficulty Calculation
- **Merit Calculation**: Offers a normalized value indicating the significance of the prime gap relative to the logarithm of the prime.
- **Difficulty Calculation**: Adds a random component to introduce variability.

### Concurrency and Network Interaction
- **Concurrency Handling**: Utilizes Python's `concurrent.futures` module for parallel task execution.
- **Network Interaction**: Engages with a local Abe blockchain explorer API for balance checks.

### Logging and Output
- **Details Logged**: Includes prime values, generated Bitcoin addresses, balance checks, and cryptographic metrics like entropy and Hamming distances.

## Detailed Cryptographic and System Components

### Prime Generation
- **Method**: Use of `sympy.primerange` for generating primes within a user-specified range.
- **Caching Strategy**: Employ a dictionary to speed up retrieval of primes for known ranges.

### Prime Gaps
- **Evaluation**: Calculate gaps between consecutive primes and assess their cryptographic relevance through merit and difficulty metrics.

### Cryptographic Calculations
#### Merit of a Prime Gap
<p align="center">
  <img src="https://github.com/DaCryptoRaccoon/CurvePrimePython/blob/main/3.jpg" alt="Merit of a Prime Gap">
</p>

- **Importance**: Provides insight into the size of the gap relative to the logarithmic scale of the prime.

#### Difficulty Calculation
- **Purpose**: Introduces a random factor to simulate varying 'difficulty' levels in cryptographic operations.

### Bitcoin Address Generation
#### From Private Key to Address
- **Steps**:
  1. Hexadecimal conversion of the private key.
  2. Public key generation using elliptic curve cryptography (ECC) via the bitcoin library.
  3. Bitcoin address derivation from the public key, adhering to Bitcoin's address generation protocols.

### Network Interactions
#### Balance Checking
- **Functionality**: Custom function interacts with a local blockchain explorer to check the balance of each generated Bitcoin address.
- **Error Handling**: Implements timeouts and retries using exponential backoff strategies.

### Concurrency
#### Thread Pool Executor
- **Utility**: Manages concurrent tasks efficiently, significantly enhancing script performance by parallelizing operations, especially those that are I/O bound.

### Output and Monitoring
#### Logging
- **Utility**: Extensive logging provides real-time feedback on script progress and is instrumental for performance monitoring and debugging.

#### Dynamic Adjustments
- **Adaptability**: The script dynamically adjusts the range of primes it searches based on specific conditions, mimicking adaptive algorithms used in cryptographic applications.

## Example of Script Output for a Specific Iteration

### Iteration 298432 Detailed Breakdown
```plaintext
Iteration: 298432
PVK: 58512954562131726889
Hex PVK: 0000000000000000000000000000000000000000000000032c07c628ca6f1229
SHA-256 PVK: cb26b1900bfc6557622152dfab76fc204848cae23b7ab4b5105e3bcc05007290
Address: 1CcYuLShSdVWhaEL15R7jZ7Rmbc5ydr35h
Balance: 0
Gap Start: 58512954562131726883
Gap Size: 6
Merit: 0.13182241455357108
Difficulty: 0.16933420118515963
Range Searched: 36893488147419103232 - 73786976294838206463
Range Searched Percentage: 58.60%
Best Merit Found: 12.25948455348213
Best Difficulty Found: 12.297095455593032
Kangaroo Hops: 59390
Best Prime Found: 58512954562131726889
Next Range: 400000
Public Key: 04efdfd8595afc13158e33e7e643a67df47f667917da4161258b72a1333510d53d84c2a651e3ea5d345468c8bbeaf87768f53cc8f2815f77605421dd8b2a07e99f
SHA-256 Public Key: e7a55a6f171f258a132205502125948a98f88b196df461525d2708bd1dd7fa9c
Hamming Distance to Previous PVK: 2
Entropy of PVK: 1.58
Entropy of Public Key: 3.92
API Balance Request Status: OK
```
## Detailed Breakdown of Iteration 298432

Let's delve deeper into the cryptographic and systemic processes of this Bitcoin-related Python script, illuminating how it functions through an illustrative iteration. To provide clarity, I will use the data point you mentioned for the specific iteration of 298432.

Cryptographic Elements and Operations
1. Private Key (PVK) Generation:

PVK Value: 58512954562131726889 is randomly chosen or derived during execution, representing a raw numerical private key.
Hexadecimal Conversion: The private key is converted to a hexadecimal representation, 0000000000000000000000000000000000000000000000032c07c628ca6f1229, to align with cryptographic standards for key encoding.

2. SHA-256 Hash of PVK:

Calculation: The hexadecimal private key undergoes a SHA-256 hash, resulting in cb26b1900bfc6557622152dfab76fc204848cae23b7ab4b5105e3bcc05007290. This hash function is vital in blockchain technologies for its collision resistance and fixed output size, enhancing security by obfuscating the original key.

3. Bitcoin Address Generation:

Public Key Derivation: From the hexadecimal private key, a public key 04efdfd...a07e99f is generated using elliptic curve cryptography (ECC). This process is deterministic and crucial for enabling Bitcoin transactions.
Address Derivation: The public key is then used to derive the Bitcoin address 1CcYuLShSdVWhaEL15R7jZ7Rmbc5ydr35h. This address acts as the public identifier for receiving Bitcoin transactions.

4. Cryptographic Security Measures:

Hamming Distance: Calculated between the current and previous PVK to measure the difference at the bit level. A Hamming distance of 2 suggests minimal change, enhancing the unpredictability of key generation.
Entropy Measurement: Indicates the randomness and unpredictability within the system, with the PVK having an entropy of 1.58 and the public key 3.92. Higher entropy values suggest greater security against predictive attacks.
Prime Number Exploration and Cryptographic Challenges

1. Prime Gaps:

Gap Size and Start: Identifying gaps between consecutive primes (size 6 from start 58512954562131726883) is not only mathematically intriguing but also relevant in studying the distribution of prime numbers, which can have cryptographic applications.

2. Merit and Difficulty:

Merit: 0.13182241455357108 calculated as the gap size divided by the natural logarithm of the starting prime, offering a way to evaluate the significance of the prime gap.
Difficulty: 0.16933420118515963 includes a random factor to simulate challenge conditions similar to those in cryptographic proofs or mining challenges.
System Performance and Optimization

1. Range and Search Efficiency:

Searched Range: 36893488147419103232 - 73786976294838206463 with 58.60% of the range explored. This indicates the breadth of the computational search in seeking viable cryptographic keys.
Dynamic Range Adjustments: The script adapts its search range (next set to 400000), showing flexibility in handling computational workloads.

2. Concurrency and Network Interactions:

API Balance Check: Confirms the balance of the derived Bitcoin address, showing an interaction with a local blockchain explorer API. The status "OK" ensures that the network connection and API response were successful.

3. Record-Keeping and Monitoring:

Best Values Logging: Records the best-found merit and difficulty (12.25948455348213 and 12.297095455593032 respectively) to gauge the progress and effectiveness of the search strategy over time.

Mathematical Foundations and Technical Details
In the exploration of cryptographic puzzles related to Bitcoin, my script integrates several complex mathematical concepts, focusing particularly on prime number theory, cryptographic functions, and Bitcoin address generation. Here is an in-depth look at the core mathematical and cryptographic operations employed:

Prime Number Generation and Caching
Primes are fundamental to numerous cryptographic protocols, including those used in blockchain technologies. The script uses the sympy.primerange function to efficiently generate prime numbers within a specified range. Caching these primes is crucial to optimize performance, especially when repeatedly querying similar ranges. The caching mechanism works as follows:

Prime Cache Initialization: A dictionary is set up to store prime numbers indexed by their range.

Prime Generation: If a range is not in the cache, the script calls primerange(start, end) to fetch primes and stores them in the cache.

```
prime_cache = {}

def generate_primes(start, end):
    if (start, end) not in prime_cache:
        prime_cache[(start, end)] = list(primerange(start, end))
    return prime_cache[(start, end)]
Cryptographic Calculations
```
Merit of a Prime Gap
The merit of a prime gap offers insight into the significance of the gap relative to the prime itself, calculated as:

<p align="center">
  <img src="https://github.com/DaCryptoRaccoon/CurvePrimePython/blob/main/5.jpg" alt="KeyTools">
</p>
This formula adjusts the raw gap size by the natural logarithm of the prime, providing a normalized measure of the gap's rarity or significance.

Difficulty Calculation

To introduce variability and challenge in evaluating prime gaps, a difficulty metric is calculated by incorporating a random factor:

<p align="center">
  <img src="https://github.com/DaCryptoRaccoon/CurvePrimePython/blob/main/4.jpg" alt="KeyTools">
</p>

Here, RandomFactor is a random number between 0 and 1, adding an element of unpredictability to the difficulty, simulating conditions akin to cryptographic proofs or mining challenges.

Bitcoin Address Generation

Generating a Bitcoin address from a private key involves several steps rooted in cryptographic algorithms:

Private Key Generation: Each prime number from the generated list is considered as a potential private key (PVK).
Hexadecimal Conversion: The private key is converted to a 64-character hexadecimal format.
Public Key Derivation: Using elliptic curve cryptography (ECC), a public key is derived from the private key.
Bitcoin Address Computation: The public key is then processed through Bitcoin's specific hashing algorithms (SHA-256 followed by RIPEMD-160) to produce a Bitcoin address.
The entire process adheres to Bitcoin's cryptographic protocols, ensuring that the addresses are valid for transactions within the Bitcoin network.

Concurrency and Efficiency

To maximize efficiency, especially when dealing with I/O operations such as network requests to check Bitcoin address balances, the script employs Python’s concurrent.futures module. This module allows parallel execution of code, significantly speeding up the address generation and balance checking processes by utilizing multiple threads.

```
with ThreadPoolExecutor() as executor:
    future = executor.submit(check_balance, bitcoin_address)
    balance, api_status = future.result()
```

Practical Applications and Implications

The use of these mathematical and cryptographic principles allows for a robust exploration of both the theoretical and practical aspects of prime numbers within the context of blockchain and Bitcoin. By understanding the rarity and distribution of prime gaps, one can gain deeper insights into the mathematical underpinnings of cryptographic security and its implementation in modern blockchain technologies.

This detailed examination not only underscores the script's capabilities in handling complex cryptographic tasks but also highlights its utility in educational and research-focused applications, particularly in fields related to cryptography and blockchain technology.

This amalgamates complex mathematical theories with practical implementations of cryptography, offering a robust platform for exploring prime numbers, generating Bitcoin addresses, and assessing cryptographic metrics. By continuously monitoring, adjusting, and logging its operations, it not only serves as a tool for generating cryptographic assets but also provides insights into the deeper mathematical structures that underpin modern cryptography and blockchain technology.

Happy Hunting! 

This project is licensed under the MIT License.
<p align="center">
  Made with ❤️ DaCryptoRaccoon
</p>
