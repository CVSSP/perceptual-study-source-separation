$(document).on('pageshow', function() {

    $activePage('.page-link').on("click",function(){
        $activePage('.menu').collapsible("option", "collapsed", true);
    });

})

$(document).on('pageshow', function (e) {
    if (window.history.length == 1 || $.mobile.navigate.history.activeIndex == 0)
        $activePage ('.back').hide();
});

function fromAToBArray(a, b)
{
    if (b <= a)
        b = a + 1;

    var n = b - a;
    var array = new Array(n);
    for (var i = 0; i < n; ++i)
        array[i] = a + i;

    return array;
}

function arrayFilledWith(value, size)
{
    var array = new Array(size);
    for (var i = 0; i < size; ++i)
        array[i] = value;
    return array;
}

function randomNumber(min, max, shouldRound)
{
    var val = Math.random();
    var range = max - min;
    val *= range;
    val += min;

    if (shouldRound)
        val = Math.floor (val)
    return val;
}

/**
 * Shuffles array in place.
 * @param {Array} a items The array containing the items.
 * From: https://stackoverflow.com/questions/6274339/how-can-i-shuffle-an-array
 */
function shuffle(a) {
    var j, x, i;
    for (i = a.length; i; i--) {
        j = Math.floor(Math.random() * i);
        x = a[i - 1];
        a[i - 1] = a[j];
        a[j] = x;
    }
}

function selectMaximum (a, b)
{
    if (a > b)
        return a;
    else
        return b;
}

function selectMinimum (a, b)
{
    if (a < b)
        return a;
    else
        return b;
}


/** JQM **/
/* Wrapper for selecting elements on active page:
https://forum.jquery.com/topic/usage-of-ids-impossible
*/
function $activePage(query='') {return $('.ui-page-active ' + query);}

/*
 * AudioLoader
 */

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext = new AudioContext();

function AudioLoader(urlList, continuousPlayback=true, loopPlayback=true) {

    this.urlList = urlList;
    this.buffers = arrayFilledWith(null, urlList.length);

    this.gainNodes = [audioContext.createGain(), audioContext.createGain()]
    this.gainNodeIndex = 0;

    for (var i = 0; i < 2; ++i)
    {
        this.gainNodes[i].connect(audioContext.destination);
        this.gainNodes[i].gain.value = 0.0;
    }

    this.startedPlayingAtTime = null;
    this.fadeTime = 0.1;
    this.currentIndex = null;
    this.onsetTime = 0;
    this.continuousPlayback = continuousPlayback;
    this.loopPlayback = loopPlayback;
    this.hasPlayed = []
    this.allOk = false;
}

AudioLoader.prototype.loadBuffer = function (url, index, callBack=null) {

    console.log('Loading ', url, ' (index: ', index, ')');

    // Load buffer asynchronously
    var request = new XMLHttpRequest();
    request.responseType = "arraybuffer";
    request.open("GET", url, true);

    var loader = this;

    request.onload = function() {

        // Asynchronously decode the audio file data in request.response
        audioContext.decodeAudioData(request.response,
            function(buffer) {

                if (!buffer) {
                    alert('error decoding file data: ' + url);
                    return;
                }

                loader.buffers[index] = buffer;
                loader.checkBuffers (callBack);
            },

            function(error) {
                console.error('decodeAudioData error', error);
            }

        );
    }

    request.send();

    this.hasPlayed.push(false);
}


AudioLoader.prototype.checkBuffers = function(callBack) {

    this.allOk = true;
    for (var i = 0; i < this.buffers.length; ++i)
    {
        if (this.buffers[i] == null)
            this.allOk = false;
    }

    if (this.allOk)
    {
        $.mobile.loading ('hide');
        if (typeof callBack == 'function')
            callBack();
    }
}

AudioLoader.prototype.load = function(callBack=null) {

    $.mobile.loading ('show');

    this.allOk = false;
    for (var i = 0; i < this.urlList.length; ++i)
        this.loadBuffer (this.urlList[i], i, callBack);

    this.timerStarted = false;
}

AudioLoader.prototype.play = function (index=0, loop=false) {

    if ((index != this.currentIndex) && this.allOk)
    {
        this.stop();

        console.log('Playing index: ', index);

        // get an AudioBufferSourceNode for playing our buffer
        this.source = audioContext.createBufferSource();

        // buffer config
        var buf = this.buffers[index];
        this.source.buffer = buf;
        this.source.loop = this.loopPlayback;
        this.source.loopStart = false;

        if (!this.loopPlayback)
            this.source.onended = this.resetContinuousPlay.bind(this);

        // ramping
        var currentGainNode = this.gainNodes[this.gainNodeIndex];
        this.source.connect(currentGainNode);

        // Playhead calculation (but not sample accurate)
        if (this.continuousPlayback)
        {
            if (this.currentIndex == null)
            {
                this.onsetTime = 0;
            }
            else
            {
                var prevBufDuration = this.buffers[this.currentIndex].duration;
                this.onsetTime += (audioContext.currentTime - this.startedPlayingAtTime);

                if (this.onsetTime > prevBufDuration)
                    this.onsetTime = this.onsetTime % prevBufDuration;

                if (this.onsetTime > buf.duration)
                    this.onsetTime = 0;
            }
        }

        this.hasPlayed[index] = true;
        this.currentIndex = index;
        this.startedPlayingAtTime = audioContext.currentTime;

        this.startTimer();

        this.source.start(0, this.onsetTime);
        currentGainNode.gain.linearRampToValueAtTime(
            1.0, audioContext.currentTime + this.fadeTime);

    }
}

