import random 
import tkinter as tk
from tkinter import messagebox, simpledialog

class banking_exception(Exception):
    """Base class for banking-related errors."""
    pass

class invalid_Amount_exception(banking_exception):
    """Raised when the amount is zero or negative."""
    pass

class Insufficient_funds_exception(banking_exception):
    """Raised when there is not enough money in the account."""
    pass

class invalid_transfer_exception(banking_exception):
    """Raised when a transfer is not possible (e.g. wrong recipient)."""
    pass

class BankAccount:
    """Represent the operation such as deposit, transfer, mobile up and withdrawal"""

    def __init__(self, account_id, passcode, account_category, funds=0):
        """ Initialize bank account"""
        self.account_id = account_id
        self.passcode = passcode
        self.account_category = account_category
        self.funds = funds

    def deposit(self, amount):
        """ Adding money to the account"""
        if amount <= 0:
           raise invalid_Amount_exception("Amount must be positive")
        self.funds += amount
        return "Deposit completed."
        
    def withdraw(self, amount):
        """Taking out the money, if funds is sufficient """
        if amount <= 0:
            raise invalid_Amount_exception("Amount must be positive")
        if amount > self.funds:
                raise Insufficient_funds_exception("Insufficient funds")
        self.funds -= amount
        return "Withdrawal completed."
    
    def transfer(self, amount, recipient_account):
        """Transferring money to another account if sufficient """
        if recipient_account is None:
            raise invalid_transfer_exception("Invalid recipient account")
        withdrawal_message = self.withdraw(amount)
        recipient_account.deposit(amount)
        return "Transfer completed."
  
    def topUpMobileNO(self, amount, mobile_no):
        """Recharge mobile phone """
        if amount <= 0:
            raise invalid_Amount_exception("Amount must be positive")
        if amount > self.funds:
            raise Insufficient_funds_exception("Insufficient funds")
        self.funds -= amount
        return f"Recharge of {amount} to Phone Number: {mobile_no} is successful."

class PersonalAccount(BankAccount):
    def __init__(self, account_id, passcode, funds=0):
        super().__init__(account_id, passcode, "Personal", funds)

class BusinessAccount(BankAccount):
    def __init__(self, account_id, passcode, funds=0):
        super().__init__(account_id, passcode, "Business", funds)

class BankingSystem:
    def __init__(self, filename="accounts.txt"):
        self.filename = filename
        self.accounts = self.load_accounts()

    def load_accounts(self):
        accounts = {}
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    account_id, passcode, account_category, funds = line.strip().split(",")
                    funds = float(funds)   # convert funds to float
                    if account_category == "Personal":
                        account = PersonalAccount(account_id, passcode, funds)
                    else:
                        account = BusinessAccount(account_id, passcode, funds)
                    accounts[account_id] = account
        except FileNotFoundError:
            pass
        return accounts
    
    def save_accounts(self):
        """account save to the file"""
        with open(self.filename, "w") as file:
            for account in self.accounts.values():
                file.write(f"{account.account_id},{account.passcode},{account.account_category},{account.funds}\n")
    
    def create_account(self, account_type):
        """Creating new account"""
        account_id = str(random.randint(10000, 99999))
        passcode = str(random.randint(1000, 9999))
        if account_type == "Personal":
            account = PersonalAccount(account_id, passcode)
        else:
            account = BusinessAccount(account_id, passcode)
        self.accounts[account_id] = account
        self.save_accounts()
        return account

    def login(self, account_id, passcode):
        """verifying the account"""
        account = self.accounts.get(account_id)
        if account and account.passcode == passcode:
            return account
        raise ValueError("Account number or password is not recognized")
    
    def delete_account(self, account_id):
        """Delete an account by account ID"""
        if account_id in self.accounts:
            del self.accounts[account_id]
            self.save_accounts()
        else:
            raise ValueError("Account does not exist")

