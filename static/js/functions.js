const socket = new WebSocket('ws://' + location.host + '/echo');


function welcome() {
	document.getElementById("paragraph").innerHTML += "<br/>This text was added by JavaScript 😀"
}
