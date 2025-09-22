import csv, os
print("🏦 💸 Welcome To Raghad Bank  💸🏦")
FIELDNAMES = [
    "id","first_name","last_name","password",
    "checking","savings","active","overdraft_count",
    "has_checking","has_savings"
]

class Customer:
    def __init__(self, id: int,first_name: str,last_name: str,password: str,checking: int, savings: int, active: bool,overdraft_count: int,has_checking: bool = True,has_savings: bool  = True):
        self.id = int(id)
        self.first_name = first_name
        self.last_name  = last_name
        self.password   = password
        self.checking   = int(checking)
        self.savings    = int(savings)
        self.active     = bool(active)
        self.overdraft_count = int(overdraft_count)
        self.has_checking = bool(has_checking)
        self.has_savings  = bool(has_savings)

class BankingApp:
    def __init__(self, csv_file="bank.csv"):
        self.csv_file = csv_file
        self._ensure_csv()
        self.customers = self._load_customers()
        self.current_index = None
        print(f"Loaded {len(self.customers)} customers.")

    def _ensure_csv(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w", newline="") as f:
                csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()

    def _load_customers(self):
        items = []
        with open(self.csv_file, "r", newline="") as f:
            for row in csv.DictReader(f):
                row["id"] = int(row["id"])
                row["checking"] = int(row["checking"])
                row["savings"] = int(row["savings"])
                row["active"] = str(row["active"]).lower() == "true"
                row["overdraft_count"] = int(row["overdraft_count"])
                row["has_checking"] = str(row.get("has_checking","true")).lower() == "true"
                row["has_savings"]  = str(row.get("has_savings","true")).lower()  == "true"
                items.append(row)
        return items

    def _save_customers(self):
        with open(self.csv_file, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDNAMES)
            w.writeheader()
            for r in self.customers:
                out = r.copy()
                out["active"]       = "true" if r["active"] else "false"
                out["has_checking"] = "true" if r.get("has_checking", True) else "false"
                out["has_savings"]  = "true" if r.get("has_savings",  True) else "false"
                w.writerow(out)

    def entry_menu(self):
        while True:
            print("\n🏦 Raghad Bank — Menu")
            print("1) Login")
            print("2) Create account")
            print("q) Quit")
            choice = input("> ").strip().lower()

            if choice in {"1","l","login"}:
                self.login()
            elif choice in {"2","c","create","signup"}:
                self.signup()
            elif choice in {"q","quit"}:
                print("💜 Thank you!")
                break
            else:
                print("Invalid choice")

    def signup(self):
        print("\n Create New Customer")
        first = input("First name: ").strip()
        last  = input("Last name : ").strip()
        while True:
            pw = input("Password ").strip()
            print("ur acount being created ")

            print("Open which account(s)?\n 1) Checking only\n 2) Savings only\n 3) Both")
            opt = input("Choose 1/2/3: ").strip()
            has_checking = opt in {"1","3"}
            has_savings  = opt in {"2","3"}

            new_id = max((r["id"] for r in self.customers), default=10000) + 1
            new_row = {
            "id": new_id,
            "first_name": first, "last_name": last, "password": pw,
            "checking": 0, "savings": 0,
            "active": True, "overdraft_count": 0,
            "has_checking": has_checking, "has_savings": has_savings
        }
            self.customers.append(new_row)
            self._save_customers()
            print(f"Account created! Your ID: {new_row['id']}")

    def login(self):
        print("\n Login")
        try:
            cid = int(input("Account ID: ").strip())
        except ValueError:
            print("Invalid ID.")
            return
        idx = next((i for i, r in enumerate(self.customers) if r["id"] == cid), None)
        if idx is None:
            print(" No such account.")
            return
        pw = input("Password: ").strip()
        if pw != self.customers[idx]["password"]:
            print(" Wrong password.")
            return
        self.current_index = idx
        u = self.customers[idx]
        print(f"Welcome {u['first_name']} {u['last_name']}! (ID {u['id']})")

if __name__ == "__main__":
    app = BankingApp()
    app.entry_menu()
