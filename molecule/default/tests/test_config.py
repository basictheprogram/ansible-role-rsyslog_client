"""Assert that rsyslog configuration files are present and correct on client hosts."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from testinfra.host import Host


def test_rsyslog_conf_exists(host: Host, *, is_receiver: bool) -> None:
    """/etc/rsyslog.conf must exist and be owned by root on client hosts."""
    if is_receiver:
        pytest.skip("receiver host: rsyslog is not installed by this role")
    f = host.file("/etc/rsyslog.conf")
    assert f.exists
    assert f.user == "root"
    assert f.group == "root"


def test_rsyslog_d_directory_exists(host: Host, *, is_receiver: bool) -> None:
    """/etc/rsyslog.d/ drop-in directory must be present on client hosts."""
    if is_receiver:
        pytest.skip("receiver host: rsyslog is not installed by this role")
    d = host.file("/etc/rsyslog.d")
    assert d.exists
    assert d.is_directory
