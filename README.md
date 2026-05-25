# realtime.rsyslog_client

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-realtime.rsyslog__client-blue.svg)](https://galaxy.ansible.com/realtime/rsyslog_client)
[![ansible-lint](https://img.shields.io/badge/ansible--lint-enforced-brightgreen.svg)](https://github.com/ansible/ansible-lint)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen.svg?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Ansible Core](https://img.shields.io/badge/ansible--core-%3E%3D2.20-blue.svg)](https://docs.ansible.com/ansible/latest/index.html)

Ansible role that configures rsyslog as a log-forwarding client on
Debian/Ubuntu and RHEL/EL 9 hosts.

The role handles OS-specific package installation (apt on Debian/Ubuntu,
dnf on EL), removes legacy `/etc/rsyslog.d/` configuration fragments
left by previous deployments, and then delegates the actual rsyslog
configuration to the [robertdebock.rsyslog](https://github.com/robertdebock/ansible-role-rsyslog)
role authored by Robert de Bock.

Set `rsyslog_receiver: true` on any host that should receive logs rather
than forward them. Client setup — package installation, legacy cleanup,
and the robertdebock.rsyslog delegation — is skipped entirely on those
hosts.

---

## Requirements

- ansible-core >= 2.20
- The `robertdebock.rsyslog` role must be installed before using this
  role. See [Dependencies](#dependencies) below.

---

## Role variables

### `rsyslog_client_packages`

List of packages installed for rsyslog client operation. Override to
add platform-specific modules such as `rsyslog-gnutls` or `rsyslog-relp`.

```yaml
rsyslog_client_packages:
  - rsyslog
```

### `rsyslog_receiver`

When `true`, skip all client configuration on this host. Intended for
hosts that act as centralised syslog receivers rather than log
forwarders.

```yaml
rsyslog_receiver: false
```

All rsyslog configuration — forwarding targets, TLS, queues, rulesets —
is controlled through variables passed to `robertdebock.rsyslog`. Refer
to that role's documentation for the full variable reference.

---

## Dependencies

This role calls `robertdebock.rsyslog` at runtime via
`ansible.builtin.import_role`. It is a **runtime dependency**, not a
Galaxy meta dependency, so it will not be installed automatically by
`ansible-galaxy install`. Install it explicitly:

```yaml
# requirements.yml
---
roles:
  - name: robertdebock.rsyslog
    src: https://github.com/robertdebock/ansible-role-rsyslog
```

```bash
ansible-galaxy role install -r requirements.yml
```

---

## Example playbook

```yaml
---
- name: Configure rsyslog forwarding clients
  hosts: log_clients
  roles:
    - role: realtime.rsyslog_client
      vars:
        rsyslog_client_packages:
          - rsyslog
          - rsyslog-gnutls
        # robertdebock.rsyslog variables go here too — they are passed
        # through to the upstream role automatically via role variable scope.

- name: Configure rsyslog receivers (skip client setup)
  hosts: log_receivers
  roles:
    - role: realtime.rsyslog_client
      vars:
        rsyslog_receiver: true
```

---

## Platform support

| Platform | Versions                   |
|----------|----------------------------|
| Ubuntu   | jammy, noble, resolute     |
| Debian   | bookworm, trixie           |
| EL       | 9                          |

---

## License

MIT

---

## Author

Bob Tanner — Real Time Enterprises, Inc.

This role is a wrapper around
[robertdebock.rsyslog](https://github.com/robertdebock/ansible-role-rsyslog)
by Robert de Bock. All substantive rsyslog configuration is handled by
that upstream role.
