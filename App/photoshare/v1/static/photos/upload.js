// static/photos/upload.js

document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('uploadForm');
    const presignForm = document.getElementById('presignForm');
    const photoInput = document.getElementById('photoInput');
    const keyInput = document.getElementById('keyInput');
    const preview = document.getElementById('preview');
    const downloadLink = document.getElementById('downloadLink');

    // Helper to get CSRF token from cookies
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') return decodeURIComponent(value);
        }
        return '';
    }

    // ===== Upload photo =====
    uploadForm.addEventListener('submit', async function (e) {
        e.preventDefault();

        const file = photoInput.files[0];
        if (!file) {
            alert('Please select a file to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('photo', file);

        try {
            const response = await fetch('/api/upload', { // Ensure URL matches Django URL
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                },
                body: formData,
            });

            const data = await response.json();
            console.log('Upload response:', data);

            if (!response.ok) {
                const msg = data.error || 'Failed to upload photo.';
                alert(`Error: ${msg}`);
                return;
            }

            if (!data.presigned_url) {
                alert('Server did not return a presigned URL.');
                return;
            }

            // Show preview and download link
            preview.src = data.presigned_url;
            preview.style.display = 'block';

            downloadLink.href = data.presigned_url;
            downloadLink.style.display = 'inline';
            downloadLink.textContent = 'Download Photo';

            alert('Photo uploaded successfully!');
        } catch (err) {
            console.error('Upload error:', err);
            alert('An unexpected error occurred while uploading.');
        }
    });

    // ===== Get presigned URL manually =====
    // ===== Get presigned URL manually =====
presignForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    const key = keyInput.value.trim();
    if (!key) {
        alert('Please enter an S3 key.');
        return;
    }

    try {
        const response = await fetch('/api/presign', { // Ensure this view exists
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ key }),
        });

        const data = await response.json();
        console.log('Presign response:', data);

        // Minimal update: check for error field
        if (!response.ok || data.error) {
            alert(data.error || 'Failed to get presigned URL.');
            preview.style.display = 'none';
            downloadLink.style.display = 'none';
            return;
        }

        if (!data.presigned_url) {
            alert('Server did not return a presigned URL.');
            preview.style.display = 'none';
            downloadLink.style.display = 'none';
            return;
        }

        // Show preview and download link
        preview.src = data.presigned_url;
        preview.style.display = 'block';

        downloadLink.href = data.presigned_url;
        downloadLink.style.display = 'inline';
        downloadLink.textContent = 'Download Photo';

    } catch (err) {
        console.error('Presign error:', err);
        alert('An unexpected error occurred while getting the presigned URL.');
        preview.style.display = 'none';
        downloadLink.style.display = 'none';
    }
});

});
