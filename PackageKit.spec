# TODO:
# - BASH command-not-found functionality disabled for now as it needs patched bash
#   (details in bash from Fedora Rawhide)
#
# Conditional build:
%bcond_without	qt	# don't build packagekit-qt library
%bcond_without	doc	# build without docs
%bcond_without	gir	# gobject introspection, time to time broken
%bcond_without	poldek	# build Poldek backend
%bcond_without	smart	# build SMART backend
%bcond_without	yum		# build YUM backend
%bcond_with	browser	# build browser plugin (patrys says: it's flawed by concept)

# default backend, configurable at runtime
%define		backend	poldek

Summary:	System daemon that is a D-Bus abstraction layer for package management
Summary(pl.UTF-8):	Demon systemowy będący warstwą abstrakcji D-Bus do zarządzania pakietami
Name:		PackageKit
Version:	0.6.15
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://www.packagekit.org/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	432f505462a00473c941ff907d97953e
Patch1:		%{name}-PLD.patch
Patch2:		bashism.patch
Patch3:		smart-at-fix.patch
URL:		http://www.packagekit.org/
BuildRequires:	NetworkManager-devel >= 0.6.5
%if %{with qt}
BuildRequires:	QtCore-devel >= 4.4.0
BuildRequires:	QtDBus-devel >= 4.4.0
BuildRequires:	QtGui-devel >= 4.4.0
BuildRequires:	QtSql-devel >= 4.4.0
BuildRequires:	QtXml-devel >= 4.4.0
%endif
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1.11
%{?with_qt:BuildRequires:	cppunit-devel}
BuildRequires:	dbus-devel >= 1.2.0
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-dtd42-xml
BuildRequires:	fontconfig-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.22.0
%{?with_gir:BuildRequires:	gobject-introspection-devel}
BuildRequires:	gstreamer-devel
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	gtk+3-devel >= 3.0.0
%{?with_doc:BuildRequires:	gtk-doc >= 1.9}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libarchive-devel
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
BuildRequires:	pm-utils
%{?with_poldek:BuildRequires:	poldek-devel >= 0.30-0.20080820.23.20}
BuildRequires:	polkit-devel >= 0.97
BuildRequires:	python-devel
%{?with_qt:BuildRequires:	qt4-build >= 4.4.0}
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel
BuildRequires:	udev-glib-devel
%if %{with browser}
BuildRequires:	cairo-devel
BuildRequires:	nspr-devel
BuildRequires:	xulrunner-devel
%endif
Requires(post,postun):	shared-mime-info
Requires:	%{name}-backend
Requires:	%{name}-libs = %{version}-%{release}
Requires:	ConsoleKit
Requires:	crondaemon
Requires:	polkit >= 0.92
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
Requires:	glib2 >= 1:2.22.0

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
Requires:	glib2-devel >= 1:2.22.0
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

%package backend-poldek
Summary:	PackageKit Poldek backend
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	poldek >= 0.30-0.20080820.23.20}
Provides:	%{name}-backend
Conflicts:	%{name} < 0.6.8-3

%description backend-poldek
A backend for PackageKit to enable Poldek functionality.

%package backend-smart
Summary:	PackageKit SMART backend
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	smart

%description backend-smart
A backend for PackageKit to enable SMART functionality.

%package backend-yum
Summary:	PackageKit YUM backend
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-packagekit = %{version}-%{release}
Requires:	yum >= 3.2.19
Provides:	%{name}-backend

%description backend-yum
A backend for PackageKit to enable yum functionality.

%package qt
Summary:	packagekit-qt library
Summary(pl.UTF-8):	Biblioteka packagekit-qt
Group:		Libraries
Obsoletes:	packagekit-qt < 0.4.0
Obsoletes:	qpackagekit < 0.4.0

%description qt
packagekit-qt library.

%description qt -l pl.UTF-8
Biblioteka packagekit-qt.

%package qt-devel
Summary:	Header files for packagekit-qt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki packagekit-qt
Group:		Development/Libraries
Requires:	%{name}-qt = %{version}-%{release}
Requires:	QtCore-devel >= 4.4.0
Requires:	QtDBus-devel >= 4.4.0
Requires:	QtGui-devel >= 4.4.0
Requires:	QtSql-devel >= 4.4.0
Requires:	QtXml-devel >= 4.4.0
Obsoletes:	qpackagekit-devel < 0.4.0

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

