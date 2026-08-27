import asyncio
import json
import random
import sys
from datetime import datetime

import websockets


BACKEND_URL = "ws://127.0.0.1:8000"


async def run_agent(customer_id: str):

    websocket_url = (
        f"{BACKEND_URL}/ws/agent/{customer_id}"
    )

    print(
        f"Connecting agent for {customer_id}..."
    )

    async with websockets.connect(
        websocket_url
    ) as websocket:

        print(
            f"Agent connected for {customer_id}"
        )

        while True:

            # Simulating data coming from
            # the legacy desktop application
            data = {
                "status": random.choice(
                    ["RUNNING", "RUNNING", "WARNING"]
                ),
                "value": random.randint(50, 100),
                "timestamp": datetime.now().isoformat()
            }

            await websocket.send(
                json.dumps(data)
            )

            print(
                f"{customer_id} → "
                f"status={data['status']} "
                f"value={data['value']}"
            )

            await asyncio.sleep(2)


if __name__ == "__main__":

    customer_id = sys.argv[1]

    asyncio.run(
        run_agent(customer_id)
    )
