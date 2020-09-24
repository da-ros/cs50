// Reference DOM objects
var constructB = document.getElementById("constructBut");
var result = document.getElementById("resModel");
var templates = document.getElementById("modelTemplates");

// Obtain preselected values from dropdown and declare input text variables
var numPersons = "";
var floors = "";
var type = document.getElementById("buildingBox").value;

// Add listener to selection dropdown
document.getElementById("buildingBox").onchange = function(){
    type = this.value;
    };

// Add Listener to Construct Button
constructB.onclick = function(){
    numPersons = document.getElementById("personBox").value;
    floors = document.getElementById("floorBox").value;

    result.innerHTML = "<h2 id='resTitle'>You Selected the Following Options: </h2><br>"+numPersons+" Persons<br>"+floors+" Floors<br>Type: "+type;
    result.style.display = "block";

    // Add model templates
    templates.innerHTML = "<img src='template.jpg' alt='map of results' width='1400' height='800'>";
    templates.style.display = "block";
};

