
$(document).ready(function() {
    // jQuery methods go here...
    $('#search_form').on('submit', function() {
        // get search query
        var query = $('#search_query').val();
        // get search type
        const type = $('#search_type').val();
        // get search results
        $('#search_results').html('').load(
            // send encoded query and type to url
            `${this.dataset.url}?q=${encodeURIComponent(query)}&type=${encodeURIComponent(type)}`);
        return false;
    });
});
