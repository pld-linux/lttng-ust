#
# Conditional build:
%bcond_with	java		# JNI interface [builds with java-sun 1.6, but not gcj 4.9]
%bcond_without	python		# Python agent
%bcond_without	systemtap	# SystemTap integration
%bcond_with	static_libs	# static libraries
#
Summary:	LTTng Userspace Tracer
Summary(pl.UTF-8):	LTTng Userspace Tracer - narzędzia LTTng do śledzenia przestrzeni użytkownika
Name:		lttng-ust
Version:	2.14.0
Release:	1
License:	LGPL v2.1 (library), MIT (headers), GPL v2 (programs)
Group:		Libraries
Source0:	https://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2
# Source0-md5:	d5bcaf37ebbf258d2de37326c8c2d4a1
Patch0:		%{name}-link.patch
URL:		https://lttng.org/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.12
# for examples build
BuildRequires:	cmake >= 2.8.11
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool >= 2:2
BuildRequires:	numactl-devel
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python3}
%{?with_python:BuildRequires:	python3-modules}
BuildRequires:	rpmbuild(macros) >= 1.294
BuildRequires:	sed >= 4.0
%{?with_systemtap:BuildRequires:	systemtap-sdt-devel}
BuildRequires:	userspace-rcu-devel >= 0.13
%if %{with java}
BuildRequires:	java-log4j
BuildRequires:	jdk
BuildRequires:	jpackage-utils
%endif
Requires:	userspace-rcu >= 0.13
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm} aarch64 mips ppc ppc64 s390 s390x tile
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# non-function rcu_reader_bp symbol
%define		skip_post_check_so_1	liblttng-ust\.so.* liblttng-ust-cyg-profile\.so.* liblttng-ust-cyg-profile-fast\.so.* liblttng-ust-dl\.so.* liblttng-ust-java\.so.* liblttng-ust-python-agent\.so.* liblttng-ust-tracepoint\.so.*
# non-function lttng_ust_context_info_tls symbol
%define		skip_post_check_so_2	liblttng-ust-jul-jni\.so.* liblttng-ust-log4j-jni\.so.*
# lttng_ust_sigbus_state symbol must be defined in executable
%define		skip_post_check_so_3	liblttng-ust-ctl\.so.*

%define		skip_post_check_so	%{skip_post_check_so_1} %{skip_post_check_so_2} %{skip_post_check_so_3}

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
Requires:	userspace-rcu-devel >= 0.13
%{?with_systemtap:Requires:	systemtap-sdt-devel}

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

%package -n python3-lttng-ust
Summary:	Python agent for LTTng Userspace Tracer library
Summary(pl.UTF-8):	Agent Pythona do biblioteki LTTng Userspace Tracer
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-lttng-ust
Python agent for LTTng Userspace Tracer library.

%description -n python3-lttng-ust -l pl.UTF-8
Agent Pythona do biblioteki LTTng Userspace Tracer.

%prep
%setup -q
%patch -P0 -p1

%{__sed} -i -e '1s,/usr/bin/env python$,%{__python},' tools/lttng-gen-tp

%build
%{__libtoolize}
%{__aclocal} -I config
%{__autoconf}
%{__autoheader}
%{__automake}
export CLASSPATH=.:%{_javadir}/log4j.jar
%configure \
	PYTHON=%{__python3} \
	%{?with_java:JAVA_HOME="%{java_home}" JAVAC=javac} \
	--disable-silent-rules \
	%{?with_java:--enable-jni-interface --enable-java-agent-all} \
	%{?with_python:--enable-python-agent} \
	%{?with_systemtap:--with-sdt} \
	%{?with_static_libs:--enable-static}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	lttnglibjavadir=%{_javadir}

# *.la kept - no .pc files for individual libraries

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/lttng-ust/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/lttng-ust/{ChangeLog,README.md,java-agent.md,python-agent.md}

%if %{with java}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblttng-ust-{context-jni,java,jul-jni,log4j-jni}.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{_libdir}/liblttng-ust-{context-jni,java,jul-jni,log4j-jni}.a}
%endif
%if %{with python}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblttng-ust-python-agent.la \
	%{?with_static_libs:$RPM_BUILD_ROOT%{_libdir}/liblttng-ust-python-agent.a}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n java-lttng-ust -p /sbin/ldconfig
%postun	-n java-lttng-ust -p /sbin/ldconfig

