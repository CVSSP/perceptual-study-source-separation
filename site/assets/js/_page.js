$(document).on('pageshow', function (e) {
    if (window.history.length == 1 || $.mobile.navigate.history.activeIndex == 0)
        $activePage ('.back').hide();
});

// http://jonnyreeves.co.uk/2012/listening-for-jquery-mobile-slider-events/
$(document).on({
    "mousedown touchstart": function () {
        $(this).trigger('start');
    },
    "mouseup touchend": function () {
        $(this).trigger('stop');
    }
}, ".ui-slider-handle");
