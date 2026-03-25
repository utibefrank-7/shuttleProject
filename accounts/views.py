from django.shortcuts import render,redirect 
from .forms import SignupForm, LoginForm
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.contrib.auth import logout
from django.http import HttpResponseForbidden, HttpResponse
from .models import Driverprofile, DriverApplication,Bus
from .forms import DriverprofileForm, DriverApplicationForm,BusForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .gmail_service import send_gmail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model





# Create your views here.
def home_view(request):
    return render (request, "accounts/home.html")
def about_view(request):
    return render (request, "accounts/About.html" )

def features_view(request):
    return render(request, "accounts/features.html" )


def signup_view(request):

        if request.method == "POST":
            form = SignupForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)

                # Ensure user is not verified
                user.is_verified = False
                user.save()

                # Generate token
                token = default_token_generator.make_token(user)

                # Create verification link
                verification_link = request.build_absolute_uri(
                    reverse("verify_email", args=[user.id, token])
                )

                # Send email
                send_gmail(
                    user.email,
                    "Verify your account",
                    f"Click this link to verify your account:\n{verification_link}"
                )

                # Stop here — do NOT log user in
                return render(request, "accounts/verification_email.html")

        else:
            form = SignupForm()

        return render(request, 'accounts/signup.html', {'form': form})


def send_verification_email(request, user):
    token = default_token_generator.make_token(user)

    link = request.build_absolute_uri(
        reverse('verify_email', args=[user.id, token])
    )

    send_gmail(
        user.email,
        "Verify your account",
        f"Click this link to verify your account:\n{link}"
    )
User=get_user_model()
def verify_email_view(request, user_id, token):
    user = get_object_or_404(User, id=user_id)

    if default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        return HttpResponse("Email verified successfully ✅")
    else:
        return HttpResponse("Invalid or expired link ❌")
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()  # ✅ user is created here

            # ✅ NOW you can check verification
            if not user.is_verified:
                return HttpResponse("Please verify your email first.")

            login(request, user)

            # ROLE REDIRECTION
            if user.role == "owner":
                return redirect("owner_dashboard")

            elif user.role == "admin":
                return redirect("admin_dashboard")

            elif user.role == "driver":
                return redirect("driver_dashboard")

            else:
                return redirect("home")

    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})

def test_email_view(request):

    import os
    print("EMAIL:", os.environ.get("EMAIL_HOST_USER"))
    print("PASSWORD:", os.environ.get("EMAIL_HOST_PASSWORD"))
    from django.core.mail import send_mail
    send_gmail(
        'Test Subject',
        'Hello from Django',
        os.environ.get("EMAIL_HOST_USER"),
        ['utibefrank07@gmail.com'],
        fail_silently=False,
    )
    return  HttpResponse("Email sent!")
    

#@login_required for login protection 
@login_required
@role_required(allowed_roles=["driver"])#middleware protection
def driver_dashboard_view(request):

    user = request.user

    if user.role!="driver":
        return HttpResponseForbidden("Access Denied")
    application = DriverApplication.objects.filter(driver=user).order_by("created_at").first()

    context ={
        "application":application
    }
    return render(request,"accounts/driver_dashboard.html", context)



@login_required
def driver_profile_view(request):
    user= request.user

    if user.role!= "driver":
        return HttpResponseForbidden(
            'only driver allowed.'
        )
    
  # Get or create profile
    profile, created = Driverprofile.objects.get_or_create(
        user=user
    )

    context = {

        "user": user,
        "profile": profile,

    }

    return render(
        request,
        "accounts/driver_profile.html",
        context
    )
@login_required
def driver_profile_update_view(request):
    user =request.user

    if user.role !="driver":
        return HttpResponseForbidden("only driver allowed")
    profile, created = Driverprofile.objects.get_or_create(
        user=request.user
    )

    if request.method=="POST":
        form =DriverprofileForm(
            request.POST,
            request.FILES,
            instance=profile
    )
        if form.is_valid():

            form.save()
            return redirect("driver_profile")
    else:
        form= DriverprofileForm(instance=profile)
    
    return render(

        request,
        "accounts/driver_profile_update.html",{"form":form}
    )  


  
    
@login_required
def driver_application_view(request):

    user = request.user

    # Only drivers allowed
    if user.role != "driver":
        return HttpResponseForbidden(
            "Only Drivers can Apply. You are not signed up as a Driver."
        )

    # Prevent multiple pending applications from one driver 
    active_application = DriverApplication.objects.filter(
        driver=user,
        status="pending"
    ).first()

    if active_application:
        return render(
            request,
            "accounts/already_applied.html"
        )

    # Handle form submission
    if request.method == "POST":

        form = DriverApplicationForm(request.POST)

        if form.is_valid():

            application = form.save(commit=False)

            application.driver = user

            application.save()
            messages.success(
                request, "your application has been submitted successfully."
            )

            return redirect("driver_dashboard")

    else:
        form = DriverApplicationForm()
        messages.error(request, "you already have a pending application.")

    return render(
        request,
        "accounts/driver_application.html",
        {"form": form}
    )

