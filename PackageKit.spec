# TODO:
# - BASH command-not-found functionality disabled for now as it needs patched bash
#   (details in bash from Fedora Rawhide)
# - package browser plugin
#
# Conditional build:
%bcond_without	qt	# don't build packagekit-qt library
#
Summary:	System daemon that is a D-Bus abstraction layer for package management
Summary(pl.UTF-8):	Demon systemowy będący warstwą abstrakcji D-Bus do zarządzania pakietami
Name:		PackageKit
Version:	0.4.5
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://www.packagekit.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	a335d299bb7e14d910c600d0975dd375
Patch0:		%{name}-ac.patch
Patch1:		%{name}-PLD.patch
URL:		http://www.packagekit.org/
BuildRequires:	NetworkManager-devel >= 0.6.5
BuildRequires:	PolicyKit-devel >= 0.8
%if %{with qt}
BuildRequires:	QtCore-devel >= 4.4.0
BuildRequires:	QtDBus-devel >= 4.4.0
BuildRequires:	QtGui-devel >= 4.4.0
%endif
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
%{?with_qt:BuildRequires:	cppunit-devel}
BuildRequires:	dbus-devel >= 1.2.0
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	docbook-to-man
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.16.1
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libarchive-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	poldek-devel >= 0.30-0.20080820.23.20
BuildRequires:	python-devel
%{?with_qt:BuildRequires:	qt4-build >= 4.4.0}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel
BuildRequires:	xulrunner-devel
Requires(post,postun):	shared-mime-info
Requires:	%{name}-libs = %{version}-%{release}
Requires:	PolicyKit >= 0.8
Requires:	crondaemon
Requires:	poldek >= 0.30-0.20080820.23.20
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

%description libs
packagekit-glib library.

%description libs -l pl.UTF-8
Biblioteka packagekit-glib.

%package devel
Summary:	Header files for packagekit-glib library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki packagekit-glib
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.16.1

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

%package qt
Summary:	packagekit-qt library
Summary(pl.UTF-8):	Biblioteka packagekit-qt
Group:		Libraries
Obsoletes:	qpackagekit

%description qt
packagekit-qt library.

%description qt -l pl.UTF-8
Biblioteka packagekit-qt.

%package qt-devel
Summary:	Header files for packagekit-qt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki packagekit-qt
Group:		Development/Libraries
Requires:	%{name}-qt = %{version}-%{release}
Obsoletes:	qpackagekit-devel

%description qt-devel
Header files for packagekit-qt library.

%description qt-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki packagekit-qt.

%package qt-static
Summary:	Static packagekit-qt library
Summary(pl.UTF-8):	Statyczna biblioteka packagekit-qt
Group:		Development/Libraries
Requires:	%{name}-qt-devel = %{version}-%{release}

%description qt-static
Static packagekit-qt library.

%description qt-static -l pl.UTF-8
Statyczna biblioteka packagekit-qt.

%package apidocs
Summary:	PackageKit library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki PackageKit
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
PackageKit library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki PackageKit.

%package docs
Summary:	PackageKit documentation
Summary(pl.UTF-8):	Dokumentacja PackageKit
Group:		Documentation

%description docs
PackageKit documentation.

%description docs -l pl.UTF-8
Dokumentacja PackageKit.

%package gstreamer-plugin
Summary:	GStreamer codecs installer
Summary(pl.UTF-8):	Instalator kodeków GStreamera
Group:		Applications
Requires:	%{name} = %{version}-%{release}

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

%package -n bash-completion-packagekit
Summary:	bash-completion for PackageKit
Summary(pl.UTF-8):	bashowe uzupełnianie nazw dla PackageKit
Group:		Applications/Shells
Requires:	bash-completion

%description -n bash-completion-packagekit
This package provides bash-completion for PackageKit.

%description -n bash-completion-packagekit -l pl.UTF-8
Pakiet ten dostarcza bashowe uzupełnianie nazw dla PackageKit.

%package -n pm-utils-packagekit
Summary:	PackageKit script for pm-utils
Summary(pl.UTF-8):	Skrypt PackageKit dla pm-utils
Group:		Applications/System
Requires:	pm-utils

%description -n pm-utils-packagekit
PackageKit script for pm-utils.

%description -n pm-utils-packagekit -l pl.UTF-8
Skrypt PackageKit dla pm-utils.

%package -n python-packagekit
Summary:	PackageKit Python bindings
Summary(pl.UTF-8):	Wiązania PackageKit dla Pythona
Group:		Development/Languages/Python
Requires:	python-dbus
Requires:	python-pygobject

