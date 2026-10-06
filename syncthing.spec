# vim: et:ts=3:sw=3:sts=3

# Upstream binaries are static and already stripped
%global debug_package %{nil}
%global __strip /bin/true
%global _build_id_links none

%ifarch x86_64
%global debarch amd64
%endif
%ifarch aarch64
%global debarch arm64
%endif


Name:          syncthing
Version:       2.1.6
Release:       1%{?dist}
Summary:       Open Source Continuous File Synchronization

License:       MPL-2.0
URL:           https://syncthing.net
Source0:       https://github.com/syncthing/syncthing/releases/download/v%{version}/syncthing_%{version}_amd64.deb
Source1:       https://github.com/syncthing/syncthing/releases/download/v%{version}/syncthing_%{version}_arm64.deb
Source2:       syncthing.sysusers

ExclusiveArch: x86_64 aarch64

BuildRequires: binutils
BuildRequires: tar
BuildRequires: gzip
BuildRequires: xz
BuildRequires: systemd-rpm-macros

%{?sysusers_requires_compat}


%description
Syncthing is a continuous file synchronization program. It synchronizes files
between two or more computers in real time, safely protected from prying eyes.

This package repackages the official upstream release binaries which are built
without the built-in auto-upgrade mechanism.


%prep
%setup -q -c -T
ar x %{_sourcedir}/syncthing_%{version}_%{debarch}.deb
tar xf data.tar.*


%build
# Upstream unit uses options which require systemd >= 257
%if 0%{?rhel} && 0%{?rhel} < 10
sed -i \
   -e 's/^PrivateTmp=disconnected$/PrivateTmp=true/' \
   -e '/^PrivatePIDs=/d' \
   lib/systemd/system/syncthing@.service
%endif


%install
install -p -D -m 0755 usr/bin/syncthing %{buildroot}%{_bindir}/syncthing

# Systemd units
install -p -D -m 0644 lib/systemd/system/syncthing@.service %{buildroot}%{_unitdir}/syncthing@.service
install -p -D -m 0644 usr/lib/systemd/user/syncthing.service %{buildroot}%{_userunitdir}/syncthing.service

# Larger UDP buffers for QUIC
install -p -D -m 0644 usr/lib/sysctl.d/30-syncthing.conf %{buildroot}%{_sysctldir}/30-syncthing.conf

# System user
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/syncthing.conf
mkdir -m 700 -p %{buildroot}%{_sharedstatedir}/%{name}

# Man pages, desktop files and icons
mkdir -p %{buildroot}%{_datadir}
cp -a usr/share/man usr/share/applications usr/share/icons %{buildroot}%{_datadir}/

# Documentation
cp -p usr/share/doc/syncthing/{README,AUTHORS,LICENSE}.txt .


%pre
%sysusers_create_compat %{SOURCE2}


%post
%systemd_post syncthing@.service
%systemd_user_post syncthing.service
%sysctl_apply 30-syncthing.conf


%preun
%systemd_preun syncthing@.service
%systemd_user_preun syncthing.service
if [ $1 -eq 0 ]; then
   systemctl --no-reload stop 'syncthing@*.service' > /dev/null 2>&1 || :
fi


%postun
if [ $1 -ge 1 ]; then
   systemctl daemon-reload > /dev/null 2>&1 || :
   systemctl try-restart 'syncthing@*.service' > /dev/null 2>&1 || :
fi


%files
%license LICENSE.txt
%doc README.txt AUTHORS.txt
%{_bindir}/syncthing
%{_unitdir}/syncthing@.service
%{_userunitdir}/syncthing.service
%{_sysctldir}/30-syncthing.conf
%{_sysusersdir}/syncthing.conf
%{_mandir}/man*/syncthing*
%{_datadir}/applications/syncthing-*.desktop
%{_datadir}/icons/hicolor/*/apps/syncthing.*
%dir %attr(0700,syncthing,syncthing) %{_sharedstatedir}/%{name}


%changelog
* Tue Oct 06 2026 Lars Kiesow <lkiesow@uos.de> - 2.1.6-1
- Update to 2.1.6

* Sat Oct 03 2026 Lars Kiesow <lkiesow@uos.de> - 2.1.5-1
- Initial build
