
// document.getElementById('login-btn').addEventListener('click', function() {
//     window.location.href = 'quotation.html';
// });



// document.getElementById("submit-email-btn").addEventListener("click", function() {
//     window.location.href = "code.html"; // Redirect to code.html
// });
// document.getElementById("submit-code-btn").addEventListener("click", function() {
//     window.location.href = "newpass.html"; // Redirect to code.html
// });


// document.getElementById('save-password-btn').addEventListener('click', function() {
//     window.location.href = 'index.html';
// });


// document.getElementById('logout-btn').addEventListener('click', function() {
//     window.location.href = 'index.html'; 
// });





document.getElementById('login-form').addEventListener('submit', function(event) {
    debugger;
    event.preventDefault(); 

    const email = document.getElementById('email');
    const password = document.getElementById('password');


    email.classList.remove('is-invalid');
    password.classList.remove('is-invalid');

    let isValid = true;

    if (!email.checkValidity()) {
        email.classList.add('is-invalid');
        isValid = false;
    }

    if (!password.checkValidity()) {
        password.classList.add('is-invalid');
        isValid = false;
    }

    if (isValid) {
        this.submit();  // Submit the form if everything is valid
    }
});


const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');

togglePassword.addEventListener('click', function () {

    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);


    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
});




