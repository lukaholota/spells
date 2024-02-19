$(document).ready(function(){
    $('.multiple-select').each(function() {
        $('option').mousedown(function(e) {
            e.preventDefault();
            var originalScrollTop = $(this).parent().scrollTop();
            $(this).prop('selected', $(this).prop('selected') ? false : true);
            var self = this;
            $(this).parent().focus();
            setTimeout(function() {
                $(self).parent().scrollTop(originalScrollTop);
            }, 0);

            return false;
        });
    });
});