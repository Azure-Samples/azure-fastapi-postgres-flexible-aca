import os

from azure.monitor.opentelemetry import configure_azure_monitor

from .app import app  # noqa

if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor()
__all__ = ["app"]
