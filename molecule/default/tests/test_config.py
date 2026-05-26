"""Assert that rsyslog configuration files are present and correct."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from testinfra.host import Host


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
