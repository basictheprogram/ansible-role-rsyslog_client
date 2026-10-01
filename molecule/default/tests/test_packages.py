"""Assert rsyslog package presence matches client vs. receiver mode."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from testinfra.host import Host


def test_rsyslog_package_installed(host: Host, *, is_receiver: bool) -> None:
    """Assert that rsyslog is installed on every client (non-receiver) platform."""
    if is_receiver:
        pytest.skip("receiver host: client packages intentionally not installed")
    pkg = host.package("rsyslog")
    assert pkg.is_installed


def test_rsyslog_package_absent_on_receiver(host: Host, *, is_receiver: bool) -> None:
    """Assert that rsyslog is NOT installed by this role on a receiver host."""
    if not is_receiver:
        pytest.skip("only applies to receiver hosts")
    pkg = host.package("rsyslog")
    assert not pkg.is_installed
