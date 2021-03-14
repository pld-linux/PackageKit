# TODO:
# - BASH command-not-found functionality disabled for now as it needs patched bash
#   (details in bash from Fedora Rawhide)
#
# Conditional build:
%bcond_without	doc		# build without docs
%bcond_without	introspection	# gobject introspection, time to time broken
%bcond_without	static_libs	# static library
%bcond_without	python		# Python binding (used by entropy and portage backends)
%bcond_without	vala		# Vala binding
# backends
%bcond_with	alpm		# ALPM (Arch Linux package manager) backend
%bcond_with	apt		# APT (Debian/Ubuntu) backend using C++ API
%bcond_with	dnf		# DNF (Fedora/RHEL/Mageia/OpenMandriva/OpenSUSE/Rosa) backend
%bcond_with	entropy		# Entropy (Sabayon) backend (Python)
%bcond_with	nix		# Nix (NixOS) backend [broken as of 1.2.0]
%bcond_without	poldek		# Poldek (PLD) backend
%bcond_with	portage		# portage (Gentoo) backend (Python)
%bcond_with	slack		# Slack (Slackware) backend
%bcond_with	zypp		# ZYPP (openSUSE/SLE) backend [broken as of 1.2.0]

%if %{without python}
%undefine	with_entropy
%undefine	with_portage
%endif

Summary:	System daemon that is a D-Bus abstraction layer for package management
Summary(pl.UTF-8):	Demon systemowy będący warstwą abstrakcji D-Bus do zarządzania pakietami
Name:		PackageKit
Version:	1.2.2
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	https://www.freedesktop.org/software/PackageKit/releases/%{name}-%{version}.tar.xz
# Source0-md5:	2bfa2687bcc4e189bb90e2228c11e558
Patch0:		%{name}-poldek.patch
Patch2:		%{name}-meson.patch
Patch3:		consolekit-fallback.patch
URL:		https://www.freedesktop.org/software/PackageKit/
%{?with_apt:BuildRequires:	AppStream-devel >= 0.12}
BuildRequires:	NetworkManager-devel >= 0.6.5
# pkgconfig(libalpm) >= 12.0.0
%{?with_alpm:BuildRequires:	alpm-devel >= 5.2}
%{?with_dnf:BuildRequires:	appstream-glib-devel}
%{?with_apt:BuildRequires:	apt-devel >= 1.9.2}
BuildRequires:	bash-completion-devel >= 2.0
BuildRequires:	connman-devel
%{?with_slack:BuildRequires:	curl-devel}
BuildRequires:	dbus-devel >= 1.2.0
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-dtd42-xml
BuildRequires:	fontconfig-devel
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.54.0
%{?with_introspection:BuildRequires:	gobject-introspection-devel >= 0.9.9}
BuildRequires:	gstreamer-devel >= 1.0.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0.0
BuildRequires:	gtk+3-devel >= 3.0.0
%{?with_doc:BuildRequires:	gtk-doc >= 1.11}
BuildRequires:	libarchive-devel
%{?with_dnf:BuildRequires:	libdnf-devel >= 0.43.1}
%if %{with apt} || %{with nix}
BuildRequires:	libstdc++-devel >= 6:4.7
%endif
%{?with_slack:BuildRequires:	libstdc++-devel >= 6:5}
BuildRequires:	libxslt-progs
%{?with_zypp:BuildRequires:	libzypp-devel >= 15}
BuildRequires:	meson >= 0.50
BuildRequires:	ninja >= 1.5
# nix-expr nix-main nix-store
%{?with_nix:BuildRequires:	nix-devel >= 1.12}
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
# just to detect which reboot modes to use (library not linked)
#BuildRequires:	plymouth-devel >= 0.9.5
%{?with_poldek:BuildRequires:	poldek-devel >= 0.30-1.rc6.4}
BuildRequires:	polkit-devel >= 0.114
# or 1:3.2
%{?with_python:BuildRequires:	python-devel >= 1:2.7}
BuildRequires:	readline-devel
BuildRequires:	rpm-build >= 4.6
%{?with_dnf:BuildRequires:	rpm-devel >= 1:4.6}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	systemd-devel >= 1:213
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel
%{?with_vala:BuildRequires:	vala >= 2:0.16}
BuildRequires:	xz
Requires(post,postun):	shared-mime-info
Requires:	%{name}-backend
Requires:	%{name}-libs = %{version}-%{release}
Requires:	crondaemon
Requires:	polkit >= 0.114
Suggests:	ConsoleKit-x11
Obsoletes:	PackageKit-backend-pisi < 1.2
Obsoletes:	PackageKit-backend-ports < 1.2
Obsoletes:	PackageKit-backend-smart < 1.0
Obsoletes:	PackageKit-backend-urpmi < 1.2
Obsoletes:	PackageKit-backend-yum < 1.2
Obsoletes:	PackageKit-docs < 0.8.4
Obsoletes:	pm-utils-packagekit < 0.8.15
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PackageKit is a D-Bus abstraction layer that allows the session user
to manage packages in a secure way using a cross-distro,
cross-architecture API.

