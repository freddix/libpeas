Summary:	GObject Plugin System
Name:		libpeas
Version:	1.8.0
Release:	1
License:	LGPL v2
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/libpeas/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	31ac6d2341d7a358d48808a547ab8660
URL:		http://live.gnome.org/Libpeas
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gjs-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	python
BuildRequires:	python-pygobject3-devel
BuildRequires:	python3-devel
#BuildRequires:	seed-devel
BuildRequires:	vala
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libpeas is a gobject-based plugins engine, and is targetted at giving
every application the chance to assume its own extensibility. It also
has a set of features including, but not limited to:

 - multiple extension points
 - on demand (lazy) programming language support for C, Python and JS
 - simplicity of the API

%package loader-python
Summary:	Python loader for libpeas library
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description loader-python
Python loader for libpeas library.

%package loader-python3
Summary:	Python3 loader for libpeas library
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description loader-python3
Python3 loader for libpeas library.

%package loader-seed
Summary:	JavaScript (seed) loader for libpeas library
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description loader-seed
JavaScript (seed) loader for libpeas library.

%package loader-gjs
Summary:	JavaScript (GJS) loader for libpeas library
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description loader-gjs
JavaScript (GJS) loader for libpeas library.

%package devel
Summary:	Header files for libpeas library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libpeas library.

%package gtk
Summary:	GObject Plugin System
Group:		X11/Libraries
Requires(post,postun):	gtk+-update-icon-cache
Requires:	%{name} = %{version}-%{release}
Requires:	hicolor-icon-theme

%description gtk
libpeas is a gobject-based plugins engine, and is targetted at giving
every application the chance to assume its own extensibility. It also
has a set of features including, but not limited to:

 - multiple extension points
 - on demand (lazy) programming language support for C, Python and JS
 - simplicity of the API

%package gtk-devel
Summary:	Header files for libpeas-gtk library
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-gtk = %{version}-%{release}

%description gtk-devel
Header files for libpeas-gtk library.

%package apidocs
Summary:	libpeas API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API and internal documentation for libpeas library.

%prep
%setup -q

# kill gnome common deps
sed -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

sed -i 's/peas-demo//' Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-seed		\
	--disable-silent-rules	\
	--disable-static	\
	--enable-vala		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*/*/*.la

%find_lang libpeas

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%post gtk
/sbin/ldconfig
%update_icon_cache hicolor

%postun	gtk
/sbin/ldconfig
%update_icon_cache hicolor

%files -f libpeas.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %ghost %{_libdir}/libpeas-1.0.so.?
%attr(755,root,root) %{_libdir}/libpeas-1.0.so.*.*.*
%dir %{_libdir}/libpeas-1.0
%dir %{_libdir}/libpeas-1.0/loaders
%{_libdir}/girepository-1.0/Peas-1.0.typelib

%files loader-python
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpeas-1.0/loaders/libpythonloader.so

%files loader-python3
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpeas-1.0/loaders/libpython3loader.so

%if 0
%files loader-seed
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpeas-1.0/loaders/libseedloader.so
%endif

%files loader-gjs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpeas-1.0/loaders/libgjsloader.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpeas-1.0.so
%{_includedir}/libpeas-1.0
%{_pkgconfigdir}/libpeas-1.0.pc
%{_datadir}/gir-1.0/Peas-1.0.gir

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libpeas-gtk-1.0.so.?
%attr(755,root,root) %{_libdir}/libpeas-gtk-1.0.so.*.*.*
%{_libdir}/girepository-1.0/PeasGtk-1.0.typelib
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/scalable/*/*.svg

%files gtk-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpeas-gtk-1.0.so
%{_pkgconfigdir}/libpeas-gtk-1.0.pc
%{_datadir}/gir-1.0/PeasGtk-1.0.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libpeas

