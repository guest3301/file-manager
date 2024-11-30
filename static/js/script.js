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
        showModal(JSON.stringify(data, null, 2));
        if (data.success) {
            updateFileList();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showModal(`Error: ${error}`);
    });
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
        showModal(JSON.stringify(data, null, 2));
        if (data.success) {
            updateFileList();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showModal(`Error: ${error}`);
    });
});

function updateFileList() {
    fetch('/')
    .then(response => response.text())
    .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newFileList = doc.getElementById('fileList').innerHTML;
        document.getElementById('fileList').innerHTML = newFileList;
    })
    .catch(error => console.error('Error:', error));
}

function showModal(message) {
    const modal = document.getElementById('modal');
    const modalMessage = document.getElementById('modalMessage');
    const closeButton = document.getElementById('closeButton');

    modalMessage.textContent = message;
    modal.style.display = "block";

    closeButton.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}