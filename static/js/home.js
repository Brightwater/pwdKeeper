// Creates all widgets for all the available services
// Uses info from passwords.py : listAllServices(user)
function addServices() {
	var strServices = document.getElementById("services").textContent;	// Unedited list sent by passwords.py : listAllServices(user)
	var services = strServices.split("'");								// List of services (every other element)
	
	for (i = 1; i < services.length; i += 2) {
		addService(services[i]);
    }
    // Deletes the services string afterwards
    document.getElementById("services").innerHTML = "";
}

// Creates individual service widgets
function addService(name) {
	var serviceView = document.getElementById("serviceView"); 	// button title
	var divId = name.replace(' ', '_');							// div ids are the service's name with "_" instead of " "
	
	serviceView.innerHTML += '<button id="btn' + divId + '" onclick="toggleHidden(this.id)">' + name + ' </button>';
}

function loadPage() {
	addServices();
}

// Runs once page is loaded
if (window.addEventListener) {
	window.addEventListener("load", loadPage, false);
} else if (window.attachEvent) {
	window.attachEvent("onload", loadPage);
}