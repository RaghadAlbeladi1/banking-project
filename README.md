# 🏦💸 Raghad Bank 💸🏦  
*A simple yet fun Banking System built with Python & CSV*  

Welcome to **Raghad Bank** — a CLI-based banking app where you can open accounts, deposit, withdraw, and transfer money with overdraft protection & reactivation rules.  

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python) ![CSV](https://img.shields.io/badge/Data-CSV-lightgrey?logo=files) ![Interface](https://img.shields.io/badge/Interface-CLI-green?logo=windowsterminal) ![GitHub](https://img.shields.io/badge/Hosted_on-GitHub-black?logo=github) ![VS Code](https://img.shields.io/badge/Editor-VS%20Code-blue?logo=visualstudiocode)  

---

## Project Structure
```
 Raghad-Bank/
├──  bank.csv        → Data file (auto-created on first run)  
├──  banking.py      → Main application code  
└──  README.md       → Project documentation  
```

## ✨ Features (User Stories → Implementation)

| #  | User Story | Where in Code? |
|----|-------------|----------------|
| 1️⃣ | Create new account (checking/savings/both) | `Transaction.create_account` |
| 2️⃣ | Login / Logout | `Transaction.login` & `Transaction.customer_menu` |
| 3️⃣ | Deposit | `Transaction.deposit` → `BankAccount.deposit` |
| 4️⃣ | Withdraw (with overdraft rules) | `Transaction.withdraw` → `BankAccount.withdraw` |
| 5️⃣ | Transfers (between my accounts or to other customers) | `Transaction.transfer` |
| 6️⃣ | Overdraft protection ($35 fee, deactivate after 2 overdrafts) | `BankAccount.withdraw` |
| 7️⃣ | Reactivation after deposit | `BankAccount.deposit` + `Transaction.reactivation_assistance` |
| 8️⃣ | Pretty print account info | `Customer.display` |

---

## How to Run

### 1️⃣ Prerequisites
Make sure you have Python 3.10+ installed on your system:
```bash
python3 --version
```

### 2️⃣ Run the Application
Execute the program directly:
```bash
python3 banking.py
```

### 3️⃣ Main Menu
Upon running, you'll see the main menu:
```
🏦💸 Welcome To Raghad Bank 💸🏦
1) Login
2) Create Account
3) Quit
```

##  Data Model

Each row in `bank.csv` = one customer record:
```csv
id, first_name, last_name, password, checking, savings, active, overdraft_count, has_checking, has_savings
```

**Data Types:**
- **Integers** → id, checking, savings, overdraft_count
- **Booleans** → stored as "true"/"false"
- **Empty balances** → stored as empty string, loaded as None in memory

##  Example Walkthrough

### Create New Account
```
> 2
 Create New Account
First name: Raghad
Last name: Albeladi
Password: ****
Which account(s) to open?
1) Checking only
2) Savings only
3) Both
> 3
Account created! Your ID: 10001 🥰
```

###  Login
```
> 1
 Login
Customer ID: 10001
Password: ****
Welcome Raghad Albeladi!
```

###  Customer Menu
After successful login, you'll access the customer menu:
```
✨ Raghad Bank -- Menu ✨
1)➕ Deposit
2)➖ Withdraw
3)🔁 Transfer
4)📋 Show Info
5)❌ Logout
```

###  Deposit Example
```
> 1
Choose account:
1) Checking
2) Savings
> 1
Amount?: $200
Deposited $200. Balance: $0 -> $200
```

###  Withdraw Example
```
> 2
Choose account withdraw:
1) Checking
2) Savings
> 1
 amount?: $50
Withdrew $50. Balance: $200 -> $150
```

###  Overdraft Example
When you try to withdraw more than your balance:
```
> 2
Choose account withdraw:
1) Checking
2) Savings
> 1
 amount?: $200
Insufficient funds. $35 overdraft fee applied.
Withdrew $200. Balance: $150 -> $-85
Overdraft count: 1
```

After 2 overdrafts, your account gets deactivated:
```
> 2
Choose account withdraw:
1) Checking
2) Savings
> 1
 amount?: $100
Insufficient funds. $35 overdraft fee applied.
Withdrew $100. Balance: $-85 -> $-220
Overdraft count: 2
⚠️  Account deactivated due to 2 overdrafts!
```

###  Account Reactivation
When your account is deactivated, you need to deposit enough to reach $0:
```
> 1
Choose account:
1) Checking (INACTIVE - Balance: $-220)
2) Savings
> 1
Current balance: $-220
Minimum deposit needed to reactivate: $220
Amount?: $250
Deposited $250. Balance: $-220 -> $30
🎉 Account reactivated! Welcome back!
```

###  Transfer Example
#### Between Your Own Accounts
```
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

###  Show Account Information
```
> 4

--- Account Information for Raghad Albeladi ---
Checking Balance: $50.00 (open=True)
Savings Balance : $100.00 (open=True)
Active: True
Overdraft Count: 0
```

###  Logout
```
> 5
Logged out
💜 Thank you for using Raghad Bank! 💜
```

## Challenges & Key Takeaways

- ✅ Handling overdrafts & automatic deactivation/reactivation rules
- ✅ Converting CSV text into proper **types** (int, bool, None)
- ✅ Writing one **BankAccount engine** that works for both account types
- ✅ Designing a menu-driven CLI that feels smooth & user-friendly
- ✅ Learned how important **data persistence** is (CSV as a mini-database)

## Icebox Features (Future Ideas)

- Transaction history log (CSV/JSON)
- View past transactions with filtering
- Unit tests (pytest) for deposit/withdraw/transfer
- Enhanced CLI styling (colors, ASCII art banners)
- Forgot password & reset flow

## Technologies Used        (#fix)

- 🐍 Python 3.10+
- 📑 CSV for data persistence
- 🖥️ CLI (menu-driven interaction)
- 🛠️ Visual Studio Code
- 🌐 GitHub for version control

## 🎓 Education & Training      (#fix)

This project was developed as part of my learning journey with:

<div align="center">

**General Assembly**  
<img src="https://www.clipartmax.com/png/small/354-3547041_download-general-assembly-clipart-logo-brand-trademark-general-assembly-logo-black.png" alt="General Assembly Logo" width="200"/>

**Saudi Digital Academy**  
<img src="https://sda.edu.sa/assets/images/logo.png" alt="Saudi Digital Academy Logo" width="200"/>

*Empowering the next generation of digital talent* 🚀

</div>

## System Requirements

- Python 3.10 or higher
- No additional dependencies required

## Notes

- Account IDs are automatically generated starting from 10001
- The system supports both checking and savings accounts
- All transactions show balance changes for transparency
- Secure password authentication for account access
- Overdraft protection with $35 fee and account deactivation after 2 overdrafts

## Fun Ending

Thank you for visiting **Raghad Bank**! 💜  
Every deposit counts, every withdrawal teaches discipline — but don't worry, here overdrafts are just Python learning opportunities 😉  

![funny gif](https://media4.giphy.com/media/GeimqsH0TLDt4tScGw/200w.webp)

---

**Made with 💜 by Raghad Albeladi**
