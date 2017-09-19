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
    this.onsetTime = null;
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
        this.switchStop();

        console.log('Playing index: ', index);

        // get an AudioBufferSourceNode for playing our buffer
        this.source = audioContext.createBufferSource();

        // buffer config
        var buf = this.buffers[index];
        this.source.buffer = buf;
        this.source.loop = this.loopPlayback;
        this.source.loopStart = false;

        if (!this.loopPlayback)
        {
            this.source.onended = function() {
                if (this.currentIndex == index)
                    this.currentIndex = null;
            }.bind(this);
        }

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

        console.log('time: ', this.onsetTime);

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

AudioLoader.prototype.switchStop = function () {
    this.stop (false);
}

AudioLoader.prototype.stop = function(resetStartPosition=true) {

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

        if (resetStartPosition)
            this.currentIndex = null;
    }
}

AudioLoader.prototype.haveAllBuffersPlayed = function () {
    return this.hasPlayed.every(function (bool) {return bool})
}