%description -l pl.UTF-8
PackageKit to warstwa abstrakcji D-Bus pozwalająca użytkownikowi
sesyjnemu w bezpieczny sposob zarządzać pakietami przy użyciu API
zgodnego z wieloma dystrybucjami i architekturami.

%package libs
Summary:	packagekit-glib library
Summary(pl.UTF-8):	Biblioteka packagekit-glib
Group:		Libraries
Requires:	glib2 >= 1:2.54.0
Obsoletes:	browser-plugin-packagekit < 1.1.0

%description libs
packagekit-glib library.

%description libs -l pl.UTF-8
Biblioteka packagekit-glib.

%package devel
Summary:	Header files for packagekit-glib library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki packagekit-glib
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-devel >= 1.2.0
Requires:	glib2-devel >= 1:2.54.0
Requires:	sqlite3-devel

%description devel
Header files for packagekit-glib library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki packagekit-glib.

%package static
Summary:	Static packagekit-glib library
Summary(pl.UTF-8):	Statyczna biblioteka packagekit-glib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static packagekit-glib library.

%description static -l pl.UTF-8
Statyczna biblioteka packagekit-glib.

%package -n vala-packagekit
Summary:	Vala API for PackageKit library
Summary(pl.UTF-8):	API języka Vala do biblioteki PackageKitu
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.16
BuildArch:	noarch

%description -n vala-packagekit
Vala API for PackageKit library.

%description -n vala-packagekit -l pl.UTF-8
API języka Vala do biblioteki PackageKitu.

%package apidocs
Summary:	PackageKit library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki PackageKit
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
PackageKit library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki PackageKit.

%package backend-alpm
Summary:	PackageKit ALPM backend
Summary(pl.UTF-8):	Backend PackageKit oparty na bibliotece ALPM
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-backend = %{version}-%{release}

%description backend-alpm
A backend for PackageKit to enable Arch Linux packages via ALPM
library.

%description backend-alpm -l pl.UTF-8
Backend PackageKit dodający obsługę pakietów Arch Linuksa poprzez
bibliotekę ALPM.

%package backend-aptcc
Summary:	PackageKit APTcc backend
Summary(pl.UTF-8):	Backend PackageKit APTcc
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	AppStream >= 0.12
Requires:	apt >= 1.9.2
Provides:	%{name}-backend = %{version}-%{release}

%description backend-aptcc
A backend for PackageKit to enable APT support via C++ API.

%description backend-aptcc -l pl.UTF-8
Backend PackageKit dodający obsługę zarządcy pakietów APT poprzez API
C++.

%package backend-dnf
Summary:	PackageKit dnf backend
Summary(pl.UTF-8):	Backend PackageKit oparty na bibliotece dnfhif
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libdnf >= 0.43.1
Requires:	rpm >= 1:4.6
Provides:	%{name}-backend = %{version}-%{release}
Obsoletes:	PackageKit-backend-hawkey < 1.0
Obsoletes:	PackageKit-backend-hif < 1.2

