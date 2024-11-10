from datetime import datetime  # Import datetime class directly
from django.http import JsonResponse
from django.shortcuts import render
from pymongo import MongoClient
from django.conf import settings
import pytz

client = MongoClient(settings.MONGO_DB_URI)
db = client.get_database()
customer_collection = db['tbl_customer_data']

# Create your views here.
def customer_view(request):

    # return render(request, 'product/product.html')
    message_list = []  # Initialize an empty list to store messages

    return render(request,'customerData/customerData.html',{'messages': message_list})


def get_customer_list(request):
    print("---------------------------------------------------------------------------------------------------------")
    print(request.method)
    if request.method == 'GET':
        print("##################################################################################")
        try:
            # Query the MongoDB for all products where IsDeleted = 0
            customer = customer_collection.find({"IsDeleted": 0})
            print(customer)
            # product_list = list(products)
            customer_list = [{**doc, '_id': str(doc['_id'])} for doc in customer]
            print(customer_list)

            return JsonResponse(customer_list, safe=False)
        except Exception as e:
            return JsonResponse({'message': 'Unable to get customer list!', 'tags': 'error'}, status=500, safe=False)


def get_current_ist_time():
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist)

# def add_customer(request):
#     if request.method == 'POST':
#         try:
#             print("_________________________________________________________")
#             print(request.POST)
#             # Extract data from request
#             product_id = request.POST.get('product-Id')
#             product_name = request.POST.get('product-name')
#             quantity = int(request.POST.get('product-quantity'))
#             unit_price = float(request.POST.get('product-unit'))
#             created_by = request.session.get('user_id')  # Assuming 'user_id' is stored in session

#             # Get the next Productid automatically
#             last_product = customer_collection.find_one(sort=[("Productid", -1)])  # Find the last inserted product
#             new_product_id = last_product['Productid'] + 1 if last_product else 1  # Increment the Productid

#             # Create the product data to insert
#             product_data = {
#                 "Productid": new_product_id,
#                 "ProductId": product_id,
#                 "ProductName": product_name,
#                 "Quantity": quantity,
#                 "IsDeleted": 0,
#                 "UnitPrice": unit_price,
#                 "CreatedBy": created_by,
#                 "CreatedAt": get_current_ist_time(),  # Store in ISO format
#                 "UpdatedAt": None,
#                 "UpdatedBy": None,  # Set to the creator for now
#             }
#             print("-------------------------------------------------------")
#             print(product_data)

#             print("_______________________________________________")
#             # Insert the new product into the collection
#             print(customer_collection.insert_one(product_data))
#             print("----------------------------------------------")

#             # Return success response
#             return JsonResponse({'message': 'Product added successfully', 'tags': 'success'})

#         except Exception as e:
#             print(f"An error occurred: {e}")
#             # Handle any errors that occur
#             return JsonResponse({'message': 'Unable to add product!', 'tags': 'error'})

#     # If the request method is not POST, return an error response
#     return JsonResponse({'message': 'Unable to proccess request. Please Contact Administrator!', 'tags': 'error'})


# def get_customer_by_id(request):
#     print("_____________________________________________________________")
#     print(request)
#     if request.method == 'GET':
#         try:
#             #product_id = request.GET.get('product-Id')
#             product_id = request.GET.get('product-Id')  # Correctly retrieve from request.GET

#             print(f"Requested Product ID: {product_id}")    

#             product = customer_collection.find_one(
#                 {"ProductId": product_id, "IsDeleted": 0},
#                 {"_id": 0, "Productid": 1 ,"ProductId": 1, "ProductName": 1, "Quantity": 1, "UnitPrice": 1}  # Fields to return
#             )

#             print(product)
#             if product:
#                 # If product is found, return the details in the JSON response
#                 return JsonResponse({
#                     'message': 'Product retrieved successfully.',
#                     'tags': 'success',
#                     'product': {
#                         'Productid': product.get('Productid'),
#                         'ProductId': product.get('ProductId'),
#                         'ProductName': product.get('ProductName'),
#                         'Quantity': product.get('Quantity'),
#                         'UnitPrice': product.get('UnitPrice')
#                     }
#                 })
#             else:
#                 # If product is not found or is marked as deleted
#                 return JsonResponse({'message': 'Unable to get product details!', 'tags': 'error'})
                
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             return JsonResponse({'message': 'Unable to get product details!', 'tags': 'error'})
#     return JsonResponse({'message': 'Unable to proccess request. Please Contact Administrator!', 'tags': 'error'})


# def edit_customer_by_id(request):
#     if request.method == 'POST':
#         try:
#             print("_________________________________________________________")
#             print(request.POST)
#             # Extract data from request
#             product_id = request.POST.get('product-id')
#             product_name = request.POST.get('product-name')
#             quantity = int(request.POST.get('product-quantity'))
#             unit_price = float(request.POST.get('product-unit'))
#             updated_by = request.session.get('user_id')  # Assuming 'user_id' is stored in session

#             print("-------------------------------------------------------")
#             result = customer_collection.update_one(
#                 {"ProductId": product_id},      # Find the document with matching ProductId
#                 {"$set": {"ProductName": product_name, 
#                           "Quantity": quantity, 
#                           "UnitPrice": unit_price,
#                           "UpdatedAt": get_current_ist_time(),
#                           "UpdatedBy":  updated_by}}
#             )

#             print(result)
#             print(result.modified_count)

#             if result.modified_count > 0:
#                 return JsonResponse({'message': 'Product updated successfully.', 'tags': 'success'})
#             else:
#                 print("Product not found or already deleted.")
#                 JsonResponse({'message': 'Product not found!', 'tags': 'error'})

#         except Exception as e:
#             print(f"An error occurred: {e}")
#             # Handle any errors that occur
#             return JsonResponse({'message': 'Unable to update product!', 'tags': 'error'})

#     # If the request method is not POST, return an error response
#     return JsonResponse({'message': 'Unable to proccess request. Please Contact Administrator!', 'tags': 'error'})
 
def delete_customer_by_id(request):
    print("_____________________________________________________________")
    if request.method == 'POST':
        print(request.POST)
        try:
            customer_id = int(request.POST.get('customerId'))  # Convert customerId to int
            print(customer_id)
            
            result = customer_collection.update_one(
                {"CustomerId": customer_id},      # Find the document with matching ProductId
                {"$set": {"IsDeleted": 1}}      # Set IsDeleted field to 1
            ) 

            print(result)
            print(result.modified_count)
            if result.modified_count > 0:
                
                return JsonResponse({'message': 'Customer deleted successfully.', 'tags': 'success'})
            else:
                print("Customer not found or already deleted.")
                JsonResponse({'message': 'Customer not found!', 'tags': 'error'})

        except Exception as e:
            print(f"An error occurred: {e}")
            return JsonResponse({'message': 'Unable to delete customer!', 'tags': 'error'})
    return JsonResponse({'message': 'Unable to proccess request. Please Contact Administrator!', 'tags': 'error'})
