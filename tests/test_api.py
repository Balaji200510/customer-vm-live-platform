"""
Basic smoke tests for the backend.

Run with:
    pytest tests/test_api.py

These are the kind of tests a CI pipeline would run automatically
BEFORE new code is deployed to the staging VM (and eventually to
real customer VMs) - this is the "safe testing" piece of the design.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_customer_and_agent_relay():
    """
    Simulates the full pipeline in-process:
    an agent connects and sends data, a browser connects and should
    receive it, relayed by the backend.
    """
    with client.websocket_connect("/ws/customer/test-customer") as browser_ws:
        with client.websocket_connect("/ws/agent/test-customer") as agent_ws:
            agent_ws.send_text('{"customer_id": "test-customer", "metric": "jobs_processed", "value": 42, "timestamp": 1234567890}')
            data = browser_ws.receive_json()
            assert data["value"] == 42
            assert data["metric"] == "jobs_processed"
