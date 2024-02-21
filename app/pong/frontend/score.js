// function fetchDataFromBackend() {
//     // Make a GET request to your backend API endpoint
//     fetch('/api/data')
//         .then(response => {
//             // Check if the response is successful (status code 200)
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             // Parse the JSON response
//             return response.json();
//         })
//         .then(data => {
//             // Data contains the retrieved entry from the database
//             // Display the data on the webpage
//             displayData(data);
//         })
//         .catch(error => {
//             // Handle errors
//             console.error('There was a problem with the fetch operation:', error);
//         });
// }

// function showScoreboard(data) {
//     // Assuming data is an object with properties representing the entry fields
//     // Access the properties of the data object and display them on the webpage
//     const container = document.getElementById('data-container');
//     container.innerHTML = `
//         <h2>Data Details</h2>
//         <p>ID: ${data.id}</p>
//         <p>Name: ${data.name}</p>
//         <!-- Add more fields as needed -->
//     `;
// }

// // Call the fetchDataFromBackend function when the page loads or when needed
// fetchDataFromBackend();