class BankAccount():
    def __init__(self, balance):
        self.__balance = balance
    def deposit(self, money):
        if(money > 0):
            self.balance += money
        else:
            print("Fail")
    def withdraw(self, money):
        if(money <= self.balance and money > 0):
            self.balance -= money
        else:
            print("Not enough")
    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self,money):
        if(money >= 0):
            self.__balance = money
        else:
            raise ValueError("Balance can't be negative")
        
if __name__ == "__main__":
    bankcount = BankAccount(1000)
    print(f"Balance:{bankcount.balance}")
    bankcount.balance = 6000
    print(f"Balance:{bankcount.balance}")
    bankcount.deposit(2800)
    print(f"Balance:{bankcount.balance}")
    bankcount.withdraw(3800)
    print(f"Balance:{bankcount.balance}")