%description backend-dnf
A backend for PackageKit to enable RPM packages support via dnf
library (used in Fedora).

%description backend-dnf -l pl.UTF-8
Backend PackageKit dodający obsługę pakietów RPM poprzez bibliotekę
dnf (używaną w dystrybucji Fedora).

%package backend-entropy
Summary:	PackageKit Entropy backend
Summary(pl.UTF-8):	Backend PackageKit Entropy
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-packagekit = %{version}-%{release}
#Requires:	python-entropy
Provides:	%{name}-backend = %{version}-%{release}

%description backend-entropy
A backend for PackageKit to enable Sabayon packages support through
Entropy package manager.

%description backend-entropy -l pl.UTF-8
Backend PackageKit dodający obsługę pakietów dystrybucji Sabayon przy
użyciu zarządcy pakietów Entropy.

%package backend-nix
Summary:	PackageKit Nix backend
Summary(pl.UTF-8):	Backend PackageKit oparty na zarządcy pakietów Nix
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	nix >= 1.12
Provides:	%{name}-backend = %{version}-%{release}

%description backend-nix
A backend for PackageKit to enable Nix packages support (used in
NixOS).

%description backend-nix -l pl.UTF-8
Backend PackageKit dodający obsługę pakietów Nix (używanych w NixOS).

%package backend-poldek
Summary:	PackageKit Poldek backend
Summary(pl.UTF-8):	Backend PackageKit oparty na Poldku
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	poldek >= 0.30-1.rc6.4
Provides:	%{name}-backend = %{version}-%{release}

%description backend-poldek
A backend for PackageKit to enable RPM packages support through Poldek
- native PLD package manager.

%description backend-poldek -l pl.UTF-8
Backend PackageKit dodający obsługę pakietów RPM poprzez Poldka -
natywnego zarządcę pakietów dystrybucji PLD.

%package backend-portage
Summary:	PackageKit Portage backend
Summary(pl.UTF-8):	Backend PackageKit Portage
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-packagekit = %{version}-%{release}
#Requires:	python-portage
Provides:	%{name}-backend = %{version}-%{release}

%description backend-portage
A backend for PackageKit to enable Gentoo Portage support.

%description backend-portage -l pl.UTF-8
Backend PackageKit dodający obsługę systemu Portage dystrybucji
Gentoo.

%package backend-slack
Summary:	PackageKit Slack backend
Summary(pl.UTF-8):	Backend PackageKit Slack
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-backend = %{version}-%{release}
Obsoletes:	PackageKit-backend-katja < 1.2

%description backend-slack
Slack backend for PackageKit to enable Slackware repositories support.

%description backend-slack -l pl.UTF-8
Backend PackageKit Slack dodający obsługę repozytoriów Slackware.

%package backend-zypp
Summary:	PackageKit Zypp backend
Summary(pl.UTF-8):	Backend PackageKit Zypp
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libzypp >= 15
Provides:	%{name}-backend = %{version}-%{release}

%description backend-zypp
A backend for PackageKit to enable RPM packages support through Zypp
library (originated in openSUSE/SLE).

%description backend-zypp -l pl.UTF-8
Backend PackageKit dodający obsługę pakietów RPM poprzez bibliotekę
Zypp (pochodzącą z dystrybucji openSUSE/SLE).

%package gstreamer-plugin
Summary:	GStreamer codecs installer
Summary(pl.UTF-8):	Instalator kodeków GStreamera
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-gtk3-module = %{version}-%{release}

%description gstreamer-plugin
The PackageKit GStreamer plugin allows any GStreamer application to
install codecs from configured repositories using PackageKit.

%description gstreamer-plugin -l pl.UTF-8
Wtyczka GStreamer pozwala każdej aplikacji używającej GStreamera
zainstalować kodeki ze skonfigurowanych źródeł PackageKit.

%package gtk3-module
Summary:	GTK+ 3.x module to detect and install missing fonts
Summary(pl.UTF-8):	Moduł GTK+ 3.x do wykrywania i instalowania brakujących czcionek
Group:		X11/Libraries
Obsoletes:	PackageKit-gtk-module < 1.2.0

