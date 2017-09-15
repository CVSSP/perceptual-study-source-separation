$(document).on('pageshow', function (e) {
    if (window.history.length == 1 || $.mobile.navigate.history.activeIndex == 0)
        $activePage ('.back').hide();
});
