from django.shortcuts import render, redirect
from profiles.models import Customer_Data, Account_Data,Transactions
import random
from django.http import HttpResponse
from .utils import Classes

cur_customer = None #Stores customer obj

# Create your views here.
def randomGen():
    return int(random.uniform(100000, 999999))

def home(request):
    '''
    Load Landing page.
    '''
    return render(request,'profiles/home.html')
    
def user_details(request):
    '''
    Ask for additional details if user is new.
    '''

    if request.method == 'POST':
        phoneno = request.POST.get('phoneno')
        email = request.POST.get('email')
        address = request.POST.get('address')
        Classes.New_Customer(request.user.username, phoneno,email,address)
        return redirect('profiles:dashboard')
    return render(request, 'profiles/user_details.html') 


def display_menu(request):
    '''
    Show the dashboard
    '''
    global cur_customer
    try:
        cust_details = Customer_Data.objects.filter(Name = request.user.username)
        if(cust_details):
           print("Existing Customer")
           customer = Classes.Customer(request.user.username)
           print("customer obj", customer)
        else:
            print("Making New Customer")
            return redirect('profiles:user_details')
        cur_customer = customer
        return render(request, 'profiles/user_account.html', 
        {'customer':customer})
    except Exception as e:
        return render(request,'profiles/error.html',{'error':e})

     

def account_management(request):
    '''
    Show account details
    Can create account
    Can delete account
    '''
    try:
        accounts = cur_customer.accounts
        user_accnos = list(accounts.keys())
        print("user_accnos", user_accnos)
        return render(request, 'profiles/account_details.html', 
        {'customer':cur_customer, 'accounts':accounts, 'can_close_accnos':user_accnos})
    except Exception as e:
        return render(request,'profiles/error.html',{'error':e})


def withdraw(request):
    '''
    Withdraw money from your bank account
    '''
    accounts = cur_customer.accounts
    msg=""
    try:
        if request.method == "POST":
            acc_num=int(request.POST.get('acc_no')) if request.POST.get('acc_no') is not None else 0
            amount=int(request.POST.get('amount'))
            print('requestPOST=',acc_num,type(acc_num))
            #print('account dict:',accounts.keys())
            if acc_num in accounts:
                #acc_obj= accounts[acc_num]
                acc_q=Account_Data.objects.get(Accno=acc_num)
                balance=acc_q.Balance
                print("balance:",balance)
                if(balance>=amount):
                    trans=Classes.Account(acc_q)
                    trans.create_transaction(amount,"withdraw")
                    balance-=amount
                    acc_q.Balance=balance
                    print("balance:",acc_q.Balance)
                    acc_q.save()
                    cur_customer.accounts[acc_num].account_details.Balance-=amount
                    msg="<td>Withdrawn Successfully!</td><br>"
                else:
                    msg="<td>Not sufficient balance!</td><br>"
                
            else:
                msg="<p>Invalid account number</p><br>"
        return render(request, 'profiles/withdraw.html',{'customer':cur_customer, 'accounts':accounts,'msg':msg})
    except Exception as e:
        return render(request,'profiles/error.html',{'error':e})

def deposit(request):
    '''
    Deposite money to your bank account
    '''
    accounts = cur_customer.accounts
    msg="<br>Enter a valid account no. and also check for your balance!</p><br>"
    try:
        if request.method == "POST":
            acc_num= int(request.POST.get('acc_no')) if request.POST.get('acc_no') is not None else 0
            amount=int(request.POST.get('amount'))
            if acc_num in accounts:
                #acc_obj= accounts[acc_num]
                acc_q=Account_Data.objects.get(Accno=acc_num)
                balance=acc_q.Balance
                print("balance:",balance)
                trans=Classes.Account(acc_q)
                trans.create_transaction(amount,"deposit")
                balance+=abs(amount)
                acc_q.Balance=balance
                print("balance:",acc_q.Balance)
                acc_q.save()
                cur_customer.accounts[acc_num].account_details.Balance+=amount
                msg="<td>Deposited Successfully!</td><br>"
            else:
                msg="<p>Invalid account number</p><br>"
        return render(request, 'profiles/deposit.html',{'customer':cur_customer, 'accounts':accounts,'msg':msg})
    except Exception as e:
        return render(request,'profiles/error.html',{'error':e})

