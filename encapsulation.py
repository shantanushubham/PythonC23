# In Python - Access Specifiers mean nothing. Everything is always public, unlike Java/C++.

# Starting with _ = Protected Member = Meant for internal use only. Convention Only
# Starting with __ = Private. Access is blocked. But if assigned, a new copy is created in the memory and the object
# maintains two copies as soon as an assignment happens


class BankAccount:

    __member = 10

    def __init__(self, balance) -> None:
        self.__balance = balance

    def deposit(self, amount):
        self.__balance += amount

    # Getter
    def get_balance(self):
        return self.__balance

    def __get_card_number(self):
        return "5133-1298-5611-9722"

    def do_card_transaction(self):
        card_number = self.__get_card_number()
        print("Transaction Success")

    @staticmethod # Convention Only
    def get_member():
        return BankAccount.__member

# [10][][][100]
#  m        m


account = BankAccount(1000)
# account.deposit(9000)  # Correct
# account.__balance = 5000  # Semantically it is not right
# print(account.get_balance())
# print(account.__balance)
print(account.do_card_transaction())
BankAccount.__member = 100
print(BankAccount.get_member())


class Balance:
    
    def __init__(self, balance) -> None:
        self._balance = balance

    def workout(self, decrease):
        self._balance = self._balance - decrease

    def getBalance(self):
        print(self._balance)


# x = Balance(70)
# x.getBalance()
# print(x._balance)

