# Raghad Bank

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Data](https://img.shields.io/badge/Storage-CSV-lightgrey)
![Interface](https://img.shields.io/badge/Interface-CLI-green)
![Status](https://img.shields.io/badge/Project-Banking_App-purple)

Simple, menu-driven banking app using Python and CSV storage. Supports new account creation, login/logout, deposit, withdraw, and transfers with overdraft protection.

## Demo (GIF)
- App Walkthrough: add a short screen recording showing login → deposit → withdraw → internal transfer → external transfer.
- Animated Welcome: you can add an animated "Welcome to Raghad Bank" GIF.

Placeholders:

![Welcome](assets/welcome.gif)

![App Demo](assets/demo.gif)

## Quick Start

Prerequisites:
- Python 3.10+

Run the app:

```bash
python3 banking.py
```

Example session:

```bash
$ python3 banking.py
🏦💸 Welcome To Raghad Bank 💸🏦
1) Login
2) Create Account
3) Quit
> 2
 Create New Account
First name: Raghad
Last name: A.
Password: ****
Which account(s) to open?
1) Checking only
2) Savings only
3) Both
> 3
Account created! Your ID: 10001

🏦💸 Welcome To Raghad Bank 💸🏦
1) Login
2) Create Account
3) Quit
> 1
 Login
Customer ID: 10001
Password: ****
Welcome Raghad A.!

 Raghad Bank-- Menu 
1) Deposit
2) Withdraw
3) Transfer
4) Show Info
5) Logout
> 1
Choose account:
1) Checking
2) Savings
> 1
Amount?: $200
Deposited $200. Balance: $0 -> $200

> 2
Choose account withdraw:
1) Checking
2) Savings
> 1
 amount?: $50
Withdrew $50. Balance: $200 -> $150

> 3
Transfer type:
1) Between my accounts (Checking ⇄ Savings)
2) To another customer
> 1
From which account?
1) Checking
2) Savings
> 1
Amount: $100
Starting transfer of $100 from checking to savings...
Withdrew $100. Balance: $150 -> $50
Deposited $100. Balance: $0 -> $100
Transfer completed successfully.
```

## Project Structure

- banking.py: application code
- bank.csv: data file (auto-created with headers on first run)
- README.md: you are here

## Features (Requirements → Implementation)

- Add New Customer: `Transaction.create_account`
- Login / Logout: `Transaction.login`, `Transaction.customer_menu`
- Checking / Savings / Both: `Transaction.create_account` (`has_checking`, `has_savings`)
- Deposit (checking/savings): `Transaction.deposit` → `BankAccount.deposit`
- Withdraw (checking/savings): `Transaction.withdraw` → `BankAccount.withdraw`
- Overdraft protection:
  - Max $100 per withdrawal: `BankAccount.withdraw`
  - Block below −$100 result: `BankAccount.withdraw`
  - $35 fee when crossing to negative: `BankAccount.withdraw`
  - Deactivate on repeated overdrafts: `BankAccount.withdraw`
  - Reactivate when balance becomes non‑negative: `BankAccount.deposit`
- Transfers:
  - Between my accounts: `Transaction.transfer` (t == "1")
  - To another customer: `Transaction.transfer` (t == "2")

## Data Model

Each row in `bank.csv` is one customer with fields:

```text
id, first_name, last_name, password, checking, savings, active, overdraft_count, has_checking, has_savings
```

Type handling:
- Integers: `id`, `checking`, `savings`, `overdraft_count`
- Booleans: `active`, `has_checking`, `has_savings` (stored as "true"/"false")
- Empty balances stored as empty string in CSV; loaded as `None` in memory.

## Classes

- `Customer`: pretty print account info
- `BankAccount`: deposit, withdraw, transfer logic (shared)
- `CheckingAccount` / `SavingsAccount`: thin wrappers setting `account_type`
- `Transaction`: menus, login flow, CSV I/O (`ensure_csv_exists`, `load_customers`, `save_customers`, optional `view_csv`)

## How It Works (CLI Flow)

1) Start app → Main menu
2) Create account or Login
3) After login → Customer menu (Deposit, Withdraw, Transfer, Show Info, Logout)
4) Every successful change persists to `bank.csv`

## Challenges & Takeaways

- Implementing overdraft rules and state (active/reactivation)
- Converting CSV text to proper types and back
- Designing one account engine with two account types

## Icebox Features

- ➜ Transaction History Log
  - Format -> CSV or JSON per customer
  - What to store -> timestamp, action (deposit/withdraw/transfer), account_type, amount, balances before/after, notes
  - Where -> `transactions.csv` or `transactions/` folder per user
  - How to integrate -> append on every successful operation in `BankAccount.deposit/withdraw/transfer`

- ➜ View Full History
  - Menu option -> “View My Transaction History” under customer menu
  - Behavior -> read and pretty-print all rows for `current_customer`
  - Filters -> optional date range / action type

- ➜ Inspect Single Transaction
  - Menu option -> “View Transaction by ID”
  - Behavior -> search by transaction_id and print extra details (pre/post balances, destination account, fees applied)

- ➜ Automated Tests
  - Framework -> pytest
  - Scope -> test at least 3 requirements: overdraft fee, max $100 per withdrawal, internal transfer correctness
  - Command -> `pytest -q`

- ➜ Enhanced CLI UX
  - Input validation -> centralized `read_amount()` and yes/no prompts
  - Styling -> colored output (optional), clearer prompts, consistent error messages
  - Typewriter-style welcome (optional) -> animated text at startup

## Screenshots / GIFs

Place your GIFs and screenshots under `assets/` and reference them above.
