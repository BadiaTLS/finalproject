
// Show the loading screen initially
var loadingScreen = document.getElementById('loading-screen');
loadingScreen.style.display = 'flex';

// Wait for 1.5 seconds and then hide the loading screen
setTimeout(function () {
    loadingScreen.classList.add('fade-out');

    // Wait for the fade-out animation to complete
    setTimeout(function () {
        // Hide the loading screen completely
        loadingScreen.style.display = 'none';

        // Show the login page
        var mainContent = document.querySelector('main');
        mainContent.style.display = 'block';
    }, 300);
}, 500);

// Rest of your JavaScript code...
var inputs = document.querySelectorAll('input[type=text], input[type=email], input[type=password]');
for (var i = 0; i < inputs.length; i++) {
    var inputEl = inputs[i];
    if (inputEl.value.trim() !== '') {
        inputEl.parentNode.classList.add('input--filled');
    }
}

// Use event delegation to attach the focus and blur event listeners to the document object
document.addEventListener('focus', onFocus, true);
document.addEventListener('blur', onBlur, true);

function onFocus(ev) {
    // Check if the event target is an input element before executing the rest of the code
    if (ev.target.matches('input[type=text], input[type=email], input[type=password]')) {
        var parent = ev.target.parentNode;
        parent.classList.add('inputs--filled');
    }
}

function onBlur(ev) {
    // Check if the event target is an input element before executing the rest of the code
    if (ev.target.matches('input[type=text], input[type=email], input[type=password]')) {
        var parent = ev.target.parentNode;
        if (ev.target.value.trim() === '') {
            parent.classList.remove('inputs--filled');
        } else if (ev.target.checkValidity() == false) {
            parent.classList.add('inputs--invalid');
        } else if (ev.target.checkValidity() == true) {
            parent.classList.remove('inputs--invalid');
        }
    }
}

var submitBtn = document.querySelector('input[type=submit]');
submitBtn.addEventListener('click', onSubmit);

function onSubmit(ev) {
    var inputsWrappers = ev.target.parentNode.querySelectorAll('span');
    for (var i = 0; i < inputsWrappers.length; i++) {
        var input = inputsWrappers[i].querySelector('input[type=text], input[type=email], input[type=password]');
        if (input.checkValidity() == false) {
            inputsWrappers[i].classList.add('inputs--invalid');
        } else if (input.checkValidity() == true) {
            inputsWrappers[i].classList.remove('inputs--invalid');
        }
    }
}

var passwordToggle = document.querySelector('.password-toggle');
passwordToggle.addEventListener('click', togglePasswordVisibility);

function togglePasswordVisibility(ev) {
    var passwordInput = ev.target.previousElementSibling;
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        ev.target.classList.remove('fa-eye-slash');
        ev.target.classList.add('fa-eye');
    } else {
        passwordInput.type = 'password';
        ev.target.classList.remove('fa-eye');
        ev.target.classList.add('fa-eye-slash');
    }
}