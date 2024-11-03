from django.shortcuts import render, redirect
from django.contrib import messages
from pymongo import MongoClient
import hashlib
from django.conf import settings  # Access SALT_KEY from settings
from django.contrib.auth import logout
from django.views import View
import random
import os
import smtplib
from email.mime.text import MIMEText
import pytz
from datetime import datetime
from decouple import config
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from pytz import timezone as pytz_timezone  # To handle time zone conversion
from django.urls import reverse

from dancoinvoice.settings import SESSION_COOKIE_AGE



client = MongoClient(settings.MONGO_DB_URI)
db = client.get_database()
users_collection = db['tbl_users']
forgot_otp_collection = db['tbl_forgot_password_otp']

def hash_password(password):
    """Hashes a password using the salt key from settings."""
    salted_password = settings.SALT_KEY + password  # Use SALT_KEY from settings
    return hashlib.sha256(salted_password.encode()).hexdigest()

def check_user_credentials(username, raw_password):
    """Checks the user's credentials against the MongoDB database."""
    user = users_collection.find_one({ "UserName": username })
    if not user:
        return False  # User does not exist

    stored_password = user.get('Password')
    hashed_password = hash_password(raw_password)
    return stored_password == hashed_password

def get_current_ist_time():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)



def login_view(request):
    print("______________________________________________________________")
    message_list = []
    if 'remember_me' in request.session:
        email = request.session.get('email')
        password = request.session.get('password')
        remember_me = request.session.get('remember_me')
    else:
        email = ""
        password = ""
        remember_me = ""
    
    if request.method == 'POST':
        print(request.method)
        email = request.POST['email']
        password = request.POST['password']
        remember_me = request.POST.get('rememberMe', 'off')

        if check_user_credentials(email, password):
            print("###########################################")
            print(email)
            request.session['user_id'] = users_collection.find_one({
                "UserName": email,
                "IsDeleted": 0,
                "IsBlock": 0
            })['UserId']            
            request.session['email'] = email
            request.session['last_login'] = timezone.now().isoformat()  # Store the current time as the last login time

            if remember_me == 'on':
                request.session['password'] = password  # Optionally store hashed password
                request.session['remember_me'] = remember_me
                request.session.set_expiry(SESSION_COOKIE_AGE)  # Set session expiry to 8 hours

                print(request.session)
                # Optionally, set the session expiration for 'Remember Me' (8 hours in this case)
                #request.session.set_expiry(28800)
            else:
                # Clear stored login details if 'Remember Me' is not checked
                request.session.pop('password', None)
                request.session.pop('remember_me', None)
                request.session.set_expiry(0)  # Session expires when the browser is closed

            quotation_main_url = reverse('quotation')  # 'dashboard' is the name of the URL pattern
            return redirect(quotation_main_url)
        else: 
            messages.error(request, 'Invalid username or password. Please enter valid credentials!')
    # Pass the remembered login details to the template
    context = {
        'email': email,
        'password': password,
        'remember_me': remember_me,
        'messages': [{'message': message.message, 'tags': message.tags} for message in messages.get_messages(request)]

    }
    print(context)
    return render(request, 'users/login.html', context)

def logout_view(request):
    logout(request)
    request.session.flush()  # Clear the session completely
    return redirect('login')


def forgotCheck_view(request):
    message_list = []  # Initialize an empty list to store messages

    return render(request,'users/forgot.html',{'messages': message_list})


# def check_user_forget(request):
#     """Handles GET and POST requests for the forgot password functionality."""
#     #template_name = 'users/forgot.html'

#     if request.method == 'POST':
#         print("-----------------------------------------------------------------------------------------------")
#         print(request.POST)
#         message_list = []

#         email = request.POST.get('check-forgot-email')
        
#         # Find the user in the MongoDB collection
#         user = users_collection.find_one({"UserName": email})
#         print(user)

