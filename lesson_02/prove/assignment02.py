"""
Course    : CSE 351
Assignment: 02
Student   : <Lidya-Langana>

Instructions:
    - review instructions in the course
"""

# Don't import any other packages for this assignment
import os
import random
import threading
from money import *
from cse351 import *

# ---------------------------------------------------------------------------
def main(): 

    print('\nATM Processing Program:')
    print('=======================\n')

    create_data_files_if_needed()

    # Load ATM data files
    data_files = get_filenames('data_files')
    # print(data_files)
    
    log = Log(show_terminal=True)
    log.start_timer()

    bank = Bank()
    # Start an ATM_Reader thread for each data file
    threads = []
    for filename in data_files:
        reader = ATM_Reader(filename, bank)
        reader.start()
        threads.append(reader)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # TODO - Add a ATM_Reader for each data file

    test_balances(bank)

    log.stop_timer('Total time')
    


# ===========================================================================
class ATM_Reader(threading.Thread):
    def __init__(self, filename, bank):
        super().__init__()
        self.filename =filename
        self.bank = bank
        
    def run(self):
        with open(self.filename, "r") as f:
            for line in f:
                line =line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split(",")
                account_number = int(parts[0])
                trans_type = parts[1]
                amount = Money(parts[2])

                if trans_type == "d":
                    self.bank.deposit(account_number,amount)
                elif trans_type =="w":
                    self.bank.withdraw(account_number,amount)
    ...


# ===========================================================================
class Account():
    def __init__(self, number):
        self.number =number
        self.balance = Money("0.00")

    def deposit(self, money):
        self.balance.add(money)

    def withdraw(self, money):
        self.balance.sub(money)

    def get_balance(self):
        return self.balance
        
    ...


# ===========================================================================
class Bank():
    def __init__(self):
        self.accounts = {}          # dict: {account_number: Account}
        self.lock = threading.Lock()

    def _get_account(self, number):
        if number not in self.accounts:
            self.accounts[number] = Account(number)
        return self.accounts[number] 
    
    def deposit(self, number, money):
        with self.lock:
            account = self._get_account(number)
            account.deposit(money) 

    def withdraw(self, number, money):
        with self.lock:
            account = self._get_account(number)
            account.withdraw(money)  
    def get_balance(self, number):
        with self.lock:
            return self._get_account(number).get_balance()        
    ...


# ---------------------------------------------------------------------------

def get_filenames(folder):
    """ Don't Change """
    filenames = []
    for filename in os.listdir(folder):
        if filename.endswith(".dat"):
            filenames.append(os.path.join(folder, filename))
    return filenames

# ---------------------------------------------------------------------------
def create_data_files_if_needed():
    """ Don't Change """
    ATMS = 10
    ACCOUNTS = 20
    TRANSACTIONS = 250000

    sub_dir = 'data_files'
    if os.path.exists(sub_dir):
        return

    print('Creating Data Files: (Only runs once)')
    os.makedirs(sub_dir)

    random.seed(102030)
    mean = 100.00
    std_dev = 50.00

    for atm in range(1, ATMS + 1):
        filename = f'{sub_dir}/atm-{atm:02d}.dat'
        print(f'- {filename}')
        with open(filename, 'w') as f:
            f.write(f'# Atm transactions from machine {atm:02d}\n')
            f.write('# format: account number, type, amount\n')

            # create random transactions
            for i in range(TRANSACTIONS):
                account = random.randint(1, ACCOUNTS)
                trans_type = 'd' if random.randint(0, 1) == 0 else 'w'
                amount = f'{(random.gauss(mean, std_dev)):0.2f}'
                f.write(f'{account},{trans_type},{amount}\n')

    print()

# ---------------------------------------------------------------------------
def test_balances(bank):
    """ Don't Change """

    # Verify balances for each account
    correct_results = (
        (1, '59362.93'),
        (2, '11988.60'),
        (3, '35982.34'),
        (4, '-22474.29'),
        (5, '11998.99'),
        (6, '-42110.72'),
        (7, '-3038.78'),
        (8, '18118.83'),
        (9, '35529.50'),
        (10, '2722.01'),
        (11, '11194.88'),
        (12, '-37512.97'),
        (13, '-21252.47'),
        (14, '41287.06'),
        (15, '7766.52'),
        (16, '-26820.11'),
        (17, '15792.78'),
        (18, '-12626.83'),
        (19, '-59303.54'),
        (20, '-47460.38'),
    )

    wrong = False
    for account_number, balance in correct_results:
        bal = bank.get_balance(account_number)
        print(f'{account_number:02d}: balance = {bal}')
        if Money(balance) != bal:
            wrong = True
            print(f'Wrong Balance: account = {account_number}, expected = {balance}, actual = {bal}')

    if not wrong:
        print('\nAll account balances are correct')



if __name__ == "__main__":
    main()

