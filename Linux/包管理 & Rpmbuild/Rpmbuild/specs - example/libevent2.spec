%define real_name libevent
Name:           libevent
Version:        2.0.21
Release:        1%{?dist}
Summary:        Abstract asynchronous event notification library

Group:          System Environment/Libraries
License:        BSD
URL:            http://libevent.org
Source0:        https://github.com/downloads/%{real_name}/%{real_name}/%{real_name}-%{version}-stable.tar.gz
BuildRequires:  openssl-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides: 	libevent 
Requires: 	compat-libevent14

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{real_name}. If you like to develop programs using %{real_name},
you will need to install %{real_name}-devel.


%prep
%setup -q -n libevent-%{version}-stable

%build
%configure \
    --disable-dependency-tracking
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

#%check
#make verify

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,0755)
%doc README
%{_libdir}/libevent-*.so.*
%{_libdir}/libevent_core-*.so.*
%{_libdir}/libevent_extra-*.so.*

%files devel
%defattr(-,root,root,0755)
%doc sample/*.c
%{_includedir}/evdns.h
%{_includedir}/event.h
%{_includedir}/evhttp.h
%{_includedir}/evrpc.h
%{_includedir}/evutil.h
%{_includedir}/event2/*.h
%{_libdir}/libevent.so
%{_libdir}/libevent.a
%{_libdir}/libevent_core.so
%{_libdir}/libevent_core.a
%{_libdir}/libevent_extra.so
%{_libdir}/libevent_extra.a
%{_libdir}/libevent_openssl-2.0.so.5
%{_libdir}/libevent_openssl-2.0.so.5.*
%{_libdir}/libevent_openssl.a
%{_libdir}/libevent_openssl.so
%{_libdir}/libevent_pthreads-2.0.so.5
%{_libdir}/libevent_pthreads-2.0.so.5.*
%{_libdir}/libevent_pthreads.a
%{_libdir}/libevent_pthreads.so
%{_libdir}/pkgconfig/libevent.pc
%{_libdir}/pkgconfig/libevent_openssl.pc
%{_libdir}/pkgconfig/libevent_pthreads.pc

%{_bindir}/event_rpcgen.*

%changelog
* Wed Jul 02 2014 Ivan Polonevich <joni @ wargaming dot net> - 2.0.19-2
- Rebuild for WG
- add deps openssl-dev

* Fri Jul 27 2012 Devrim GUNDUZ <devrim@gunduz.org> 2.0.19-1
- Update to 2.0.19

* Tue Aug 09 2011 Devrim GUNDUZ <devrim@gunduz.org> 2.0.12-1
- Update to 2.0.12

* Thu Nov 11 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.4.13-2
- Update to 1.4.13
- Use bigger release number, so that repos will pick up this one.

* Tue Jan 13 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.4.9-1
- Initial build for PostgreSQL RPM Repository, based on Fedora spec.