class BankingGUI:
    """Graphical User Interface for the Banking System using Tkinter."""

    def __init__(self, master):
        self.master = master
        self.master.title("Banking System GUI")
        self.master.geometry("300x200")

        self.bank = BankingSystem()
        self.account = None

        # Create main menu buttons
        self.label = tk.Label(master, text="Welcome to the Banking System", font=('Arial', 12))
        self.label.pack(pady=10)

        self.open_account_button = tk.Button(master, text="Open Account", command=self.open_account)
        self.open_account_button.pack(fill='x', padx=20, pady=5)

        self.login_button = tk.Button(master, text="Login to Account", command=self.login)
        self.login_button.pack(fill='x', padx=20, pady=5)

        self.exit_button = tk.Button(master, text="Exit", command=master.quit)
        self.exit_button.pack(fill='x', padx=20, pady=5)

    def open_account(self):
        """Open a new Personal or Business account."""
        account_type = simpledialog.askstring("Account Type", "Select account type (Personal or Business):")
        if account_type not in ["Personal", "Business"]:
            messagebox.showerror("Error", "Unsupported account type")
            return

        account = self.bank.create_account(account_type)
        messagebox.showinfo("Account Created", 
                           f"Account created!\nAccount ID: {account.account_id}\nPasscode: {account.passcode}")

    def login(self):
        """Log in to an existing account and show account operations."""
        account_id = simpledialog.askstring("Login", "Enter your Account ID:")
        passcode = simpledialog.askstring("Login", "Enter your Passcode:")

        try:
            self.account = self.bank.login(account_id, passcode)
            self.account_operations()
        except ValueError as e:
            messagebox.showerror("Login Failed", str(e))

    def account_operations(self):
        """Show the account operations window."""
        self.ops_window = tk.Toplevel(self.master)
        self.ops_window.title(f"Account: {self.account.account_id}")
        self.ops_window.geometry("300x400")

        tk.Label(self.ops_window, 
                text=f"Account Type: {self.account.account_category}",
                font=('Arial', 10, 'bold')).pack(pady=5)
        
        self.funds_label = tk.Label(self.ops_window, 
                                  text=f"Funds: {self.account.funds:.2f}",
                                  font=('Arial', 10))
        self.funds_label.pack(pady=5)

        # Operation buttons
        buttons = [
            ("Deposit", self.deposit),
            ("Withdraw", self.withdraw),
            ("Mobile Recharge", self.mobile_recharge),
            ("Transfer", self.transfer),
            ("Delete Account", self.delete_account),
            ("Logout", self.ops_window.destroy)
        ]

        for text, command in buttons:
            tk.Button(self.ops_window, text=text, command=command).pack(fill='x', padx=20, pady=5)

    def update_funds_label(self):
        self.funds_label.config(text=f"Funds: {self.account.funds:.2f}")

    def deposit(self):
        amount_str = simpledialog.askstring("Deposit", "Enter amount to deposit:")
        try:
            amount = float(amount_str)
            msg = self.account.deposit(amount)
            self.bank.save_accounts()
            self.update_funds_label()
            messagebox.showinfo("Deposit", msg)
        except (ValueError, banking_exception) as e:
            messagebox.showerror("Error", str(e))

    def withdraw(self):
        amount_str = simpledialog.askstring("Withdraw", "Enter amount to withdraw:")
        try:
            amount = float(amount_str)
            msg = self.account.withdraw(amount)
            self.bank.save_accounts()
            self.update_funds_label()
            messagebox.showinfo("Withdraw", msg)
        except (ValueError, banking_exception) as e:
            messagebox.showerror("Error", str(e))

    def mobile_recharge(self):
        mobile_no = simpledialog.askstring("Mobile Recharge", "Enter phone number:")
        amount_str = simpledialog.askstring("Mobile Recharge", "Enter recharge amount:")
        try:
            amount = float(amount_str)
            msg = self.account.topUpMobileNO(amount, mobile_no)
            self.bank.save_accounts()
            self.update_funds_label()
            messagebox.showinfo("Mobile Recharge", msg)
        except (ValueError, banking_exception) as e:
            messagebox.showerror("Error", str(e))

    def transfer(self):
        recipient_id = simpledialog.askstring("Transfer", "Enter recipient account ID:")
        amount_str = simpledialog.askstring("Transfer", "Enter amount to transfer:")
        try:
            amount = float(amount_str)
            recipient_account = self.bank.accounts.get(recipient_id)
            if recipient_account is None:
                messagebox.showerror("Error", "Recipient account does not exist.")
                return
            msg = self.account.transfer(amount, recipient_account)
            self.bank.save_accounts()
            self.update_funds_label()
            messagebox.showinfo("Transfer", msg)
        except (ValueError, banking_exception) as e:
            messagebox.showerror("Error", str(e))

    def delete_account(self):
        confirm = messagebox.askyesno("Delete Account", "Are you sure you want to delete your account?")
        if confirm:
            try:
                self.bank.delete_account(self.account.account_id)
                messagebox.showinfo("Delete Account", "Account deleted successfully.")
                self.ops_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingGUI(root)
    root.mainloop()