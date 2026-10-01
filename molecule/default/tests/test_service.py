"""Assert that the rsyslog service is enabled and running on client hosts."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from testinfra.host import Host


def test_rsyslog_service_enabled(host: Host, *, is_receiver: bool) -> None:
    """Assert that rsyslog service is enabled at boot on client hosts."""
    if is_receiver:
        pytest.skip("receiver host: client setup is skipped by this role")
    svc = host.service("rsyslog")
    assert svc.is_enabled


def test_rsyslog_service_running(host: Host, *, is_receiver: bool) -> None:
    """Assert that rsyslog service is running after converge on client hosts."""
    if is_receiver:
        pytest.skip("receiver host: client setup is skipped by this role")
    svc = host.service("rsyslog")
    assert svc.is_running
