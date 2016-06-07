var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res) {
    res.sendFile(__dirname + '/index.html');
});

app.post('/update_contributors', function(req, res) {
    res.send(req);
});

io.on('connection', function(socket) {
    console.log('YEAHHH')
    socket.emit('news', { hello: 'world' });
    socket.on('my other event', function(data) {
        console.log(data);
    });
});


http.listen(3000, function() {
    console.log('listening on localhost:3000');
});
