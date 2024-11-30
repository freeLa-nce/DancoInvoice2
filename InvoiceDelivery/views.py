from django.shortcuts import render, redirect
from django.contrib import messages
from pymongo import MongoClient
import hashlib
from django.conf import settings  # Access SALT_KEY from settings
import qrcode
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import random
import string
from Product.views import get_current_ist_time  # Import datetime class directly
from django.views.decorators.http import require_POST




client = MongoClient(settings.MONGO_DB_URI)
db = client.get_database()
users_collection = db['users']
product_collection = db['tbl_product']
invoice_collection = db['tbl_invoice']
customer_collection = db['tbl_customer_data']


def generate_invoice_number():
    # Define the length of the invoice number
    length = 10
    # Generate a random alphanumeric string of the defined length
    invoice_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return invoice_number


def invoice_view(request):
    message_list = []  # Initialize an empty list to store messages
    # Generate a random invoice number
    # invoice_number = generate_invoice_number()


    return render(request, 'invoicedelivery/invoicedelivery.html', {
        'messages': message_list
    })


def convert_to_date(date_string, format="%Y-%m-%d"):
    try:
        return datetime.strptime(date_string, format)
    except ValueError as e:
        print(f"Error converting date: {e}")
        return None


@csrf_exempt
def get_invoice_number(request):
    if request.method == 'GET':
        invoice_number = generate_invoice_number()
        return JsonResponse({'invoice_number': invoice_number})
    
@csrf_exempt
def save_invoice(request):
    print("----------------------------------------------------------")
    if request.method == 'POST':
        print(request.POST)
        data = json.loads(request.body)
        print(data)
        products = data.get('products', [])
        totalAmount = data.get('totalAmount',0)
        recieptName = data.get('recipient_name','')
        recieptAdd = data.get('recipient_add','')
        recipientPhone = data.get('recipient_phone',0)
        invoiceNumber = data.get('invoice_number',0)

        invoiceDate = data.get('invoice_date',0)
        userId = request.session.get('user_id')

        try:
            # Loop through each product to update its quantity in the collection
            for product in products:
                print(product)
                product_name = product['name']
                quantity = product['quantity']
                amount = product['amount']
                
                # Get the next Productid automatically
                last_invoice = invoice_collection.find_one(sort=[("InvoiceId", -1)])  # Find the last inserted product
                print(last_invoice)
                new_invoice_id = last_invoice['InvoiceId'] + 1 if last_invoice else 1  # Increment the Productid
                print(new_invoice_id)

                invoice_date = convert_to_date(invoiceDate)

                print("___________________________________________________________________")
                # Create the product data to insert
                invoice_data = {
                    "InvoiceId": new_invoice_id,
                    "InvoiceNumber":invoiceNumber,
                    "CustomerName": recieptName,
                    "CustomerAdd": recieptAdd,
                    "CustomerPhone": recipientPhone,
                    "InvoiceDate": invoice_date,
                    "TotalAmount": totalAmount,
                    "ProductName": product_name,
                    "Quantity": quantity,
                    "Amount": amount,
                    "IsDeleted": 0,
                    "CreatedBy": userId,
                    "CreatedAt": get_current_ist_time(),  # Store in ISO format
                    "UpdatedAt": None,
                    "UpdatedBy": None,  # Set to the creator for now
                }
                print("-------------------------------------------------------")
                print(invoice_data)

                print("_______________________________________________")
                # Insert the new product into the collection
                print(invoice_collection.insert_one(invoice_data))
                print("----------------------------------------------")


                print("############################################################")
                last_customer = customer_collection.find_one(sort=[("CustomerId", -1)])  # Find the last inserted product
                print(last_customer)
                new_customer_id = last_customer['CustomerId'] + 1 if last_customer else 1  # Increment the Productid
                print(new_customer_id)


                #Create the product data to insert
                customer_data = {
                    "CustomerId": new_customer_id,
                    "InvoiceNumber": invoiceNumber,
                    "CustomerName": recieptName,
                    "Address": recieptAdd,
                    "PhoneNumber": recipientPhone,
                    "InvoiceDate": invoice_date,
                    "ProductName": product_name,
                    "Quantity": quantity,
                    "IsDeleted": 0,
                    "Amount": amount,
                    "CreatedBy": userId,
                    "CreatedAt": get_current_ist_time(),  # Store in ISO format
                    "UpdatedAt": None,
                    "UpdatedBy": None,  # Set to the creator for now
                }
                print("-------------------------------------------------------")
                print(customer_data)

                print("_______________________________________________")
                # Insert the new product into the collection
                print(customer_collection.insert_one(customer_data))

                # Return success response
                return JsonResponse({'message': 'Invoice created successfully', 'tags': 'success'})

        except Exception as e:
            print(f"An error occurred: {e}")
            # Handle any errors that occur
            return JsonResponse({'message': 'Unable to create invoice!', 'tags': 'error'})

    # If the request method is not POST, return an error response
    return JsonResponse({'message': 'Unable to proccess request. Please Contact Administrator!', 'tags': 'error'})



@csrf_exempt  # If using CSRF tokens, this might not be needed.

def edit_invoice(request):
    print("####################################################################################")
    print("----------------------------------------------------------------------------------")
    print(request.POST)
    if request.method == 'POST':
        try:
            # Extract 'invoiceNumber' from POST data 
            invoice_number = request.POST.get('invoiceNumber')
            if not invoice_number:
                return JsonResponse({'message': 'Its look like there is an issue with system. Please contact administrator!','tags': 'error'})


            # MongoDB query to find all matching documents and sort
            last_customer = customer_collection.find_one(
                {
                    "InvoiceNumber": invoice_number,  # Match the provided invoice number
                    "isDeleted": 0                    # Ensure the document is not marked as deleted
                }
            )

            print(last_customer)

            # If you want to retrieve all matching documents (not just the last one)
            all_customers = list(customer_collection.find(
                {
                    "InvoiceNumber": invoice_number,
                    "isDeleted": 0
                }
            ))

            print(all_customers)

            # If everything goes well, return a success response
            return JsonResponse({
                'message': 'Invoice edited successfully',
                'tags': 'success'
            })

        except Exception as e:
            # In case of any error, return an error response
            return JsonResponse({
                'message': str(e),
                'tags': 'error'
            })