window.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('send-button').addEventListener('click', function() {
        var selected_location = document.getElementById('location-select').value;
        fetch("/send_to_pico", { 
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'location=' + encodeURIComponent(selected_location), 
        })
        .then(response => {
            console.log('Message sent to Pico');
        });
    });
});
