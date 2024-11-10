// // Function to update the invoice date in the preview section
// document.getElementById('invoice-date').addEventListener('change', function () {
//     document.getElementById('display-invoice-date').textContent = this.value;
// });

// // Function to update the invoice preview table
// function updateInvoiceTable() {
//     const rows = document.querySelectorAll('#input-container .row');
//     const tableBody = document.getElementById('invoice-table-body');
//     tableBody.innerHTML = '';

//     rows.forEach(row => {
//         const itemDescription = row.querySelector('input[placeholder="Item Description"]').value;
//         const itemQuantity = row.querySelector('input[placeholder="Quantity"]').value;
//         const itemPrice = row.querySelector('input[placeholder="Price"]').value;
//         const total = itemQuantity * itemPrice;

//         if (itemDescription && itemQuantity && itemPrice) {
//             const newRow = `
//                 <tr>
//                     <td>${itemDescription}</td>
//                     <td>${itemQuantity}</td>
//                     <td>${itemPrice}</td>
//                     <td>${total.toFixed(2)}</td>
//                 </tr>
//             `;
//             tableBody.innerHTML += newRow;
//         }
//     });

//     // Update total amount
//     let totalAmount = 0;
//     document.querySelectorAll('#invoice-table-body tr').forEach(row => {
//         totalAmount += parseFloat(row.cells[3].textContent);
//     });
//     document.getElementById('total-amount').textContent = totalAmount.toFixed(2);
// }

// // Add a new row of input fields
// document.getElementById('add-row-btn').addEventListener('click', function () {
//     const newRow = document.createElement('div');
//     newRow.className = 'row mb-2';

//     newRow.innerHTML = `
// <div class="col-lg-5 mb-2">
// <select class="form-control-2" id="item-description" data-placeholder="Item Description" style="width: 100%;" required></select>

// <div class="col-lg-3 mb-2">
// <input type="number" class="form-control-2" placeholder="Quantity"  required>
// </div>
// <div class="col-lg-3 mb-2">
// <input type="number" class="form-control-2" placeholder="Price" required>
// </div>
// <div class="col-lg-1 mb-3 d-flex align-items-end">
// <button type="button" class="btn btn-danger btn-sm" onclick="deleteRow(this)">
// <i class="fas fa-trash-alt"></i>
// </button>
// </div>
//     `;

//     document.getElementById('input-container').appendChild(newRow);
//     // updateInvoiceTable();
// });

// // Event listener for input changes
// document.getElementById('input-container').addEventListener('input', updateInvoiceTable);

// // Function to delete a row
// function deleteRow(button) {
//     button.closest('.row').remove();
//     updateInvoiceTable();
// }

// // // Function to print the invoice
// document.getElementById("print-invoice").addEventListener("click", function() {
//     // Select the invoice section
//     var invoiceContent = document.getElementById("invoice-preview").innerHTML;

//     // Open a new window for printing
//     var printWindow = window.open('', '', 'height=600,width=800');
    
//     // Write the HTML of the invoice content into the new window
//     printWindow.document.write('<html><head><title>Print Invoice</title>');
//     printWindow.document.write('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">'); // Optional: include Bootstrap for styling
//     printWindow.document.write('<style>@media print { body { margin: 0; } }</style>'); // Optional: additional styles for print
//     printWindow.document.write('</head><body>');
//     printWindow.document.write(invoiceContent);
//     printWindow.document.write('</body></html>');

//     // Close the document to apply styles
//     printWindow.document.close();

//     // Wait for the content to load and then print
//     printWindow.onload = function() {
//         printWindow.print();
//         printWindow.close();
//     };
// });




// // Function to handle logout
// // document.getElementById("logout-btn").addEventListener("click", function () {
// //     window.location.href = "index.html";
// // });







// document.getElementById('productSearch').addEventListener('input', function() {
//     const searchQuery = this.value.toLowerCase();
//     const suggestions = document.getElementById('productSuggestions');
//     suggestions.innerHTML = ''; // Clear previous suggestions

//     if (searchQuery) {
//         getData.forEach(product => {
//             if (product.productName.toLowerCase().includes(searchQuery)) {
//                 const suggestionItem = document.createElement('a');
//                 suggestionItem.className = 'dropdown-item';
//                 suggestionItem.href = '#';
//                 suggestionItem.innerText = product.productName;
//                 suggestionItem.addEventListener('click', () => {
//                     fillProductDetails(product);
//                     suggestions.innerHTML = ''; // Clear suggestions after selection
//                 });
//                 suggestions.appendChild(suggestionItem);
//             }
//         });
//     }
// });

// function fillProductDetails(product) {
//     document.getElementById('productSearch').value = product.productName;
//     document.getElementById('productQuantity').value = product.productQuantity;
//     document.getElementById('productAmount').value = product.productAmount;
// }




// document.getElementById("generate-qr").addEventListener("click", function() {
//     // Get values from the input fields
//     var item = document.getElementById("item-description").value;
//     var quantity = document.getElementById("quantity").value;
//     var price = document.getElementById("price").value;

//     // Concatenate data
//     var qrData = "Item: " + item + "\nQuantity: " + quantity + "\nPrice: $" + price;

//     // Generate QR code
//     var qrcodeContainer = document.getElementById("qrcode");
//     qrcodeContainer.innerHTML = ""; // Clear previous QR code
//     new QRCode(qrcodeContainer, {
//         text: qrData,
//         width: 150,
//         height: 150,
//         colorDark: "#000000",
//         colorLight: "#ffffff",
//         correctLevel: QRCode.CorrectLevel.H
//     });
// });
