$(document).ready(function() {
    function setupAutocomplete(elementId, url) {
        $('#' + elementId).select2({
            ajax: {
                url: url,
                dataType: 'json',
                delay: 250,
                data: function(params) {
                    return {
                        q: params.term // search term
                    };
                },
                processResults: function(data) {
                    return {
                        results: data.results
                    };
                },
                cache: true
            },
            minimumInputLength: 1,
            theme: 'classic'
        });
    }

    setupAutocomplete('title', '{% url "service-autocomplete" %}');
    setupAutocomplete('category', '{% url "category-autocomplete" %}');
    setupAutocomplete('tag', '{% url "tag-autocomplete" %}');
});
