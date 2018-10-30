import openSocket from 'socket.io-client';
const  socket = openSocket('http://localhost:5000');
//const  socket = openSocket('http://info319.mariuslillevik.no:5000');
function init_socket(){
    // const socket = openSocket.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('connected', {data: 'I\'m connected!'});
    });

    socket.on('connected', (data) => {
       console.log(data);
    });
    setInterval(() => {
        socket.emit('message', 'test data')
    }, 15000);
}
function received_tweet(cb) {
    socket.on('tweet', function (tweet) {
        console.log(tweet);
        cb(JSON.parse(tweet));
    });
}
export { init_socket, received_tweet };