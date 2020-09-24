// Reference DOM objects
var searchF = document.getElementById("searchF");
var result = document.getElementById("resFinance");
var entities = document.getElementById("creditEntities");

// Obtain preselected values from dropdown and declare input text variables
var job = "";
var income = 0;
var numChildren = document.getElementById("childrenBox").value;

// Add listener to selection dropdown
document.getElementById("childrenBox").onchange = function(){
    numChildren = this.value;
    };

// Add Listener to searchF Button
searchF.onclick = function(){
    job = document.getElementById("jobBox").value;
    income = document.getElementById("incomeBox").value;

    result.innerHTML = "<h2 id='resTitle'>You Selected the Following Options: </h2><br>Job: "+job+"<br>Annual Income: "+income+"<br>Children: "+numChildren;
    result.style.display = "block";

    // Add model templates
    entities.innerHTML = "<img src='mortgage.png' alt='map of results' width='800' height='600'>";
    entities.style.display = "block";
};
