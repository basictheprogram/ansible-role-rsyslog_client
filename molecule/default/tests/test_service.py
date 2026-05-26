"""Assert that the rsyslog service is enabled and running after converge."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from testinfra.host import Host


def test_rsyslog_service_enabled(host: Host) -> None:
    """Assert that rsyslog service is enabled at boot."""
    svc = host.service("rsyslog")
    assert svc.is_enabled


def test_rsyslog_service_running(host: Host) -> None:
    """Assert that rsyslog service is running after converge."""
    svc = host.service("rsyslog")
    assert svc.is_running