#         if user:
#             # Check if the user is deleted
#             if user.get('IsDeleted'):
#                 messages.error(request, 'User is deleted. Cannot reset the password.')
#             # Check if the user is blocked
#             elif user.get('IsBlocked'):
#                 messages.error(request, 'User is blocked. Cannot reset the password.')
#             else:
#                 print("------------------------------------------------------------------------------------------")
#                 otp = generate_otp()
#                 print(otp)
                
#                 # Send OTP to the user's email
#                 try:
#                     print("#############################################################################")
#                     #send_otp_email(email, otp)
#                     print("#############################################################################")
#                     #messages.success(request, 'Password reset instructions have been sent to your email.')


#                     # Insert OTP record into the MongoDB collection
#                     insert_forgot_password_otp(email, otp)
#                     messages.success(request, 'Password reset instructions have been sent to your email.')
#                     return redirect('forgot_otp_view')  # Replace with the correct name of your URL pattern



#                 except Exception as e:
#                     messages.error(request, f"Error sending email: {str(e)}")
#         else:
#             messages.error(request, 'Invalid username or password')

#     return render(request, 'users/forgot.html')


def check_user_forget(request):
    """Handles GET and POST requests for the forgot password functionality."""
    message_list = []

    # Check if there is an email stored in the session (similar to "Remember Me")
    if 'forgot_email' in request.session:
        email = request.session.get('forgot_email')
    else:
        email = ""
    if request.method == 'POST':
        email = request.POST.get('check-forgot-email')
        
        # Find the user in the MongoDB collection
        user = users_collection.find_one({"UserName": email})

        if user:
            if user.get('IsDeleted'):
                message_list.append({'message': 'User is deleted. Cannot reset the password.', 'tags': 'error'})
            elif user.get('IsBlocked'):
                message_list.append({'message': 'User is blocked. Cannot reset the password.', 'tags': 'error'})
            else:
                otp = generate_otp()
                try:
#                   print("#############################################################################")
#                   #send_otp_email(email, otp)
#                   print("#############################################################################")
#                   #messages.success(request, 'Password reset instructions have been sent to your email.')

#                   # Insert OTP record into the MongoDB collection
                    insert_forgot_password_otp(email, otp)
                    message_list.append({'message': 'Password reset instructions have been sent to your email.', 'tags': 'success'})
                    return redirect('forgot_otp_view')  # Replace with your URL name
                except Exception as e:
                    message_list.append({'message': f"Error sending email: {str(e)}", 'tags': 'error'})
        else:
            message_list.append({'message': 'Invalid username or password', 'tags': 'error'})

    return render(request, 'users/forgot.html', {'messages': message_list})



def check_user_forget(request):
    """Handles GET and POST requests for the forgot password functionality."""
    message_list = []

    # Check if there is an email stored in the session (similar to "Remember Me")
    # if 'forgot_email' in request.session:
    #     email = request.session.get('forgot_email')
    # else:
    #     email = ""
    if request.method == 'POST':
        email = request.POST.get('check-forgot-email')
        request.session['check-forgot-email'] = email
        # Find the user in the MongoDB collection
        user = users_collection.find_one({"UserName": email})

        if user:
            if user.get('IsDeleted'):
                message_list.append({'message': 'User is deleted. Cannot reset the password.', 'tags': 'error'})
            elif user.get('IsBlocked'):
                message_list.append({'message': 'User is blocked. Cannot reset the password.', 'tags': 'error'})
            else:
                otp = generate_otp()
                try:
#                   print("#############################################################################")
#                   #send_otp_email(email, otp)
#                   print("#############################################################################")
#                   #messages.success(request, 'Password reset instructions have been sent to your email.')

#                   # Insert OTP record into the MongoDB collection
                    insert_forgot_password_otp(email, otp)
                    message_list.append({'message': 'Password reset instructions have been sent to your email.', 'tags': 'success'})
                    return redirect('forgot_otp_view')  # Replace with your URL name
                except Exception as e:
                    message_list.append({'message': f"Error sending email: {str(e)}", 'tags': 'error'})
        else:
            message_list.append({'message': 'Invalid username or password', 'tags': 'error'})

    return render(request, 'users/forgot.html', {'messages': message_list})


