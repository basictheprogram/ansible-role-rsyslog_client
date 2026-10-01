"""Session-scoped pytest fixtures for the rsyslog_client Molecule scenario."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from testinfra.host import Host


@pytest.fixture
def is_receiver(host: Host) -> bool:
    """Return whether this host is designated rsyslog_receiver: true (see host_vars/el10.yml)."""
    return bool(host.ansible.get_variables().get("rsyslog_receiver", False))