%description -n python-packagekit
PackageKit Python bindings.

%description -n python-packagekit
Wiązania PackageKit dla Pythona.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
mkdir m4

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-dummy \
	--disable-ruck \
	--disable-command-not-found \
	--enable-poldek \
	--%{?with_qt:en}%{!?with_qt:dis}able-qt \
	--with-html-dir=%{_gtkdocdir} \
	--with-default-backend=poldek
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# use pk-gstreamer-install as codec installer
ln -s pk-gstreamer-install $RPM_BUILD_ROOT%{_libdir}/gst-install-plugins-helper

rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.{la,a}
rm -f $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/*.{la,a}
rm -f $RPM_BUILD_ROOT%{_libdir}/packagekit-backend/*.{la,a}
rm -f $RPM_BUILD_ROOT%{_libdir}/packagekit-backend/libpk_backend_test_*.so
rm -f $RPM_BUILD_ROOT%{_libdir}/PackageKitDbusTest.py
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d/org.freedesktop.PackageKit{Apt,Test}Backend.conf
rm -f $RPM_BUILD_ROOT%{_datadir}/dbus-1/system-services/org.freedesktop.PackageKit{Apt,Test}Backend.service
rm -rf $RPM_BUILD_ROOT%{_datadir}/PackageKit/helpers/test_spawn

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

%post	qt -p /sbin/ldconfig
%postun	qt -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README TODO
%attr(755,root,root) %{_bindir}/packagekit-bugreport.sh
%attr(755,root,root) %{_bindir}/pkcon
%attr(755,root,root) %{_bindir}/pkgenpack
%attr(755,root,root) %{_bindir}/pkmon
%attr(750,root,root) /etc/cron.daily/packagekit-background.cron
%dir %{_libdir}/packagekit-backend
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_poldek.so
%attr(755,root,root) %{_sbindir}/packagekitd
%dir %{_sysconfdir}/PackageKit
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/PackageKit.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/Vendor.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysconfig/packagekit-background
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.PackageKit.conf
%dir %{_datadir}/PackageKit
%attr(755,root,root) %{_datadir}/PackageKit/pk-upgrade-distro.sh
%{_datadir}/PolicyKit/policy/org.freedesktop.packagekit.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.PackageKit.service
%{_datadir}/mime/packages/packagekit-catalog.xml
%{_datadir}/mime/packages/packagekit-package-list.xml
%{_datadir}/mime/packages/packagekit-servicepack.xml
%{_mandir}/man1/pkcon.1*
%{_mandir}/man1/pkgenpack.1*
%{_mandir}/man1/pkmon.1*
%dir /var/cache/PackageKit
%dir /var/cache/PackageKit/downloads
%dir /var/lib/PackageKit
%ghost /var/lib/PackageKit/job_count.dat
%ghost /var/lib/PackageKit/transactions.db

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpackagekit-glib.so.11

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-glib.so
%{_libdir}/libpackagekit-glib.la
%{_pkgconfigdir}/packagekit-glib.pc
%dir %{_includedir}/PackageKit
%{_includedir}/PackageKit/backend
%{_includedir}/PackageKit/packagekit-glib

%files static
%defattr(644,root,root,755)
%{_libdir}/libpackagekit-glib.a

%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-qt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpackagekit-qt.so.11

%files qt-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-qt.so
%{_libdir}/libpackagekit-qt.la
%{_pkgconfigdir}/packagekit-qt.pc
%{_includedir}/PackageKit/packagekit-qt
%{_datadir}/cmake/Modules/FindQPackageKit.cmake

%files qt-static
%defattr(644,root,root,755)
%{_libdir}/libpackagekit-qt.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/PackageKit

%files docs
%defattr(644,root,root,755)
%{_datadir}/PackageKit/website

%files gstreamer-plugin
%defattr(644,root,root,755)
%doc contrib/gstreamer-plugin/README
%attr(755,root,root) %{_libdir}/gst-install-plugins-helper
%attr(755,root,root) %{_libdir}/pk-gstreamer-install

%files gtk-module
%defattr(644,root,root,755)
%doc contrib/gtk-module/{GLASS.txt,README}
%attr(755,root,root) %{_libdir}/gtk-2.0/modules/libpk-gtk-module.so

%files -n bash-completion-packagekit
%defattr(644,root,root,755)
%{_sysconfdir}/bash_completion.d/pk-completion.bash

%files -n pm-utils-packagekit
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/pm-utils/sleep.d/95packagekit

%files -n python-packagekit
%defattr(644,root,root,755)
%dir %{py_sitescriptdir}/packagekit
%{py_sitescriptdir}/packagekit/*.py[co]
