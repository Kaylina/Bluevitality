%define prefix /opt/netxms
%define debug_package %{nil}
%define relise_vers 4
%define main_ver 2.0
%define vermodif M

Name         : netxms
Version      : %{main_ver}
Vendor       : Raden Solutions
Release      : %{vermodif}%{relise_vers}.3%{?dist}
Group        : Applications/Monitoring
License      : LGPL
Packager     : Ivan Polonevich <loverjoni at gmai.com>
Source	     : http://www.netxms.org/download/%{name}-%{version}-%{vermodif}%{relise_vers}.tar.gz
Source1      : http://www.netxms.org/download/webui/nxmc-%{version}-%{vermodif}%{relise_vers}.war
Source3      : http://www.netxms.org/download/nxshell-%{version}-%{vermodif}%{relise_vers}.jar
Source4      : netxms_profile_d
URL          : http://www.netxms.org/
Summary      : Monitoring system for Unix/Linux systems
BuildRoot    : %{_tmppath}/%{name}-%{version}-root
BuildRequires: openssl-devel gcc-c++
BuildRequires: libcurl-devel openldap-devel
BuildRequires: java-1.7.0-openjdk-devel
BuildRequires: postgresql-devel

Patch0	     : nxagent.init.patch
Patch1	     : netxms_mac.patch
Patch2       : netxmsd.init.patch
Patch3       : netxms2_jvm.patch
Patch4       : netxms_drdb.patch
Patch5       : netxms_dcitem.patch

%description
Monitoring system for Unix/Linux systems

%package     web
Summary      : NetXMS web console
Group        : System/Libraries
Provides     : %{name}-web
Requires     : tomcat6
%description web
Web interface as WAR file

%package shell
Summary      : NetXMS interactive shell
Group        : System/Libraries
Requires     : java-1.7.0-openjdk
%description shell
Python-based interactive shell and sripting engine for NetXMS

%package     common
Summary      : NetXMS common libraries
Group        : System/Libraries
Provides     : %{name}-common
%description common
Common library for NetXMS

%package     client
Summary      : NetXMS client installation.
Group        : Applications/Monitoring
Requires     : openssl
Requires     : %{name}-common = %{version}-%{release} 
Provides     : nxagentd
Provides     : %{name}-client
%description client
Package for NetXMS client installation.

%package     server
Summary      : NetXMS Monitoring system server.
Group        : Applications/Monitoring
Requires     : openssl
Requires     : %{name}-common = %{version}-%{release}
Requires     : postgresql
Requires     : postgresql-libs
Requires     : perl-CPAN
Requires     : perl-IO-Compress-Base
Requires     : perl-IO-Compress-Bzip2
Requires     : perl-IO-Compress-Zlib
Requires     : perl-IO-Socket-SSL
Requires     : perl-App-Options
Requires     : perl-libwww-perl
Provides     : netxmsd
Provides     : %{name}-server
%description server
NetXMS monitoring system server.

%prep
%setup -n %{name}-%{version}-%{vermodif}%{relise_vers}
%patch0 -p0 -b .fix_init_nxagent
%patch2 -p0 -b .fix_init_netxmsd
%patch4 -p0 -b .fix_drbd
%patch5 -p0 -b .fix_data_collection_error_resend

%build
sed -i 's/\#PREFIX\#/\/opt\/netxms/g' %{SOURCE4}  
sed -i 's/NXAGENTD_CONFIG="\/etc\/nxagentd.conf"/NXAGENTD_CONFIG="\/opt\/netxms\/etc\/nxagentd.conf"/g' contrib/startup/redhat/nxagentd.in
sed -i 's/NETXMSD_CONFIG="\/etc\/netxmsd.conf"/NETXMSD_CONFIG="\/opt\/netxms\/etc\/netxmsd.conf"/g' contrib/startup/redhat/netxmsd.in
JAVA_HOME=/usr/lib/jvm/java
JRE_HOME=/usr/lib/jvm/jre
PATH="$PATH:$JAVA_HOME/bin:$JRE_HOME/bin"

LDFLAGS="-L$JRE_HOME/lib/ -L$JRE_HOME/lib/amd64/server/  $LDFLAGS"
for i in -I$JAVA_HOME/include{,/linux}; do
      java_inc="$java_inc $i"
done
CPPFLAGS="$java_inc $CPPFLAGS"
export PATH LDFLAGS CPPFLAGS

./configure --prefix=%{prefix} \
  --with-client      \
  --with-server      \
  --with-agent       \
  --with-pgsql       \
  --with-openssl     \
  --with-snmp	     \
  --with-jdk 

make

