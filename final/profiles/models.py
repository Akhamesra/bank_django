from django.db import models

# Create your models here.
class Customer_Data(models.Model):
    Cust_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    Phone_no = models.CharField(max_length=10,null=True)
    Email = models.EmailField(null=True)
    Address = models.TextField(null=True)
    class Meta:
        db_table = 'customer'
    def __str__(self):
        return f"{self.Name}"
   
class Account_Data(models.Model):
    Accno = models.IntegerField(primary_key=True)
    Owner = models.ForeignKey(Customer_Data, on_delete=models.CASCADE)
    Balance = models.FloatField()
    #Name = models.CharField(max_length=200)
    class Meta:
        db_table = 'account'

class Transactions(models.Model): 
    Trans_ID = models.AutoField(primary_key=True)
    Accno = models.ForeignKey(Account_Data, on_delete=models.CASCADE)
    Amount = models.FloatField()
    Type = models.CharField(max_length=30)
    #Type can be "withdraw" or "deposit"
    class Meta:
        db_table = 'transactions'
        
# class Money_Transfers(models.Model):             
#     Trans_ID = models.AutoField(primary_key=True)
#     From_accno = models.ForeignKey(Account_Data, on_delete=models.CASCADE, related_name = 'From_accno')
#     To_accno = models.ForeignKey(Account_Data, on_delete=models.CASCADE, related_name = 'To_accno')
#     Amount = models.FloatField()
#     class Meta:
#         db_table = 'transfers'
    
       
    