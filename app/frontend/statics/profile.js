function showProfile()
{
	
	var mainElement = document.getElementById('content');
	mainElement.innerHTML = '<h1>Profile Page</h1>';
	
	console.log(User);
	var username = document.createElement("p");
	username.textContent = "Username: " + User.username;
	mainElement.appendChild(username);

	var email = document.createElement("p");
	email.textContent = "Email: " + User.email;
	mainElement.appendChild(email);

	var first_name = document.createElement("p");
	first_name.textContent = "First Name: " + User.first_name;
	mainElement.appendChild(first_name);

	var last_name = document.createElement("p");
	last_name.textContent = "Last Name: " + User.surname;
	mainElement.appendChild(last_name);




	

}
