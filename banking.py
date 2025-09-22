import csv
import os


print("🏦 💸 Welcome To Raghad Bank  💸🏦")
FIELDNAMES = [
    "id",
    "first_name",
    "last_name",
    "password",
    "checking",
    "savings",
    "active",
    "overdraft_count",
]

class BalanceError(Exception):
    pass

class AuthError(Exception):
    pass

class BankAccount:
    OVERDRAFT_FEE = 35
    MAX_WITHDRAW = 100
    MIN_ALLOWED_BALANCE = -100 
    OVERDRAFT_DISABLE_AFTER = 2 

    def __init__(self, row: dict, kind: str):
        self.row = row
        self.kind = kind

    @property
    def balance(self):
        return int(self.row[self.kind])

    @balance.setter
    def balance(self, val: int):
        self.row[self.kind] = int(val)

    def _is_active(self):
        return bool(self.row["active"])

    def _total_balance(self):
        return int(self.row["checking"]) + int(self.row["savings"])

    def deposit(self, amount: int):
        if amount <= 0:
            raise ValueError("Deposit amount must be > 0.")
        self.balance = self.balance + amount
        if self._total_balance() >= 0:
            self.row["active"] = True
        return self.balance

    def withdraw(self, amount: int) :

        if not self._is_active():
            raise BalanceError("Account is deactivated. Please deposit to reactivate.")

        if amount <= 0 or amount > self.MAX_WITHDRAW:
            raise BalanceError("Cannot withdraw more than $100 in one transaction (and must be > 0).")

        projected = self.balance - amount
        fee = self.OVERDRAFT_FEE if projected < 0 else 0

        if projected - fee < self.MIN_ALLOWED_BALANCE:
            raise BalanceError("Resulting balance cannot go below -$100.")

        self.balance = projected - fee

        if fee > 0:
            self.row["overdraft_count"] += 1
            if self.row["overdraft_count"] >= self.OVERDRAFT_DISABLE_AFTER:
                self.row["active"] = False

        return self.balance
class CheckingAccount(BankAccount):
    def __init__(self, row: dict):
        super().__init__(row, "checking")

class SavingsAccount(BankAccount):
    def __init__(self, row: dict):
        super().__init__(row, "savings")

class InterestAccount(BankAccount):  
    def __init__(self, row: dict, kind="savings", interest=0.03):
        super().__init__(row, kind)
        self.interest = float(interest)
    def deposit(self, amount: int):
        super().deposit(amount)
        self.balance = int(self.balance * (1 + self.interest))
        return self.balance

class ChargingAccount(BankAccount): 
    def __init__(self, row: dict, kind="checking", fee=3):
        super().__init__(row, kind)
        self.extra_fee = int(fee)
    def withdraw(self, amount: int):
        return super().withdraw(amount + self.extra_fee)

