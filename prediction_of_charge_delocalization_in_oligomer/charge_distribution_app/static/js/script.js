function open_form(formName) {
    var i;
    var x = document.getElementsByClassName("tabcontent");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    document.getElementById(formName).style.display = "block";
}

function oligomer_compute_form_submit(e){
    e.preventDefault();
    document.getElementById("output").innerHTML = "";
    document.getElementById("output").style.display = "block";
    document.getElementById("plot").innerHTML = "";
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
    // Creating Our XMLHttpRequest object 
    let xhr = new XMLHttpRequest();

    // Making our connection  
    let url = window.location.href +'/ocompute';
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // function execute after request is successful 
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            
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
            //formatted_response = "<p>" +  + "</p>"
            if (json_response['status'] === "Solved"){
                document.getElementById("output").innerHTML = formatted_response;
                const charge_plot = document.createElement('img');

                if (!json_response.charge_dist && !json_response.global_min_plot){
                    alert('no images found in response');
                }

                else {
                    if (json_response.charge_dist) {
                        // Display the Base64-encoded images
                        charge_plot.src = `data:image/png;base64,${json_response.charge_dist}`;
                        charge_plot.alt = 'Image';
                        imagesContainer = document.getElementById("plot")
                        imagesContainer.appendChild(charge_plot);
                    }

                    else {
                        alert('Charge Distribution plot image not found in the response');
                    }


                    if(json_response.global_min_plot) {
                        // Display the global minimum plot
                        let global_min_plot = document.createElement('img');
                        global_min_plot.src = `data:image/png;base64,${json_response.global_min_plot}`;
                        global_min_plot.alt = 'Generated Image';
                        document.getElementById("plot").appendChild(global_min_plot);
                    }
                    else {
                        alert('global mininmum plot image  not found in response');
                    }

                }
        

                
            }

            else {
                alert("Unable to solve Oligomer. Please try with different values.");
            }
        }

        else {
            alert("Error in the response. Please try again.");
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
    // Creating Our XMLHttpRequest object 
    let xhr = new XMLHttpRequest();

    // Making our connection  
    let url = window.location.href + '/series/ocompute';
    xhr.open("POST", url, false);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

    // function execute after request is successful 
    xhr.onload = function () {
        let json_response = JSON.parse(this.responseText);

        if (!json_response.global_min_plot && !json_response.ground_state_plot){
            alert('no images found in response');
        }

        else {
            if (json_response.ground_state_plot) {
                // Display the ground state plot
                let ground_state_plot = document.createElement('img');
                ground_state_plot.src = `data:image/png;base64,${json_response.ground_state_plot}`;
                ground_state_plot.alt = 'Generated Image';
                document.getElementById("plot").appendChild(ground_state_plot);
            
                // Add a line break
                document.getElementById("plot").appendChild(document.createElement('br'));
                document.getElementById("plot").appendChild(document.createElement('br'));
            }
            else {
                alert('ground state plot image  not found in response');
            }
            
            if (json_response.global_min_plot){
                // Display the global minimum plot
                let global_min_plot = document.createElement('img');
                global_min_plot.src = `data:image/png;base64,${json_response.global_min_plot}`;
                global_min_plot.alt = 'Generated Image';
                document.getElementById("plot").appendChild(global_min_plot);
    
            } 
            else {
                alert('global mininmum plot image  not found in response');
            }
        }        
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
