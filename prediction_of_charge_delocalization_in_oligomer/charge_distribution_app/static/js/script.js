function open_form(formName) {
    var i;
    var x = document.getElementsByClassName("tabcontent");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    document.getElementById(formName).style.display = "block";
}

function create_image_element() {

}

function oligomer_compute_form_submit(e){
    e.preventDefault();
    document.getElementById("output").innerHTML = "";
    document.getElementById("output").style.display = "block";
    document.getElementById("plot").innerHTML = "";
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

        let formatted_response = `
            <p>Oligomer: ${json_response['Oligomer']}</p>
            <p>Global Minimum: ${json_response['Global Minimum']}</p>
            <p>Ground State: ${json_response['Ground State']}</p>
            <p>Excited State: ${json_response['Excited State']}</p>
            <p>Charges:</p>
            <ul>
                ${json_response['Charges'].map(charge => `<li>${charge}</li>`).join('')}
            </ul>
        `;
        console.log(json_response);
        //formatted_response = "<p>" +  + "</p>"
        if (json_response['status'] === "Solved"){
            document.getElementById("output").innerHTML = formatted_response;
            document.getElementById("plot").innerHTML = '<img src="' + staticFileUrl + json_response['barplot'] + '">'
        }
        
    }
    // Sending our request 
    xhr.send(JSON.stringify(request));
}

function series_oligomer_compute_form_submit(e){
    e.preventDefault();
    document.getElementById("output").innerHTML = "";
    document.getElementById("output").style.display = "none";
    document.getElementById("plot").innerHTML = "";
    console.log(this.elements[0].value);
    console.log(this.elements[1].value);
    console.log(this.elements[2].value);
    console.log(this.elements[3].value);

    couplings = this.elements[2].value.split(",").filter(function(element) {
        return element !== '';
      });
      shift_ends = this.elements[3].value.split(",").filter(function(element) {
        return element !== '';
      });
    

    request = {
    "n_low": this.elements[0].value,
    "n_high": this.elements[1].value,
    "couplings": couplings,
    "shift_ends": shift_ends
    };
    console.log(request);
    // Creating Our XMLHttpRequest object 
    let xhr = new XMLHttpRequest();

    // Making our connection  
    let url = 'http://localhost:8000/series/ocompute';
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // function execute after request is successful 
    xhr.onload = function () {
        console.log(this.responseText);
        let json_response = JSON.parse(this.responseText);
        console.log(json_response);
        
        // Display the ground state plot
        let groundStateImg = document.createElement('img');
        groundStateImg.src = staticFileUrl + json_response['ground_state_plot'];
        document.getElementById("plot").appendChild(groundStateImg);
    
        // Add a line break
        document.getElementById("plot").appendChild(document.createElement('br'));
        document.getElementById("plot").appendChild(document.createElement('br'));
    
        // Display the global minimum plot
        let globalMinImg = document.createElement('img');
        globalMinImg.src = staticFileUrl + json_response['global_min_plot'];
        document.getElementById("plot").appendChild(globalMinImg);
    }
    // Sending our request 
    xhr.send(JSON.stringify(request));
}

function genericFormEventListener(form_id, eventListenerName){
    const form = document.getElementById(form_id);
    form.addEventListener("submit", eventListenerName);
}

function dom_load_content(e){
    open_form("oligomer");
}

function allEventListeners(){

    //oligomer & series oligomer tab
    document.getElementById("oligomer_tab").addEventListener("click", function(){
        open_form("oligomer");
    });
    document.getElementById("series_oligomer_tab").addEventListener("click", function(){
        open_form("series_oligomer");
    });

    //DOM Content load event listener
    document.addEventListener('DOMContentLoaded', dom_load_content);

    

    //oligomer compute form event listener
    genericFormEventListener("oligomer_compute_form", oligomer_compute_form_submit);

    

     //series oligomer compute form event listener
     genericFormEventListener("series_oligomer_compute_form", series_oligomer_compute_form_submit);
     



}

function main(){
    allEventListeners();
}

main();