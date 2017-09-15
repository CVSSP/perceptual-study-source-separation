function Soundboard(config) {

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

        $(this).off().on ('click', function(i){

            play (i);

        }.bind (null, i));

    });

    $activePage (".soundboard-stop").off().on ('click', this.loader.stop.bind(this.loader));
}
