import openSocket from 'socket.io-client';
const  socket = openSocket('http://localhost:5000');
//const  socket = openSocket('http://info319.mariuslillevik.no:5000');
function init_socket(){
    // const socket = openSocket.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('connected', {data: 'I\'m connected!'});
    });

    socket.on('connected', (data) => {
       //Do something?
    });
}
function received_tweet(cb) {
    socket.on('tweet', function (tweet) {
        cb(JSON.parse(tweet));
    });
}

function reveived_wordcount(cb){
    socket.on('word_count', function (wordcount) {
        cb(wordcount);
    })
}

function reveived_hashtag(cb){
    socket.on('hashtag_count', function (hashtagcount) {
        cb(hashtagcount);
    })
}
export { init_socket, received_tweet, reveived_wordcount , reveived_hashtag };