from django.urls import path
from .views import customer_otp_request, customer_otp_verify, staff_login, owner_login, owner_staff_signup
urlpatterns = [
    path('customer/otp/request/', customer_otp_request, name='customer-otp-request'),
    path('customer/otp/verify/', customer_otp_verify, name='customer-otp-verify'),
    path('staff/login/', staff_login, name='staff-login'),              

    path('owner/login/', owner_login, name='owner-login'),
    path('owner-staff/signup/', owner_staff_signup, name='owner-staff-signup'),
]