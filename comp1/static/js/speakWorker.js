importScripts('/static/js/speakGenerator.js');

onmessage = function(event) {
  postMessage(generateSpeech(event.data.text, event.data.args));
};

