function submitForm(event) {
    event.preventDefault();  // Verhindert das Standardverhalten des Formulars

    // Formulardaten abrufen
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Request-Objekt erstellen
    const xhr = new XMLHttpRequest();

    // Anfrage einrichten
    xhr.open('POST', 'https://yb8ev7e9hh.execute-api.eu-central-1.amazonaws.com/prod/login', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Antwort-Handler einrichten
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            console.log('Response received:', xhr.responseText);  // Protokolliert die gesamte Antwort
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                if (response.message === 'Login successful') {
                    alert('Login successful!');
                    // Temporär den Redirect entfernen oder ändern
                    // window.location.href = 'home.html';  // Ändern Sie dies zu Ihrer gewünschten Seite
                } else {
                    alert('Login failed: ' + (response.message || 'Unknown error'));
                }
            } else {
                alert('Request failed: ' + xhr.status + ' ' + xhr.statusText);
            }
        }
    };

    xhr.onerror = function() {
        alert('Network error. Please check your connection and try again.');
    };

    // Anfrage senden
    xhr.send(JSON.stringify({
        email: email,
        password: password
    }));
}
