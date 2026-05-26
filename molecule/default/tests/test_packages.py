"""Assert that rsyslog package is installed on every supported platform."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from testinfra.host import Host


def test_rsyslog_package_installed(host: Host) -> None:
    """Assert that rsyslog is installed on every supported platform."""
    pkg = host.package("rsyslog")
    assert pkg.is_installed
