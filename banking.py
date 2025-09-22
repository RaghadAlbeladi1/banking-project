import csv
import os
FIELDNAMES = ["id", "first_name", "last_name", "password", "checking", "savings", "active", "overdraft_count", "has_checking", "has_savings"]

class Customer:
    def __init__(self, id, first_name, last_name, password,checking, savings, active, overdraft_count,has_checking, has_savings):
        self.id = int(id)
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

        self.checking = int(checking) if str(checking).strip() not in ("", "None") else None
        self.savings  = int(savings)  if str(savings).strip()  not in ("", "None") else None

        self.active = str(active).strip().lower() == "true"
        self.overdraft_count = int(overdraft_count)
        self.has_checking = str(has_checking).strip().lower() == "true"
        self.has_savings  = str(has_savings).strip().lower() == "true"

    def display(self):
        ck = 0 if self.checking is None else self.checking
        sv = 0 if self.savings  is None else self.savings
        print(f"\n--- Account Information for {self.first_name} {self.last_name} ---")
        print(f"Checking Balance: ${ck:.2f} (open={self.has_checking})")
        print(f"Savings Balance : ${sv:.2f} (open={self.has_savings})")
        print(f"Active: {self.active}")
        print(f"Overdraft Count: {self.overdraft_count}")


from typing import Dict
class BankAccount:
    def __init__(self, customer_record: Dict, account_type: str):
        self.customer_record = customer_record
        self.account_type = account_type  

    def flag_key_for_open_state(self):
        if self.account_type == "checking":
            return "has_checking"
        else:
            return "has_savings"

    def balance_key(self):
        return self.account_type

    def is_account_open(self):
        return bool(self.customer_record.get(self.flag_key_for_open_state(), False))

    def open_account(self):
        if self.is_account_open():
            print("This account type is already opened.")
            return False

        self.customer_record[self.balance_key()] = 0
        self.customer_record[self.flag_key_for_open_state()] = True
        print(f"{self.account_type.capitalize()} account opened with starting balance = $0.")
        return True

    def get_balance(self):
        current_value = self.customer_record.get(self.balance_key(), None)
        return 0 if current_value is None else int(current_value)

    def set_balance(self, new_balance: int):
        self.customer_record[self.balance_key()] = int(new_balance)

    def deposit(self, amount: int):
        if not self.is_account_open():
            print("Open this account first before depositing.")
            return False

        if amount <= 0:
            print("Deposit amount must be positive.")
            return False

        old_balance = self.get_balance()
        new_balance = old_balance + int(amount)
        self.set_balance(new_balance)

        if new_balance >= 0 and self.customer_record.get("active") is False:
            self.customer_record["active"] = True
            print("Account reactivated (balance is now non-negative).")

        print(f"Deposited ${amount}. Balance: ${old_balance} -> ${new_balance}")
        return True

    def withdraw(self, amount: int):
        if not self.is_account_open():
            print("Open this account first before withdrawing.")
            return False

        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False

        if amount > 100:
            print("Cannot withdraw more than $100 in a single transaction.")
            return False

        current_balance = self.get_balance()
        tentative_balance = current_balance - int(amount)

        if tentative_balance < -100:
            print("Withdrawal denied: resulting balance would be less than -$100.")
            return False

        new_balance = tentative_balance

        crossed_from_non_negative_to_negative = (current_balance >= 0) and (new_balance < 0)
        if crossed_from_non_negative_to_negative:
            new_balance -= 35
            current_overdrafts = int(self.customer_record.get("overdraft_count", 0)) + 1
            self.customer_record["overdraft_count"] = current_overdrafts
            print(f"Overdraft fee $35 applied. Overdraft count is now: {current_overdrafts}")

            if current_overdrafts >= 2:
                self.customer_record["active"] = False
                print("Account deactivated due to multiple overdrafts.")

        self.set_balance(new_balance)
        print(f"Withdrew ${amount}. Balance: ${current_balance} -> ${new_balance}")
        return True

    def transfer(self, amount: int, destination_account: "BankAccount"):
        print(f"Starting transfer of ${amount} from {self.account_type} to {destination_account.account_type}...")
        was_withdrawn = self.withdraw(amount)
        if not was_withdrawn:
            print("Transfer aborted (withdrawal failed).")
            return False

        was_deposited = destination_account.deposit(amount)
        if not was_deposited:
            print("Transfer failed on deposit stage.")
            return False

        print("Transfer completed successfully.")
        return True
    
