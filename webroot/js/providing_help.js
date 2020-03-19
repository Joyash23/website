// wait for the DOM to be loaded
$(function() {
    var options = {
        success:       showResponse,  // post-submit callback
        error:         showError,
    }
    // bind 'myForm' and provide a simple callback function
    $('#myForm').ajaxForm(options);

    // post-submit callback 
    function showResponse(responseText, statusText, xhr, $form)  {
        $("#failed").hide("slow");
        $("#myForm").hide("slow");
        $("#success").show("slow")
    }

    function showError(responseText, statusText, xhr, $form)  {
        $("#failed").show("slow");
    }
});
