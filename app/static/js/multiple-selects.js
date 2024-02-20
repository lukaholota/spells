$(document).ready(function(){
    $('.multiple-select').each(function() {
        $(this).find('option').mousedown(function(e) {
            var originalScrollTop = $(this).parent().scrollTop();
            $(this).prop('selected', !$(this).prop('selected'));
            var self = this;
            $(this).parent().focus();
            setTimeout(function() {
                $(self).parent().scrollTop(originalScrollTop);
            }, 0);
            e.target.dispatchEvent(new Event('input', { bubbles: true }));

            return false;
        });
    });
});