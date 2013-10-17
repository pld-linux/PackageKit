# TODO:
# - send poldek patch upstream
# - BASH command-not-found functionality disabled for now as it needs patched bash
#   (details in bash from Fedora Rawhide)
#
# Conditional build:
%bcond_without	doc	# build without docs
%bcond_without	gir	# gobject introspection, time to time broken
%bcond_without	poldek	# build Poldek backend
%bcond_without	smart	# build SMART backend
%bcond_without	yum	# build YUM backend
%bcond_with	browser	# build browser plugin (patrys says: it's flawed by concept)

# default backend, configurable at runtime
%define		backend	poldek

Summary:	System daemon that is a D-Bus abstraction layer for package management
Summary(pl.UTF-8):	Demon systemowy będący warstwą abstrakcji D-Bus do zarządzania pakietami
Name:		PackageKit
Version:	0.8.11
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://www.packagekit.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	676ebf95830373b84d5599f4e5039b72
Patch0:		%{name}-poldek.patch
Patch1:		%{name}-PLD.patch
Patch2:		bashism.patch
Patch3:		smart-at-fix.patch
Patch4:		%{name}-gstreamer.patch
Patch5:		%{name}-bashcomp.patch
Patch6:		%{name}-connman.patch
URL:		http://www.packagekit.org/
BuildRequires:	NetworkManager-devel >= 0.6.5
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
BuildRequires:	connman-devel
BuildRequires:	dbus-devel >= 1.2.0
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-dtd42-xml
BuildRequires:	fontconfig-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.30.0
%{?with_gir:BuildRequires:	gobject-introspection-devel >= 0.9.9}
BuildRequires:	gstreamer-devel >= 1.0.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0.0
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	gtk+3-devel >= 3.0.0
%{?with_doc:BuildRequires:	gtk-doc >= 1.11}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libarchive-devel
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
BuildRequires:	pm-utils
%{?with_poldek:BuildRequires:	poldek-devel >= 0.30-1.rc6.4}
BuildRequires:	polkit-devel >= 0.98
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	readline-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	systemd-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel
BuildRequires:	xz
%if %{with browser}
BuildRequires:	cairo-devel
BuildRequires:	nspr-devel >= 4.8
BuildRequires:	xulrunner-devel >= 8.0
%endif
Requires(post,postun):	shared-mime-info
Requires:	%{name}-backend
Requires:	%{name}-libs = %{version}-%{release}
Requires:	ConsoleKit-x11
Requires:	crondaemon
Requires:	polkit >= 0.92
Obsoletes:	PackageKit-docs < 0.8.4
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
Requires:	glib2 >= 1:2.30.0

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
Requires:	glib2-devel >= 1:2.30.0
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

%package apidocs
Summary:	PackageKit library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki PackageKit
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
PackageKit library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki PackageKit.

%package backend-poldek
Summary:	PackageKit Poldek backend
Summary(pl.UTF-8):	Backend PackageKit oparty na Poldku
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	poldek >= 0.30-1.rc6.4
Provides:	%{name}-backend = %{version}-%{release}
Conflicts:	PackageKit < 0.6.8-3

%description backend-poldek
A backend for PackageKit to enable Poldek functionality.

%description backend-poldek -l pl.UTF-8
Backend PackageKit dodający obsługę Poldka.

%package backend-smart
Summary:	PackageKit SMART backend
Summary(pl.UTF-8):	Backend PackageKit oparty na zarządcy pakietów SMART
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	smart

%description backend-smart
A backend for PackageKit to enable SMART functionality.

%description backend-smart -l pl.UTF-8
Backend PackageKit dodający obsługę zarządcy pakietów SMART.

%package backend-yum
Summary:	PackageKit YUM backend
Summary(pl.UTF-8):	Backend PackageKit oparty na Yumie
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-packagekit = %{version}-%{release}
Requires:	yum >= 3.2.19
Provides:	%{name}-backend = %{version}-%{release}

%description backend-yum
A backend for PackageKit to enable yum functionality.

%description backend-yum -l pl.UTF-8
Backend PackageKit dodający obsługę Yuma.

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

%description -n bash-completion-packagekit
This package provides bash-completion for PackageKit console commands.

