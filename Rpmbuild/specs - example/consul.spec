Name:           consul
Version:        0.4.0
Release:        2%{?dist}
Summary:        Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

Group:          System Environment/Daemons
License:        MPLv2.0
URL:            http://www.consul.io
#Source0:        https://dl.bintray.com/mitchellh/consul/%{version}_linux_amd64.zip
Source0:        %{version}_linux_amd64.zip
Source1:        consul.init
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%description
Consul is a tool for service discovery and configuration. Consul is distributed, highly available, and extremely scalable.

Consul provides several key features:
 - Service Discovery - Consul makes it simple for services to register themselves and to discover other services via a DNS or HTTP interface. External services such as SaaS providers can be registered as well.
 - Health Checking - Health Checking enables Consul to quickly alert operators about any issues in a cluster. The integration with service discovery prevents routing traffic to unhealthy hosts and enables service level circuit breakers.
 - Key/Value Storage - A flexible key/value store enables storing dynamic configuration, feature flagging, coordination, leader election and more. The simple HTTP API makes it easy to use anywhere.
 - Multi-Datacenter - Consul is built to be datacenter aware, and can support any number of regions without complex configuration.

%prep
%setup -q -c

%install
mkdir -p %{buildroot}/%{_sbindir}
cp consul %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_sysconfdir}/%{name}
mkdir -p %{buildroot}/%{_initrddir}
cp %{_sourcedir}/%{name}.init %{buildroot}/%{_initrddir}/%{name}
mkdir -p %{buildroot}/var/lib/%{name}/data

%post
chkconfig --add %{name}

%preun
/etc/init.d/consul stop
/sbin/chkconfig --del %{name}

%postun

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_sysconfdir}/%{name}
/var/lib/%{name}
/var/lib/%{name}/data
%attr(755, root, root) %{_initrddir}/consul
%attr(755, root, root) %{_sbindir}/consul

%doc


%changelog
* Mon Oct 06 2014 Alexandr Tselobyonock <a_tselobyonock @ wargaming dot net> - 0.4.0-2
- Added /var/lib/consul dir removal on package uninstall

* Mon Oct 06 2014 Alexandr Tselobyonock <a_tselobyonock @ wargaming dot net> - 0.4.0-1
- First release

