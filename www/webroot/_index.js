$(document).ready(function () {
    var userLang = navigator.language || navigator.userLanguage;
    var shortLang = userLang.slice(0, 2);
    var supported_languages = ['it', 'de', 'fr', 'en']
    var lang_domain = 'en';

    if (supported_languages.includes(shortLang)) {
        lang_domain = shortLang
    }
    if (location.host === "www.{{ domain() }}") {
        window.location.href = "{{ scheme() }}://" + lang_domain + ".{{ domain() }}";
        return;
    }
    if (location.host === "0.0.0.0:8080") {
        window.location.href = "{{ scheme() }}://" + lang_domain + ".localhost:8080";
        return;
    }
    $.ajax({
        url: "/api/provider/stats",
        success: showResponse,
        //error: showError,
        dataType: "json"
    });

    function showResponse(responseText, statusText, xhr, $form) {
        $("#provider_count").text(responseText.providers_count);
        $("#help_requests_count").text(responseText.help_requests_count);
    }
    function showError(responseText, statusText, xhr, $form) {
        alert("error"+xhr);
        $("#provider_count").text(responseText.providers_count);
    }

});