from profiles.models import *
import random
from datetime import date,datetime

def randomGen():
    return int(random.uniform(100000, 999999))

class Account:
    def __init__(self, account_details):
        self.account_no = account_details.Accno
        self.account_details = account_details
        self.transac = {}
        transaction_list = Transactions.objects.filter(From_Acc = account_details)
        for trans in transaction_list:
            self.transac[trans.Trans_ID] = Transaction(trans)

    def create_transaction(self,to_acc, amt,type, chk):
        new_trans = New_Transaction(self,to_acc,amt,type, chk)
        
    def get_transaction_log(self):
        for tr in self.transac:
            self.transac[tr].display()
        return self.transac
                   

        
class New_Account(Account):
    def __init__(self, customer_obj):
        new_acc = Account_Data()
        new_acc.Accno = randomGen()
        new_acc.Balance = 0
        new_acc.Owner = customer_obj.customer_data
        new_acc.save()
        super().__init__(new_acc)  #Call to base class constrcutor  

#For existing customer        
class Customer:
    def __init__(self, username):
        self.customer_data = Customer_Data.objects.get(Name = username)
        self.accounts = {}
        account_data_list = Account_Data.objects.filter(Owner=self.customer_data)
        print(account_data_list)
        for account_data in account_data_list:
            self.accounts[account_data.Accno] = Account(account_data)
        
    def create_account(self):
        new_account = New_Account(self)
        self.accounts[new_account.account_no] = new_account
        
    def close_account(self, accno):
        del_account = self.accounts[accno]
        del_account.account_details.delete()
        del self.accounts[accno]
        
                
            
        
class New_Customer(Customer):
    def __init__(self, name, phone_no, email,address):
        #Insert details to DB
        cust_user=Customer_Data()
        cust_user.Name = name
        cust_user.Phone_no = phone_no
        cust_user.Email = email
        cust_user.Address = address
        cust_user.save()
        super().__init__(name)

    
        
class Transaction:
    def __init__(self, trans_data):
        #Read existing transaction details from DB
        self.trans_id=trans_data.Trans_ID
        self.trans_details=trans_data
        
    def display(self):
        '''Display transaction details'''
        print("self.trans_id: ",self.trans_id)
        print("self.trans_details: ",self.trans_details.Type)
   
  
        
class New_Transaction(Transaction):
    def __init__(self, account_obj,to_acc, amount, trans_type,chk):  

        trans_details=Transactions()
        trans_details.Amount=amount
        trans_details.Type=trans_type
        trans_details.From_Acc=account_obj.account_details
        trans_details.To_Acc = to_acc
        trans_details.same = chk
        trans_details.save()
        super().__init__(trans_details)


