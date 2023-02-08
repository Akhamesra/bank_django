from django.db import models
from django.core.validators import MinLengthValidator,MinValueValidator

class Customer_Data(models.Model):
    Cust_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    Phone_no = models.CharField(max_length=10,null=True, validators=[MinLengthValidator(10)])
    Email = models.EmailField(null=True)
    Address = models.TextField(null=True)
    class Meta:
        db_table = 'customer'
    def __str__(self):
        return self.Name
   
class Account_Data(models.Model):
    Accno = models.IntegerField(primary_key=True)
    Owner = models.ForeignKey(Customer_Data, on_delete=models.CASCADE)
    Balance = models.FloatField(validators=[MinValueValidator(0)])
    class Meta:
        db_table = 'account'
    def __str__(self):
        return str(self.Accno)
    

class Transactions(models.Model): 
    Trans_ID = models.AutoField(primary_key=True)
    Accno = models.ForeignKey(Account_Data, on_delete=models.CASCADE)
    Amount = models.FloatField(validators=[MinValueValidator(0)])
    Type = models.CharField(max_length=30)
    #Type can be "withdraw" or "deposit"
    class Meta:
        db_table = 'transactions'
    def __str__(self):
        return str(self.Amount)
    
       
    