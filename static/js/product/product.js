// var form = document.getElementById("myForm"),
//     id = document.getElementById("productid"),
//     pname = document.getElementById("productname"),
//     quantity = document.getElementById("quantity"),
//     unit = document.getElementById("unit"),
//     date = document.getElementById("date"),
//     submitBtn = document.querySelector(".submit"),
//     userInfo = document.getElementById("data"),
//     modal = document.getElementById("userForm"),
//     modalTitle = document.querySelector("#userForm .modal-title"),
//     newUserBtn = document.querySelector(".newUser");

// let getData = localStorage.getItem('userProfile') ? JSON.parse(localStorage.getItem('userProfile')) : [];

// let isEdit = false, editId;
// showInfo();

// newUserBtn.addEventListener('click', () => {
//     submitBtn.innerText = 'Submit';
//     modalTitle.innerText = "Fill the Form";
//     isEdit = false;
//     form.reset();
// });

// function showInfo() {
//     document.querySelectorAll('.productDetails').forEach(info => info.remove());
//     getData.forEach((element, index) => {
//         let createElement = `
//             <tr class="productDetails">
//                 <td>${index + 1}</td>
//                 <td>${element.productId}</td>
//                 <td>${element.productName}</td>
//                 <td>${element.productQuantity}</td>
//                 <td>${element.productUnit}</td>
//                 <td>${element.productDate}</td>

//                 <td>
//                     <button class="btn btn-success" onclick="readInfo('${element.productId}', '${element.productName}', '${element.productQuantity}', '${element.productUnit}', '${element.productDate}')" data-bs-toggle="modal" data-bs-target="#readData"><i class="bi bi-eye"></i></button>
//                     <button class="btn btn-primary" onclick="editInfo(${index}, '${element.productId}', '${element.productName}', '${element.productQuantity}', '${element.productUnit}', '${element.productDate}')" data-bs-toggle="modal" data-bs-target="#userForm"><i class="bi bi-pencil-square"></i></button>
//                     <button class="btn btn-danger" onclick="deleteInfo(${index})"><i class="bi bi-trash"></i></button>
//                 </td>
//             </tr>`;
//         userInfo.innerHTML += createElement;
//     });
// }
// showInfo();

// function readInfo(id, name, quantity, unit, date) {
//     document.querySelector('#showId').value = id;
//     document.querySelector("#showName").value = name;
//     document.querySelector("#showQuantity").value = quantity;
//     document.querySelector("#showUnit").value = unit;
//     document.querySelector("#showDate").value = date;
// }

// function editInfo(index, productId, productName, productQuantity, productUnit, productDate) {
//     isEdit = true;
//     editId = index;
//     id.value = productId;
//     pname.value = productName;
//     quantity.value = productQuantity;
//     unit.value = productUnit;
//     date.value = productDate;

//     submitBtn.innerText = "Update";
//     modalTitle.innerText = "Update The Form";
// }

// function deleteInfo(index) {
//     if (confirm("Are you sure you want to delete?")) {
//         getData.splice(index, 1);
//         localStorage.setItem("userProfile", JSON.stringify(getData));
//         showInfo();
//     }
// }

// form.addEventListener('submit', (e) => {
//     e.preventDefault();

//     const information = {
//         productId: id.value,
//         productName: pname.value,
//         productQuantity: quantity.value,
//         productUnit: unit.value,
//         productDate: date.value,
//     };

//     if (!isEdit) {
//         getData.push(information);
//     } else {
//         isEdit = false;
//         getData[editId] = information;
//     }

//     localStorage.setItem('userProfile', JSON.stringify(getData));

//     submitBtn.innerText = "Submit";
//     modalTitle.innerHTML = "Fill The Form";

//     showInfo();

//     form.reset();
// });

// document.getElementById("logout-btn").addEventListener("click", function() {
//     // Redirect to the login page
//     window.location.href = "index.html";
// });

// //-------------------------excel sheet data-------------------------//


// document.getElementById("customFileBtn").addEventListener("click", function() {
//     document.getElementById("fileInput").click();
// });

// document.getElementById("fileInput").addEventListener("change", handleFileUpload);

// function handleFileUpload(event) {
//     const file = event.target.files[0];
//     if (file) {
//         const reader = new FileReader();

//         reader.onload = function(e) {
//             const data = new Uint8Array(e.target.result);
//             const workbook = XLSX.read(data, { type: "array" });

//             const firstSheetName = workbook.SheetNames[0];
//             const worksheet = XLSX.utils.sheet_to_json(workbook.Sheets[firstSheetName], { header: 1 });

//             document.querySelectorAll('.productDetails').forEach(info => info.remove());

//             worksheet.slice(1).forEach((row, index) => {
//                 const [productId, productName, productQuantity, productUnit, productDate] = row;

//                 const tableRow = `
//                     <tr class="productDetails">
//                         <td>${index + 1}</td>
//                         <td>${productId || ''}</td>
//                         <td>${productName || ''}</td>
//                         <td>${productQuantity || ''}</td>
//                         <td>${productUnit || ''}</td>
//                         <td>${productDate || ''}</td>
//                         <td>
//                             <button class="btn btn-primary" onclick="readInfo('${productId}', '${productName}', '${productQuantity}', '${productUnit}', '${productDate}')" data-bs-toggle="modal" data-bs-target="#readData"><i class="bi bi-eye"></i></button>
//                             <button class="btn btn-success" onclick="editInfo(${index}, '${productId}', '${productName}', '${productQuantity}', '${productUnit}', '${productDate}')" data-bs-toggle="modal" data-bs-target="#userForm"><i class="bi bi-pencil-square"></i></button>
//                             <button class="btn btn-danger" onclick="deleteInfo(${index})"><i class="bi bi-trash"></i></button>
//                         </td>
//                     </tr>`;
//                 document.getElementById("data").innerHTML += tableRow;

//                 const productData = {
//                     productId, productName, productQuantity, productUnit, productDate
//                 };
//                 getData.push(productData);
//             });

//             localStorage.setItem('userProfile', JSON.stringify(getData));
//         };

//         reader.readAsArrayBuffer(file);
//     }
// }



// document.getElementById('productSearch').addEventListener('input', function() {
//     const searchTerm = this.value.toLowerCase();
//     const products = document.querySelectorAll('.product-item');

//     products.forEach(function(product) {
//         const productName = product.textContent.toLowerCase();
//         if (productName.includes(searchTerm)) {
//             product.style.display = 'block';
//         } else {
//             product.style.display = 'none';
//         }
//     });
// })