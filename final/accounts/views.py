# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout

def register(request):
    try:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("accounts:signin")
        else:
            form = UserCreationForm()
    
        return render(request, "accounts/create_account.html", {"form": form})
    except Exception as e:
        return render(request,'profiles/error.html',{'error':e})

def sign_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect("profiles:admin_view")
            return redirect("profiles:dashboard")
    else:
        form = AuthenticationForm()
        #print('invalid')
    return render(request, "accounts/sign_in.html",{"form": form})
        #return redirect("accounts:signin")

def logout_view(request):
    # Logout the user if he hits the logout submit button
    logout(request)
    return redirect("profiles:home")
    # return render("test.html", context)

def tnc(request):
    return render(request, "accounts/tnc.html")