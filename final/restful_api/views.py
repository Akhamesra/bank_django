from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from profiles.models import Customer_Data, Account_Data,Transactions
import random
from .utils import Classes
from rest_framework.decorators import api_view
from rest_framework.response import Response

# cur_customer = None #Stores customer obj

# Create your views here.
def randomGen():
    # return a 6 digit random number
    return int(random.uniform(100000, 999999))

def home(request):
    return render(request,'profiles/home.html')
@api_view(['GET'])

def account_management(request):
    cur_customer = Classes.Customer(request.user.username)
    accounts = cur_customer.accounts
    user_accnos = list(accounts.keys())
    print("user_accnos", user_accnos)
    return Response(
        {'user_accnos':user_accnos, 'can_close_accnos':user_accnos}  
    )
@api_view(['GET'])
def stat_gen(request):
    cur_customer = Classes.Customer(request.user.username)
    accounts = cur_customer.accounts
    msg=""
    user_accnos = list(accounts.keys())
    all_transactions = {}
    for acc in accounts:
        print("acc_no:",acc)
        acc_q=Account_Data.objects.get(Accno=int(acc))
        trans=Classes.Account(acc_q)
        transaction=trans.get_transaction_log()
        trans_objs_list = list(transaction.values())
        all_transactions[acc] = all_transactions.get(acc, [])+trans_objs_list
    big_list = dict()
    for accno, transac_obj_list in all_transactions.items():
        big_list[accno] = list()
        for transac_obj in transac_obj_list:
            li = list()
            li.append(transac_obj.trans_id)
            li.append(transac_obj.trans_details.Amount)
            li.append(transac_obj.trans_details.Type)
            big_list[accno].append(li)
    return Response({
        'msg':msg,  'user_accnos' : user_accnos, 'all_transac' : big_list
    })

@api_view(['GET'])
def show_details(request):
    customer = Classes.Customer(request.user.username)
    return Response({
        'name' : customer.customer_data.Name,
        'phone': customer.customer_data.Phone_no,
        'email': customer.customer_data.Email,
        'address': customer.customer_data.Address
    })
