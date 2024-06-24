function submitForm() {
    event.preventDefault();

    // Get form data
    const vorname = document.getElementById('vorname').value;
    const nachname = document.getElementById('nachname').value;
    const email = document.getElementById('email').value;
    const geburtsdatum = document.getElementById('geburtsdatum').value;
    const strasse = document.getElementById('strasse').value;
    const hausnummer = document.getElementById('hausnummer').value;
    const plz = document.getElementById('plz').value;
    const stadt = document.getElementById('stadt').value;
    const sicherheitsfrage = document.getElementById('sicherheitsfrage').value;
    const sicherheitsantwort = document.getElementById('sicherheitsantwort').value;
    const phone = document.getElementById('phone').value;
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm_password').value;

    // Create request object
    const xhr = new XMLHttpRequest();

    // Set up request
    xhr.open('POST', 'https://yb8ev7e9hh.execute-api.eu-central-1.amazonaws.com/prod/register', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Set up response handler
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                alert('Registration successful! Please check your email to verify your account.');
                document.getElementById('vorname').value = '';
                document.getElementById('nachname').value = '';
                document.getElementById('email').value = '';
                document.getElementById('geburtsdatum').value = '';
                document.getElementById('strasse').value = '';
                document.getElementById('hausnummer').value = '';
                document.getElementById('plz').value = '';
                document.getElementById('stadt').value = '';
                document.getElementById('sicherheitsfrage').value = '';
                document.getElementById('sicherheitsantwort').value = '';
                document.getElementById('phone').value = '';
                document.getElementById('password').value = '';
                document.getElementById('confirm_password').value = '';
            } else {
                alert('Registration failed: ' + xhr.responseText);
            }
        }
    };

    // Send request
    xhr.send(JSON.stringify({
        vorname: vorname,
        nachname: nachname,
        email: email,
        geburtsdatum: geburtsdatum,
        strasse: strasse,
        hausnummer: hausnummer,
        plz: plz,
        stadt: stadt,
        sicherheitsfrage: sicherheitsfrage,
        sicherheitsantwort: sicherheitsantwort,
        phone: phone,
        password: password,
        confirm_password: confirm_password
    }));
}