%install
[ $RPM_BUILD_ROOT = / ] || rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
%{__mkdir_p} $RPM_BUILD_ROOT/etc/sysconfig
%{__mkdir_p} $RPM_BUILD_ROOT/etc/rc.d/init.d
%{__mkdir_p} $RPM_BUILD_ROOT/etc/profile.d
%{__mkdir_p} $RPM_BUILD_ROOT%{prefix}/etc
%{__mkdir_p} $RPM_BUILD_ROOT/etc/ld.so.conf.d
%{__mkdir_p} $RPM_BUILD_ROOT/var/lib/tomcat6/webapps
%{__cp} %{SOURCE4} $RPM_BUILD_ROOT/etc/profile.d/%{name}.sh
%{__cp} %{SOURCE1} $RPM_BUILD_ROOT/var/lib/tomcat6/webapps/nxmc.war
%{__cp} %{SOURCE3} $RPM_BUILD_ROOT%{prefix}/bin
%{__ln_s} %{prefix}/bin/nxshell-%{version}-%{vermodif}%{relise_vers}.jar $RPM_BUILD_ROOT%{prefix}/bin/nxshell.jar
%{__cp} $RPM_BUILD_DIR/%{name}-%{version}-%{vermodif}%{relise_vers}/contrib/startup/redhat/nxagentd $RPM_BUILD_ROOT/etc/rc.d/init.d/nxagentd
%{__cp} $RPM_BUILD_DIR/%{name}-%{version}-%{vermodif}%{relise_vers}/contrib/startup/redhat/netxmsd $RPM_BUILD_ROOT/etc/rc.d/init.d/netxmsd
%{__cp} $RPM_BUILD_DIR/%{name}-%{version}-%{vermodif}%{relise_vers}/contrib/netxmsd.conf-dist $RPM_BUILD_ROOT%{prefix}/etc/netxmsd.conf
%{__cp} $RPM_BUILD_DIR/%{name}-%{version}-%{vermodif}%{relise_vers}/contrib/nxagentd.conf-dist $RPM_BUILD_ROOT%{prefix}/etc/nxagentd.conf
touch $RPM_BUILD_ROOT/etc/sysconfig/nxagentd
touch $RPM_BUILD_ROOT/etc/sysconfig/netxmsd
echo "%{prefix}/lib" > $RPM_BUILD_ROOT/etc/ld.so.conf.d/netxms.conf

%post client
ldconfig
/sbin/chkconfig --add nxagentd

%post server
ldconfig
/sbin/chkconfig --add netxmsd

%post web
rm -rf /var/lib/tomcat6/webapps/nxmc
rm -rf /var/cache/tomcat6/work/Catalina/localhost/nxmc

%preun client
/sbin/service nxagentd stop

%postun client
ldconfig

%preun server
/sbin/service netxmsd stop

%postun server
ldconfig

%clean
[ $RPM_BUILD_ROOT = / ] || rm -rf $RPM_BUILD_ROOT

%files web
%{_var}/lib/tomcat6/webapps/nxmc.war

%files shell
%{prefix}/bin/nxshell*

%files common
%{prefix}/bin/nxencpasswd
%{prefix}/lib/libnetxms.*
%{prefix}/lib/libnxclient.*
%{prefix}/lib/libnxdb.*
%{prefix}/lib/libnxsnmp.*
%{prefix}/lib/libnxsqlite.*
%{prefix}/lib/libnxtre.*
%{prefix}/lib/libnxexpat.*
%{prefix}/lib/libnxjansson.*
/etc/profile.d/%{name}.sh

%files client
%defattr(-,root,root)
%attr(644,root,root) /etc/ld.so.conf.d/netxms.conf
%attr(755,root,root) %{_initrddir}/nxagentd

%config(noreplace) %{prefix}/etc/nxagentd.conf
%config(noreplace) /etc/sysconfig/nxagentd

%{prefix}/bin/nxagentd
%{prefix}/bin/nxappget
%{prefix}/bin/nxapush
%{prefix}/bin/nxpush
%{prefix}/bin/nxevent
%{prefix}/bin/nxalarm
%{prefix}/bin/nxsms

%{prefix}/lib/libappagent.*
%{prefix}/lib/libnxlp.*
%{prefix}/lib/netxms/*.nsm

%files server
%defattr(-,root,root)
%attr(644,root,root) /etc/ld.so.conf.d/netxms.conf
%config(noreplace) /etc/sysconfig/netxmsd
%{prefix}/bin/netxmsd
%{prefix}/bin/nxadm
%{prefix}/bin/nxap
%{prefix}/bin/nxdbmgr
%{prefix}/bin/nxget
%{prefix}/bin/nxmibc
%{prefix}/bin/nxscript
%{prefix}/bin/nxsnmp*
%{prefix}/bin/nxupload
%{prefix}/bin/nxaction
%{prefix}/bin/nxdevcfg
%{prefix}/bin/nxgenguid

%{prefix}/lib/netxms/jira.hdlink
%{prefix}/lib/libavaya-ers.*
%{prefix}/lib/libcisco.*
%{prefix}/lib/libnxcore.*
%{prefix}/lib/libnxmap.*
%{prefix}/lib/libnxsd.*
%{prefix}/lib/libnxsl.*
%{prefix}/lib/libnxsms_*.*
%{prefix}/lib/libnxsrv.*
%{prefix}/lib/libstrophe.*
%{prefix}/lib/libnsm_*.*
%{prefix}/lib/%{name}/ndd/*
%{prefix}/share/%{name}/*
# Postgresql Lib
%{prefix}/lib/libnxddr_pgsql.so
%{prefix}/lib/%{name}/dbdrv/pgsql.ddr

%attr(755,root,root) %{_initrddir}/netxmsd
%config(noreplace) %{prefix}/etc/netxmsd.conf
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README THANKS TODO doc/manuals/*.odt doc/manuals/*.doc

%changelog
* Thu May 14 2015 Ivan Polonevich <loverjoni at google.com> - 2.0-M4.0
- init spec
- Add patch to fix resend event on "data collection event"
