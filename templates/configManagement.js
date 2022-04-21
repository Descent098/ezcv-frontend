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



// Display config
function displayconfig(config){
    config_div = document.getElementById("config")
    config_form = document.getElementById("configForm")
    checkboxesHTML = "";
    selectHTML = "";
    textHTML = "";
    numberHTML = "";
    for (var key in config) {
        if (config[key] ===""){
            textHTML += getConfigFormField(key, config[key], "text");
        } else if ( typeof config[key] === "boolean" || config[key].toLowerCase() =="true" || config[key].toLowerCase() =="false" ){ // Booleans
            checkboxesHTML += getConfigFormField(key, config[key], "boolean");
        } else if (key == "theme"){
            selectHTML += getConfigFormField(key, config[key], "theme");
        }else if (isNumber(config[key])){   // Numbers
            numberHTML += getConfigFormField(key, config[key], "number");
        } else { // Strings
        textHTML += getConfigFormField(key, config[key], "text");
    }
    config_form.innerHTML =  textHTML + numberHTML + checkboxesHTML + selectHTML;
} // End of key iteration


};

function getConfigFormField(key, value, type){
    switch (type) {
        case "text":
            return `<div class="form-group col-md-6" style="position: static;">
            <label for="input-text-1">${key}</label>
            <input type="text" class="form-control" id="${key}" name="${key}" value="${value}">
        </div>`
        case "number":
            return `<div class="form-group col-md-3" style="position: static;">
            <label for="input-text-1">${key}</label>
            <input type="number" class="form-control" id="${key}" name="${key}" value="${value}">
            
        </div>`
        case "boolean":
            if (typeof value === "boolean"){
                value = value.toString()
            }
            if (value.toLowerCase() =="true"){
                checked = "checked"
            } else {
                checked = ""
            }
            return `<div class="checkbox col-md-3" style="position: static;">
                <label>
                    <input type="checkbox" id="${key}" name="${key}" ${checked}> <span style="font-size:X-Large">${key}</span>
                </label>
            </div>`
        case "theme":
            optionsHTML = themeSelector(value);
            return `<div class="form-group col-md-12" style="position: static;">
            <label for="select-1">Theme</label>
            <select class="form-control" id="theme" name="theme">${optionsHTML}</select>
            </div>`
        default:
            return `<div class="form-group col-md-6" style="position: static;">
            <label for="input-text-1">${key}</label>
            <input type="text" class="form-control" id="${key}" name="${key}" value="${value}">
        </div>`
    }
}
