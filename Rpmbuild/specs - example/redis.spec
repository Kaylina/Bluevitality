Name:             redis
Version:          2.8.5
Release:          2%{?dist}
Summary:          A persistent key-value database

Group:            Applications/Databases
License:          BSD
URL:              http://code.google.com/p/redis/
Source0:          http://redis.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:          %{name}.logrotate
Source2:          %{name}.init
Source3:          sentinel.init
Patch0:           redis-2.8.3-conf.patch
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    tcl

Requires:         logrotate
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(pre):    shadow-utils
Requires(preun):  chkconfig
Requires(preun):  initscripts

%description
Redis is an advanced key-value store. It is similar to memcached but the data
set is not volatile, and values can be strings, exactly like in memcached, but
also lists, sets, and ordered sets. All this data types can be manipulated with
atomic operations to push/pop elements, add/remove elements, perform server side
union, intersection, difference between sets, and so forth. Redis supports
different kind of sorting abilities.

%prep
%setup -q
%patch0 -p1

%build
%ifarch i386 i686
CFLAGS="-march=i686"
export CFLAGS
make
%else
make %{?_smp_mflags}
%endif

%install
rm -fr %{buildroot}
make install PREFIX=%{buildroot}%{_prefix}
# Install misc other
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
install -p -D -m 755 %{SOURCE3} %{buildroot}%{_initrddir}/sentinel
install -p -D -m 644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -p -D -m 644 sentinel.conf %{buildroot}%{_sysconfdir}/sentinel.conf
install -d -m 755 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{name}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{name}

# Fix non-standard-executable-perm error
chmod 755 %{buildroot}%{_bindir}/%{name}-*

# Ensure redis-server location doesn't change
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/%{name}-server %{buildroot}%{_sbindir}/%{name}-server

%clean
rm -fr %{buildroot}

%post
/sbin/chkconfig --add redis
/sbin/chkconfig --add sentinel

%pre
getent group redis &> /dev/null || groupadd -r redis &> /dev/null
getent passwd redis &> /dev/null || \
useradd -r -g redis -d %{_sharedstatedir}/redis -s /sbin/nologin \
-c 'Redis Server' redis &> /dev/null
exit 0

%preun
if [ $1 = 0 ]; then
  /sbin/service redis stop &> /dev/null
  /sbin/chkconfig --del redis &> /dev/null
  /sbin/service sentinel stop &> /dev/null
  /sbin/chkconfig --del sentinel &> /dev/null
fi

%files
%defattr(-,root,root,-)
%doc 00-RELEASENOTES BUGS COPYING README
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%defattr(-,redis,redis,-)
%config(noreplace) %{_sysconfdir}/sentinel.conf
%dir %attr(0755, redis, root) %{_localstatedir}/lib/%{name}
%dir %attr(0755, redis, root) %{_localstatedir}/log/%{name}
%dir %attr(0755, redis, root) %{_localstatedir}/run/%{name}
%{_bindir}/%{name}-*
%{_sbindir}/%{name}-*
%{_initrddir}/%{name}
%{_initrddir}/sentinel


%changelog
* Wed Feb 05 2014 Ivan Polonevich <joni @ wargaming dot net> - 2.8.5-2
- Rebuild for WG

* Wed Feb 05 2014 Denis Frolov <d.frolov81@mail.ru> - 2.8.5-1
- Update to 2.8.5

* Mon Dec 16 2013 Denis Frolov <d.frolov81@mail.ru> - 2.8.3-1
- Update to 2.8.3

* Wed Nov 27 2013 Denis Frolov <d.frolov81@mail.ru> - 2.8.2-1
- Update to 2.8.2

* Wed Nov 27 2013 Denis Frolov <d.frolov81@mail.ru> - 2.8.1-1
- Update to 2.8.1

* Mon Sep 02 2013 Denis Frolov <d.frolov81@mail.ru> - 2.6.16-1
- Update to 2.6.16

* Sat Jul 12 2013 Denis Frolov <d.frolov81@mail.ru> - 2.6.14-1
- Update to 2.6.14

* Sun Mar 31 2013 Denis Frolov <d.frolov81@mail.ru> - 2.6.12-1
- Update to 2.6.12

* Wed Mar 21 2013 Denis Frolov <d.frolov81@mail.ru> - 2.6.11-1
- Update to 2.6.11

* Mon Oct 29 2012 Denis Frolov <d.frolov81@mail.ru> - 2.6.2-1
- Update to 2.6.2

* Fri Sep 07 2012 Denis Frolov <d.frolov81@mail.ru> - 2.4.17-1
- Update to 2.4.17

* Fri Aug 17 2012 Denis Frolov <d.frolov81@mail.ru> - 2.4.16-1
- Update to 2.4.16

* Fri Jul 20 2012 Denis Frolov <d.frolov81@mail.ru> - 2.4.15-1
- Update to 2.4.15

* Sat Jun 09 2012 Denis Frolov <d.frolov81@mail.ru> - 2.4.14-1
- Update to 2.4.14

* Fri May 11 2012 Denis Frolov <d.frolov81@mail.ru> - 2.4.13-1
- Update to 2.4.13

* Tue Apr 19 2012 Denis Frolov <d.frolov81@mail.ru> - 2.4.10-1
- Update to 2.4.10

* Tue Mar 20 2012 Denis Frolov <d.frolov81@mail.ru> - 2.4.9-1
- Update to 2.4.9

* Wed Jan 12 2012 Denis Frolov <d.frolov81@mail.ru> - 2.4.6-1
- Update to 2.4.6

* Sat Apr 23 2011 Silas Sewell <silas@sewell.ch> - 2.2.5-2
- Remove google-perftools-devel

* Sat Apr 23 2011 Silas Sewell <silas@sewell.ch> - 2.2.5-1
- Update to redis 2.2.5

* Tue Oct 19 2010 Silas Sewell <silas@sewell.ch> - 2.0.3-1
- Update to redis 2.0.3

* Fri Oct 08 2010 Silas Sewell <silas@sewell.ch> - 2.0.2-1
- Update to redis 2.0.2
- Disable checks section for el5

* Fri Sep 11 2010 Silas Sewell <silas@sewell.ch> - 2.0.1-1
- Update to redis 2.0.1

* Sat Sep 04 2010 Silas Sewell <silas@sewell.ch> - 2.0.0-1
- Update to redis 2.0.0

* Thu Sep 02 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-3
- Add Fedora build flags
- Send all scriplet output to /dev/null
- Remove debugging flags
- Add redis.conf check to init script

* Mon Aug 16 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-2
- Don't compress man pages
- Use patch to fix redis.conf

* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 1.2.6-1
- Initial package
