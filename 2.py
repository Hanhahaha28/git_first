class BankAcount():
    def __init__(self,balance):
        self.__balance = balance
        
    def deposit(self,money):
        if(money>0):
            self.balance += money
        else:
           print("Fail")
    def withdraw(self,money):
        if(money>=self.balance):
            self.balance -= money
        else:
            print("Insufficient")

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self,money):
        if(money>=0):
            self.__balance = money 
        else:
            raise ValueError("Balance can't be negative")  



if __name__ == "__main__":
    bankAcount = BankAcount(1000)
    bankAcount.balance = 2000
    print(f"Balance:{bankAcount.balance}")
    bankAcount.deposit(600)
    print(f"Balance: {bankAcount.balance}")
    bankAcount.withdraw(1200)
    print(f"Balance: {bankAcount.balance}")

