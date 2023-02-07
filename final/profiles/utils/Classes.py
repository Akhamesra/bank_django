from profiles.models import *
import random
from datetime import date,datetime

def randomGen():
    # return a 6 digit random number
    return int(random.uniform(100000, 999999))
  
class Account:
    def __init__(self, account_details):
        self.account_no = account_details.Accno
        self.account_details = account_details
        self.transac = {}
        transaction_list = Transactions.objects.filter(Accno = account_details)
        for trans in transaction_list:
            self.transac[trans.Trans_ID] = Transaction(trans)

    def create_transaction(self,amt,type):
        new_trans = New_Transaction(self,date.today(),datetime.now(),amt,type)
        
    def get_transaction_log(self):
        for tr in self.transac:
            self.transac[tr].display()
        return self.transac
                   
                
        
class New_Account(Account):
    def __init__(self, customer_obj):
        #Store account details to DB
        #Then call base class constrcutor to get details into obj attribs from DB
        #accno = randomGen()
        new_acc = Account_Data()
        new_acc.Accno = randomGen()
        new_acc.Balance = 0
        new_acc.Owner = customer_obj.customer_data
        new_acc.save()
        super().__init__(new_acc)  #Call to base class constrcutor  
                
        
class Login_Details:
    def __init__(self, user, passwd):
        self.username = user
        self.password = passwd  
        
    #def login(self): 
    #Could have a login function which checks if user exists in DB - not sure if its apt 
    #Yet to link log in details with customer
    def get_customer(self):
        #Access DB and get customer whose credentials match
        customer_data = Customer_Data.objects.get(Name = self.username)
        #customer = Customer(
        return customer #None returned if customer is new, not in DB yet
        #pass
        
  
#For existing customer        
class Customer:
    def __init__(self, log_in_obj):
        self.customer_data = Customer_Data.objects.get(Name = log_in_obj.username)
        #get raises exception if no val found
        #if(not(self.customer_data)):
        #    raise CustomerDoesNotExist
        self.login_credentials = log_in_obj
        #Take other details from DB
        self.accounts = {}
        account_data_list = Account_Data.objects.filter(Owner=self.customer_data)
        print(account_data_list)
        for account_data in account_data_list:
            self.accounts[account_data.Accno] = Account(account_data)
        
    def create_account(self):
        new_account = New_Account(self)
        #Adding new account to dictionary of accounts owned by customer
        self.accounts[new_account.account_no] = new_account
        
    def close_account(self, accno):
        del_account = self.accounts[accno]
        del_account.account_details.delete()
        del self.accounts[accno]
        
                
            
        
class New_Customer(Customer):
    def __init__(self, log_in_obj, name, phone_no, email,address):
        #Insert details to DB
        cust_user=Customer_Data()
        cust_user.Name = name
        cust_user.Phone_no = phone_no
        cust_user.Email = email
        cust_user.Address = address
        cust_user.save()
        super().__init__(log_in_obj)
        #self.accounts = {}
    
        
class Transaction:
    def __init__(self, trans_data):
        #Read existing transaction details from DB
        self.trans_id=trans_data.Trans_ID
        self.trans_details=trans_data
        
    def display(self):
        #Display transaction details

        print("self.trans_id: ",self.trans_id)
        print("self.trans_details: ",self.trans_details.Type)
   
  
        
class New_Transaction(Transaction):
    def __init__(self, account_obj, date, time, amount, tran_type):  
        #trans_id will be got by auto-increment  
        trans_details=Transactions()
        trans_details.Amount=amount
        trans_details.Type=tran_type
        trans_details.Accno=account_obj.account_details
        trans_details.save()
        super().__init__(trans_details)
        

       
        
               
                        
        
                
        
               
