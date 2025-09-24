import csv
import os
FIELDNAMES = ["id", "first_name", "last_name", "password", "checking", "savings", "active", "overdraft_count", "has_checking", "has_savings"]

class Database:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file
        self.ensure_csv_exists()

    def ensure_csv_exists(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writeheader()

    def view_csv(self):
        try:
            with open(self.csv_file, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    print(row)
        except csv.Error as e:
            print(e)

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

    def save_customers(self, customers):
        with open(self.csv_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            for cust in customers:
                row = cust.copy()
                row["checking"] = "" if row["checking"] is None else row["checking"]
                row["savings"] = "" if row["savings"] is None else row["savings"]
                row["active"] = "true" if row["active"] else "false"
                row["has_checking"] = "true" if row["has_checking"] else "false"
                row["has_savings"] = "true" if row["has_savings"] else "false"
                writer.writerow(row)

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
            print("This account is already opened.")
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
        # Block withdraw if account/customer is inactive  (Cynthia)
        if not self.customer_record.get("active", True):
            print("Account is not active.")
            return False
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

        if tentative_balance < -65:
            print("Withdrawal denied: resulting balance would be less than -$100.")
            return False

        new_balance = tentative_balance

        if new_balance < 0:
            new_balance -= 35
            current_overdrafts = int(self.customer_record.get("overdraft_count", 0)) + 1
            self.customer_record["overdraft_count"] = current_overdrafts
            print(f"Overdraft fee $35 applied. Overdraft count is now: {current_overdrafts}")

            if current_overdrafts >= 2:
                self.customer_record["active"] = False
                print(" deactivated due to multiple overdrafts.")
        self.set_balance(new_balance)
        print(f"Withdrew ${amount}. Balance: ${current_balance} -> ${new_balance}")
        return True

    def transfer(self, amount: int, destination_account: "BankAccount"):
        # Block transfer if either source or destination is inactive    (Cynthia)
        if not self.customer_record.get("active", True):
            print("Source account is not active.")
            return False
        if not destination_account.customer_record.get("active", True):
            print("Destination account is not active.")
            return False
        print(f"Starting transfer of ${amount} from {self.account_type} to {destination_account.account_type}...")
        was_withdrawn = self.withdraw(amount)
        if not was_withdrawn:
            print("Transfer aborted (withdrawal failed).")
            return False

        was_deposited = destination_account.deposit(amount)
        if not was_deposited:
            print("Transfer failed")
            return False

        print("Transfer completed successfully.")
        return True
    
class Transaction:
    def __init__(self, csv_file="bank.csv"):
        self.db = Database(csv_file)
        self.csv_file = csv_file
        self.customers = self.db.load_customers()
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
            return BankAccount(customer, "checking")
        if choice == "2" and customer.get("has_savings", False):
            return BankAccount(customer, "savings")

        print("Invalid choice.")
        return None


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
        self.db.save_customers(self.customers)
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
            if self.current_customer and not self.current_customer.get("active", True):
                self.reactivation_assistance()
                if self.current_customer and not self.current_customer.get("active", True):
                    print("Your account is not active. Logging out.")
                    self.current_customer = None
                    break
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
                continue
            

    def reactivation_assistance(self):
        cust = self.current_customer
        if not cust:
            return
        first = cust.get("first_name", "")
        last = cust.get("last_name", "")
        overdrafts = cust.get("overdraft_count", 0)

        account_needs = []
        if cust.get("has_checking", False):
            bal = cust.get("checking", 0) or 0
            if bal < 0:
                account_needs.append(("checking", -bal))
        if cust.get("has_savings", False):
            bal = cust.get("savings", 0) or 0
            if bal < 0:
                account_needs.append(("savings", -bal))

        print(f"Hi {first} {last} - your account has overdrafted {overdrafts} times - you will need to deposit the amounts below to reactivate..")
        if account_needs:
            for acc, need in account_needs:
                print(f"please insert ${need} of money into your {acc}")
        else:
            print("Your balances are non-negative. A small deposit will reactivate your account.")

        for acc, need in account_needs:
            while True:
                resp = input(f"Deposit now into {acc}? (Y/N) ").strip().lower()
                if resp in ("y", "yes"):
                    try:
                        default_str = str(need)
                        amt_str = input(f"Amount to deposit into {acc} [default {default_str}]: ").strip()
                        amount = int(amt_str) if amt_str else int(need)
                    except:
                        print("Invalid amount.")
                        continue
                    #Todo: check if the amount is enough to the account be on 0 or more (Cynthia)
                    if acc == "checking":
                        old_balance = cust["checking"] if cust["checking"] is not None else 0
                    else:
                        old_balance = cust["savings"] if cust["savings"] is not None else 0

                    if old_balance + amount < 0:
                        print(f"Amount not sufficient. You need at least ${need} to reactivate this account.")
                        continue
                    target = BankAccount(cust, acc)
                    if target.deposit(amount):
                        self.db.save_customers(self.customers)
                        if cust.get("active", True):
                            print("💜 Thank you for using Raghad Bank!💜-> your account has been reactivated")
                            return
                    break
                elif resp in ("n", "no"):
                    break
                else:
                    print("Please answer Y or N.")

        if cust.get("active", True):
            print("💜 Thank you for using Raghad Bank!💜-> your account has been reactivated")

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
            self.db.save_customers(self.customers)


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
            self.db.save_customers(self.customers)


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
                to_acc = BankAccount(self.current_customer, "savings")
            else:
                if not self.current_customer.get("has_checking", False):
                    print("No Checking account open.")
                    return
                to_acc = BankAccount(self.current_customer, "checking")

            try:
                amount = int(input("Amount: $"))
            except:
                print("Invalid amount.")
                return

            if from_acc.transfer(amount, to_acc):
                self.db.save_customers(self.customers)

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
                to_acc = BankAccount(other, "checking")
            elif dest_choice == "2":
                to_acc = BankAccount(other, "savings")
            else:
                print("Invalid choice.")
                return

            try:
                amount = int(input("Amount: $"))
            except:
                print("Invalid amount.")
                return

            if from_acc.transfer(amount, to_acc):
                self.db.save_customers(self.customers)

        else:
            print("Invalid choice.")
 

if __name__ == "__main__":
    Transaction()