# Constants for resend logic
MAX_RESEND_ATTEMPTS = 2
RESEND_COOLDOWN_HOURS = 1

def resend_forget_otp(request):
    """Function to resend OTP two times with a 1-hour cooldown period"""
    print("#########################################################################################")
    print(request.POST)
    if 'check-forgot-email' in request.session:
        email = request.session.get('check-forgot-email')
    else:
        email = ""
    if request.method == 'POST':
        email = request.session.get('check-forgot-email')

        # Find the user in the MongoDB collection
        user = users_collection.find_one({"UserName": email})

        if user:
            if user.get('IsDeleted'):
                return JsonResponse({'message': 'User is deleted. Cannot reset the password.', 'tags': 'error'})
            elif user.get('IsBlocked'):
                return JsonResponse({'message': 'User is blocked. Cannot reset the password.', 'tags': 'error'})

            # Retrieve resend count and timestamp from session
            resend_attempts = request.session.get('resend_attempts', 0)
            print(resend_attempts)
            last_resend_time = request.session.get('last_resend_time')

            # Check if it's the first request or check cooldown period
            if last_resend_time:
                last_resend_time = timezone.datetime.fromisoformat(last_resend_time)  # Convert ISO string to datetime object

                # Check if last_resend_time is naive or aware
                if timezone.is_naive(last_resend_time):
                    last_resend_time = timezone.make_aware(last_resend_time)

                # Calculate time difference
                time_diff = timezone.now() - last_resend_time

                # Check if user is in cooldown period
                if resend_attempts >= MAX_RESEND_ATTEMPTS and time_diff < timedelta(hours=RESEND_COOLDOWN_HOURS):
                    return JsonResponse({'message': 'Multiple OTP requests. Please try again after one hour.', 'tags': 'error'})
                elif time_diff >= timedelta(hours=RESEND_COOLDOWN_HOURS):
                    # Reset attempts after cooldown period
                    resend_attempts = 0

            # Proceed with sending OTP
            otp = generate_otp()
            try:
                #print("#############################################################################")
#               #send_otp_email(email, otp)
#               print("#############################################################################")
#               #messages.success(request, 'Password reset instructions have been sent to your email.')
                # send_otp_email(email, otp)  # Uncomment to actually send the email
                insert_forgot_password_otp(email, otp)  # Insert OTP record into MongoDB
                
                # Update session with the new resend attempt count and timestamp
                request.session['resend_attempts'] = resend_attempts + 1
                request.session['last_resend_time'] = timezone.now().isoformat()  # Store timestamp as ISO format

                return JsonResponse({'message': 'Password reset instructions have been sent to your email.', 'tags': 'success'})
            
            except Exception as e:
                return JsonResponse({'message': f"Error sending email: {str(e)}", 'tags': 'error'})
        else:
            return JsonResponse({'message': 'Invalid username or password', 'tags': 'error'})

    return JsonResponse({'message': 'An unexpected error occurred. Please try again.', 'tags': 'error'})




def generate_otp():
    """Generates a random 6-digit OTP."""
    return random.randint(100000, 999999)

def get_next_forgot_otp_id():
    # Find and increment the forgot_otp_id counter in the counters collection
    counter = db['counters'].find_one_and_update(
        {"_id": "forgot_otp_id"},
        {"$inc": {"sequence_value": 1}},
        return_document=True
    )
    print(counter)
    return counter['sequence_value']


def insert_forgot_password_otp(email, otp):
    current_time = get_current_ist_time()  # Get current IST time
    print("-----------------------------------------------------------------------")
    print(current_time)
    forgot_otp_id = get_next_forgot_otp_id()  # Get the next auto-incremented ID
    print(forgot_otp_id)
    
    forgot_otp_document = {
        "forgot_otp_id": forgot_otp_id,
        "email": email,
        "otp": otp,
        "is_active": True,
        "created_by": email,
        "created_at": current_time,
        "updated_at": current_time,
        "updated_by": email,
        "is_deleted": False
    }
    print(forgot_otp_document)
    # Insert the document into the collection
    print(forgot_otp_collection.insert_one(forgot_otp_document))


