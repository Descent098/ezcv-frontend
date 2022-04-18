// Display metadata
function displayMetadata(metadata){
    metadata_div = document.getElementById("metadata")
    metadata_form = document.getElementById("metadataForm")

    for (var key in metadata) {
        console.log(`${key}: ${metadata[key]}`);
        if ( typeof metadata[key] === "boolean" || metadata[key].toLowerCase() =="true" || metadata[key].toLowerCase() =="false" ){ // Booleans
            if (typeof metadata[key] === "boolean"){
                metadata[key] = metadata[key].toString()
            }
            if (metadata[key].toLowerCase() =="true"){
                checked = "checked"
            } else {
                checked = ""
            }
            metadata_form.innerHTML += `<div class="form-group"><label for="${key}">${key}</label><input type="checkbox" class="form-control" id="${key}" name="${key}" ${checked}></div>`
        } else if (isNumber(metadata[key])){   // Numbers
            metadata_form.innerHTML += `<div class="form-group"><label for="${key}">${key}</label><input type="number" class="form-control" id="${key}" name="${key}" value="${metadata[key]}"></div>`
        } else { // Strings
        metadata_form.innerHTML += `<div class="form-group row">
                <label for="${key}" class="col-4 col-form-label">${key}</label> 
                <div class="col-8">
                    <input id="${key}" name="${key}" value="${metadata[key]}" type="text" class="form-control">
                </div>
            </div>`
    }
} // End of key iteration
};

function getMetadataAsJSON(){// TODO
    data = {};
    
    metadata_form = document.getElementById("metadataForm");
    // const formEntries = new FormData(metadata_form).entries();
    // const formData = Object.assign(...Array.from(formEntries, ([name, value]) => ({[name]: value})));
    const formData = serializeForm(metadata_form);
    // console.log(formData);
    for (var index in formData) {
        data[formData[index]["name"]] = formData[index]["value"];
    }
    console.log(data)
    return data
}

function isNumber(num){
    // Checks if num is a number (or entirely numbers)
    if (typeof num === 'boolean') {
        return false
    }
    return !isNaN(num)
}