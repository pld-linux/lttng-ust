#
# Conditional build:
%bcond_without	java		# JNI interface
%bcond_without	systemtap	# SystemTap integration
#
Summary:	LTTng Userspace Tracer
Summary(pl.UTF-8):	LTTng Userspace Tracer - narzędzia LTTng do śledzenia przestrzeni użytkownika
Name:		lttng-ust
Version:	2.2.0
Release:	1
License:	LGPL v2.1 (library), MIT (headers), GPL v2 (programs)
Group:		Libraries
Source0:	http://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2
# Source0-md5:	b659444593f67d9b07abc73f7aa123e3
Patch0:		%{name}-link.patch
URL:		http://lttng.org/ust
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_java:BuildRequires:	jdk}
BuildRequires:	rpmbuild(macros) >= 1.294
BuildRequires:	libtool >= 2:2
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
BuildRequires:	userspace-rcu-devel >= 0.7.2
Requires:	userspace-rcu >= 0.7.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# rcu_reader_bp is some kind of symbol that check doesn't support
%define		skip_post_check_so	liblttng-ust-cyg-profile\.so.* liblttng-ust-cyg-profile-fast\.so.* liblttng-ust-tracepoint\.so.*

%description
The LTTng Userspace Tracer (UST) is a library accompanied by a set of
tools to trace userspace code. 

%description -l pl.UTF-8
LTTng Userspace Tracer (UST) to biblioteka, której towarzyszą
narzędzia do śledzenia kodu w przestrzeni użytkownika.

%package devel
Summary:	Header files for LTTNG-UST libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek LTTNG-UST
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	userspace-rcu-devel >= 0.7.2

%description devel
Header files for LTTNG-UST libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek LTTNG-UST.

%package static
Summary:	Static LTTNG-UST libraries
Summary(pl.UTF-8):	Statyczne biblioteki LTTNG-UST
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LTTNG-UST libraries.

%description static -l pl.UTF-8
Statyczne biblioteki LTTNG-UST.

%package -n java-lttng-ust
Summary:	JNI interface for LTTng Userspace Tracer library
Summary(pl.UTF-8):	Interfejs JNI do biblioteki LTTng Userspace Tracer
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description -n java-lttng-ust
JNI interface for LTTng Userspace Tracer library.

%description -n java-lttng-ust -l pl.UTF-8
Interfejs JNI do biblioteki LTTng Userspace Tracer.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
%{?with_java:CPPFLAGS="%{rpmcppflags} -I%{_jvmdir}/java/include -I%{_jvmdir}/java/include/linux"}
%configure \
	--disable-silent-rules \
	%{?with_java:--with-jni-interface} \
	%{?with_systemtap:--with-sdt}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# *.la kept - no .pc files for individual libraries

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/lttng-ust/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/lttng-ust/{ChangeLog,README}

%if %{with java}
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p liblttng-ust-java/liblttng-ust-java.jar $RPM_BUILD_ROOT%{_javadir}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblttng-ust-java.{la,a}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n java-lttng-ust -p /sbin/ldconfig
%postun	-n java-lttng-ust -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog README
%attr(755,root,root) %{_libdir}/liblttng-ust.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust.so.0
%attr(755,root,root) %{_libdir}/liblttng-ust-ctl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-ctl.so.2
%attr(755,root,root) %{_libdir}/liblttng-ust-cyg-profile.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-cyg-profile.so.0
%attr(755,root,root) %{_libdir}/liblttng-ust-cyg-profile-fast.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-cyg-profile-fast.so.0
%attr(755,root,root) %{_libdir}/liblttng-ust-fork.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-fork.so.0
%attr(755,root,root) %{_libdir}/liblttng-ust-libc-wrapper.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-libc-wrapper.so.0
%attr(755,root,root) %{_libdir}/liblttng-ust-tracepoint.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-tracepoint.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lttng-gen-tp
%attr(755,root,root) %{_libdir}/liblttng-ust.so
%attr(755,root,root) %{_libdir}/liblttng-ust-ctl.so
%attr(755,root,root) %{_libdir}/liblttng-ust-cyg-profile.so
%attr(755,root,root) %{_libdir}/liblttng-ust-cyg-profile-fast.so
%attr(755,root,root) %{_libdir}/liblttng-ust-fork.so
%attr(755,root,root) %{_libdir}/liblttng-ust-libc-wrapper.so
%attr(755,root,root) %{_libdir}/liblttng-ust-tracepoint.so
%{_libdir}/liblttng-ust.la
%{_libdir}/liblttng-ust-ctl.la
%{_libdir}/liblttng-ust-cyg-profile.la
%{_libdir}/liblttng-ust-cyg-profile-fast.la
%{_libdir}/liblttng-ust-fork.la
%{_libdir}/liblttng-ust-libc-wrapper.la
%{_libdir}/liblttng-ust-tracepoint.la
%{_includedir}/lttng
%{_pkgconfigdir}/lttng-ust.pc
%{_mandir}/man1/lttng-gen-tp.1*
%{_mandir}/man3/lttng-ust.3*
%{_mandir}/man3/lttng-ust-cyg-profile.3*
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/liblttng-ust.a
%{_libdir}/liblttng-ust-ctl.a
%{_libdir}/liblttng-ust-cyg-profile.a
%{_libdir}/liblttng-ust-cyg-profile-fast.a
%{_libdir}/liblttng-ust-fork.a
%{_libdir}/liblttng-ust-libc-wrapper.a
%{_libdir}/liblttng-ust-tracepoint.a

%if %{with java}
%files -n java-lttng-ust
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblttng-ust-java.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-java.so.0
%attr(755,root,root) %{_libdir}/liblttng-ust-java.so
%{_javadir}/liblttng-ust-java.jar
%endif
