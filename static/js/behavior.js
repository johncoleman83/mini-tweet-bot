document.addEventListener("DOMContentLoaded", function(event) {
var features = document.getElementById("features");
var featuresBox = document.getElementById("features-box");
features.addEventListener("click", function() {
    

    if (featuresBox.className == "empty") {
	featuresBox.className = "features-box-data";
	} else {
	    featuresBox.className = "empty";
	}

});

});
