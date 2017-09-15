$(document).on('pageshow', function() {

    $activePage('.page-link').on("click",function(){
        $activePage('.menu').collapsible("option", "collapsed", true);
    });

})
