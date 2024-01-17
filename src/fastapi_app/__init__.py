from .app import app  # noqa
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor()
__all__ = ["app"]
