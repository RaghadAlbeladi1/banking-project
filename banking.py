import csv
class BankAccount:
    print("🏦 💸 Welcome To Raghad Bank  💸🏦")
    def __init__(self):
        self.csv_file = "bank.csv"
        self.customers = self.load_customers()

    def load_customers(self):
        customers = []
        with open(self.csv_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["checking"] = int(row["checking"])
                row["savings"] = int(row["savings"])
                row["active"] = True if row["active"].lower() == "true" else False
                row["overdraft_count"] = int(row["overdraft_count"])
                customers.append(row)
        return customers

    def save_customers(self):
        with open(self.csv_file, mode="w", newline="") as file:
            fieldnames = ["id","first_name","last_name","password","checking","savings","active","overdraft_count"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.customers)


bank = BankAccount()
print("Loaded customers:")
for customer in bank.customers:
    print(customer)