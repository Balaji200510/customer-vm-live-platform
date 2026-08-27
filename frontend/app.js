let socket = null;


function connectDashboard() {

    const customerId =
        document
            .getElementById("customerId")
            .value
            .trim();

    if (!customerId) {
        alert("Please enter customer ID");
        return;
    }


    // Close old WebSocket connection
    if (socket) {
        socket.close();
    }


    // IMPORTANT:
    // This URL must match the FastAPI route
    const websocketUrl =
        `ws://127.0.0.1:8001/ws/customer/${customerId}`;


    console.log(
        "Connecting to:",
        websocketUrl
    );


    socket = new WebSocket(
        websocketUrl
    );


    socket.onopen = function () {

        console.log(
            "Customer WebSocket connected"
        );

        document
            .getElementById("connectionStatus")
            .textContent = "Connected";
    };


    socket.onmessage = function (event) {

        console.log(
            "Received:",
            event.data
        );

        const data =
            JSON.parse(event.data);


        document
            .getElementById("customer")
            .textContent =
                data.customer_id;


        document
            .getElementById("appStatus")
            .textContent =
                data.status;


        document
            .getElementById("value")
            .textContent =
                data.value;


        document
            .getElementById("updated")
            .textContent =
                data.received_at ||
                data.timestamp;
    };


    socket.onclose = function () {

        console.log(
            "Customer WebSocket disconnected"
        );

        document
            .getElementById("connectionStatus")
            .textContent =
                "Disconnected";
    };


    socket.onerror = function (error) {

        console.error(
            "WebSocket error:",
            error
        );
    };
}
