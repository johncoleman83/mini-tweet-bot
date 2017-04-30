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

	var featuresTwo = document.getElementById("features-two");

	featuresTwo.addEventListener("click", function() {

		if (featuresBox.className == "empty") {
			featuresBox.className = "features-box-data";
		} else {
			featuresBox.className = "empty";
		}

	});

	var hamburger = document.getElementById("hamburger");
	var navigation = document.getElementById("navigation");

	hamburger.addEventListener("click", function() {

		if (navigation.className == "hidden") {
			navigation.className = "visible";
		} else {
			navigation.className = "hidden";
		}

	});

});
