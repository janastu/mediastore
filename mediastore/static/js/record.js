(function() {
navigator.getUserMedia = navigator.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia;

var ctx = new (window.AudioContext || window.webkitAudioContext)();

if (navigator.getUserMedia) {
    navigator.getUserMedia(
            {
                audio: true
            },

            function(stream) {
                var recorder = new MediaRecorder(stream, 
                        {
                            audioBitsPerSecond: 128000,
                            mimeType: 'audio/ogg, codecs=opus'
                        }
                    );
                var chunks = [];

                recorder.ondataavailable = function(e) {
                    chunks.push(e.data);
                }

                recorder.onstop = function(e) {
                    var blob = new Blob(chunks, { type: 'audio/ogg, codecs=opus' });

                }
            },

            function(error) {
                console.log("Error: " + error);
            }
    );
} else {
    console.log("getUserMedia not supported on this browser");
}
})();
