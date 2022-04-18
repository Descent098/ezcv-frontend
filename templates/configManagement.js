// Display config
function displayconfig(config){
    config_div = document.getElementById("config")
    config_form = document.getElementById("configForm")

    for (var key in config) {
        console.log(`${key}: ${config[key]}`);
        if ( typeof config[key] === "boolean" || config[key].toLowerCase() =="true" || config[key].toLowerCase() =="false" ){ // Booleans
            if (typeof config[key] === "boolean"){
                config[key] = config[key].toString()
            }
            if (config[key].toLowerCase() =="true"){
                checked = "checked"
            } else {
                checked = ""
            }
            config_form.innerHTML += `<div class="form-group"><label for="${key}">${key}</label><input type="checkbox" class="form-control" id="${key}" name="${key}" ${checked}></div>`
        } else if (key == "theme"){
            optionsHTML = themeSelector(config[key]);
            config_form.innerHTML += `<div class="form-group"><label for="${key}">${key}</label><select class="form-control" id="${key}" name="${key}"> ${optionsHTML}</select></div>`
        }else if (isNumber(config[key])){   // Numbers
            config_form.innerHTML += `<div class="form-group"><label for="${key}">${key}</label><input type="number" class="form-control" id="${key}" name="${key}" value="${config[key]}"></div>`
        } else { // Strings
        config_form.innerHTML += `<div class="form-group row">
                <label for="${key}" class="col-4 col-form-label">${key}</label> 
                <div class="col-8">
                    <input id="${key}" name="${key}" value="${config[key]}" type="text" class="form-control">
                </div>
            </div>`
    }
} // End of key iteration


};


function themeSelector(theme){

    themes = ["aerial", "creative", "cv", "dimension", "ethereal", "freelancer", "grayscale", "identity", "lens", "paradigm_shift","read_only",  "solid_state", "strata"];
    themeHTML = "";
    for (var i = 0; i < themes.length; i++) {
        if (themes[i] == theme){
            themeHTML += `<option value="${themes[i]}" selected>${themes[i]}</option>`;
        } else {
            themeHTML += `<option value="${themes[i]}">${themes[i]}</option>`;;
        }
    }
    return themeHTML
}



function getconfigAsJSON(){// TODO
    data = {};
    
    config_form = document.getElementById("configForm");
    // const formEntries = new FormData(config_form).entries();
    // const formData = Object.assign(...Array.from(formEntries, ([name, value]) => ({[name]: value})));
    const formData = serializeForm(config_form);
    // console.log(formData);
    for (var index in formData) {
        data[formData[index]["name"]] = formData[index]["value"];
    }
    console.log(data)
    return data
}
function serializeCurrentContent() {
    // Serialize the current content of the config
    var config = getconfigAsJSON();


    fetch("/config", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(config)
    }).then(res => {
        console.log("Request complete! response:", res);
        window.location.reload();
    });

    // console.log(content_json)
    // return content_json;
}

function isNumber(num){
    // Checks if num is a number (or entirely numbers)
    return !isNaN(num)
}