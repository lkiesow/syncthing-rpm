Name:      syncthing-repository
Summary:   Syncthing RPM Repository
Version:   1
Release:   1%{?dist}
License:   CC-0
URL:       https://github.com/lkiesow/syncthing-rpm
Source0:   syncthing.repo
BuildArch: noarch


%description
RPM repository for Syncthing on Rocky Linux, Red Hat Enterprise Linux and
equivalent distributions.


%prep


%build


%install
install -m 0644 -p -D %{SOURCE0} %{buildroot}%{_sysconfdir}/yum.repos.d/syncthing.repo


%files
%config(noreplace) %{_sysconfdir}/yum.repos.d/syncthing.repo


%changelog
* Sat Oct 03 2026 Lars Kiesow <lkiesow@uos.de> - 1-1
- Initial build
