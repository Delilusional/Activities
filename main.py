from wallet import User

account = User("Senyor", 1000)
account.working("5 hours", 500)
account.buying("Coffee", 150)
account.deposit(500)
account.withdraw(1000)
account.generate_receipt()