def send_otp_email(recipient_email, otp):
    """Sends the OTP to the user's email."""
    
    try:

        subject = "Your OTP for Password Reset"
        body = f"Your OTP for password reset is: {otp}. Please use this to reset your password."

        smtp_server = config('SMTP_SERVER')
        smtp_port = config('SMTP_PORT', cast=int)
        smtp_username = config('SMTP_USERNAME')
        smtp_password = config('SMTP_PASSWORD')

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = smtp_username
        msg['To'] = recipient_email

        print(smtp_username)
        print(smtp_password)
        

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            print("Logging in to the SMTP server...")
            server.login(smtp_username, smtp_password)
            print(f"Sending email to {recipient_email}...")
            server.sendmail(smtp_username, recipient_email, msg.as_string())
            print(f"Email sent successfully to {recipient_email}")


    except Exception as e:
        print(f"Failed to send OTP email to {recipient_email}. Error: {str(e)}")


def forgot_otp_view(request):
    message_list = []
    return render(request, 'users/forgot_otp_code.html', {'messages': message_list})


def check_forgot_password_otp(request):
    print("--------------------------------------------------------------------------------------------")
    print(request.POST)
    message_list = []

    if 'check-forgot-email' in request.session:
        email = request.session.get('check-forgot-email')
    else:
        email = ""
    if request.method == 'POST' and email != "":
        # Combine all the code inputs into a single string to form the complete OTP
        otp_code = ''.join([request.POST.get(f'code{i}', '') for i in range(1, 7)])
        if otp_code:
            otp_code = int(otp_code)
        print(email)
        print(otp_code)

        # Find the OTP record for the given email and OTP
        otp_record = forgot_otp_collection.find_one({"otp": otp_code, "email": email})
        print(otp_record)
        # Check if the OTP exists
        if otp_record:
            # Check if the OTP is active
            print("############################################################")
            if not otp_record.get('is_active', True):
                message_list.append({'message': 'Wrong OTP, please enter a valid OTP.', 'tags': 'error'})
            # Check if the OTP has expired (created more than 1 hour ago)
            print("###########################################################")
            created_at = otp_record.get('created_at')
            if created_at:

                if created_at.tzinfo is None:
                    created_at = timezone.make_aware(created_at)  # Make aware without specifying timezone
                current_time_ist = get_current_ist_time()

                # Calculate the time difference
                time_difference = current_time_ist - created_at

                # Check if the difference is more than 1 hour
                if time_difference > timedelta(hours=1):
                    print("###################################################################################")
                    message_list.append({'message': 'OTP expired. Please request a new one.', 'tags': 'error'})

            # OTP is valid, proceed with redirect to another view
            return redirect('forgot_change_password_view')  # Redirect to another view (e.g., password reset page)
        else:
            # OTP does not exist or is incorrect
            message_list.append({'message': 'Unable to verify otp!', 'tags': 'error'})

    # If not POST or no email found in session
    message_list.append({'message': 'An unexpected error occurred. Please try again.', 'tags': 'error'})
    return render(request, 'users/forgot_otp_code.html', {'messages': message_list})



def forgot_change_password_view(request):
    message_list = []
    return render(request, 'users/newpass.html', {'messages': message_list})


def forgot_password_change(request):
    message_list = []
    if 'check-forgot-email' in request.session:
        email = request.session.get('check-forgot-email')
    else:
        email = ""
    if request.method == 'POST' and email != "":
        newpswd = request.POST.get('new-password')
        cnfmpswd = request.POST.get('confirm-password')
        if newpswd == cnfmpswd:
            password = hash_password(newpswd)
            try:
                users_collection.update_one(
                    {"UserName": email},
                    {"$set": {"Password": password}}
                )
                message_list.append({'message': 'Password updated successfully!', 'tags': 'success'})
            except Exception as e:
                message_list.append({'message': 'Unable to change password. Please try again.', 'tags': 'error'})
        else:
            message_list.append({'message': 'Password and confirm password match!', 'tags': 'error'})

    else:
        # OTP does not exist or is incorrect
        message_list.append({'message': 'Unable to change password!', 'tags': 'error'})
    return render(request, 'users/newpass.html', {'messages': message_list})



