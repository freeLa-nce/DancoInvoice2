from django.shortcuts import render, redirect
from django.contrib import messages
from pymongo import MongoClient
import hashlib
from django.conf import settings  # Access SALT_KEY from settings
import qrcode
from django.http import HttpResponse
from reportlab.pdfgen import canvas


client = MongoClient(settings.MONGO_DB_URI)
db = client.get_database()
users_collection = db['users']


def quotation_view(request):
    message_list = []  # Initialize an empty list to store messages

    return render(request, 'quotation/quotation.html',{'messages': message_list})


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





