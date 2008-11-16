Summary:	System daemon that is a D-Bus abstraction layer for package management
Summary(pl.UTF-8):	Demon systemowy będący warstwą abstrakcji D-Bus do zarządzania pakietami
Name:		PackageKit
Version:	0.3.4
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	http://www.packagekit.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	5b02713b8b1a18508f64d3db746d710f
URL:		http://www.packagekit.org/
BuildRequires:	NetworkManager-devel >= 0.6.5
BuildRequires:	PolicyKit-devel >= 0.8
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	dbus-devel >= 1.2.0
BuildRequires:	dbus-glib-devel >= 0.76
BuildRequires:	docbook-to-man
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.16.1
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	libarchive-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	poldek-devel >= 0.30-0.20080820.23.2
BuildRequires:	python-devel
BuildRequires:	rpm-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel
Requires(post,postun):	shared-mime-info
Requires:	%{name}-libs = %{version}-%{release}
Requires:	PolicyKit >= 0.8
Requires:	crondaemon
Requires:	poldek >= 0.30-0.20080820.23.2
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

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-poldek \
	--with-html-dir=%{_gtkdocdir} \
	--with-default-backend=poldek
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

%post
%update_mime_database

%postun
%update_mime_database

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog HACKING NEWS README TODO
%attr(755,root,root) %{_bindir}/packagekit-bugreport.sh
%attr(755,root,root) %{_bindir}/pkcon
%attr(755,root,root) %{_bindir}/pkgenpack
%attr(755,root,root) %{_bindir}/pkmon
%attr(750,root,root) /etc/cron.daily/packagekit-background.cron
%attr(755,root,root) %{_libexecdir}/pk-generate-package-list
%attr(755,root,root) %{_libexecdir}/pk-import-desktop
%attr(755,root,root) %{_libexecdir}/pk-import-specspo
%dir %{_libdir}/packagekit-backend
%attr(755,root,root) %{_libdir}/packagekit-backend/libpk_backend_poldek.so
%attr(755,root,root) %{_sbindir}/packagekitd
%dir %{_sysconfdir}/PackageKit
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/PackageKit/PackageKit.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/packagekit-background
/etc/dbus-1/system.d/org.freedesktop.PackageKit.conf
%{_datadir}/PolicyKit/policy/org.freedesktop.packagekit.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.PackageKit.service
%{_datadir}/mime/packages/packagekit-catalog.xml
%{_datadir}/mime/packages/packagekit-pack.xml
%{_mandir}/man1/pkcon.1*
%{_mandir}/man1/pkgenpack.1*
%{_mandir}/man1/pkmon.1*
%dir /var/cache/PackageKit
%dir /var/cache/PackageKit/downloads
%dir /var/lib/PackageKit
%ghost /var/lib/PackageKit/transactions.db
%dir /var/run/PackageKit
%ghost /var/run/PackageKit/job_count.dat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/udev/rules.d/51-packagekit-firmware.rules
%attr(755,root,root) /%{_lib}/udev/packagekit-firmware.sh

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpackagekit.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpackagekit.so.7

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