class Transaction:
    def __init__(self, csv_file="bank.csv"):
        self.csv_file = csv_file
        self.customers = self.load_customers()
        self.current_customer = None
        self.show_main_menu()

    def choose_account(self, customer, action_label: str = ""):
        label = f" {action_label}" if action_label else ""
        print(f"\nChoose account{label}:")
        options = []
        if customer.get("has_checking", False):
            options.append(("1", "Checking"))
        if customer.get("has_savings", False):
            options.append(("2", "Savings"))

        if not options:
            print("You have no open accounts. Please open an account first.")
            return None

        for code, name in options:
            print(f"{code}) {name}")

        choice = input("> ").strip()
        if choice == "1" and customer.get("has_checking", False):
            return CheckingAccount(customer)
        if choice == "2" and customer.get("has_savings", False):
            return SavingsAccount(customer)

        print("Invalid choice.")
        return None

    def load_customers(self):
        customers = []
        if os.path.exists(self.csv_file):
            with open(self.csv_file, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if not row["id"]:
                        continue
                    row["id"] = int(row["id"])
                    row["checking"] = int(row["checking"]) if row["checking"] not in ("", "None") else None
                    row["savings"] = int(row["savings"]) if row["savings"] not in ("", "None") else None
                    row["active"] = row["active"].lower() == "true"
                    row["overdraft_count"] = int(row["overdraft_count"])
                    row["has_checking"] = row["has_checking"].lower() == "true"
                    row["has_savings"] = row["has_savings"].lower() == "true"
                    customers.append(row)
        return customers

    def save_customers(self):
        with open(self.csv_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            for cust in self.customers:
                row = cust.copy()
                row["checking"] = "" if row["checking"] is None else row["checking"]
                row["savings"] = "" if row["savings"] is None else row["savings"]
                row["active"] = "true" if row["active"] else "false"
                row["has_checking"] = "true" if row["has_checking"] else "false"
                row["has_savings"] = "true" if row["has_savings"] else "false"
                writer.writerow(row)

    def show_main_menu(self):
        while True:
            print("\n🏦💸 Welcome To Raghad Bank 💸🏦")
            print("1) Login")
            print("2) Create Account")
            print("3) Quit")
            choice = input("> ").strip()

            if choice == "1":
                self.login()
            elif choice == "2":
                self.create_account()
            elif choice == "3":
                print("💜Thank you for using Raghad Bank!💜")
                break
            else:
                print("Invalid choice")

    def create_account(self):
        print("\n Create New Account")
        first = input("First name: ").strip()
        last = input("Last name: ").strip()
        pw = input("Password: ").strip()

        new_id = (max([c["id"] for c in self.customers]) + 1) if self.customers else 10001

        print("Which account(s) to open?")
        print("1) Checking only")
        print("2) Savings only")
        print("3) Both")
        opt = input("> ").strip()
        has_checking = opt in {"1", "3"}
        has_savings = opt in {"2", "3"}

        new_customer = {
            "id": new_id,
            "first_name": first,
            "last_name": last,
            "password": pw,
            "checking": 0 if has_checking else None,
            "savings": 0 if has_savings else None,
            "active": True,
            "overdraft_count": 0,
            "has_checking": has_checking,
            "has_savings": has_savings
        }

        self.customers.append(new_customer)
        self.save_customers()
        print(f"Account created! Your ID: {new_id}")

    def login(self):
        print("\n Login")
        try:
            cid = int(input("Customer ID: "))
        except:
            print("Invalid ID")
            return
        pw = input("Password: ")

        cust = next((c for c in self.customers if c["id"] == cid and c["password"] == pw), None)
        if not cust:
            print("Wrong ID or password")
            return

        if not cust["active"]:
            print(" Account deactivated")
            return

        self.current_customer = cust
        print(f"Welcome {cust['first_name']} {cust['last_name']}!")
        self.customer_menu()

    def customer_menu(self):
        while True:
            print("\n Raghad Bank-- Menu ")
            print("1) Deposit")
            print("2) Withdraw")
            print("3) Transfer")
            print("4) Show Info")
            print("5) Logout")
            choice = input("> ")

            if choice == "1":
                self.deposit()
            elif choice == "2":
                self.withdraw()
            elif choice == "3":
                self.transfer()
            elif choice == "4":
                Customer(**self.current_customer).display()
            elif choice == "5":
                print("Logged out")
                self.current_customer = None
                break
            else:
                print("Invalid choice")

    def deposit(self):
        account = self.choose_account(self.current_customer)
        if account is None:
            return
        try:
            amount = int(input("Amount?: $"))
        except:
            print("valid Amount")
            return
        if account.deposit(amount):
            self.save_customers()


    def withdraw(self):
        account = self.choose_account(self.current_customer, "withdraw")
        if account is None:
            return
        try:
            amount = int(input(" amount?: $"))
        except:
            print(" Valid Amount .")
            return

        if account.withdraw(amount):
            self.save_customers()


    def transfer(self):
        print("\nTransfer type:")
        print("1) Between my accounts (Checking ⇄ Savings)")
        print("2) To another customer")
        t = input("> ").strip()

        if t == "1":
            print("\nFrom which account?")
            from_acc = self.choose_account(self.current_customer, "transfer from")
            if from_acc is None:
                return

            if from_acc.account_type == "checking":
                if not self.current_customer.get("has_savings", False):
                    print("No Savings account open.")
                    return
                to_acc = SavingsAccount(self.current_customer)
            else:
                if not self.current_customer.get("has_checking", False):
                    print("No Checking account open.")
                    return
                to_acc = CheckingAccount(self.current_customer)

            try:
                amount = int(input("Amount: $"))
            except:
                print("Invalid amount.")
                return

            if from_acc.transfer(amount, to_acc):
                self.save_customers()

        elif t == "2":
            try:
                other_id = int(input("Recipient ID: "))
            except:
                print("Invalid ID.")
                return

            other = next((c for c in self.customers if c["id"] == other_id), None)
            if not other:
                print("Customer not found.")
                return
            if not other.get("active", True):
                print("Recipient account is not active.")
                return

            print("\nFrom which account?")
            from_acc = self.choose_account(self.current_customer, "transfer from")
            if from_acc is None:
                return

            print("\nTo which account of recipient?")
            dest_options = []
            if other.get("has_checking", False):
                dest_options.append(("1", "Checking"))
            if other.get("has_savings", False):
                dest_options.append(("2", "Savings"))

            if not dest_options:
                print("Recipient has no open accounts.")
                return

            for code, name in dest_options:
                print(f"{code}) {name}")

            dest_choice = input("> ").strip()
            if dest_choice == "1":
                to_acc = CheckingAccount(other)
            elif dest_choice == "2":
                to_acc = SavingsAccount(other)
            else:
                print("Invalid choice.")
                return

            try:
                amount = int(input("Amount: $"))
            except:
                print("Invalid amount.")
                return

            if from_acc.transfer(amount, to_acc):
                self.save_customers()

        else:
            print("Invalid choice.")


class CheckingAccount(BankAccount):
    def __init__(self, customer_record: Dict):
        super().__init__(customer_record, "checking")
class SavingsAccount(BankAccount):
    def __init__(self, customer_record: Dict):
        super().__init__(customer_record, "savings")

if __name__ == "__main__":
    Transaction()