# rendering bus assigned to a particular driver
def driver_assigned_bus_view(request):
    driver = Driverprofile.objects.get(user=request.user)
    bus = Bus.objects.filter(driver=driver).first()

    return render(request, "accounts/driver_assigned_bus.html", {
        'bus':bus
    })

@login_required
@role_required(allowed_roles=["owner"]) #middleware protection
def owner_dashboard_view(request):

    buses =Bus.objects.filter(owner=request.user)

    return render(request,'accounts/owner_dashboard.html',
                  {
                  "buses":buses    

                  }
    )


@login_required
def register_bus_view(request):
    if request.user.role !="owner":
        return HttpResponseForbidden()
    
    if request.method =="POST":
        form =BusForm(request.POST, request.FILES)

        if form.is_valid():
            bus = form.save(commit=False)
            bus.owner = request.user
            bus.status ="pending"
            bus.save()
            return redirect("owner_dashboard")
        
    else:
        form=BusForm()
    return render(request, "accounts/register_bus.html", {"form":form}
    )

def update_bus_view(request,bus_id):
    bus= Bus.objects.get(id=bus_id, owner=request.user)
    #ensures owner can edit their own bus
    if request.method=="POST":
        form =BusForm(
           request.POST,
           request.FILES,
           instance=bus
)
        if form.is_valid():
            form.save()
            return redirect('owner_dashboard')
        

    else:
        form =BusForm(instance=bus)

    return render(  request, "accounts/update_bus.html",{ 
      
            'form':form,
            'bus':bus
    })
           
        
    








 
@login_required
@role_required(allowed_roles=["admin"])#middleware protection 
def admin_dashboard_view(request):
    if request.user.role !="admin":
        return HttpResponseForbidden("you're forbidden to use this Url ")
   
    total_drivers = Driverprofile.objects.count()
    pending_applications =DriverApplication.objects.filter(status="pending").count()
    total_buses =Bus.objects.count()
    approved_buses =Bus.objects.filter(status="approved").count()
    rejected_buses =Bus.objects.filter(status="reject").count()

    context ={
        "total_drivers":total_drivers,
        "pending_applications":pending_applications,
        "total_buses":total_buses,
        "approved_buses":approved_buses,
        "rejected_buses":rejected_buses,
    }
    return render(
        request, "accounts/admin_dashboard.html",
        context
    )

def admin_driver_applications_view(request):
    applications = DriverApplication.objects.all()
    context={
        "applications":applications

    }   
    return render(request, "accounts/admin_driver_applications.html", context)  

    # search function  
def admin_bus_management_view(request):
    buses=Bus.objects.all()
    query = request.GET.get("q")
    if query:
        buses = buses.filter(
            Q(vehicle_name__icontains=query)|
            Q(plate_no__icontains=query)|
            Q(driver__user__username__icontains=query)
            
        )
    drivers =Driverprofile.objects.all()
    status =request.GET.get("status")
    if status:
        buses =buses.filter(status=status)

    context={
        "buses":buses,
        "drivers":drivers,
    }  
    return render(request, "accounts/admin_bus_management.html", context)
@login_required
def approve_bus_view(request, id):
    if request.user.role !="admin":
        return HttpResponseForbidden()
    bus = Bus.objects.get(id=id)
    bus.status="approved"
    bus.save()
    return redirect("admin_dashboard")

@login_required
def reject_bus_view(request, id):
    if request.user.role !="admin":
        return HttpResponseForbidden()
    bus = Bus.objects.get(id=id)
    bus.status="reject"
    bus.save()
    return redirect("admin_dashboard")





@login_required
def approve_application_view(request,id):

    if request.user.role != "admin":

        return HttpResponseForbidden()

    application = DriverApplication.objects.get(id=id)

    application.status="approved"

    application.save()

    return redirect("admin_dashboard")



@login_required
def reject_application_view(request,id):

    if request.user.role != "admin":

        return HttpResponseForbidden()

    application = DriverApplication.objects.get(id=id)

    application.status="rejected"

    application.save()

    return redirect("admin_dashboard")

def assign_driver_view(request, bus_id):
   
   if request.method =="POST":
       
         driver_id =request.POST.get("driver_id")
         driver =get_object_or_404(Driverprofile, id=driver_id)
         bus =get_object_or_404(Bus, id=bus_id)
        
         bus.driver =driver
         bus.save()

   return redirect("admin_dashboard")









def delete_bus_view(request, bus_id):
    bus =Bus.objects.get(id=bus_id)
    bus.delete()
    return redirect("bus_management")







def logout_view(request):

    logout(request)

    return redirect("login")

