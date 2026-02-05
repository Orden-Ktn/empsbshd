setTimeout(function() {
    let alerts = document.querySelectorAll('.alert-fill'); // Sélectionne les alertes par leur classe
    alerts.forEach(function(alert) {
        alert.style.display = 'none';
    });
}, 8000);


const passwordInput = document.querySelector('.password-input');
    const passwordToggle = document.querySelector('.password-toggle');

    passwordToggle.addEventListener('click', function () {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            passwordToggle.classList.remove('bx-show');
            passwordToggle.classList.add('bx-hide');
        } else {
            passwordInput.type = 'password';
            passwordToggle.classList.remove('bx-hide');
            passwordToggle.classList.add('bx-show');
        }
    });

document.getElementById('login-form').addEventListener('submit', function(e) {
    // Afficher le loader
    document.getElementById('loader').style.display = 'flex';
    
    // Masquer le formulaire
    document.getElementById('login-container').style.display = 'none';
});