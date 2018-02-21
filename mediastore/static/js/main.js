(function() {
    navigator.getUserMedia = navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia;

    var recorder;
    var ctx;

    function startStream(stream) {
        var input = ctx.createMediaStreamSource(stream);
        recorder = new Recorder(input);
    }

    window.startRecording = function(button) {
        recorder && recorder.record();
    }

    window.stopRecording = function(button) {
        recorder && recorder.stop();
        recorder.exportWAV(function(blob) {
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/media");
            xhr.setRequestHeader('Content-type', 'application/octet-stream');
            xhr.send(blob);
        });
    }

    if (navigator.getUserMedia) {
        ctx = new (window.AudioContext || window.webkitAudioContext)();
        navigator.getUserMedia({ audio: true }, startStream, function(e) {
            console.log("Error: " + e);
        });
    } else {
        console.log("no getUserMedia");
    }
})();
