function showAbout() {
    // Update the content
    document.getElementById('content').innerHTML = "<p>This is the about me page.</p>";

    // Update the URL without reloading the page
    history.pushState({ page: 'about' }, 'About Me', '/about');
}

// Event listener for back and forward buttons
window.onpopstate = function(event) {
    if (event.state && event.state.page === 'home') {
        showHome();
    } else if (event.state && event.state.page === 'about') {
        showAbout();
    }
};