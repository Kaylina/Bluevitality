%define _noarch_libdir /usr/lib
%define _kafka_noarch_libdir %{_noarch_libdir}/kafka

%define __jar_repack 0
Summary: Kafka and distributed topic based producer consumer queue
Name: kafka
Version: 0.8.1.1
Release: 1
License: Apache (v2)
Group: Applications
Source0: http://www.eu.apache.org/dist/kafka/%{version}/kafka_2.9.2-%{version}.tgz
Source1: kafka.init
Source2: log4j.properties
Source3: server.properties
Source4: sysconfig
URL: http://kafka.apache.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Distribution: WG
Vendor: m6d
#BuildRequires: java-1.7.0-openjdk-devel
Requires: java-1.7.0-openjdk

%description
Follow this example and you can do no wrong

%prep

%setup -n %{name}_2.9.2-%{version}

%build

%install
pwd
install -p -d %{buildroot}%{_kafka_noarch_libdir}
cp -r bin libs config %{buildroot}%{_kafka_noarch_libdir}

mkdir -p %{buildroot}%{_sysconfdir}/kafka
install -p -D -m 755 %{S:1} %{buildroot}%{_initrddir}/kafka
install -p -D -m 644 %{S:2} %{buildroot}%{_sysconfdir}/kafka
install -p -D -m 644 %{S:3} %{buildroot}%{_sysconfdir}/kafka
install -p -D -m 644 %{S:4} %{buildroot}%{_sysconfdir}/sysconfig/kafka

install -d %{buildroot}%{_localstatedir}/lib/kafka
install -d %{buildroot}%{_localstatedir}/log/kafka

%pre
getent group kafka >/dev/null || groupadd -r kafka
getent passwd kafka >/dev/null || useradd -r -g kafka -d / -s /sbin/nologin kafka
exit 0

%post
/sbin/chkconfig --add kafka

%preun
if [ $1 = 0 ] ; then
  /sbin/service kafka stop >/dev/null 2>&1
  /sbin/chkconfig --del kafka
fi

%postun
if [ "$1" -ge "1" ] ; then
  /sbin/service kafka condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE
%dir %attr(0750, kafka, kafka) %{_localstatedir}/lib/kafka
%dir %attr(0750, kafka, kafka) %{_localstatedir}/log/kafka
%{_kafka_noarch_libdir}
%{_initrddir}/kafka
%config(noreplace) %{_sysconfdir}/sysconfig/kafka
%config(noreplace) %{_sysconfdir}/kafka

%clean
#used to cleanup things outside the build area and possibly inside.

%changelog
* Fri May 02 2014 Ivan Polonevich <joni @ wargaming dot net> - 0.8.1.1-1
Update upstream

* Mon Mar 17 2014 Ivan Polonevich <joni @ wargaming dot net> - 0.8.1-2
- Update upstream

* Wed Jul 11 2012 Edward Capriolo <edward@m6d.com>
- Rebuild against kafka trunk for mirror mode support
* Mon May  7 2012  Edward Capriolo <edward@m6d.com>
- Fix init scripts, clear conf dir, skip system test dir
* Tue May  3 2012  Edward Capriolo <edward@m6d.com>
- Taking care of business
* Tue May  2 2012  Edward Capriolo <edward@m6d.com>
- Oldest at the bottom 

