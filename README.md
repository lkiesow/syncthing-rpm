# RPM Repository for Syncthing

RPM packages for [Syncthing](https://syncthing.net) on Rocky Linux, Red Hat
Enterprise Linux, AlmaLinux and equivalent distributions in versions 9 and 10,
for x86_64 and aarch64.

The packages repackage the official upstream release binaries. These are built
without Syncthing's built-in auto-upgrade mechanism, so updates are handled by
`dnf`. The repository is checked for new Syncthing releases daily and updated
automatically.


## Installation

Install the repository package for EL9/10:

```sh
dnf install -y "https://raw.githubusercontent.com/lkiesow/syncthing-rpm/el$(rpm -E %rhel)/syncthing-repository-1-1.el$(rpm -E %rhel).noarch.rpm"
```

Then install Syncthing:

```sh
dnf install syncthing
```


## Running Syncthing

The package ships the upstream systemd template unit `syncthing@.service`,
where the instance name is the user Syncthing runs as. The package creates a
dedicated system user `syncthing` with the home directory `/var/lib/syncthing`:

```sh
systemctl enable --now syncthing@syncthing.service
```

To run Syncthing as another user instead, e.g. to sync files in that user's
home directory, use `syncthing@<user>.service`.

The web interface listens on `127.0.0.1:8384` by default. To access it
remotely, either use an SSH tunnel or change the GUI listen address in the
configuration and open the port in the firewall.

A user unit `syncthing.service` is available as well for running Syncthing in
a user session (`systemctl --user enable --now syncthing.service`).


## Firewall

firewalld already ships service definitions for Syncthing:

```sh
firewall-cmd --permanent --add-service=syncthing      # sync protocol (22000/tcp+udp, 21027/udp)
firewall-cmd --permanent --add-service=syncthing-gui  # web interface (8384/tcp)
firewall-cmd --reload
```


## Customizing the Service

The upstream unit applies sandboxing. Adjust it with a drop-in file instead of
editing the unit, e.g. `systemctl edit syncthing@syncthing.service`.
See the comments in `/usr/lib/systemd/system/syncthing@.service` for options
like syncing file ownership (`AmbientCapabilities=CAP_CHOWN CAP_FOWNER`) or
further hardening with `ProtectSystem=strict` and `ReadWritePaths=`.

Note that the `syncthing` user needs write access to all folders you want to
share.
