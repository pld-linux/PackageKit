# TODO:
# - BASH command-not-found functionality disabled for now as it needs patched bash
#   (details in bash from Fedora Rawhide)
#
# Conditional build:
%bcond_without	doc		# build without docs
%bcond_without	introspection	# gobject introspection, time to time broken
%bcond_with	alpm		# ALPM (Arch Linux package manager) backend
%bcond_with	apt		# APT (Debian/Ubuntu) backend using C++ API
%bcond_with	dnf		# DNF (Fedora/RHEL) backend
%bcond_with	entropy		# Entropy (Sabayon) backend (Python)
%bcond_with	nix		# Nix (NixOS) backend
%bcond_with	pisi		# PiSi (Pardus) backend (Python)
%bcond_without	poldek		# Poldek (PLD) backend
%bcond_with	portage		# portage (Gentoo) backend (Python)
%bcond_with	ports		# ports (FreeBSD) backend (Ruby)
%bcond_with	slack		# Slack (Slackware) backend
%bcond_with	urpmi		# urpmi (Mandriva/Mageia) backend (Perl)
%bcond_with	yum		# YUM (Fedora) backend (Python)
%bcond_with	zypp		# ZYPP (openSUSE/SLE) backend
%bcond_without	python		# Python binding (only for a few backends)
%bcond_without	vala		# Vala binding

# Python binding is built when building any python binding
%if %{without entropy} && %{without pisi} && %{without ports} && %{without yum}
%undefine	with_python
%endif

Summary:	System daemon that is a D-Bus abstraction layer for package management
Summary(pl.UTF-8):	Demon systemowy będący warstwą abstrakcji D-Bus do zarządzania pakietami
Name:		PackageKit
Version:	1.1.13
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	https://www.freedesktop.org/software/PackageKit/releases/%{name}-%{version}.tar.xz
# Source0-md5:	7635892baa047639cf5590d6f57324c1
Patch0:		%{name}-poldek.patch
Patch1:		%{name}-bashcomp.patch

Patch3:		consolekit-fallback.patch
URL:		https://www.freedesktop.org/software/PackageKit/
%{?with_apt:BuildRequires:	AppStream-devel >= 0.11}
BuildRequires:	NetworkManager-devel >= 0.6.5
# pkgconfig(libalpm) >= 12.0.0
%{?with_alpm:BuildRequires:	alpm-devel >= 5.2}
%{?with_dnf:BuildRequires:	appstream-glib-devel}
%{?with_apt:BuildRequires:	apt-devel >= 1.7}
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
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
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	gtk+3-devel >= 3.0.0
%{?with_doc:BuildRequires:	gtk-doc >= 1.11}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libarchive-devel
%{?with_dnf:BuildRequires:	libdnf-devel >= 0.22.0}
%if %{with apt} || %{with nix}
BuildRequires:	libstdc++-devel >= 6:4.7
%endif
%{?with_slack:BuildRequires:	libstdc++-devel >= 6:5}
BuildRequires:	libtool >= 2:2
BuildRequires:	libxslt-progs
%{?with_zypp:BuildRequires:	libzypp-devel >= 15}
# nix-expr nix-main nix-store
%{?with_nix:BuildRequires:	nix-devel >= 1.12}
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
# when released; just to detect which reboot modes to use (library not linked)
#BuildRequires:	plymouth-devel >= 0.9.5
%{?with_poldek:BuildRequires:	poldek-devel >= 0.30-1.rc6.4}
BuildRequires:	polkit-devel >= 0.114
# or 1:3.2
%{?with_python:BuildRequires:	python-devel >= 1:2.7}
BuildRequires:	readline-devel
%{?with_dnf:BuildRequires:	rpm-devel >= 4.?}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.311
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
Obsoletes:	PackageKit-backend-smart
Obsoletes:	PackageKit-backend-yum
Obsoletes:	PackageKit-docs < 0.8.4
Obsoletes:	pm-utils-packagekit
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
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description -n vala-packagekit
Vala API for PackageKit library.

%description -n vala-packagekit -l pl.UTF-8
API języka Vala do biblioteki PackageKitu.

%package apidocs
Summary:	PackageKit library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki PackageKit
Group:		Documentation
Requires:	gtk-doc-common
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

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
Requires:	AppStream >= 0.11
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
Provides:	%{name}-backend = %{version}-%{release}
Obsoletes:	PackageKit-backend-hawkey
Obsoletes:	PackageKit-backend-hif

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

%package backend-pisi
Summary:	PackageKit PiSi backend
Summary(pl.UTF-8):	Backend PackageKit PiSi
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-packagekit = %{version}-%{release}
#Requires:	python-piksemel
#Requires:	python-pisi
Provides:	%{name}-backend = %{version}-%{release}

%description backend-pisi
A backend for PackageKit to enable PiSi packages support. PiSi
packages are originated in Pardus distribution.

%description backend-pisi -l pl.UTF-8
Backend PackageKit dodający obsługę pakietów PiSi. Pakiety PiSi
wywodzą się z dystrybucji Pardus.

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

%package backend-ports
Summary:	PackageKit Ports backend
Summary(pl.UTF-8):	Backend PackageKit Ports
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
#Requires:	ruby-pkgtools
Provides:	%{name}-backend = %{version}-%{release}

%description backend-ports
A backend for PackageKit to enable FreeBSD Ports support.

%description backend-ports -l pl.UTF-8
Backend PackageKit dodający obsługę portów systemu FreeBSD.

%package backend-slack
Summary:	PackageKit Slack backend
Summary(pl.UTF-8):	Backend PackageKit Slack
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-backend = %{version}-%{release}
Obsoletes:	PackageKit-backend-katja

%description backend-slack
Slack backend for PackageKit to enable Slackware repositories support.

