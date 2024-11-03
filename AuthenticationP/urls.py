from django.urls import path
from . import views  # Import all views at once


urlpatterns = [
    path('', views.login_view, name='login'),
    path('forgot/', views.forgotCheck_view, name='forgot'),
    path('logout/', views.logout_view, name='logout'),
    path('check_forgot_user/', views.check_user_forget, name='checkUserForgot'),
    path('forgot_otp/',views.forgot_otp_view,name='forgot_otp'),
    path('resend_forgot_otp/', views.resend_forget_otp, name='resend_forget_otp'),
    path('check_forgot_password_otp', views.check_forgot_password_otp, name="check_forgot_password_otp"),
    path('forgot_change_password_view', views.forgot_change_password_view, name="forgot_change_password_view"),
    path('forgot_password_change', views.forgot_password_change,name="forgot_password_change"),
    path('reset-password/', views.reset_view, name='reset_view'),  # Ensure the name is 'reset_view'
    path('check-old-password/', views.check_old_password,name='check_old_password'),
    path('reset_password_change/',views.reset_password_change, name="reset_password_change"),
    path('dashboard/', views.dashboard_view, name='dashboard'),

]
