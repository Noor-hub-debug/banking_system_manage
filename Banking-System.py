from abc import ABC, abstractmethod

class Account(ABC):
    accounts = []
    loan_limit = 2

    def __init__(self, name, email, address, account_type):      #start
        self.name = name                                         #name
        self.email = email                                       #email
        self.address = address
        self.account_no = len(Account.accounts) + 1
        self.balance = 0                                         # start with 0
        self.account_type = account_type                         # ac type 0
        self.loan_count = 0                                      # loan 0
        self.transactions = []                                   # []
        Account.accounts.append(self)

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            self.transactions.append(f"Deposited ${amount}")
            print(f"\nDeposited ${amount}. New balance: ${self.balance}")
        else:
            print("\nInvalid deposit amount")

    def withdraw(self, amount):
        if amount >= 0 and amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrew ${amount}")
            print(f"\nWithdrew ${amount}. New balance: ${self.balance}")
        else:
            print("\nInvalid withdrawal amount")

    def check_balance(self):
        print(f"\nAvailable balance: ${self.balance}")

    def check_transactions(self):
        print("\nTransaction History:")
        for transaction in self.transactions:
            print(transaction)

    def take_loan(self, amount):
        if self.loan_count < Account.loan_limit and amount > 0:
            self.balance += amount
            self.transactions.append(f"Took a loan of ${amount}")
            self.loan_count += 1
            print(f"\nTook a loan of ${amount}. New balance: ${self.balance}")
        else:
            print("\nLoan limit exceeded or invalid loan request")

    def transfer(self, user, amount):
        if user in Account.accounts and amount > 0 and self.balance >= amount:
            user.deposit(amount)
            self.withdraw(amount)
            print(f"\nTransferred ${amount} to {user.name}'s account.")
        else:
            print("\nAccount does not exist or invalid transfer amount")

    @abstractmethod
    def show_info(self):
        pass

class SavingsAccount(Account):
    def __init__(self, name, email, address):        # saving ac
        super().__init__(name, email, address, "Savings")
        self.interest_rate = 0.03  

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(interest)
        print("\nInterest is applied")

    def show_info(self):
        print(f"Account Type: {self.account_type}")
        print(f"Name: {self.name}")
        print(f"Account Number: {self.account_no}")
        print(f"Current Balance: ${self.balance}")

class Admin:
    def create_account(self, name, email, address, account_type):                           # admin panel 
        if account_type == "Savings":
            account = SavingsAccount(name, email, address)
        else:
            account = Account(name, email, address, "Current")
        print(f"\nAccount created for {account.name}. Account Number: {account.account_no}")

    def delete_account(self, account):
        if account in Account.accounts:
            Account.accounts.remove(account)
            print(f"\nAccount for {account.name} has been deleted.")
        else:
            print("\nAccount does not exist.")

    def see_all_accounts(self):
        print("\nAll User Accounts:")
        for account in Account.accounts:
            account.show_info()

    def check_total_balance(self):
        total_balance = sum(account.balance for account in Account.accounts)
        print(f"\nTotal Available Balance in the bank: ${total_balance}")

    def check_total_loan_amount(self):
        total_loan = sum(account.balance for account in Account.accounts if account.loan_count > 0)
        print(f"\nTotal Loan Amount in the bank: ${total_loan}")

    def toggle_loan_feature(self, status):
        if status:
            Account.loan_limit = 2
            print("\nLoan is enabled.")
        else:
            Account.loan_limit = 0
            print("\nLoan  is disabled.")

# Main program

current_user = None
admin = Admin()

while True:
    if current_user is None:
        print("\nNo user logged in!")
        choice = input("\nRegister/Login (R/L) / Exit (E): ")
        if choice == "R":
            name = input("Name: ")
            email = input("Email: ")
            address = input("Address: ")
            account_type = input("Account Type (Savings/Current): ")      #  ac type
            admin.create_account(name, email, address, account_type)      #  admin
        elif choice == "L":
            account_no = int(input("Account Number: "))
            for account in Account.accounts:
                if account.account_no == account_no:
                    current_user = account
                    break
            else:
                print("\nAccount does not exist.")
        elif choice == "E":
            break
    else:
        print(f"\nWelcome {current_user.name}!\n")
        print("1. Withdraw")
        print("2. Deposit")
        print("3. Check Available Balance")
        print("4. Check Transaction History")
        print("5. Take a Loan")
        print("6. Transfer Money")
        print("7. Logout\n")

        option = input("Choose Option: ")

        if option == "1":
            amount = float(input("Enter withdrawal amount: $"))
            current_user.withdraw(amount)
        elif option == "2":
            amount = float(input("Enter deposit amount: $"))
            current_user.deposit(amount)
        elif option == "3":
            current_user.check_balance()
        elif option == "4":
            current_user.check_transactions()
        elif option == "5":
            amount = float(input("Enter loan amount: $"))
            current_user.take_loan(amount)
        elif option == "6":
            user_account_no = int(input("Enter user's account number: "))
            user = None
            for account in Account.accounts:
                if account.account_no == user_account_no:
                    user = account
                    break
            if user:
                amount = float(input("Enter transfer amount: $"))
                current_user.transfer(user, amount)
            else:
                print("\n user's account does not exist.")
        elif option == "7":
            current_user = None
        else:
            print("Invalid Option")

# To run the program, you can copy and paste the code into a Python environment.
