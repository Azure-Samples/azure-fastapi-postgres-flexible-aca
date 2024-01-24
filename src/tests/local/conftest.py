import multiprocessing
import sys
import time

import ephemeral_port_reserve
import pytest
import requests
import uvicorn

from fastapi_app import seed_data
from fastapi_app.app import app

# Set start method to "fork" to avoid issues with pickling on OSes that default to "spawn"
if sys.platform != "win32":
    multiprocessing.set_start_method("fork")


def wait_for_server_ready(url: str, timeout: float = 10.0, check_interval: float = 0.5) -> bool:
    """Make requests to provided url until it responds without error."""
    conn_error = None
    for _ in range(int(timeout / check_interval)):
        try:
            requests.get(url)
        except requests.ConnectionError as exc:
            time.sleep(check_interval)
            conn_error = str(exc)
        else:
            return True
    raise RuntimeError(conn_error)


def run_server(port: int):
    uvicorn.run(app, port=port)


@pytest.fixture(scope="session")
def live_server_url():
    """Returns the url of the live server"""
    seed_data.load_from_json()

    # Start the process
    hostname = ephemeral_port_reserve.LOCALHOST
    free_port = ephemeral_port_reserve.reserve()
    proc = multiprocessing.Process(target=run_server, args=(free_port,), daemon=True)
    proc.start()

    # Return the URL of the live server once it is ready
    url = f"http://{hostname}:{free_port}"
    wait_for_server_ready(url, timeout=10.0, check_interval=0.5)
    yield url

    # Clean up the process and database
    proc.kill()
    seed_data.drop_all()