%post	-n python3-lttng-ust -p /sbin/ldconfig
%postun	-n python3-lttng-ust -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE README.md
%attr(755,root,root) %{_libdir}/liblttng-ust.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust.so.1
%attr(755,root,root) %{_libdir}/liblttng-ust-common.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-common.so.1
%attr(755,root,root) %{_libdir}/liblttng-ust-ctl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-ctl.so.6
%attr(755,root,root) %{_libdir}/liblttng-ust-cyg-profile.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-cyg-profile.so.1
%attr(755,root,root) %{_libdir}/liblttng-ust-cyg-profile-fast.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-cyg-profile-fast.so.1
%attr(755,root,root) %{_libdir}/liblttng-ust-dl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-dl.so.1
%attr(755,root,root) %{_libdir}/liblttng-ust-fd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-fd.so.1
%attr(755,root,root) %{_libdir}/liblttng-ust-fork.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-fork.so.1
%attr(755,root,root) %{_libdir}/liblttng-ust-libc-wrapper.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-libc-wrapper.so.1
%attr(755,root,root) %{_libdir}/liblttng-ust-pthread-wrapper.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-pthread-wrapper.so.1
%attr(755,root,root) %{_libdir}/liblttng-ust-tracepoint.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-tracepoint.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lttng-gen-tp
%attr(755,root,root) %{_libdir}/liblttng-ust.so
%attr(755,root,root) %{_libdir}/liblttng-ust-common.so
%attr(755,root,root) %{_libdir}/liblttng-ust-ctl.so
%attr(755,root,root) %{_libdir}/liblttng-ust-cyg-profile.so
%attr(755,root,root) %{_libdir}/liblttng-ust-cyg-profile-fast.so
%attr(755,root,root) %{_libdir}/liblttng-ust-dl.so
%attr(755,root,root) %{_libdir}/liblttng-ust-fd.so
%attr(755,root,root) %{_libdir}/liblttng-ust-fork.so
%attr(755,root,root) %{_libdir}/liblttng-ust-libc-wrapper.so
%attr(755,root,root) %{_libdir}/liblttng-ust-pthread-wrapper.so
%attr(755,root,root) %{_libdir}/liblttng-ust-tracepoint.so
%{_libdir}/liblttng-ust.la
%{_libdir}/liblttng-ust-common.la
%{_libdir}/liblttng-ust-ctl.la
%{_libdir}/liblttng-ust-cyg-profile.la
%{_libdir}/liblttng-ust-cyg-profile-fast.la
%{_libdir}/liblttng-ust-dl.la
%{_libdir}/liblttng-ust-fd.la
%{_libdir}/liblttng-ust-fork.la
%{_libdir}/liblttng-ust-libc-wrapper.la
%{_libdir}/liblttng-ust-pthread-wrapper.la
%{_libdir}/liblttng-ust-tracepoint.la
%{_includedir}/lttng
%{_pkgconfigdir}/lttng-ust.pc
%{_pkgconfigdir}/lttng-ust-ctl.pc
%{_mandir}/man1/lttng-gen-tp.1*
%{_mandir}/man3/do_tracepoint.3*
%{_mandir}/man3/lttng-ust.3*
%{_mandir}/man3/lttng-ust-cyg-profile.3*
%{_mandir}/man3/lttng-ust-dl.3*
%{_mandir}/man3/lttng_ust_*.3*
%{_mandir}/man3/tracef.3*
%{_mandir}/man3/tracelog.3*
%{_mandir}/man3/tracepoint.3*
%{_mandir}/man3/tracepoint_enabled.3*
%{_examplesdir}/%{name}-%{version}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liblttng-ust.a
%{_libdir}/liblttng-ust-common.a
%{_libdir}/liblttng-ust-ctl.a
%{_libdir}/liblttng-ust-cyg-profile.a
%{_libdir}/liblttng-ust-cyg-profile-fast.a
%{_libdir}/liblttng-ust-dl.a
%{_libdir}/liblttng-ust-fd.a
%{_libdir}/liblttng-ust-fork.a
%{_libdir}/liblttng-ust-libc-wrapper.a
%{_libdir}/liblttng-ust-pthread-wrapper.a
%{_libdir}/liblttng-ust-tracepoint.a
%endif

%if %{with java}
%files -n java-lttng-ust
%defattr(644,root,root,755)
%doc doc/java-agent.md
%attr(755,root,root) %{_libdir}/liblttng-ust-context-jni.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-context-jni.so.0
%attr(755,root,root) %{_libdir}/liblttng-ust-context-jni.so
%attr(755,root,root) %{_libdir}/liblttng-ust-java.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-java.so.0
%attr(755,root,root) %{_libdir}/liblttng-ust-java.so
%attr(755,root,root) %{_libdir}/liblttng-ust-jul-jni.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-jul-jni.so.0
%attr(755,root,root) %{_libdir}/liblttng-ust-jul-jni.so
%attr(755,root,root) %{_libdir}/liblttng-ust-log4j-jni.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-log4j-jni.so.0
%attr(755,root,root) %{_libdir}/liblttng-ust-log4j-jni.so
%{_javadir}/liblttng-ust-agent.jar
%{_javadir}/liblttng-ust-java.jar
%{_javadir}/lttng-ust-agent-all-1.0.0.jar
%{_javadir}/lttng-ust-agent-all.jar
%{_javadir}/lttng-ust-agent-common-1.0.0.jar
%{_javadir}/lttng-ust-agent-common.jar
%{_javadir}/lttng-ust-agent-jul-1.0.0.jar
%{_javadir}/lttng-ust-agent-jul.jar
%{_javadir}/lttng-ust-agent-log4j-1.0.0.jar
%{_javadir}/lttng-ust-agent-log4j.jar
%endif

%if %{with python}
%files -n python3-lttng-ust
%defattr(644,root,root,755)
%doc doc/python-agent.md
%attr(755,root,root) %{_libdir}/liblttng-ust-python-agent.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblttng-ust-python-agent.so.1
%attr(755,root,root) %{_libdir}/liblttng-ust-python-agent.so
%{py3_sitescriptdir}/lttngust
%{py3_sitescriptdir}/lttngust-%{version}-py*.egg-info
%endif