def transfer(request):
    '''
    Transfer money from your account to someone else account
    '''
    accounts = cur_customer.accounts
    msg=""
    try:
        if request.method == 'POST':
            # withdraw from
            # deposit to
            from_acc= int(request.POST.get('from_acc'))
            to_acc= int(request.POST.get('to_acc'))
            amount=int(request.POST.get('amount'))
            if from_acc == to_acc:
                msg="<p>from and to account number are same</p><br>"
            if from_acc in accounts:
                from_details = Account_Data.objects.get(Accno=from_acc)
                from_bal = from_details.Balance
                to_details = Account_Data.objects.get(Accno=to_acc)
                to_bal = to_details.Balance
                if(from_bal>=amount):
                # set transaction
                    from_trans=Classes.Account(from_details)
                    from_trans.create_transaction(amount,"withdraw")
                    to_trans=Classes.Account(to_details)
                    to_trans.create_transaction(amount, "deposit")
                    from_bal-=amount
                    to_bal+=amount
                    from_details.Balance=from_bal
                    to_details.Balance=to_bal
                    from_details.save()
                    to_details.save()
                    # update db
                    from_obj = Account_Data.objects.get(Accno=from_acc)
                    curr_from = from_obj.Balance
                    curr_from += amount
                    Account_Data.objects.filter(Accno=from_acc).update(Balance=curr_from)
                    to_obj = Account_Data.objects.get(Accno=to_acc)
                    curr_to = to_obj.Balance
                    curr_to += amount
                    Account_Data.objects.filter(Accno=to_acc).update(Balance=curr_to)
                    msg="<td>Transaction Successful!</td><br>"
                else:
                    msg="<td>Balance not enough to withdraw this amount</td><br>"
        return render(request, 'profiles/transfer.html',{'accounts':accounts, 'msg':msg})
    except Exception as e:
        return render(request,'profiles/error.html',{'error':e})

def stat_gen(request):
    '''
    Show transaction history
    '''
    try:
        accounts = cur_customer.accounts
        print(accounts)
        msg=""
        all_transactions = {}
        for acc in accounts:
            print("acc_no:",acc)
            acc_q=Account_Data.objects.get(Accno=int(acc))
            trans=Classes.Account(acc_q)
            transaction=trans.get_transaction_log()
            trans_objs_list = list(transaction.values())
            all_transactions[acc] = all_transactions.get(acc, [])+trans_objs_list
        return render(request, 'profiles/stat_gen.html',{'customer':cur_customer, 'accounts':accounts, 'transaction':all_transactions,'msg':msg})
    except Exception as e:
        return render(request,'profiles/error.html',{'error':e})

def get_transaction_action(request):
    '''

    '''
    try:
        accounts = cur_customer.accounts
        msg="filter"
        button_action = request.GET['account_action']
        all_transactions = {}
        if(button_action == 'withdraw'):
            for acc in accounts:
                transaction=Transactions.objects.filter(Accno_id=int(acc),Type="withdraw")
                all_transactions[acc] = list(transaction)
        elif(button_action == 'deposit'):
            for acc in accounts:
                transaction=Transactions.objects.filter(Accno_id=int(acc),Type="deposit")
                all_transactions[acc] = list(transaction)
        elif(button_action == 'all'):
            return redirect('profiles:stat_gen')
        print("all_trans:", all_transactions)
        return render(request,'profiles/stat_gen.html',{'customer':cur_customer, 'accounts':accounts, 'transaction':all_transactions,'msg':msg});
    except Exception as e:
        return render(request,'profiles/error.html',{'error':e})

def get_function_chosen(request):
    '''
    Choose views
    '''
    try:
        menu_chosen = request.GET['function_chosen']
        if(menu_chosen=='view_accounts'):
            return redirect('profiles:account_management') #name of view given in urls.py
        elif(menu_chosen=='withdraw'):
            return redirect('profiles:withdraw') #name of view given in urls.py
        elif(menu_chosen=='deposit'):
            return redirect('profiles:deposit') #name of view given in urls.py
        elif(menu_chosen=='stat_gen'):
            return redirect('profiles:stat_gen') #name of view given in urls.py
        elif(menu_chosen=='show_details'):
            return redirect('profiles:show_details') #name of view given in urls.py
        elif(menu_chosen=='transfer'):
            return redirect('profiles:transfer') #name of view given in urls.py
    except Exception as e:
        return render(request,'profiles/error.html',{'error':e})

    
def get_account_action(request):
    '''
    Take input - create or close 
    Create account
    Close account
    '''
    try:
        account_action = request.GET['account_action']
        #err_msg=""
        if(account_action == 'create'):
            cur_customer.create_account()
        elif(account_action == 'close'):
            close_accno = int(request.GET['close_accno'])
            cur_customer.close_account(close_accno)
        else:
            print("Got neither create nor close")
        return redirect('profiles:account_management')
    except Exception as e:
        return render(request,'profiles/error.html',{'error':e})

def admin_view(request):
    '''
    Admin view
    Show all users detail
    '''
    try:
        data = Account_Data.objects.all()
        context ={
            'data' : data,
        }
        return render(request, "profiles/admin.html", context)
    except Exception as e:
        return render(request,'profiles/error.html',{'error':e})


def show_details(request):
    '''
    Show user information
    '''
    try:
        return render(request, 'profiles/show_details.html', 
        {'customer':cur_customer})
    except Exception as e:
        return render(request,'profiles/error.html',{'error':e})

def error(request):
    '''
    Load error when exception occures
    '''
    return render(request,'profiles/error.html', error)