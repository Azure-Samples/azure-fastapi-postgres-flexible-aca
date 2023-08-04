from multiprocessing import Process

import pytest
import uvicorn

from fastapi_app import seed_data
from fastapi_app.app import app


def run_server():
    uvicorn.run(app)


@pytest.fixture(scope="session")
def live_server():
    seed_data.load_from_json()
    proc = Process(target=run_server, daemon=True)
    proc.start()
    yield
    proc.kill()
    seed_data.drop_all()


@pytest.fixture(scope="session")
def mock_functions_env():
    pass


@pytest.fixture(scope="session")
def live_server_url(live_server):
    """Returns the url of the live server"""
    return "http://localhost:8000"
