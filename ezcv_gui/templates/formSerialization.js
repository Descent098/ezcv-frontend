var serializeForm = (function (slice) { /// from https://stackoverflow.com/questions/30964568/how-to-get-a-key-value-data-set-from-a-html-form
return function (form) {
    //no form, no serialization
    if (form == null)
        return null;

    //get the form elements and convert to an array
    return slice.call(form.elements)
        .filter(function (element) {
            //remove disabled elements
            return !element.disabled;
        }).filter(function (element) {
            //remove disabled elements
            return element.name!=null && element.name!="" && element.name!="next" && element.name != "previous" && element.name!="submit";
        }).filter(function (element) {
            //remove <select multiple> elements with no values selected
            return !/^select$/i.test(element.tagName) || element.selectedOptions.length > 0;
        }).map(function (element) {
            switch (element.tagName.toLowerCase()) {
                case 'checkbox':
                    console.log(`checkbox is ${element.checked}`);
                    return {
                        name: element.name,
                        value: element.checked
                    };
                case 'radio':
                    console.log(`radio is ${element.checked}`);
                    return {
                        name: element.name,
                        value: element.value === null ? true : false
                    };
                case 'select':
                    if (element.multiple) {
                        return {
                            name: element.name,
                            value: slice.call(element.selectedOptions)
                                .map(function (option) {
                                    return option.value;
                                })
                        };
                    }

                    return {
                        name: element.name,
                        value: isNumber( element.value) ? parseInt(element.value) : element.value
                    };
                default:
                    if (element.type =="number"){
                        return {
                            name: element.name,
                            value: parseInt(element.value)
                        };
                    } else if (element.type == "checkbox"){
                        return {
                            name: element.name,
                            value: element.checked
                        };
                    }
                    
                    else {
                        return {
                            name: element.name,
                            value: element.value
                        };
                    };
            }
        });
}
}(Array.prototype.slice));

function isNumber(num){
    // Checks if num is a number (or entirely numbers)
    return !isNaN(num)
}