%description backend-slack -l pl.UTF-8
Backend PackageKit Slack dodający obsługę repozytoriów Slackware.

%package backend-urpmi
Summary:	PackageKit URPMI backend
Summary(pl.UTF-8):	Backend PackageKit URPMI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
#Requires:	perl-URPM
Provides:	%{name}-backend = %{version}-%{release}

%description backend-urpmi
A backend for PackageKit to enable RPM packages support through URPMI
package manager (originated in Mandriva).

%description backend-urpmi -l pl.UTF-8
Backend PackageKit dodający obsługę pakietów RPM poprzez zarządcę
URPMI (pochodzącego z dystrybucji Mandriva).

%package backend-yum
Summary:	PackageKit YUM backend
Summary(pl.UTF-8):	Backend PackageKit YUM
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-packagekit = %{version}-%{release}
#Requires:	python-urlgrabber
#Requires:	python-rpm # ? import rpmUtils
#Requires:	python-sqlite3
#Requires:	python-yum
Provides:	%{name}-backend = %{version}-%{release}

%description backend-yum
A backend for PackageKit to enable RPM packages support using Yum.

%description backend-yum -l pl.UTF-8
Backend PackageKit dodający obsługę pakietów RPM przy użyciu Yuma.

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
Requires:	%{name}-gtk-module = %{version}-%{release}

%description gstreamer-plugin
The PackageKit GStreamer plugin allows any GStreamer application to
install codecs from configured repositories using PackageKit.

%description gstreamer-plugin -l pl.UTF-8
Wtyczka GStreamer pozwala każdej aplikacji używającej GStreamera
zainstalować kodeki ze skonfigurowanych źródeł PackageKit.

%package gtk-module
Summary:	GTK+ module to detect and install missing fonts
Summary(pl.UTF-8):	Moduł GTK+ do wykrywania i instalowania brakujących czcionek
Group:		X11/Libraries

%description gtk-module
The PackageKit GTK+ module allows any pango application to install
missing fonts from configured repositories using PackageKit.

%description gtk-module -l pl.UTF-8
Moduł GTK+ pozwala każdej aplikacji używającej pango zainstalować
brakującą czcionkę ze skonfigurowanych źródeł PackageKit.

%package gtk3-module
Summary:	GTK+ 3.x module to detect and install missing fonts
Summary(pl.UTF-8):	Moduł GTK+ 3.x do wykrywania i instalowania brakujących czcionek
Group:		X11/Libraries

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
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

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
%patch1 -p1

%patch3 -p1

%build
%if %{with doc}
%{__gtkdocize}
%endif
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%{?with_zypp:CPPFLAGS="%{rpmcppflags} -D_RPM_5 -I/usr/include/rpm"}
%configure \
	--disable-command-not-found \
	--disable-dummy \
	%{!?with_doc:--disable-gtk-doc} \
	%{!?with_introspection:--disable-introspection} \
	--disable-silent-rules \
	--enable-bash-completion=%{bash_compdir} \
	%{__enable_disable alpm} \
	%{__enable_disable apt aptcc} \
	%{__enable_disable dnf} \
	%{__enable_disable entropy} \
	%{__enable_disable nix} \
	%{__enable_disable pisi} \
	%{__enable_disable poldek} \
	%{__enable_disable portage} \
	%{__enable_disable ports} \
	%{__enable_disable slack} \
	%{__enable_disable urpmi} \
	%{__enable_disable yum} \
	%{__enable_disable zypp} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# use pk-gstreamer-install as codec installer
ln -s pk-gstreamer-install $RPM_BUILD_ROOT%{_libdir}/gst-install-plugins-helper

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gtk-{2,3}.0/modules/*.{la,a}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/packagekit-backend/*.{la,a}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/packagekit-backend/libpk_backend_test_*.so
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/PackageKit/helpers/test_spawn

%py_postclean

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

%if %{with pisi}
%files backend-pisi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_pisi.so
%dir %{_datadir}/PackageKit/helpers/pisi
%attr(755,root,root) %{_datadir}/PackageKit/helpers/pisi/pisiBackend.py
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

%if %{with ports}
%files backend-ports
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_ports.so
%dir %{_datadir}/PackageKit/helpers/ports
%attr(755,root,root) %{_datadir}/PackageKit/helpers/ports/portsBackend.rb
%{_datadir}/PackageKit/helpers/ports/ruby_packagekit
%endif

%if %{with slack}
%files backend-slack
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_slack.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/Slackware.conf
%dir /var/cache/PackageKit/metadata
%ghost /var/cache/PackageKit/metadata/metadata.db
%endif

%if %{with urpmi}
%files backend-urpmi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_urpmi.so
%dir %{_datadir}/PackageKit/helpers/urpmi
%attr(755,root,root) %{_datadir}/PackageKit/helpers/urpmi/urpmi-dispatched-backend.pl
%{_datadir}/PackageKit/helpers/urpmi/perl_packagekit
%{_datadir}/PackageKit/helpers/urpmi/urpmi_backend
%endif

%if %{with yum}
%files backend-yum
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_yum.so
%{_datadir}/PackageKit/helpers/yum
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/Yum.conf
%endif

%if %{with zypp}
%files backend-zypp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_zypp.so
%endif

%files gstreamer-plugin
%defattr(644,root,root,755)
%doc contrib/gstreamer-plugin/README
%attr(755,root,root) %{_libdir}/gst-install-plugins-helper
%attr(755,root,root) %{_libexecdir}/pk-gstreamer-install

%files gtk-module
%defattr(644,root,root,755)
%doc contrib/gtk-module/{GLASS.txt,README}
%attr(755,root,root) %{_libdir}/gtk-2.0/modules/libpk-gtk-module.so

%files gtk3-module
%defattr(644,root,root,755)
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
