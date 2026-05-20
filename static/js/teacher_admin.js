// Teacher admin JS: Show/hide semesters field based on selected education levels
(function($) {
    function updateSemesterFieldVisibility() {
        // Get selected level values from the 'to' multiple select (chosen options)
        var $levelsTo = $('#id_levels_to');
        if ($levelsTo.length === 0) {
            // Fallback: try the regular id_levels element if using standard select
            $levelsTo = $('#id_levels');
        }
        var selected = [];
        if ($levelsTo.length) {
            selected = $levelsTo.val() || [];
        }

        // Check if 'bachelor' is in selected
        var hasBachelor = selected.includes('bachelor');

        // Show/hide semesters fieldset
        var $semestersRow = $('.field-semesters');
        if ($semestersRow.length) {
            if (hasBachelor) {
                $semestersRow.show();
                // Optionally make semesters required by adding a flag
            } else {
                $semestersRow.hide();
                // Optionally clear selection? No, keep as is.
            }
        }
    }

    $(document).ready(function() {
        // Run on load
        updateSemesterFieldVisibility();

        // Bind change event to the levels 'to' select (the chosen box)
        var $levelsTo = $('#id_levels_to');
        if ($levelsTo.length) {
            $levelsTo.change(updateSemesterFieldVisibility);
        } else {
            // Also try binding to the main select if filter_horizontal not used
            $('#id_levels').change(updateSemesterFieldVisibility);
        }

        // Additionally, listen to add/remove button clicks for the filter_horizontal widget
        // The widget triggers DOMNodeInserted/removed? But change event on select should catch updates.
    });
})(django.jQuery);