%description gtk3-module
The PackageKit GTK+ 3.x module allows any pango application to install
missing fonts from configured repositories using PackageKit.

%description gtk3-module -l pl.UTF-8
Moduł GTK+ 3.x pozwala każdej aplikacji używającej pango zainstalować
brakującą czcionkę ze skonfigurowanych źródeł PackageKit.

%package -n bash-completion-packagekit
Summary:	Bash completion for PackageKit console commands
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów dla poleceń konsolowych PackageKit
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2
BuildArch:	noarch

%description -n bash-completion-packagekit
This package provides bash-completion for PackageKit console commands.

%description -n bash-completion-packagekit -l pl.UTF-8
Pakiet ten dostarcza bashowe uzupełnianie parametrów dla poleceń
konsolowych PackageKit.

%package -n python-packagekit
Summary:	PackageKit Python bindings
Summary(pl.UTF-8):	Wiązania PackageKit dla Pythona
Group:		Development/Languages/Python
Requires:	python-dbus
Requires:	python-pygobject

%description -n python-packagekit
PackageKit Python bindings.

%description -n python-packagekit -l pl.UTF-8
Wiązania PackageKit dla Pythona.

%prep
%setup -q
%patch0 -p1
%patch2 -p1
%patch3 -p1

%if %{with static_libs}
%{__sed} -i -e '/^packagekit_glib2_library =/ s/shared_library/library/' lib/packagekit-glib2/meson.build
%endif

%build
%{?with_zypp:CPPFLAGS="%{rpmcppflags} -D_RPM_5 -I/usr/include/rpm"}
%meson build \
	-Dbash_command_not_found=false \
	%{!?with_introspection:-Dgobject_introspection=false} \
	%{?with_doc:-Dgtk_doc=true} \
	-Dpackaging_backend=dummy%{?with_alpm:,alpm}%{?with_apt:,aptcc}%{?with_dnf:,dnf}%{?with_entropy:,entropy}%{?with_poldek:,poldek}%{?with_portage:,portage}%{?with_slack:,slack}%{?with_zypp:,zypp}%{?with_nix:,nix} \
	%{!?with_python:-Dpython_backend=false} \
	-Dpythonpackagedir=%{py_sitescriptdir} \
	-Dsystemdsystemunitdir=%{systemdunitdir}

# TODO:
# -Ddnf_vendor=
# -Dpackagekit_user=

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/cache/PackageKit/downloads

%ninja_install -C build

%{__rm} $RPM_BUILD_ROOT%{_libdir}/packagekit-backend/libpk_backend_test_*.so
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/PackageKit/helpers/test_spawn

# use pk-gstreamer-install as codec installer
ln -s pk-gstreamer-install $RPM_BUILD_ROOT%{_libexecdir}/gst-install-plugins-helper

install -d $RPM_BUILD_ROOT%{systemdunitdir}/system-update.target.wants
ln -sf ../packagekit-offline-update.service \
        $RPM_BUILD_ROOT%{systemdunitdir}/system-update.target.wants/packagekit-offline-update.service

%if %{with python}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}

%py_postclean
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_mime_database

