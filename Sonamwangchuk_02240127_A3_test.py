import unittest
from Sonamwangchuk_02240127_A3 import (
    BankingSystem,
    BankAccount,
    PersonalAccount,
    BusinessAccount,
    invalid_Amount_exception,
    Insufficient_funds_exception,
    invalid_transfer_exception,
)

class TestBankingSystem(unittest.TestCase):

    def setUp(self):
        """Create a BankingSystem and two accounts for testing."""
        self.bank = BankingSystem(filename="test_accounts.txt")
        # Clear any loaded accounts
        self.bank.accounts.clear()
        # Create two accounts for transfer tests
        self.acc1 = PersonalAccount("11111", "1234", 500.0)
        self.acc2 = BusinessAccount("22222", "5678", 300.0)
        self.bank.accounts[self.acc1.account_id] = self.acc1
        self.bank.accounts[self.acc2.account_id] = self.acc2

    def tearDown(self):
        """Clean up test file if created."""
        import os
        try:
            os.remove("test_accounts.txt")
        except FileNotFoundError:
            pass

    def test_deposit_positive_amount(self):
        self.acc1.deposit(100)
        self.assertEqual(self.acc1.funds, 600)

    def test_deposit_zero_or_negative(self):
        with self.assertRaises(invalid_Amount_exception):
            self.acc1.deposit(0)
        with self.assertRaises(invalid_Amount_exception):
            self.acc1.deposit(-50)

    def test_withdraw_valid_amount(self):
        self.acc1.withdraw(200)
        self.assertEqual(self.acc1.funds, 300)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(Insufficient_funds_exception):
            self.acc1.withdraw(1000)

    def test_withdraw_invalid_amount(self):
        with self.assertRaises(invalid_Amount_exception):
            self.acc1.withdraw(0)
        with self.assertRaises(invalid_Amount_exception):
            self.acc1.withdraw(-20)

    def test_transfer_valid(self):
        self.acc1.transfer(200, self.acc2)
        self.assertEqual(self.acc1.funds, 300)
        self.assertEqual(self.acc2.funds, 500)

    def test_transfer_to_none_account(self):
        with self.assertRaises(invalid_transfer_exception):
            self.acc1.transfer(50, None)

    def test_transfer_insufficient_funds(self):
        with self.assertRaises(Insufficient_funds_exception):
            self.acc1.transfer(1000, self.acc2)

    def test_top_up_mobile_valid(self):
        initial_funds = self.acc1.funds
        # Note: topUpMobileNO expects amount and phone number, so we mock phone number input
        msg = self.acc1.topUpMobileNO(100)
        self.assertIn("recharge of 100", msg)
        self.assertEqual(self.acc1.funds, initial_funds - 100)

    def test_top_up_mobile_invalid_amount(self):
        with self.assertRaises(invalid_Amount_exception):
            self.acc1.topUpMobileNO(0)
        with self.assertRaises(invalid_Amount_exception):
            self.acc1.topUpMobileNO(-50)

    def test_top_up_mobile_insufficient_funds(self):
        with self.assertRaises(Insufficient_funds_exception):
            self.acc1.topUpMobileNO(self.acc1.funds + 10)

    def test_delete_existing_account(self):
        self.bank.delete_account(self.acc1.account_id)
        self.assertNotIn(self.acc1.account_id, self.bank.accounts)

    def test_delete_nonexistent_account(self):
        with self.assertRaises(ValueError):
            self.bank.delete_account("nonexistent")

    def test_login_success(self):
        account = self.bank.login(self.acc1.account_id, self.acc1.passcode)
        self.assertEqual(account.account_id, self.acc1.account_id)

    def test_login_failure(self):
        with self.assertRaises(ValueError):
            self.bank.login("wrongid", "1234")
        with self.assertRaises(ValueError):
            self.bank.login(self.acc1.account_id, "wrongpass")

if __name__ == "__main__":
    unittest.main()