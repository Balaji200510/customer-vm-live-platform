import json
import os
import random
import sys
import time
from datetime import datetime

import websocket


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "ws://127.0.0.1:8000"
)

POLL_INTERVAL = float(
    os.getenv(
        "POLL_INTERVAL_SECONDS",
        "2"
    )
)


def run_agent(customer_id: str):

    websocket_url = (
        f"{BACKEND_URL}/ws/agent/{customer_id}"
    )

    print(
        f"Connecting agent for {customer_id}..."
    )

    while True:

        try:
            ws = websocket.create_connection(
                websocket_url,
                timeout=10
            )

            print(
                f"Agent connected for {customer_id}"
            )

            try:
                while True:

                    data = {
                        "status": random.choice(
                            [
                                "RUNNING",
                                "RUNNING",
                                "WARNING"
                            ]
                        ),
                        "value": random.randint(
                            50,
                            100
                        ),
                        "timestamp": (
                            datetime.now().isoformat()
                        )
                    }

                    ws.send(
                        json.dumps(data)
                    )

                    print(
                        f"{customer_id} ? "
                        f"status={data['status']} "
                        f"value={data['value']}"
                    )

                    time.sleep(
                        POLL_INTERVAL
                    )

            finally:
                ws.close()

        except Exception as error:

            print(
                f"{customer_id} connection error: "
                f"{error}"
            )

            print(
                "Retrying in 5 seconds..."
            )

            time.sleep(5)


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "Usage: python agent/agent.py CUSTOMER_ID"
        )

        sys.exit(1)

    customer_id = sys.argv[1]

    run_agent(customer_id)