%postun
%update_mime_database

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS HACKING MAINTAINERS NEWS README
%attr(755,root,root) %{_bindir}/pkcon
%attr(755,root,root) %{_bindir}/pkmon
%attr(750,root,root) /etc/cron.daily/packagekit-background.cron
%attr(755,root,root) %{_libexecdir}/packagekit-direct
%attr(755,root,root) %{_libexecdir}/packagekitd
%attr(755,root,root) %{_libexecdir}/pk-offline-update
%dir %{_libdir}/packagekit-backend
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_dummy.so
%dir %{_sysconfdir}/PackageKit
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/PackageKit.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/Vendor.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/packagekit-background
/etc/dbus-1/system.d/org.freedesktop.PackageKit.conf
%dir %{_datadir}/PackageKit
%dir %{_datadir}/PackageKit/helpers
%attr(755,root,root) %{_datadir}/PackageKit/pk-upgrade-distro.sh
%{_datadir}/polkit-1/actions/org.freedesktop.packagekit.policy
%{_datadir}/polkit-1/rules.d/org.freedesktop.packagekit.rules
%{_datadir}/dbus-1/system-services/org.freedesktop.PackageKit.service
%{_mandir}/man1/pkcon.1*
%{_mandir}/man1/pkmon.1*
%{systemdunitdir}/packagekit.service
%{systemdunitdir}/packagekit-offline-update.service
%{systemdunitdir}/system-update.target.wants/packagekit-offline-update.service
%dir /var/cache/PackageKit
%dir /var/cache/PackageKit/downloads
%dir /var/lib/PackageKit
%ghost /var/lib/PackageKit/transactions.db

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-glib2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpackagekit-glib2.so.18
%{_libdir}/girepository-1.0/PackageKitGlib-1.0.typelib
# NOTE: dbus interface xmls are commonly used:
# - at runtime by packagekitd
# - for development of applications using PK dbus interface
%{_datadir}/dbus-1/interfaces/org.freedesktop.PackageKit.Transaction.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.PackageKit.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-glib2.so
%{_pkgconfigdir}/packagekit-glib2.pc
%dir %{_includedir}/PackageKit
%{_includedir}/PackageKit/packagekit-glib2
%{_datadir}/gir-1.0/PackageKitGlib-1.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libpackagekit-glib2.a

%if %{with vala}
%files -n vala-packagekit
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/packagekit-glib2.deps
%{_datadir}/vala/vapi/packagekit-glib2.vapi
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/PackageKit

%if %{with alpm}
%files backend-alpm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_alpm.so
%dir %{_sysconfdir}/PackageKit/alpm.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/alpm.d/groups.list
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/alpm.d/pacman.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/alpm.d/repos.list
%endif

%if %{with apt}
%files backend-aptcc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_aptcc.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apt/apt.conf.d/20packagekit
%dir %{_datadir}/PackageKit/helpers/aptcc
%attr(755,root,root) %{_datadir}/PackageKit/helpers/aptcc/get-distro-upgrade.py
%attr(755,root,root) %{_datadir}/PackageKit/helpers/aptcc/pkconffile
%{_datadir}/PackageKit/helpers/aptcc/pkconffile.nodiff
%endif

%if %{with dnf}
%files backend-dnf
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_dnf.so
%endif

%if %{with entropy}
%files backend-entropy
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_entropy.so
%dir %{_datadir}/PackageKit/helpers/entropy
%attr(755,root,root) %{_datadir}/PackageKit/helpers/entropy/entropyBackend.py
%endif

%if %{with nix}
%files backend-nix
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_nix.so
%endif

%if %{with poldek}
%files backend-poldek
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_poldek.so
%endif

%if %{with portage}
%files backend-portage
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_portage.so
%dir %{_datadir}/PackageKit/helpers/portage
%attr(755,root,root) %{_datadir}/PackageKit/helpers/portage/portageBackend.py
%endif

%if %{with slack}
%files backend-slack
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_slack.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/Slackware.conf
%dir /var/cache/PackageKit/metadata
%ghost /var/cache/PackageKit/metadata/metadata.db
%endif

%if %{with zypp}
%files backend-zypp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_zypp.so
%endif

%files gstreamer-plugin
%defattr(644,root,root,755)
%doc contrib/gstreamer-plugin/README
%attr(755,root,root) %{_libexecdir}/gst-install-plugins-helper
%attr(755,root,root) %{_libexecdir}/pk-gstreamer-install

%files gtk3-module
%defattr(644,root,root,755)
%doc contrib/gtk-module/{GLASS.txt,README}
%attr(755,root,root) %{_libdir}/gtk-3.0/modules/libpk-gtk-module.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/pk-gtk-module.desktop

%files -n bash-completion-packagekit
%defattr(644,root,root,755)
%{bash_compdir}/pkcon

%if %{with python}
%files -n python-packagekit
%defattr(644,root,root,755)
%dir %{py_sitescriptdir}/packagekit
%{py_sitescriptdir}/packagekit/*.py[co]
%endif
