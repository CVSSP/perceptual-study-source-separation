function Mushra(config) {

    console.log('MUSHRA');

    $activePage ('.ui-content').find('*').off();

    this.config = config;

    this.pageCounter = 0;
    this.numberOfSounds = 0;
    this.numberOfPages = this.config.pages.length;
    this.currentPageSoundOrder = null;

    if (this.config.add_consistency_check)
    {
        idx = randomNumber (0, this.numberOfPages, true);
        this.numberOfPages += 1;
        var newPage = JSON.parse(JSON.stringify(this.config.pages[idx]));
        newPage.name += '-duplicate';
        this.config.pages.push (newPage);
    }

    this.have_seen_this_page_before = arrayFilledWith(false, this.numberOfPages);

    // Order of pages
    this.pageOrder = fromAToBArray(0, this.numberOfPages);
    if (this.config.randomise_pages)
        shuffle(this.pageOrder);

    /* Order of sounds within page (basically a list to map from slider index to a buffer,
     where first element is first slider)
    */

    this.soundOrder = [];
    for (var i = 0; i < this.numberOfPages; ++i)
    {
        var numberOfSounds = this.config.pages[this.pageOrder[i]].sounds.length;
        var order = fromAToBArray(0, numberOfSounds);
        if (this.config.randomise_sounds_within_page)
            shuffle(order);
        this.soundOrder.push(order);
    }

    this.configureButtons();

    this.updateTitle();
    this.loadPage();
}

Mushra.prototype.configureButtons = function()
{

    $activePage('.next').removeAttr('href');

    $activePage ('.next').on("click", function (e){

        if (this.loader.haveAllBuffersPlayed() ||
            !this.config.must_play_all_samples_to_continue)
        {
            this.onNextOrBackButtonClick(1);
        }
        else
        {
            $activePage (".listen-to-all-samples-popup").popup("open");
            setTimeout(function(){
                $activePage (".listen-to-all-samples-popup").popup("close");
            }, 5000);
        }

    }.bind(this));

    $activePage ('.back').on("click", function (e){

        this.onNextOrBackButtonClick (-1);

    }.bind(this));

    // Stop audio
    $activePage ('.mushra-stop').on("click", function() {
        this.loader.stop();
    }.bind(this));

    // Reference
    $activePage ('.mushra-reference').on("click", function(){
        this.loader.play(this.numberOfSounds);
    }.bind(this));

    $activePage ('.mushra-sort').on("click", function() {
        this.sortSliders();
    }.bind(this));
}

Mushra.prototype.onNextOrBackButtonClick = function (direction)
{
    // Stop any audio
    if (this.loader)
        this.loader.stop();

    if (this.pageCounter == 0 && direction < 0)
    {
        if (this.config.back_button_can_exit_test)
            window.history.back();
    }
    else
    {
        $activePage ('.back').show();

        this.fillConfig();

        this.pageCounter = selectMinimum (this.pageCounter + direction,
                                          this.numberOfPages);

        this.pageCounter = selectMaximum (this.pageCounter, 0);

        // Complete or not
        if (this.pageCounter == this.numberOfPages)
        {
            this.complete();
            this.pageCounter -= 1;
        }
        else
        {
            this.updateTitle();
            this.loadPage();
        }
    }
}

Mushra.prototype.updateTitle = function()
{
    $activePage ('.title').html ((this.pageCounter + 1) + ' / ' +
                                 this.numberOfPages);
}

Mushra.prototype.loadPage = function()
{

    this.currentPage = this.pageOrder[this.pageCounter];
    this.currentPageSoundOrder = this.soundOrder[this.pageCounter];
    console.log('Slider -> buffer indices: ', this.currentPageSoundOrder);
    this.numberOfSounds = this.currentPageSoundOrder.length;

    this.urls = new Array(this.numberOfSounds);

    for (var i = 0; i < this.numberOfSounds; ++i)
    {
        var thisSound = this.config.pages[this.currentPage].sounds[i];
        this.urls[i] = this.config.siteURL + '/' + thisSound.url;
    }

    // Add the url to the reference audio. No need to store id here.
    this.urls.push(
        this.config.siteURL + '/' + this.config.pages[this.currentPage].reference_url);

    // Configure the audio loader
    this.loader = new AudioLoader(this.urls,
                                  this.config.continuous_playback,
                                  this.config.loop_playback);

    $activePage ('.mushra-container').hide();
    this.loader.load (this.setupGUI.bind(this));
}

Mushra.prototype.setupGUI = function()
{
    $activePage ('.mushra-container').show();

    this.createSliders();

    if (!this.have_seen_this_page_before[this.pageCounter])
        this.have_seen_this_page_before[this.pageCounter] = true;
}

