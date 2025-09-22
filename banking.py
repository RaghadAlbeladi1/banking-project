import csv, os
print("🏦 💸 Welcome To Raghad Bank  💸🏦")

FIELDNAMES = [
    "id","first_name","last_name","password",
    "checking","savings","active","overdraft_count",
    "has_checking","has_savings"           
]

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
        print("\n=== Main ===")
        choice = input("Do you want to (1)login, (2)create account, or (q)quit? ").s
