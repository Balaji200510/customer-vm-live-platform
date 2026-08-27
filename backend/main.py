from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect


app = FastAPI(title="Customer VM Live Platform")


# Store the latest data received from each customer VM
latest_data = {}


# Store connected browser WebSocket connections
# Example:
# CUST-001 -> browser connections
# CUST-002 -> browser connections
customer_connections = {}


@app.get("/")
def root():
    return {
        "message": "Customer VM Live Platform is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# --------------------------------------------------
# Customer Browser WebSocket
# --------------------------------------------------

@app.websocket("/ws/customer/{customer_id}")
async def customer_websocket(
    websocket: WebSocket,
    customer_id: str
):
    await websocket.accept()

    print(
        f"Customer browser connected: {customer_id}"
    )

    # Create connection set for this customer
    if customer_id not in customer_connections:
        customer_connections[customer_id] = set()

    customer_connections[customer_id].add(websocket)

    try:
        # Send latest available data immediately
        if customer_id in latest_data:
            await websocket.send_json(
                latest_data[customer_id]
            )

        # Keep connection alive
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        customer_connections[customer_id].discard(
            websocket
        )

        print(
            f"Customer browser disconnected: {customer_id}"
        )


# --------------------------------------------------
# Customer VM Agent WebSocket
# --------------------------------------------------

@app.websocket("/ws/agent/{customer_id}")
async def agent_websocket(
    websocket: WebSocket,
    customer_id: str
):
    await websocket.accept()

    print(
        f"Agent connected: {customer_id}"
    )

    try:
        while True:

            # Receive data from the customer VM agent
            data = await websocket.receive_json()

            # Add customer information
            data["customer_id"] = customer_id

            data["received_at"] = (
                datetime.now().isoformat()
            )

            # Store latest data
            latest_data[customer_id] = data

            print(
                f"Received from {customer_id}: {data}"
            )

            # Find browsers connected to this customer
            connections = customer_connections.get(
                customer_id,
                set()
            )

            # Send data to that customer's browsers
            for browser in connections:

                try:
                    await browser.send_json(data)

                except Exception:
                    pass

    except WebSocketDisconnect:
        print(
            f"Agent disconnected: {customer_id}"
        )
