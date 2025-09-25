# 🏦💸 Raghad Bank 💸🏦  
*A simple yet fun Banking System built with Python & CSV*  

Welcome to **Raghad Bank** — a CLI-based banking app where you can open accounts, deposit, withdraw, and transfer money with overdraft protection & reactivation rules.  

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)  ![CSV](https://img.shields.io/badge/Data-CSV-lightgrey?logo=files)  ![Interface](https://img.shields.io/badge/Interface-CLI-green?logo=windowsterminal)  ![GitHub](https://img.shields.io/badge/Hosted_on-GitHub-black?logo=github)  ![VS Code](https://img.shields.io/badge/Editor-VS%20Code-blue?logo=visualstudiocode)  

---
##  Project Structure
- bank.csv      -> Data file (auto-created on first run)  
- banking.py    -> Main application code  
- README.md     -> Project documentation 


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

##  How to Run
   ```bash
   python3 --version
