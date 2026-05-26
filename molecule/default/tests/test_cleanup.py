"""Assert that legacy /etc/rsyslog.d/ fragments are absent after converge."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from testinfra.host import Host

_LEGACY_FRAGMENTS = [
    "/etc/rsyslog.d/01-gnutls.conf",
    "/etc/rsyslog.d/90-remote-forward.conf",
    "/etc/rsyslog.d/forwarding.conf",
]


@pytest.mark.parametrize("fragment", _LEGACY_FRAGMENTS)
def test_legacy_fragments_absent(host: Host, fragment: str) -> None:
    """Legacy client-side rsyslog.d fragments must be removed by the role."""
    assert not host.file(fragment).exists
