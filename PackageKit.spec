Summary:	System daemon that is a D-BUS abstraction layer for package management
Name:		PackageKit
Version:	0.2.1
Release:	2
License:	GPL v2+
Group:		Applications
Source0:	http://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.gz
# Source0-md5:	ffc256f14094ecdbb8b734fe19d0e690
URL:		http://www.packagekit.org/
BuildRequires:	NetworkManager-devel >= 0.6.5
BuildRequires:	PolicyKit-devel >= 0.8
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	dbus-devel >= 1.2.0
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	docbook-to-man
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.16.1
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	poldek-devel >= 0.30-0.20080225.00.7
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	sqlite3-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	PolicyKit >= 0.8
Requires:	crondaemon
Requires:	poldek >= 0.30-0.20080225.00.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PackageKit is a D-Bus abstraction layer that allows the session user
to manage packages in a secure way using a cross-distro,
cross-architecture API.

%package libs
Summary:	PackageKit library
Summary(pl.UTF-8):	Biblioteka PackageKit
Group:		Libraries

%description libs
PackageKit library.

%description libs -l pl.UTF-8
Biblioteka PackageKit.

%package devel
Summary:	Header files for PackageKit
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki PackageKit
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.16.1

%description devel
Header files for PackageKit library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki PackageKit.

%package static
Summary:	Static PackageKit library
Summary(pl.UTF-8):	Statyczna biblioteka PackageKit
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static PackageKit library.

%description static -l pl.UTF-8
Statyczna biblioteka PackageKit.

%package apidocs
Summary:	PackageKit library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki PackageKit
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
PackageKit library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki PackageKit.

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
Group:		Applications/System
Requires:	pm-utils

%description -n pm-utils-packagekit
PackageKit script for pm-utils.

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

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-poldek \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/packagekit-backend/*.{la,a}

mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{no_nb,nb}

%if "%{_lib}" != "lib"
mv $RPM_BUILD_ROOT/{lib,%{_lib}}
%endif

%py_postclean

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README TODO
%attr(755,root,root) %{_bindir}/packagekit-bugreport.sh
%attr(755,root,root) %{_bindir}/pkcon
%attr(755,root,root) %{_bindir}/pkmon
%attr(750,root,root) /etc/cron.daily/packagekit-background.cron
%attr(755,root,root) %{_libexecdir}/pk-import-desktop
%attr(755,root,root) %{_libexecdir}/pk-import-specspo
%dir %{_libdir}/packagekit-backend
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_poldek.so
%attr(755,root,root) %{_sbindir}/packagekitd
%dir %{_sysconfdir}/PackageKit
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/PackageKit.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysconfig/packagekit-background
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.PackageKit.conf
%{_datadir}/PolicyKit/policy/org.freedesktop.packagekit.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.PackageKit.service
%{_mandir}/man1/pkmon.1*
%{_mandir}/man1/pkcon.1*
%dir /var/lib/PackageKit
%ghost /var/lib/PackageKit/transactions.db
%dir /var/run/PackageKit
%ghost /var/run/PackageKit/job_count.dat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/51-packagekit-firmware.rules
%attr(755,root,root) /%{_lib}/udev/packagekit-firmware.sh

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpackagekit.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit.so
%{_libdir}/libpackagekit.la
%{_pkgconfigdir}/packagekit.pc
%{_includedir}/packagekit
%{_includedir}/packagekit-backend

%files static
%defattr(644,root,root,755)
%{_libdir}/libpackagekit.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/PackageKit

%files -n bash-completion-packagekit
%defattr(644,root,root,755)
%{_sysconfdir}/bash_completion.d/pk-completion.bash

%files -n pm-utils-packagekit
%defattr(644,root,root,755)
%{_libdir}/pm-utils/sleep.d/95packagekit

%files -n python-packagekit
%defattr(644,root,root,755)
%dir %{py_sitescriptdir}/packagekit
%{py_sitescriptdir}/packagekit/*.py[co]
