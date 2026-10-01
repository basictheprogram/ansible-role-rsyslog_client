# TODO — ansible-role-rsyslog_client

## Session: ansible-sync-role pass (2026-10-01)

Ran the full 14-step sync. Most of the role was already in good shape from
a prior session; real findings and changes below.

### Changes made this session

* `.gitignore` — overwritten with the template's version (same entries,
  different order; user chose `overwrite`).
* `CLAUDE.md` — overwritten: fixed a stale "EL 9" in the description
  (actual support is EL 9–10 per `meta/main.yml`) and marked
  implementation-order items 7–8 done (`converge.yml` is already a real
  play; testinfra tests already exist — there is no separate `verify.yml`
  to author for testinfra).
* `meta/main.yml` — removed the `platforms:` key (current guidance: never
  keep it, Galaxy ignores it and ansible-lint's schema validator for it
  has a long-standing bug). Folded the OS/version list into
  `description:` instead, **dropping Debian bookworm** (confirmed EOL as
  of today via `lookup_platform.py` — full support ended ~Aug 2026,
  estimated; user confirmed `drop`). Added `issue_tracker_url` (GitHub,
  per `git remote -v`).
* `README.md` — updated intro line and platform table to match (bookworm
  dropped, EL 9–10 made explicit). Fixed the **Task Flow** section, which
  had the step order wrong: it listed preflight assertions as step 4, but
  `tasks/main.yml` actually runs preflight *first*, ahead of even
  `include_vars`.
* `molecule/default/molecule.yml` — removed the `debian-bookworm`
  platform entry. Also fixed `stdout_callback: yaml` →
  `stdout_callback: default` + `result_format: yaml` in the provisioner's
  `config_options` — the old form depends on the `community.general.yaml`
  callback plugin, which was removed in `community.general` 12.0.0 and
  broke every `molecule` invocation outright in this devcontainer. See
  "Known issues found this session" below — this almost certainly needs
  the same fix applied to every other role's `molecule.yml` in this repo.
* `molecule/default/converge.yml` — fixed `ansible_os_family` (deprecated
  top-level fact injection) to `ansible_facts.os_family` in both
  cache-update `pre_tasks`.
* **New test coverage**: this role has two behavior variants
  (`rsyslog_receiver: false`/client vs `true`/receiver-skip), but
  `converge.yml` only ever exercised the client path. Added
  `molecule/default/host_vars/el10.yml` (`rsyslog_receiver: true`), a
  shared `is_receiver` fixture in a new `molecule/default/tests/conftest.py`,
  and made `test_packages.py`/`test_service.py`/`test_config.py`
  host-aware so the `el10` host now asserts the *absence* of client
  setup instead of its presence. `el10` (Rocky Linux, RedHat family) was
  chosen because minimal RHEL-family images don't ship `rsyslog`
  preinstalled, unlike some Debian/Ubuntu images — this makes "not
  installed" a reliable signal of "role correctly skipped it" rather
  than a base-image coincidence.

### Known issues found this session (environment, not this role)

* **`molecule test` cannot currently complete in the `ansible-vscode`
  devcontainer.** After fixing the `stdout_callback` issue above, the
  `destroy` step still fails: `molecule-plugins[docker]` 2.1.0 ships its
  own `destroy.yml` playbook with a non-boolean `when:` conditional
  (`when: (lookup('env', 'HOME'))`), which this devcontainer's
  ansible-core 2.21.4 rejects outright ("Conditionals must have a
  boolean result"). This is a bug in the `molecule-plugins` package
  itself, not in anything role-specific — it would block `molecule test`
  for every role in this repo on this devcontainer, not just this one.
  Needs a `molecule-plugins[docker]` version pin/downgrade or an upstream
  fix; out of scope to chase further under a single-role sync. **As a
  result, this session's changes are ansible-lint-clean but still not
  verified against a real `molecule converge`/`verify` run.**
* The `stdout_callback: yaml` → `community.general.yaml` breakage (fixed
  in this role's `molecule.yml` above) likely affects every other role's
  `molecule.yml` in this repo that uses the same provisioner config
  block — worth a repo-wide sweep rather than fixing role-by-role as
  each one happens to get synced.

### Still open (carried over, unresolved)

* **No `LICENSE` file exists**, despite `meta/main.yml` and the README
  both claiming MIT. Step 5b of the sync only covers stacking a second
  copyright line onto an *existing* MIT `LICENSE` file — creating one
  from scratch was out of that step's literal scope, so it was flagged
  rather than done unprompted.
* **Add `requirements.yml`** (role root) — declare `robertdebock.rsyslog`
  as an explicit install-time dependency so consumers can run
  `ansible-galaxy role install -r requirements.yml`, per the README's
  Dependencies section.
* **Create `DESIGN.md`** — `CLAUDE.md`'s "Settled decisions" section
  already has solid, accurate content written from code inspection in an
  earlier session; promoting that into an actual `DESIGN.md` (the
  authoritative source `CLAUDE.md` is supposed to defer to) is still
  outstanding.
* **Open question**: should legacy `/etc/rsyslog.d/` cleanup also run on
  RedHat family hosts? `tasks/redhat.yml` has no cleanup step — only
  `tasks/debian.yml` does. If the same legacy fragments can appear on EL
  deployments, this is a real gap.
* **Open question**: should `robertdebock.rsyslog` be pinned to a
  specific version once `requirements.yml` exists? An unpinned install
  pulls the latest tag, which may introduce breaking upstream changes.
* **Open question**: does `robertdebock.rsyslog` need per-distro variable
  overrides? `vars/main.yml` is still empty (just the `first_found`
  fallback) — add `vars/<OsFamily>.yml` files if investigation or
  upstream docs show they're needed.