%package qt2
Summary:	packagekit-qt2 library
Summary(pl.UTF-8):	Biblioteka packagekit-qt2
Group:		Libraries
Obsoletes:	qpackagekit < 0.4.0

%description qt2
packagekit-qt2 library.

%description qt2 -l pl.UTF-8
Biblioteka packagekit-qt2.

%package qt2-devel
Summary:	Header files for packagekit-qt2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki packagekit-qt2
Group:		Development/Libraries
Requires:	%{name}-qt2 = %{version}-%{release}
Requires:	QtCore-devel >= 4.4.0
Requires:	QtDBus-devel >= 4.4.0
Requires:	QtGui-devel >= 4.4.0
Requires:	QtSql-devel >= 4.4.0
Requires:	QtXml-devel >= 4.4.0
Obsoletes:	qpackagekit-devel < 0.4.0

%description qt2-devel
Header files for packagekit-qt2 library.

%description qt2-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki packagekit-qt2.

%package qt2-static
Summary:	Static packagekit-qt2 library
Summary(pl.UTF-8):	Statyczna biblioteka packagekit-qt2
Group:		Development/Libraries
Requires:	%{name}-qt2-devel = %{version}-%{release}

%description qt2-static
Static packagekit-qt2 library.

%description qt2-static -l pl.UTF-8
Statyczna biblioteka packagekit-qt2.

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

%description -n python-packagekit -l pl.UTF-8
Wiązania PackageKit dla Pythona.

%package -n browser-plugin-packagekit
Summary:	PackageKit's browser plugin
Summary(pl.UTF-8):	Wtyczka PackageKit do przeglądarek WWW
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})

%description -n browser-plugin-packagekit
PackageKit's plugin for browsers.

