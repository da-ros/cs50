// Reference DOM objects
var searchB = document.getElementById("locationBut");
var checkP = document.getElementById("checkP");
var checkS = document.getElementById("checkS");
var checkE = document.getElementById("checkE");
var result = document.getElementById("resultChosen");
var map = document.getElementById("map");

// Obtain preselected values from dropdowns
var time = document.getElementById("selectTime").value;
var zone = document.getElementById("selectZone").value;

// Declare checkboxes variables
var checkPText = "";
var checkSText = "";
var checkEText = "";

// Add listener to selection dropdown and checkboxes
document.getElementById("selectTime").onchange = function(){
    time = this.value;
    };
document.getElementById("selectZone").onchange = function(){
    zone = this.value;
};
checkP.onclick = function(){
    if (checkP.checked == true){
        checkPText = checkP.value+" ";
    }
    else {
        checkPText = "";
    }
};
checkS.onclick = function(){
    if (checkS.checked == true){
        checkSText = checkS.value+" ";
    }
    else {
        checkSText = "";
    }
}
checkE.onclick = function(){
    if (checkE.checked == true){
        checkEText = checkE.value+" ";
    }
    else {
        checkEText = "";
    }
}

// Add Listener to Search Button
searchB.onclick = function(){
    result.innerHTML = "<h2 id='resTitle'>You Selected the Following Options: </h2><br>Less than "+time+" mins to Downtown<br>"+zone+" Zone<br>";
    if(checkPText != ""){
        result.innerHTML += checkPText+"<br>";
    }
    if (checkSText != ""){
        result.innerHTML += checkSText+"<br>";
    }
    if (checkEText != ""){
        result.innerHTML += checkEText+"<br>";
    }
    result.style.display = "block";

    // Add satellite map
    map.innerHTML = "<img src='map.jpg' alt='map of results' width='1400' height='800'>";
    map.style.display = "block";
};

