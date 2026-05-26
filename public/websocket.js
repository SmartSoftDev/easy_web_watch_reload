const websocket = new WebSocket('ws://localhost:8765');

websocket.addEventListener('open', (event) => {
    console.log('Successfully connected to the WebSocket server!');
});

websocket.addEventListener('message', (event) => {
    console.log('Message received from server:', JSON.parse(event.data));
    location.reload()
});

websocket.addEventListener('error', (event) => {
    console.error('WebSocket error observed:', event);
});

websocket.addEventListener('close', (event) => {
    console.log(`Connection closed. Code: ${event.code}, Reason: ${event.reason}`);
});