Mushra.prototype.createSliders = function()
{
    $activePage ('.mushra-slider-container').empty();

    for (var i = 0; i < this.numberOfSounds; ++i)
    {
        var startVal = 0;
        if (this.have_seen_this_page_before[this.pageCounter])
            startVal = this.config.pages[this.currentPage].sounds[this.currentPageSoundOrder[i]].rating;
        else if (this.config.randomise_slider_handle)
            startVal = randomNumber(0, 100, true);

        // The slider, triggers audio when user makes adjustment.
        var inputHTML = "<input type='range' name='slider' " +
        "value='" + startVal + "' min='0' max='100' step='1' class='ui-hidden-accessible' ";

        if (this.config.show_number_on_slider)
            inputHTML += "data-show-value='true'/>";
        else
            inputHTML += "/>";

        $activePage ('.mushra-slider-container').append(inputHTML);
    }

    $activePage ('.mushra-slider-container').trigger('create');
    $activePage ('.mushra-slider-container').enhanceWithin();

    var mainObj = this;

    $activePage (".ui-slider").each(function (i) {

        // A filthy hack to give a more resticted response when the user clicks
        $(this).find('.ui-slider-handle').on('start', function(){

            var input = $(this).find('input');
            input.attr('step', input.val());
            setTimeout(function () {input.attr('step', 1)}, 50);

        }.bind(this));

        $(this).off().on('slidestart', function (i) {

            //$(this).find('input').val($(this).find('input').val()).slider('refresh');

            // play this audio file
            mainObj.playBuf (i);

            // change handle colour when slider is moved
            $(this).find('.ui-slider-handle').addClass('slider-handle-active');
            // Give focus to the handle even if handle is clicked
            $(this).find('.ui-slider-handle').focus();

        }.bind(this, i));

        // Remove annoying popup displaying the value of the slider
        $(this).find('.ui-slider-handle').removeAttr('title');
        $(this).on('slidestop', function () {

            $(this).find('.ui-slider-handle').removeAttr('title');

        }.bind(this));

    });

}

Mushra.prototype.playBuf = function (i)
{
    this.loader.play (this.currentPageSoundOrder[i]);
}

Mushra.prototype.sortSliders = function()
{
    this.loader.stop();

    var values = [];
    $activePage (".ui-slider input").each (function (i) {
        values.push (parseInt ($(this).val()));
    });

    var indices = indicesNeededToSortArray (values);

    var mainObj = this;
    var tempOrder = this.currentPageSoundOrder.slice();

    $activePage (".ui-slider").each (function (i) {

        mainObj.currentPageSoundOrder[i] = tempOrder[indices[i]];

        var idx = mainObj.currentPageSoundOrder[i];

        if (mainObj.loader.hasPlayed[idx])
            $(this).find('.ui-slider-handle').addClass('slider-handle-active');
        else
            $(this).find('.ui-slider-handle').removeClass('slider-handle-active');

        $(this).find('input').val(values[indices[i]]).slider('refresh');

        $(this).find('.ui-slider-handle').removeAttr('title');
    });

    console.log('Slider -> buffer indices: ', this.currentPageSoundOrder);
}

Mushra.prototype.fillConfig = function()
{
    var setRating = function(i, value) {
        this.config.pages[this.currentPage].sounds[this.currentPageSoundOrder[i]].rating = value;
    }.bind(this);

    if ((this.config.pages[this.currentPage].duration == undefined) & (this.loader.timerStarted))
        this.config.pages[this.currentPage].duration = this.loader.endTimer();

    this.config.pages[this.currentPage].order = this.pageCounter;

    $activePage (".ui-slider input").each( function (i) {
        setRating (i, $(this).val());
    });
}

Mushra.prototype.complete = function()
{
    // Build an array of arrays for the ratings
    var values = '';
    var times = '';
    var sounds = '';
    var pages = '';
    var pageOrder = '';

    for (var i = 0; i < this.numberOfPages; ++i)
    {
        var numSounds = this.config.pages[i].sounds.length;

        for (var j = 0; j < numSounds; ++j)
        {
            values += this.config.pages[i].sounds[j].rating;
            sounds += this.config.pages[i].sounds[j].name;

            if (j < numSounds - 1)
            {
                values += this.config.separator;
                sounds += this.config.separator;
            }
        }

        var appendThis = '';
        if (i < this.numberOfPages - 1)
            var appendThis = this.config.line_terminator;

        pages += this.config.pages[i].name + appendThis;
        pageOrder += this.config.pages[i].order + appendThis;
        times += this.config.pages[i].duration + appendThis;
        values += appendThis;
        sounds += appendThis;
    }

    console.log('values: ', values);
    console.log('times: ', times);
    console.log('sounds: ', sounds);
    console.log('pages: ', pages);
    console.log('page order: ', pageOrder);

    if (this.config.allow_submission)
    {
        $activePage ('input[name="fields[data]"]').val (values);
        $activePage ('input[name="fields[sounds]"]').val (sounds);
        $activePage ('input[name="fields[pages]"]').val (pages);
        $activePage ('input[name="fields[page_order]"]').val (pageOrder);
        $activePage ('input[name="fields[page_response_time]"]').val (times);
        $activePage ('.submit-popup').popup ('open');
    }
    else{
        $.mobile.changePage (this.config.nextURL);
    }
}
