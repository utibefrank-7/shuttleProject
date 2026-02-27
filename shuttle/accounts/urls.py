from django.urls import path
from .views import signup_view, home_view, login_view, logout_view, driver_dashboard_view, owner_dashboard_view

urlpatterns=[
    path('', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('driver/dashboard/', driver_dashboard_view, name='driver_dashboard'),
    path('owner/dashboard/', owner_dashboard_view, name='owner_dashboard'),
    

]