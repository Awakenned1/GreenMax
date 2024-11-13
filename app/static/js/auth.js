document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle with animation
    const togglePassword = document.querySelector('.toggle-password');
    const passwordInput = document.querySelector('#password');

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            // Toggle password visibility
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Toggle icon with animation
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
            
            // Add scale animation
            this.style.transform = 'scale(1.1)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
        });
    }

    // Enhanced form validation
    const form = document.querySelector('.auth-form');
    const inputs = document.querySelectorAll('.form-group input');

    // Input validation functions
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function validatePassword(password) {
        return password.length >= 8;
    }

    function showError(input, message) {
        const formGroup = input.closest('.form-group');
        const existingError = formGroup.querySelector('.error-message');
        
        formGroup.classList.add('error');
        
        if (!existingError) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = message;
            formGroup.appendChild(errorDiv);
            
            // Animate error message
            errorDiv.style.opacity = '0';
            errorDiv.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                errorDiv.style.opacity = '1';
                errorDiv.style.transform = 'translateY(0)';
            }, 10);
        }
    }

    function removeError(input) {
        const formGroup = input.closest('.form-group');
        const errorMessage = formGroup.querySelector('.error-message');
        
        formGroup.classList.remove('error');
        if (errorMessage) {
            errorMessage.remove();
        }
    }

    // Real-time validation
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateInput(this);
        });

        input.addEventListener('input', function() {
            if (this.classList.contains('error')) {
                validateInput(this);
            }
        });
    });

    function validateInput(input) {
        if (!input.value && input.hasAttribute('required')) {
            showError(input, 'This field is required');
            return false;
        }

        if (input.type === 'email' && input.value && !validateEmail(input.value)) {
            showError(input, 'Please enter a valid email address');
            return false;
        }

        if (input.type === 'password' && input.value && !validatePassword(input.value)) {
            showError(input, 'Password must be at least 8 characters long');
            return false;
        }

        removeError(input);
        return true;
    }

    // Form submission handling
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            let isValid = true;

            // Validate all inputs
            inputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                return;
            }

            // Show loading state
            const button = this.querySelector('.btn-primary');
            button.classList.add('loading');
            button.innerHTML = '<span>Logging in...</span><div class="loader"></div>';

            // Simulate API call (replace with actual API call)
            setTimeout(() => {
                this.submit();
            }, 1500);
        });
    }

    // Ripple effect for buttons
    const buttons = document.querySelectorAll('.btn-primary, .social-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('div');
            ripple.className = 'ripple';
            this.appendChild(ripple);

            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size/2;
            const y = e.clientY - rect.top - size/2;

            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Social login buttons hover effect
    const socialButtons = document.querySelectorAll('.social-btn');
    socialButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });

        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Remember me checkbox custom styling
    const rememberMe = document.querySelector('.remember-me input');
    if (rememberMe) {
        rememberMe.addEventListener('change', function() {
            this.parentElement.classList.toggle('checked', this.checked);
        });
    }

    // Password strength indicator
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const strength = calculatePasswordStrength(this.value);
            updatePasswordStrengthIndicator(strength);
        });
    }

    function calculatePasswordStrength(password) {
        let strength = 0;
        if (password.length >= 8) strength++;
        if (password.match(/[A-Z]/)) strength++;
        if (password.match(/[0-9]/)) strength++;
        if (password.match(/[^A-Za-z0-9]/)) strength++;
        return strength;
    }

    function updatePasswordStrengthIndicator(strength) {
        const indicator = document.querySelector('.password-strength');
        if (!indicator) return;

        const strengthClasses = ['weak', 'medium', 'strong', 'very-strong'];
        indicator.className = 'password-strength ' + strengthClasses[strength - 1];
    }
});
document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const form = document.querySelector('.auth-form');
    const inputs = document.querySelectorAll('.auth-form input');
    const submitButton = document.querySelector('.btn-primary');
    const passwordInput = document.querySelector('#password');
    const togglePassword = document.querySelector('.toggle-password');

    // Password visibility toggle
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    }

    // Form validation
    const validators = {
        email: (value) => {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return {
                isValid: re.test(value),
                message: 'Please enter a valid email address'
            };
        },
        password: (value) => {
            return {
                isValid: value.length >= 8,
                message: 'Password must be at least 8 characters long'
            };
        },
        confirm_password: (value) => {
            const password = document.querySelector('#password').value;
            return {
                isValid: value === password,
                message: 'Passwords do not match'
            };
        }
    };

    // Input validation
    function validateInput(input) {
        const value = input.value.trim();
        const validator = validators[input.id];
        
        if (!value && input.hasAttribute('required')) {
            showError(input, 'This field is required');
            return false;
        }

        if (validator && value) {
            const result = validator(value);
            if (!result.isValid) {
                showError(input, result.message);
                return false;
            }
        }

        removeError(input);
        return true;
    }

    // Error handling
    function showError(input, message) {
        const formGroup = input.closest('.form-group');
        removeError(input);
        
        formGroup.classList.add('error');
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        formGroup.appendChild(errorDiv);
    }

    function removeError(input) {
        const formGroup = input.closest('.form-group');
        formGroup.classList.remove('error');
        const errorMessage = formGroup.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    }

    // Password strength meter
    if (passwordInput) {
        const strengthMeter = document.createElement('div');
        strengthMeter.className = 'password-strength-meter';
        passwordInput.parentElement.appendChild(strengthMeter);

        passwordInput.addEventListener('input', function() {
            updatePasswordStrength(this.value);
        });
    }

    function updatePasswordStrength(password) {
        const meter = document.querySelector('.password-strength-meter');
        if (!meter) return;

        let strength = 0;
        if (password.length >= 8) strength++;
        if (password.match(/[A-Z]/)) strength++;
        if (password.match(/[0-9]/)) strength++;
        if (password.match(/[^A-Za-z0-9]/)) strength++;

        const strengthClasses = ['weak', 'medium', 'strong', 'very-strong'];
        meter.className = 'password-strength-meter ' + (strengthClasses[strength - 1] || '');
    }

    // Form submission
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            let isValid = true;

            // Validate all inputs
            inputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });

            if (!isValid) return;

            // Show loading state
            submitButton.disabled = true;
            submitButton.classList.add('loading');
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<span>Processing...</span><div class="loader"></div>';

            try {
                const formData = new FormData(form);
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();

                if (data.success) {
                    window.location.href = data.redirect;
                } else {
                    showError(form.querySelector('input'), data.message);
                }
            } catch (error) {
                showError(form.querySelector('input'), 'An error occurred. Please try again.');
            } finally {
                submitButton.disabled = false;
                submitButton.classList.remove('loading');
                submitButton.innerHTML = originalText;
            }
        });
    }

    // Social login buttons
    const socialButtons = document.querySelectorAll('.social-btn');
    socialButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const provider = this.dataset.provider;
            window.location.href = `/auth/${provider}-login`;
        });
    });

    // Input animations
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.closest('.form-group').classList.add('focused');
        });

        input.addEventListener('blur', function() {
            if (!this.value) {
                this.closest('.form-group').classList.remove('focused');
            }
        });

        // Set initial state for inputs with values
        if (input.value) {
            input.closest('.form-group').classList.add('focused');
        }
    });
});