%description -n browser-plugin-packagekit -l pl.UTF-8
Wtyczka PackageKit do przeglądarek WWW.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p0

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
%configure \
	--disable-silent-rules \
	--disable-dummy \
	--disable-command-not-found \
	%{!?with_gir:--disable-introspection} \
	%{__enable_disable browser browser-plugin} \
	%{__enable_disable poldek} \
	%{__enable_disable smart} \
	%{__enable_disable yum} \
	%{__enable_disable dok gtk-doc}\
	%{__enable_disable qt} \
	--with-html-dir=%{_gtkdocdir} \
	--with-default-backend=%{backend} \
	--with-security-framework=polkit \
	--with-mozilla-plugin-dir=%{_browserpluginsdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# use pk-gstreamer-install as codec installer
ln -s pk-gstreamer-install $RPM_BUILD_ROOT%{_libdir}/gst-install-plugins-helper

install -d $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d
install -p contrib/pm-utils/95packagekit $RPM_BUILD_ROOT%{_libdir}/pm-utils/sleep.d

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gtk-{2,3}.0/modules/*.{la,a}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/packagekit-backend/*.{la,a}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/packagekit-backend/libpk_backend_test_*.so
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/PackageKit/helpers/test_spawn

%if %{with browser}
%{__rm} $RPM_BUILD_ROOT%{_browserpluginsdir}/*.{la,a}
%endif

%if %{with yum}
# yumBackend.py can't be compiled (invoked directly), other should be compiled
%py_comp $RPM_BUILD_ROOT%{_datadir}/PackageKit/helpers/yum
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/PackageKit/helpers/yum
%{__rm} $RPM_BUILD_ROOT%{_datadir}/PackageKit/helpers/yum/yum{Comps,Filter}.py
%{__rm} $RPM_BUILD_ROOT%{_datadir}/PackageKit/helpers/yum/yumBackend.py[co]
%endif

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

%post -n browser-plugin-packagekit
%update_browser_plugins

%postun -n browser-plugin-packagekit
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README TODO
%attr(755,root,root) %{_bindir}/packagekit-bugreport.sh
%attr(755,root,root) %{_bindir}/pkcon
%attr(755,root,root) %{_bindir}/pkgenpack
%attr(755,root,root) %{_bindir}/pkmon
%attr(755,root,root) %{_bindir}/pk-debuginfo-install
%attr(750,root,root) /etc/cron.daily/packagekit-background.cron
%dir %{_libdir}/packagekit-backend
%attr(755,root,root) %{_libdir}/packagekitd
%attr(755,root,root) %{_sbindir}/pk-device-rebind
%dir %{_sysconfdir}/PackageKit
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/PackageKit.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/Vendor.conf
%dir %{_sysconfdir}/PackageKit/events
%{_sysconfdir}/PackageKit/events/post-transaction.d
%{_sysconfdir}/PackageKit/events/pre-transaction.d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/packagekit-background
/etc/dbus-1/system.d/org.freedesktop.PackageKit.conf
%dir %{_datadir}/PackageKit
%dir %{_datadir}/PackageKit/helpers
%attr(755,root,root) %{_datadir}/PackageKit/pk-upgrade-distro.sh
%{_datadir}/polkit-1/actions/org.freedesktop.packagekit.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.PackageKit.service
%{_datadir}/mime/packages/packagekit-catalog.xml
%{_datadir}/mime/packages/packagekit-package-list.xml
%{_datadir}/mime/packages/packagekit-servicepack.xml
%{_mandir}/man1/pkcon.1*
%{_mandir}/man1/pk-debuginfo-install.1*
%{_mandir}/man1/pk-device-rebind.1*
%{_mandir}/man1/pkgenpack.1*
%{_mandir}/man1/pkmon.1*
%dir /var/cache/PackageKit
%dir /var/cache/PackageKit/downloads
%dir /var/lib/PackageKit
%ghost /var/lib/PackageKit/transactions.db

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-glib2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpackagekit-glib2.so.14
%{_libdir}/girepository-1.0/PackageKitGlib-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-glib2.so
%{_pkgconfigdir}/packagekit-glib2.pc
%dir %{_includedir}/PackageKit
%{_includedir}/PackageKit/backend
%{_includedir}/PackageKit/packagekit-glib2
%{_datadir}/gir-1.0/PackageKitGlib-1.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libpackagekit-glib2.a

%if %{with poldek}
%files backend-poldek
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_poldek.so
%endif

%if %{with smart}
%files backend-smart
%defattr(644,root,root,755)
%{_libdir}/packagekit-backend/libpk_backend_smart.so
%dir %{_datadir}/PackageKit/helpers/smart
%attr(755,root,root) %{_datadir}/PackageKit/helpers/smart/smartBackend.py
%endif

%if %{with yum}
%files backend-yum
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/Yum.conf
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_yum.so
%dir %{_datadir}/PackageKit/helpers/yum
%{_datadir}/PackageKit/helpers/yum/licenses.txt
%{_datadir}/PackageKit/helpers/yum/yum-comps-groups.conf
%attr(755,root,root) %{_datadir}/PackageKit/helpers/yum/yumBackend.py
%{_datadir}/PackageKit/helpers/yum/yumComps.py[co]
%{_datadir}/PackageKit/helpers/yum/yumFilter.py[co]

# yum plugin
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/yum/pluginconf.d/refresh-packagekit.conf
%{_prefix}/lib/yum-plugins/refresh-packagekit.py
%endif

%if %{with qt}
%files qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-qt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpackagekit-qt.so.14

%files qt-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-qt.so
%{_pkgconfigdir}/packagekit-qt.pc
%{_includedir}/PackageKit/packagekit-qt
%{_datadir}/cmake/Modules/FindQPackageKit.cmake

%files qt-static
%defattr(644,root,root,755)
%{_libdir}/libpackagekit-qt.a

%files qt2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-qt2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpackagekit-qt2.so.2

%files qt2-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-qt2.so
%{_pkgconfigdir}/packagekit-qt2.pc
%{_includedir}/PackageKit/packagekit-qt2
%{_datadir}/cmake/Modules/FindPackageKitQt2.cmake

%files qt2-static
%defattr(644,root,root,755)
%{_libdir}/libpackagekit-qt2.a
%endif

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

%files gtk3-module
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gtk-3.0/modules/libpk-gtk-module.so

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

%if %{with browser}
%files -n browser-plugin-packagekit
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/packagekit-plugin.so
%endif
