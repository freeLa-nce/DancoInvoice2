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

from Product.views import get_current_ist_time  # Import datetime class directly



client = MongoClient(settings.MONGO_DB_URI)
db = client.get_database()
users_collection = db['users']
product_collection = db['tbl_product']
quotation_collection = db['tbl_quotation']


def quotation_view(request):
    message_list = []  # Initialize an empty list to store messages

    return render(request, 'quotation/quotation.html',{'messages': message_list})


def search_items(request):
    if request.method == "GET":
        print("###################################################################33")
        print(request.GET)
        term = request.GET.get('term', '')
        print(term)
        # Use MongoDB regex to perform a "like" search for ProductName
        products = product_collection.find(
            {
            "ProductName": {"$regex": term, "$options": "i"},  # Case-insensitive search
            "IsDeleted": 0,
            "Quantity": {"$ne": 0}  # Filter where IsDeleted is 0
            },  # Case-insensitive search
            {"ProductId": 1, "ProductName": 1, "Quantity": 1, "UnitPrice": 1}  # Select only these fields
        ).limit(10)
        
        
        print(products)
        # Format the results for the AJAX response
        results = [
            {
                "id": product["ProductId"],
                "text": product["ProductName"],
                "quantity": product["Quantity"],
                "price": product["UnitPrice"]
            }
            for product in products
        ]

        print(results)
        
        return JsonResponse(results, safe=False)


@csrf_exempt
def update_product_quantity(request):
    print("----------------------------------------------------------")
    if request.method == 'POST':
        print(request.POST)
        data = json.loads(request.body)
        print(data)
        products = data.get('products', [])

        # Loop through each product to update its quantity in the collection
        for product in products:
            print(product)
            product_name = product['name']
            quantity_to_reduce = product['quantity']

            # Find the product in the collection and update its quantity
            result = product_collection.find_one({'ProductName': product_name})
            print(result)
            if result:
                new_quantity = max(0, result['Quantity'] - quantity_to_reduce)
                print(new_quantity)
                product_collection.update_one(
                    {'ProductName': product_name},
                    {'$set': {'Quantity': new_quantity}}
                )
            else:
                return JsonResponse({'success': False, 'message': f'Product "{product_name}" not found'})

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    

@csrf_exempt
def save_quotation(request):
    print("----------------------------------------------------------")
    if request.method == 'POST':
        print(request.POST)
        data = json.loads(request.body)
        print(data)
        products = data.get('products', [])
        totalAmount = data.get('totalAmount',0)
        invoiceDate = data.get('invoiceDate',0)
        userId = request.session.get('user_id')

        try:
            # Loop through each product to update its quantity in the collection
            for product in products:
                print(product)
                product_name = product['name']
                quantity = product['quantity']
                amount = product['amount']
                
                # Get the next Productid automatically
                last_quotation = quotation_collection.find_one(sort=[("Qutationid", -1)])  # Find the last inserted product
                print(last_quotation)
                new_quotation_id = last_quotation['Qutationid'] + 1 if last_quotation else 1  # Increment the Productid
                print(new_quotation_id)

                print("___________________________________________________________________")
                # Create the product data to insert
                quotation_data = {
                    "Qutationid": new_quotation_id,
                    "InvoiceDate": invoiceDate,
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
                print(quotation_data)

                print("_______________________________________________")
                # Insert the new product into the collection
                print(quotation_collection.insert_one(quotation_data))
                print("----------------------------------------------")

                # Return success response
                return JsonResponse({'message': 'Quotation created successfully', 'tags': 'success'})

        except Exception as e:
            print(f"An error occurred: {e}")
            # Handle any errors that occur
            return JsonResponse({'message': 'Unable to create quotation!', 'tags': 'error'})

    # If the request method is not POST, return an error response
    return JsonResponse({'message': 'Unable to proccess request. Please Contact Administrator!', 'tags': 'error'})

def generate_qr_code(request):
    # URL that the QR code will point to (handle QR scan at this endpoint)
    qr_data = request.build_absolute_uri('/scan_qr/')

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill='black', back_color='white')

    # Prepare the HTTP response to return the QR code as an image
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


def scan_qr(request):
    # This view is triggered when the QR code is scanned
    # You can show a message and also provide a dummy PDF download link
    return render(request, 'quotation_qr_scan_result.html', {'message': 'You have successfully scanned the QR code!'})


def download_dummy_pdf(request):
    # Create a dummy PDF file in memory
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dummy.pdf"'

    # Create PDF content
    p = canvas.Canvas(response)
    p.drawString(100, 750, "This is a dummy PDF file generated from Django.")
    p.showPage()
    p.save()

    return response





