
filterSelection("all") // Execute the function and show all columns
function filterSelection(c) {
var x, i;
  x = document.getElementsByClassName("characters");
  if (c == "all") c = "";
  // Add the "show" class (display:block) to the filtered elements, and remove the "show" class from the elements that are not selected
  for (i = 0; i < x.length; i++) {
    w3RemoveClass(x[i], "show");
    if (x[i].className.indexOf(c) > -1) w3AddClass(x[i], "show");
  }
}

// Show filtered elements
function w3AddClass(element, name) {
    var delimiter = " ";
    var i, arr1, arr2;
    // arr1 = character | char name
    arr1 = element.className.split(delimiter);
    // show or the action
    arr2 = name.split(delimiter);
    for (i = 0; i < arr2.length; i++) {
        // [character, joshua] vs [show] 
        // i = 0 
        // find the first index of show
        // can't find it, then add it
        if (arr1.indexOf(arr2[i]) == -1) {
        element.className += delimiter + arr2[i];
        }
    }
}

// Hide elements that are not selected
// remove the "name" from the class name for the element
function w3RemoveClass(element, name) {
    var delimiter = " ";
    var i, arr1, arr2;
    arr1 = element.className.split(delimiter);
    arr2 = name.split(delimiter);
    for (i = 0; i < arr2.length; i++) {
        while (arr1.indexOf(arr2[i]) > -1) {
        arr1.splice(arr1.indexOf(arr2[i]), 1);
        }
    }
    element.className = arr1.join(delimiter);
}

// Add active class to the current button (highlight it)
var delimiter = " ";
var btnContainer = document.getElementById("myBtnContainer");
var btns = btnContainer.getElementsByClassName("btn");
// init all buttons
for (var i = 0; i < btns.length; i++) {
    // add a listener function to each button
    btns[i].addEventListener("click", function(){
        var current = document.getElementsByClassName("active");
        current[0].className = current[0].className.replace(delimiter+"active", "");
        this.className += delimiter + "active";
    });
}