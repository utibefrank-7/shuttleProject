from django.shortcuts import render,redirect 
from .forms import SignupForm, LoginForm
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.contrib.auth import logout





# Create your views here.
def home_view(request):
    return render (request, "accounts/home.html")

def signup_view(request):
    if request.method =="POST":
        form =SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
        

    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form':form})

def login_view(request):
    if request.method =="POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)
           
            #ROLE REDIRECTION 

            if user.role =="owner":

                return redirect("owner_dashboard")
            
            elif user.role =="admin":

                return redirect("admin_dashboard")
            
            elif user.role =="driver":
                
                return redirect("driver_dashboard")
            else:

                return redirect("home")

    else:
        form =LoginForm()
    return render(request,"accounts/login.html", {"form":form})   
 
#@login_required for login protection 
@login_required
@role_required(allowed_roles=["driver"])#middleware protection
def driver_dashboard_view(request):
    return render(request,"accounts/driver_dashboard.html")


@login_required
@role_required(allowed_roles=["owner"]) #middleware protection
def owner_dashboard_view(request):
    return render(request,'accounts/owner_dashboard.html')


def logout_view(request):
    logout(request)
    
    return redirect("login")


# @login_required
# def admin_dashboard_view(request):
#     return render()