document.getElementById('encryptButton').addEventListener('click', () => {
    const password = document.getElementById('password').value;
    if (!password) {
        alert("Please enter a password.");
        return;
    }

    fetch('/encrypt', {
        method: 'POST',
        body: JSON.stringify({ password: password }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('decryptButton').addEventListener('click', () => {
    const password = document.getElementById('password').value;
    if (!password) {
        alert("Please enter a password.");
        return;
    }

    fetch('/decrypt', {
        method: 'POST',
        body: JSON.stringify({ password: password }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => console.error('Error:', error));
});
