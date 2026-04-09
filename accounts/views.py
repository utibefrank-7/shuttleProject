import uuid

from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.contrib.auth import logout
from django.http import HttpResponseForbidden, HttpResponse
from .models import Driverprofile, DriverApplication, Bus
from .forms import DriverprofileForm, DriverApplicationForm, BusForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .gmail_service import send_gmail
from django.contrib.auth import get_user_model
from .utils import send_verification_email
from django.utils import timezone
from datetime import timedelta
from .models import ComplaintMessage, ComplaintTicket


# Create your views here.
def home_view(request):
    return render(request, "accounts/home.html")


def about_view(request):
    return render(request, "accounts/About.html")


def features_view(request):
    return render(request, "accounts/features.html")


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # Ensure user is not verified
            user.is_verified = False
            user.is_active = False
            user.token_created = timezone.now()
            user.save()

            send_verification_email(request, user)

            return render(request, "accounts/email_sent.html", {'email': user.email})

    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


User = get_user_model()


def verify_email_view(request, token):
    try:
        uuid.UUID(str(token))

    except ValueError:
        return HttpResponse('Invalid verification link', status=400)

    user = get_object_or_404(User, verification_token=token)

    expiry_time = user.token_created_at + timedelta(minutes=3)
    if timezone.now() > expiry_time:
        return HttpResponse(
            "Your verification link has expired. It is only valid for 3 minutes. Please request a new one.",
            status=410
        )

    if user.is_verified:
        messages.info(request, 'Account already verified. Please login.')
        return redirect('login')

    user.is_verified = True
    user.is_active = True
    user.save()

    messages.success(request, 'Email verified! You can now log in.')
    return redirect('login')


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()  # ✅ user is created here

            # ✅ NOW you can check verification
            if not user.is_verified:
                return render(request, "accounts/email_sent.html", {'email': user.email})

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
        'utibefrank07@gmail.com',
        'Test Subject',
        'Hello from Django'
    )

    return HttpResponse("Email sent!")


#resending verification testing


def resend_verification_view(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
            return redirect('resend-verification')

        # If already verified no need to resend
        if user.is_verified:
            messages.info(request, "Your account is already verified. Please login.")
            return redirect('login')

        # Generate a fresh token and reset the timer
        user.verification_token = uuid.uuid4()
        user.token_created_at = timezone.now()
        user.save()

        send_verification_email(request, user)

        messages.success(request, "A new verification email has been sent. You have 3 minutes to verify.")
        return redirect('resend-verification')

    return render(request, "accounts/resend_verification.html")


#@login_required for login protection
@login_required
@role_required(allowed_roles=["driver"])  #middleware protection
def driver_dashboard_view(request):
    user = request.user

    if user.role != "driver":
        return HttpResponseForbidden("Access Denied")
    application = DriverApplication.objects.filter(driver=user).order_by("created_at").first()

    context = {
        "application": application
    }
    return render(request, "accounts/driver_dashboard.html", context)


@login_required
def driver_profile_view(request):
    user = request.user

    if user.role != "driver":
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
    user = request.user

    if user.role != "driver":
        return HttpResponseForbidden("only driver allowed")
    profile, created = Driverprofile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = DriverprofileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            form.save()
            return redirect("driver_profile")
    else:
        form = DriverprofileForm(instance=profile)

    return render(

        request,
        "accounts/driver_profile_update.html", {"form": form}
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
        'bus': bus
    })


@login_required
@role_required(allowed_roles=["owner"])  #middleware protection
def owner_dashboard_view(request):
    buses = Bus.objects.filter(owner=request.user)

    return render(request, 'accounts/owner_dashboard.html',
                  {
                      "buses": buses

                  }
                  )


@login_required
def register_bus_view(request):
    if request.user.role != "owner":
        return HttpResponseForbidden()

    if request.method == "POST":
        form = BusForm(request.POST, request.FILES)

        if form.is_valid():
            bus = form.save(commit=False)
            bus.owner = request.user
            bus.status = "pending"
            bus.save()
            return redirect("owner_dashboard")

    else:
        form = BusForm()
    return render(request, "accounts/register_bus.html", {"form": form}
                  )


def update_bus_view(request, bus_id):
    bus = Bus.objects.get(id=bus_id, owner=request.user)
    #ensures owner can edit their own bus
    if request.method == "POST":
        form = BusForm(
            request.POST,
            request.FILES,
            instance=bus
        )
        if form.is_valid():
            form.save()
            return redirect('owner_dashboard')


    else:
        form = BusForm(instance=bus)

    return render(request, "accounts/update_bus.html", {

        'form': form,
        'bus': bus
    })