AudioLoader.prototype.startTimer = function ()
{
    if (!this.timerStarted)
    {
        this.startTime = audioContext.currentTime;
        this.timerStarted = true;
    }
}

AudioLoader.prototype.endTimer = function ()
{
    this.timerStarted = false;
    return audioContext.currentTime - this.startTime;
}

AudioLoader.prototype.stop = function() {

    if (this.source)
    {
        console.log('Stopping index: ', this.currentIndex);

        var whenToStop = audioContext.currentTime + this.fadeTime;

        var currentGainNode = this.gainNodes[this.gainNodeIndex];
        currentGainNode.gain.linearRampToValueAtTime(0.0,
                                                     whenToStop);

        this.source.stop(whenToStop);

        this.gainNodeIndex = (this.gainNodeIndex + 1) % 2;
        this.source = null;

        this.currentIndex = null;
    }
}

AudioLoader.prototype.haveAllBuffersPlayed = function () {
    return this.hasPlayed.every(function (bool) {return bool})
}

function Soundboard(config) {

    $activePage ('.ui-content').find('*').off();

    // Grab audio urls relative to site url
    urls = [];
    for (var i = 0; i < config.rows.length; ++i)
    {
        for (var j = 0; j < config.rows[i].sounds.length; ++j)
        {
            var thisSound = config.rows[i].sounds[j];
            urls.push(config.siteURL + '/' + thisSound.url);
        }
    }

    // Configure the audio loader
    this.loader = new AudioLoader(urls,
                                  config.continuous_playback,
                                  config.loop_playback)
    this.loader.load();

    // Configure play buttons:

    var play = function (i) {
        this.loader.play (i);
    }.bind(this);

    $activePage (".soundboard-play").each (function (i) {

        $(this).on ('click', function(i){

            play (i);

        }.bind (null, i));

    });

    $activePage (".soundboard-stop").on ('click', this.loader.stop.bind(this.loader));

    $activePage ('.next').on("click", this.loader.stop.bind(this.loader));
    $activePage ('.prev').on("click", this.loader.stop.bind(this.loader));
}

function Mushra(config) {

    console.log('MUSHRA');

    $activePage ('.ui-content').find('*').off();

    this.config = config;

    this.pageCounter = 0;
    this.numberOfSounds = 0;
    this.numberOfPages = this.config.pages.length;

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

    // Order of sounds within page
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
        console.log(this.loader);
        this.loader.play(this.numberOfSounds);
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
            if (this.config.allow_submission)
            {
                this.complete();
                this.pageCounter -= 1;
            }
            else
                $.mobile.changePage (this.config.nextURL);
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
    this.numberOfSounds = this.currentPageSoundOrder.length;

    this.urls = new Array(this.numberOfSounds);

    for (var i = 0; i < this.numberOfSounds; ++i)
    {
        var thisSound = this.config.pages[this.currentPage].sounds[this.currentPageSoundOrder[i]];
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
        "value='" + startVal + "' min='0' max='100' class='ui-hidden-accessible'";

        if (this.config.show_number_on_slider)
            inputHTML += "data-show-value='true'/>";
        else
            inputHTML += "/>";

        $activePage ('.mushra-slider-container').append(inputHTML);
    }

    $activePage ('.mushra-slider-container').trigger('create');
    $activePage ('.mushra-slider-container').enhanceWithin();

    // Play audio when slider is moved
    var playFunc = function (i) {
            this.loader.play(i)
    }.bind(this);

    $activePage (".ui-slider").each(function (i) {

        $(this).on('slidestart', function (i) {

            // play this audio file
            playFunc (i);
            // change handle colour when slider is moved
            $(this).find('a').addClass('slider-handle-active');
            // Give focus to the handle even if handle is clicked
            $(this).find('a').focus();

        }.bind(this, i));
    });
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
    var values = '[';
    var times = '[';
    var sounds = '[';
    var pages = '[';
    var pageOrder = '[';

    for (var i = 0; i < this.numberOfPages; ++i)
    {
        values += '[';
        sounds += '[';

        var numSounds = this.config.pages[i].sounds.length;

        for (var j = 0; j < numSounds; ++j)
        {
            values += this.config.pages[i].sounds[j].rating;
            sounds += this.config.pages[i].sounds[j].name;

            if (j == numSounds - 1)
            {
                values += ']';
                sounds += ']';
            }
            else
            {
                values += ',';
                sounds += ',';
            }
        }

        pages += this.config.pages[i].name;
        pageOrder += this.config.pages[i].order;
        times += this.config.pages[i].duration;

        if (i == this.numberOfPages - 1)
        {
            pages += ']';
            pageOrder += ']';
            times += ']';
            values += ']';
            sounds += ']';
        }
        else
        {
            pages += ',';
            pageOrder += ',';
            times += ',';
            values += '],';
            sounds += '],';
        }
    }

    console.log('values: ', values);
    console.log('times: ', times);
    console.log('sounds: ', sounds);
    console.log('pages: ', pages);
    console.log('page order: ', pageOrder);

    // Append inputs to the form
    $('<input>').attr({
            type: 'hidden',
            name: 'fields[data]',
            value: values,
        }).appendTo ('div.submit-popup > form');

    $('<input>').attr({
            type: 'hidden',
            name: 'fields[sounds]',
            value: sounds,
        }).appendTo ('div.submit-popup > form');

    $('<input>').attr({
            type: 'hidden',
            name: 'fields[pages]',
            value: pages,
        }).appendTo ('div.submit-popup > form');

    $('<input>').attr({
            type: 'hidden',
            name: 'fields[page_order]',
            value: pageOrder,
        }).appendTo ('div.submit-popup > form');

    $activePage ('.submit-popup').popup('open');
}

