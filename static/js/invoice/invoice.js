// Function to update the invoice date in the preview section
document.getElementById('invoice-date').addEventListener('change', function () {
    document.getElementById('display-invoice-date').textContent = this.value;
});

// Function to update the invoice number in the preview section
document.getElementById('invoiceNo').addEventListener('input', function () {
    document.getElementById('display-invoice-no').textContent = this.value;
});

// Function to update recipient details in the preview section
function updateRecipientDetails() {
    const recipientName = document.querySelector('input[placeholder="Recipient Name"]').value;
    const streetAddress = document.querySelector('input[placeholder="Street Address"]').value;
    const phoneNumber = document.querySelector('input[placeholder="Phone Number"]').value;

    document.getElementById('display-recipient-name').textContent = recipientName;
    document.getElementById('display-recipient-address').textContent = `${streetAddress}`;
    document.getElementById('display-recipient-phone').textContent = phoneNumber;
}

// Function to update the invoice preview table
function updateInvoiceTable() {
    const rows = document.querySelectorAll('#input-container .row');
    const tableBody = document.getElementById('invoice-table-body');
    tableBody.innerHTML = '';

    rows.forEach(row => {
        const itemDescription = row.querySelector('input[placeholder="Item Description"]').value;
        const itemQuantity = row.querySelector('input[placeholder="Quantity"]').value;
        const itemPrice = row.querySelector('input[placeholder="Price"]').value;
        const total = itemQuantity * itemPrice;

        if (itemDescription && itemQuantity && itemPrice) {
            const newRow = `
                <tr>
                    <td>${itemDescription}</td>
                    <td>${itemQuantity}</td>
                    <td>${itemPrice}</td>
                    <td>${total.toFixed(2)}</td>
                </tr>
            `;
            tableBody.innerHTML += newRow;
        }
    });

    // Update total amount
    let totalAmount = 0;
    document.querySelectorAll('#invoice-table-body tr').forEach(row => {
        totalAmount += parseFloat(row.cells[3].textContent);
    });
    document.getElementById('total-amount').textContent = totalAmount.toFixed(2);
}

// Add a new row of input fields
document.getElementById('add-row-btn').addEventListener('click', function () {
    const newRow = document.createElement('div');
    newRow.className = 'row mb-2';

    newRow.innerHTML = `
        <div class="col-lg-5 mb-2">
  
            <input type="text" class="form-control-2" placeholder="Item Description" required>
        </div>
        <div class="col-lg-3 mb-2">
         
            <input type="number" class="form-control-2" placeholder="Quantity" required>
        </div>
        <div class="col-lg-3 mb-2">
  
            <input type="number" class="form-control-2" placeholder="Price" required>
        </div>
        <div class="col-lg-1 mb-3 d-flex align-items-end">
            <button type="button" class="btn btn-danger btn-sm" onclick="deleteRow(this)">
                <i class="fas fa-trash-alt"></i>
            </button>
        </div>
    `;

    document.getElementById('input-container').appendChild(newRow);
    updateInvoiceTable();
});

// Event listener for input changes
document.getElementById('input-container').addEventListener('input', updateInvoiceTable);
document.querySelectorAll('input[placeholder]').forEach(input => {
    input.addEventListener('input', updateRecipientDetails);
});

// Function to delete a row
function deleteRow(button) {
    button.closest('.row').remove();
    updateInvoiceTable();
}

// Function to print the invoice
document.getElementById("print-invoice").addEventListener("click", function() {
    // Select the invoice section
    var invoiceContent = document.getElementById("invoice-preview").innerHTML;

    // Open a new window for printing
    var printWindow = window.open('', '', 'height=1123,width=794'); // A4 dimensions: height=1123px, width=794px
    
    // Write the HTML of the invoice content into the new window
    printWindow.document.write('<html><head><title>Print Invoice</title>');
    
    // Optional: include Bootstrap for styling (you can replace this with your own styles)
    printWindow.document.write('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">');
    
    // Custom styles for print media to set A4 size and adjust content
    printWindow.document.write(`
        <style>
            @media print {
                @page { size: A4; margin: 10mm; } /* A4 page size */
                body { margin: 0; padding: 10mm; }
                table { width: 100%; border-collapse: collapse; }
                table th, table td { border: 1px solid black; padding: 8px; text-align: left; }
            }
        </style>
    `);
    
    printWindow.document.write('</head><body>');
    printWindow.document.write(invoiceContent); // Insert invoice content
    printWindow.document.write('</body></html>');

    // Close the document to apply the styles
    printWindow.document.close();

    // Wait for the content to load and then print
    printWindow.onload = function() {
        printWindow.print();
        printWindow.close();
    };
});


// Function to handle logout
document.getElementById("logout-btn").addEventListener("click", function () {
    window.location.href = "index.html";
});