%description -n bash-completion-packagekit -l pl.UTF-8
Pakiet ten dostarcza bashowe uzupełnianie parametrów dla poleceń
konsolowych PackageKit.

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1

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
	--disable-command-not-found \
	--disable-dummy \
	%{!?with_doc:--disable-gtk-doc} \
	%{!?with_gir:--disable-introspection} \
	--disable-silent-rules \
	--enable-bash-completion=%{bash_compdir} \
	%{__enable_disable browser browser-plugin} \
	%{__enable_disable poldek} \
	%{__enable_disable smart} \
	%{__enable_disable yum} \
	--with-default-backend=%{backend} \
	--with-html-dir=%{_gtkdocdir} \
	--with-mozilla-plugin-dir=%{_browserpluginsdir} \
	--with-security-framework=polkit
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
%{__rm} $RPM_BUILD_ROOT%{_libdir}/packagekit-plugins/*.{la,a}
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

# outdated copy of it
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/it_IT

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

%post -n browser-plugin-packagekit
%update_browser_plugins

%postun -n browser-plugin-packagekit
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS HACKING MAINTAINERS NEWS README TODO
%attr(755,root,root) %{_bindir}/packagekit-bugreport.sh
%attr(755,root,root) %{_bindir}/pkcon
%attr(755,root,root) %{_bindir}/pkgenpack
%attr(755,root,root) %{_bindir}/pkmon
%attr(755,root,root) %{_bindir}/pk-debuginfo-install
%attr(750,root,root) /etc/cron.daily/packagekit-background.cron
%dir %{_libdir}/packagekit-backend
%dir %{_libdir}/packagekit-plugins
%attr(755,root,root) %{_libdir}/packagekit-plugins/libpk_plugin-check-shared-libraries-in-use.so
%attr(755,root,root) %{_libdir}/packagekit-plugins/libpk_plugin-clear-firmware-requests.so
%attr(755,root,root) %{_libdir}/packagekit-plugins/libpk_plugin-no-update-process.so
%attr(755,root,root) %{_libdir}/packagekit-plugins/libpk_plugin-require-restart.so
%attr(755,root,root) %{_libdir}/packagekit-plugins/libpk_plugin-scan-desktop-files.so
%attr(755,root,root) %{_libdir}/packagekit-plugins/libpk_plugin-systemd-updates.so
%attr(755,root,root) %{_libdir}/packagekit-plugins/libpk_plugin-update-check-processes.so
%attr(755,root,root) %{_libdir}/packagekit-plugins/libpk_plugin-update-package-cache.so
%attr(755,root,root) %{_libdir}/packagekit-plugins/libpk_plugin_scripts.so
%attr(755,root,root) %{_libdir}/packagekitd
%attr(755,root,root) %{_libdir}/pk-clear-offline-update
%attr(755,root,root) %{_libdir}/pk-offline-update
%attr(755,root,root) %{_libdir}/pk-trigger-offline-update
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
%{_datadir}/polkit-1/rules.d/org.freedesktop.packagekit.rules
%{_datadir}/dbus-1/system-services/org.freedesktop.PackageKit.service
%{_datadir}/mime/packages/packagekit-catalog.xml
%{_datadir}/mime/packages/packagekit-package-list.xml
%{_datadir}/mime/packages/packagekit-servicepack.xml
%{_mandir}/man1/pkcon.1*
%{_mandir}/man1/pk-debuginfo-install.1*
%{_mandir}/man1/pk-device-rebind.1*
%{_mandir}/man1/pkgenpack.1*
%{_mandir}/man1/pkmon.1*
%{systemdunitdir}/packagekit-offline-update.service
%dir /var/cache/PackageKit
%dir /var/cache/PackageKit/downloads
%dir /var/lib/PackageKit
%ghost /var/lib/PackageKit/transactions.db

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-glib2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpackagekit-glib2.so.16
%{_libdir}/girepository-1.0/PackageKitGlib-1.0.typelib
%{_libdir}/girepository-1.0/PackageKitPlugin-1.0.typelib
# NOTE: dbus interface xmls are commonly used:
# - at runtime by packagekitd
# - for development of applications using PK dbus interface
%{_datadir}/dbus-1/interfaces/org.freedesktop.PackageKit.Transaction.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.PackageKit.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit-glib2.so
%{_pkgconfigdir}/packagekit-glib2.pc
%{_pkgconfigdir}/packagekit-plugin.pc
%dir %{_includedir}/PackageKit
%{_includedir}/PackageKit/packagekit-glib2
%{_includedir}/PackageKit/plugin
%{_datadir}/gir-1.0/PackageKitGlib-1.0.gir
%{_datadir}/gir-1.0/PackageKitPlugin-1.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libpackagekit-glib2.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/PackageKit

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
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/pk-gtk-module.desktop

%files -n bash-completion-packagekit
%defattr(644,root,root,755)
%{bash_compdir}/pkcon

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
