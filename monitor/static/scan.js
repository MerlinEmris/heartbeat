let scanSocket = null;

function connect() {
    scanSocket = new WebSocket("ws://" + window.location.host + "/ws/scan/");

    scanSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }

    scanSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 4s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 4000);
    };

    scanSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        handleResults(data);
        console.log(data);


    };

    scanSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        scanSocket.close();
    }
}
connect();