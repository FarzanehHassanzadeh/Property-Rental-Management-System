function validateForm() {
    const passwordInput = document.getElementById('password');
    const passwordError = document.getElementById('password-error');
    const password = passwordInput.value;

    // Simple password validation (example: at least 6 characters and one digit)
    const validPassword = /^(?=.*\d).{6,}$/;

    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('email-error');
    const email = emailInput.value;

    // Simple email validation pattern
    const validEmail = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

    let isValid = true; // Flag for overall validity

    // Validate password
    if (!validPassword.test(password)) {
        passwordInput.classList.add('error'); // Add error class
        passwordError.textContent = 'Password must be at least 6 characters long and contain at least one digit.';
        isValid = false; // Set flag to false
    } else {
        passwordInput.classList.remove('error'); // Remove error class if valid
        passwordError.textContent = ''; // Clear error message
    }

    // Validate email
    if (!validEmail.test(email)) {
        emailInput.classList.add('error'); // Add error class
        emailError.textContent = 'Please enter a valid email address.';
        isValid = false; // Set flag to false
    } else {
        emailInput.classList.remove('error'); // Remove error class if valid
        emailError.textContent = ''; // Clear error message
    }

    return isValid; // Allow form submission if all validations pass
}