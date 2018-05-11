function setupTypeahead() {
    /* Firefox handles the enter correctly */
    $("#pkgsearch-field").keyup(function(e) {
         if (e.which == 13) {
              $("#pkgsearch-form").submit();
         }
    });

    /* Chrome does not handle the enter, so change has to be used */
    $("#pkgsearch-field").change(function(e) {
         $("#pkgsearch-form").submit();
    });

    $("#pkgsearch-field").on("input", function(e) {
        var query = $(this).val();
        if (query === "") {
            return;
        }

        $.getJSON('/opensearch/packages/suggest', {q: query}, function(data) {
            const results = $("#searchresults");
            results.empty();
            data = data[1];
            data.forEach(function(result) {
                 $("<option/>").html(result).appendTo(results);
            });
        });
    });
}
