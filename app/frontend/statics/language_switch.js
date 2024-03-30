function changeLanguage(langCode) {


    fetch('/switch_language/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ langCode:langCode }),
    })
    .then(response => {
        if (response.ok) {
            console.log('Language switched successfully');
            window.location.reload(); // Reload the page
        } else {
            console.error('Failed to switch language');
        }
    })
    .catch(error => {
        console.error('Error switching language:', error);
    });
}
    // // Obtain the CSRF token from the cookie
    // var csrfToken = getCookie('csrftoken');

    // // Create a form element
    // var form = document.createElement('form');
    // form.method = 'POST'; // Use POST method to send language parameter
    // form.action = '/switch_language/'; // Set the action to the current URL or any other URL you prefer

    // // Create a hidden input field to store the CSRF token
    // var csrfInput = document.createElement('input');
    // csrfInput.type = 'hidden';
    // csrfInput.name = 'csrfmiddlewaretoken';
    // csrfInput.value = csrfToken;

    // // Create a hidden input field to store the language code
    // var langInput = document.createElement('input');
    // langInput.type = 'hidden';
    // langInput.name = 'lang';
    // langInput.value = langCode;

    // // Append the input fields to the form
    // form.appendChild(csrfInput);
    // form.appendChild(langInput);

    // // Append the form to the document body
    // document.body.appendChild(form);

    // // Submit the form
    // // console.log(csrfToken);
    // form.submit();
    // // console.log("test");
// }

// Function to get the value of a cookie by name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}