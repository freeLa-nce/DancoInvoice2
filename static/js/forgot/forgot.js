document.getElementById('check-user-forgot-form').addEventListener('submit', function(event) {
    const email = document.getElementById('check-forgot-email');
    email.classList.remove('is-invalid'); // Corrected to classList
    let isValid = true;

    // Perform validation
    if (!email.checkValidity()) {
        email.classList.add('is-invalid'); // Corrected to classList
        isValid = false;
    }

    // If the email is not valid, prevent form submission
    if (!isValid) {
        event.preventDefault();
    }
    // Else the form will submit normally
});