@login_required
@role_required(allowed_roles=["admin"])  #middleware protection
def admin_dashboard_view(request):
    if request.user.role != "admin":
        return HttpResponseForbidden("you're forbidden to use this Url ")

    total_drivers = Driverprofile.objects.count()
    pending_applications = DriverApplication.objects.filter(status="pending").count()
    total_buses = Bus.objects.count()
    approved_buses = Bus.objects.filter(status="approved").count()
    rejected_buses = Bus.objects.filter(status="reject").count()

    context = {
        "total_drivers": total_drivers,
        "pending_applications": pending_applications,
        "total_buses": total_buses,
        "approved_buses": approved_buses,
        "rejected_buses": rejected_buses,
    }
    return render(
        request, "accounts/admin_dashboard.html",
        context
    )


def admin_driver_applications_view(request):
    applications = DriverApplication.objects.all()
    context = {
        "applications": applications

    }
    return render(request, "accounts/admin_driver_applications.html", context)

    # search function  


def admin_bus_management_view(request):
    buses = Bus.objects.all()
    query = request.GET.get("q")
    if query:
        buses = buses.filter(
            Q(vehicle_name__icontains=query) |
            Q(plate_no__icontains=query) |
            Q(driver__user__username__icontains=query)

        )
    drivers = Driverprofile.objects.all()
    status = request.GET.get("status")
    if status:
        buses = buses.filter(status=status)

    context = {
        "buses": buses,
        "drivers": drivers,
    }
    return render(request, "accounts/admin_bus_management.html", context)


@login_required
def approve_bus_view(request, id):
    if request.user.role != "admin":
        return HttpResponseForbidden()
    bus = Bus.objects.get(id=id)
    bus.status = "approved"
    bus.save()
    return redirect("admin_dashboard")


@login_required
def reject_bus_view(request, id):
    if request.user.role != "admin":
        return HttpResponseForbidden()
    bus = Bus.objects.get(id=id)
    bus.status = "reject"
    bus.save()
    return redirect("admin_dashboard")


@login_required
def approve_application_view(request, id):
    if request.user.role != "admin":
        return HttpResponseForbidden()

    application = DriverApplication.objects.get(id=id)

    application.status = "approved"

    application.save()

    return redirect("admin_dashboard")


@login_required
def reject_application_view(request, id):
    if request.user.role != "admin":
        return HttpResponseForbidden()

    application = DriverApplication.objects.get(id=id)

    application.status = "rejected"

    application.save()

    return redirect("admin_dashboard")


def assign_driver_view(request, bus_id):
    if request.method == "POST":
        driver_id = request.POST.get("driver_id")
        driver = get_object_or_404(Driverprofile, id=driver_id)
        bus = get_object_or_404(Bus, id=bus_id)

        bus.driver = driver
        bus.save()

    return redirect("admin_dashboard")


def delete_bus_view(request, bus_id):
    bus = Bus.objects.get(id=bus_id)
    bus.delete()
    return redirect("bus_management")


@login_required(login_url="login")
def create_ticket_view(request):
    if request.method == "POST":
        subject = request.POST.get("subject")

        if not subject:
            messages.error(request, "Please provide a subject")
            return redirect("create_ticket")

        ticket = ComplaintTicket.objects.create(
            user=request.user,
            subject=subject
        )
        return redirect("ticket_detail", ticket_id=ticket.id)

    return render(request, 'accounts/create_ticket.html')


@login_required(login_url='login')
def all_tickets_view(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('home')

    tickets = ComplaintTicket.objects.all().order_by('-created_at')
    context = {
        'tickets': tickets  # ✅ key must be a string
    }
    return render(request, 'accounts/all_tickets.html', context)  # ✅ template name


#Admin sees all tickets
def ticket_detail_view(request, ticket_id):
    ticket = get_object_or_404(ComplaintTicket, id=ticket_id)

    if request.user != ticket.user and request.user.role != "admin":
        messages.error(request, "Access denied.")
        return redirect("home")

    messages_qs = ComplaintMessage.objects.filter(ticket=ticket).order_by('timestamp')

    # Handle file attachment via POST
    if request.method == "POST":
        message_text = request.POST.get('message', '')
        attachment = request.FILES.get('attachment')

        if message_text or attachment:
            ComplaintMessage.objects.create(
                ticket=ticket,
                sender=request.user,
                message=message_text,
                attachment=attachment
            )
        return redirect("ticket-detail", ticket_id=ticket.id)

    return render(request, 'accounts/ticket_detail.html', {
        'ticket': ticket,
        'messages': messages_qs,
    })


#Admin closes a ticket
@login_required(login_url='login')
def close_ticket_view(request, ticket_id):
    if request.user.role != "admin":
        messages.error(request, "Access denied.")
        return redirect("home")

    ticket = get_object_or_404(ComplaintTicket, id=ticket_id)
    ticket.status = "closed"
    ticket.save()
    messages.success(request, "Ticket closed successfully")
    return redirect("all-tickets")


def logout_view(request):
    logout(request)

    return redirect("login")
