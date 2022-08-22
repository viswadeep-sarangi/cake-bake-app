function formSubmit(formName, postURL, resultsTag){
    var formData= $(formName).serializeArray();
    console.log(formData);
    var formJson = {}
    jQuery.each( formData, function( i, field ) {
        console.log(field.name);                   
        console.log(field.value);
        console.log()
        formJson[field.name]=field.value
    });

    var formJsonString = JSON.stringify(formJson)
    $(resultsTag).text(formJsonString);
    console.log(formJsonString);
    $.ajax({
        type: "POST",
        url: postURL,
        data: formJsonString,
        success: function(respStr){
            alert(respStr['message'])
        },
        contentType : "application/json"
    });
    return false;
}