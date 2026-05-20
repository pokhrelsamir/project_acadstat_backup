(function($) {
    'use strict';

    // Hide/Show semester field based on level selection
    function toggleSemesterField(clearField) {
        const levelSelect = $('#id_level');
        const semFieldRow = $('.form-row.field-semester');

        if (levelSelect.length) {
            const level = levelSelect.val();
            const isBachelor = level === 'bachelor';

            if (isBachelor) {
                semFieldRow.show();
            } else {
                semFieldRow.hide();
                if (clearField) {
                    $('#id_semester').val('');
                }
            }
        }
    }

    $(document).ready(function() {
        // Run on page load (no clearing to preserve existing data)
        toggleSemesterField(false);

        // Run when level changes (clear semester when switching away from bachelor)
        $('#id_level').change(function() {
            toggleSemesterField(true);
        });

        // Also handle for inline forms (if any)
        $(document).on('change', '.field-level select', function() {
            const row = $(this).closest('.form-row, .inline-related, .fieldset');
            const semField = row.siblings('.form-row.field-semester, .field-semester');
            const level = $(this).val();
            if (level === 'bachelor') {
                semField.show();
            } else {
                semField.hide();
                row.find('select.id_semester, select[name="semester"]').val('');
            }
        });
    });
})(django.jQuery);
