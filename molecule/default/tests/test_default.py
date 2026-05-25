"""Testinfra tests for realtime.rsyslog_client.

Verifies that after converge:

- The rsyslog package is installed.
- The rsyslog service is enabled and running.
- Legacy /etc/rsyslog.d/ fragments that this role removes are absent.
- /etc/rsyslog.conf exists and is owned by root.
- /etc/rsyslog.d/ drop-in directory is present.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from testinfra.host import Host


# ---------------------------------------------------------------------------
# Package
# ---------------------------------------------------------------------------


def test_rsyslog_package_installed(host: Host) -> None:
    """Assert that rsyslog is installed on every supported platform."""
    pkg = host.package("rsyslog")
    assert pkg.is_installed


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------


def test_rsyslog_service_enabled(host: Host) -> None:
    """Assert that rsyslog service is enabled at boot."""
    svc = host.service("rsyslog")
    assert svc.is_enabled


def test_rsyslog_service_running(host: Host) -> None:
    """Assert that rsyslog service is running after converge."""
    svc = host.service("rsyslog")
    assert svc.is_running


# ---------------------------------------------------------------------------
# Legacy fragment cleanup
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fragment",
    [
        "/etc/rsyslog.d/01-gnutls.conf",
        "/etc/rsyslog.d/90-remote-forward.conf",
        "/etc/rsyslog.d/forwarding.conf",
    ],
)
def test_legacy_fragments_absent(host: Host, fragment: str) -> None:
    """Legacy client-side rsyslog.d fragments must be removed by the role."""
    assert not host.file(fragment).exists


# ---------------------------------------------------------------------------
# Config file sanity
# ---------------------------------------------------------------------------


def test_rsyslog_conf_exists(host: Host) -> None:
    """/etc/rsyslog.conf must exist and be owned by root."""
    f = host.file("/etc/rsyslog.conf")
    assert f.exists
    assert f.user == "root"
    assert f.group == "root"


def test_rsyslog_d_directory_exists(host: Host) -> None:
    """/etc/rsyslog.d/ drop-in directory must be present."""
    d = host.file("/etc/rsyslog.d")
    assert d.exists
    assert d.is_directory