def reset_view(request):
    message_list = []  # Initialize an empty list for messages
    print("_______________________________________________________________________________________")
    # Check if the user is logged in and session has not expired
    last_login = request.session.get('last_login')
    if last_login:
        # Convert last_login to a datetime object
        last_login_dt = datetime.fromisoformat(last_login)
        # Check if the session has expired (8 hours)
        if timezone.now() >= last_login_dt + timedelta(hours=8):

            message_list.append({'message': 'Session expired, please log in again.', 'tags': 'error'})
            return redirect('login')  # Redirect to login page if session has expired
    return render(request, 'users/reset.html', {'messages': message_list})



def check_old_password(request):
    print(request.POST)
    message_list = []
    email = request.session.get('email')
    old_password = request.POST.get('old_password')
    if request.method == 'POST' and old_password and email:
        
        hashed_old_password = hash_password(old_password)
        user_record = users_collection.find_one({"UserName": email})
        print(email)
        print(user_record)
        # Check if the OTP exists
        if user_record:
            # Check if the hashed password matches the stored password in the user record
            stored_password = user_record.get('Password')  # Assuming the hashed password is stored in 'password' field
            print(stored_password)
            print(hashed_old_password)
            if hashed_old_password == stored_password:
                return JsonResponse({'message': 'Old password is correct', 'tags': 'success'})

            else:
                return JsonResponse({'message': 'Please enter the correct old password.', 'tags': 'error'})

        else:
            return JsonResponse({'message': 'User not found.', 'tags': 'error'})
    return JsonResponse({'message': 'An unexpected error occurred. Please try again.', 'tags': 'error'})


def reset_password_change(request):
    print("------------------------------------------------------------------------")
    print(request.POST)

    
    message_list = []
    email = request.session.get('email')
    userId = request.session.get('user_id')
    old_Password = request.POST.get('reset-old-password')
    new_Password = request.POST.get('reset-new-password')
    cnfmNew_Password = request.POST.get('reset-cnfm-new-password')
    if request.method == 'POST' and email and old_Password:
        # Hash the old password
        hashed_old_password = hash_password(old_Password)

        # Find the user by email
        user_record = users_collection.find_one({"UserName": email})
        print("########################################################################")
        print(user_record)

        if user_record:
            # Check if the hashed old password matches the stored password
            stored_password = user_record.get('Password')

            if hashed_old_password == stored_password:
                # Check if new password and confirm password match
                if new_Password == cnfmNew_Password:
                    # Hash the new password before storing it
                    try:
                        hashed_new_password = hash_password(new_Password)
                        users_collection.update_one(
                            {"UserName": email},
                            {"$set": {"Password": hashed_new_password, "UpdatedAt": timezone.now().isoformat(), "UpdatedBy": userId}}
                        )
                        message_list.append({'message': 'Password updated successfully!', 'tags': 'success'})
                    except Exception as e:
                        message_list.append({'message': 'Unable to change password. Please try again.', 'tags': 'error'})
                else:
                    # New password and confirm password do not match
                    message_list.append({'message': 'New password and confirm password do not match.', 'tags': 'error'})

            else:
                # Old password is incorrect
                message_list.append({'message': 'Please enter the correct old password.', 'tags': 'error'})

        else:
            # User not found
            message_list.append({'message': 'An unexpected error occurred. Please try again.', 'tags': 'error'})
    return render(request, 'users/reset.html', {'messages': message_list})















def dashboard_view(request):
    return render(request, 'users/dashboard.html')