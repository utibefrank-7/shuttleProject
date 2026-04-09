from django.urls import path
from .views import (signup_view, home_view, login_view,
logout_view, driver_dashboard_view,
owner_dashboard_view, driver_profile_view, driver_profile_update_view,
driver_application_view, admin_dashboard_view,
register_bus_view,approve_bus_view, reject_bus_view,
approve_application_view,reject_application_view, assign_driver_view,
about_view, features_view, admin_driver_applications_view,
admin_bus_management_view,delete_bus_view,driver_assigned_bus_view,
update_bus_view,test_email_view,verify_email_view, resend_verification_view,
ticket_detail_view, create_ticket_view, close_ticket_view,all_tickets_view
)

urlpatterns=[
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('features/', features_view, name='features'),

    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('driver/dashboard/', driver_dashboard_view, name='driver_dashboard'),
    path('driver/profile', driver_profile_view, name='driver_profile'),
    path("driver/profile/update", driver_profile_update_view, name="driver_profile_update"),
    path("driver/bus/application", driver_application_view, name="driver_application"),
    path("driver/assigned/bus/", driver_assigned_bus_view, name="driver_assigned_bus"),


    path('owner/dashboard/', owner_dashboard_view, name='owner_dashboard'),
    path("owner/dashboard/register/bus", register_bus_view, name="register_bus"),
    path('owner/<int:bus_id>/bus/update', update_bus_view, name="update_bus"),
   

     path('admin_dashboard/', admin_dashboard_view, name="admin_dashboard"),
     path('admin_driver/applications', admin_driver_applications_view, name="admin_driver_applications"),

     path('admin_bus/management', admin_bus_management_view, name="bus_management"),
     path('bus/<int:id>/approve', approve_bus_view, name="approve_bus"),
     path('bus/<int:id>/reject', reject_bus_view, name="reject_bus"),

    path("application/<int:id>/approve/",approve_application_view,name="approve_application"),

    path("application/<int:id>/reject/",reject_application_view,name="reject_application"),
    path("admin_bus/delete/<int:bus_id>", delete_bus_view, name="delete_bus"),

    path("assign-driver/<int:bus_id>/", assign_driver_view, name="assign_driver"),

    path('test-email/', test_email_view, name="test_email"),
    path('verify-email/<uuid:token>/',verify_email_view, name='verify-email'),
    path('resend-verification/', resend_verification_view, name='resend-verification'),  # add this

path('tickets/', all_tickets_view, name='all-tickets'),
path('tickets/create/', create_ticket_view, name='create-ticket'),
path('ticket-detail/<int:ticket_id>/', ticket_detail_view, name='ticket-detail'),
path('tickets/<int:ticket_id>/close/', close_ticket_view, name='close-ticket'),
]       
