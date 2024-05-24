
function oligomer_compute_form_submit(e){
    e.preventDefault();
    console.log("Event Listener called");
    console.log(this.elements[0].value);
    couplings = this.elements[1].value.split(",").filter(function(element) {
        return element !== '';
      });
      shift_ends = this.elements[2].value.split(",").filter(function(element) {
        return element !== '';
      });
    request = {
        "n": this.elements[0].value,
        "couplings": couplings,
        "shift_ends": shift_ends
    };
    console.log(request);
    // Creating Our XMLHttpRequest object 
    let xhr = new XMLHttpRequest();

    // Making our connection  
    let url = 'http://localhost:8000/ocompute';
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // function execute after request is successful 
    xhr.onload = function () {
        console.log(this.responseText);
        let json_response = JSON.parse(this.responseText);
        console.log(json_response);
        //formatted_response = "<p>" +  + "</p>"
        document.getElementById("output").innerHTML = this.responseText;
        document.getElementById("barplot").innerHTML = '<img src="' + json_response['barplot'] + '">'
    }
    // Sending our request 
    xhr.send(JSON.stringify(request));
}

function allEventListeners(){
    //oligomer compute form event listener
    const form = document.getElementById("oligomer_compute_form");
    form.addEventListener("submit", oligomer_compute_form_submit);
}

function main(){
    allEventListeners();
}

main();
