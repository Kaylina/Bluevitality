%define debug_package %{nil}

Name: rabbitmq-server
Version: 3.3.4
Release: 1%{?dist}
License: MPLv1.1
Group: Development/Libraries
Source: http://www.rabbitmq.com/releases/rabbitmq-server/v%{version}/%{name}-%{version}.tar.gz
Source1: rabbitmq-server.init
Source2: rabbitmq-script-wrapper
Source3: rabbitmq-server.logrotate
Source4: rabbitmq-server.ocf
Source5: http://www.rabbitmq.com/releases/rabbitmq-erlang-client/v%{version}/amqp_client-%{version}.ez
Patch0: rabbit-server_make.patch
#Source6: mochiweb-%{version}.ez
#Source7: rabbitmq-management-%{version}.ez
#Source8: rabbitmq-management-agent-%{version}.ez
#Source9: rabbitmq-mochiweb-%{version}.ez
#Source10: webmachine-%{version}.ez
#Patch0: xmltovalidate.patch
URL: http://www.rabbitmq.com/
BuildArch: noarch
BuildRequires: python-simplejson, xmlto, libxslt, zip, nc
%if 0%{?el4}%{?el5}
BuildRequires: erlang >= R15B02-0
Requires: erlang >= R15B02-0
%else
BuildRequires: esl-erlang >= 17
Requires: esl-erlang >= 17
%endif
Requires: logrotate
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-%{_arch}-root
Summary: The RabbitMQ server
Requires(post): chkconfig initscripts
Requires(pre): chkconfig initscripts

%description
RabbitMQ is an implementation of AMQP, the emerging standard for high
performance enterprise messaging. The RabbitMQ server is a robust and
scalable implementation of an AMQP broker.

# We want to install into /usr/lib, even on 64-bit platforms
%define _rabbit_libdir %{_exec_prefix}/lib/rabbitmq
%define _rabbit_erllibdir %{_rabbit_libdir}/lib/rabbitmq_server-%{version}
%define _rabbit_wrapper %{_builddir}/`basename %{S:2}`
%define _rabbit_server_ocf %{_builddir}/`basename %{S:4}`
%define _plugins_state_dir %{_localstatedir}/lib/rabbitmq/plugins

%define _maindir %{buildroot}%{_rabbit_erllibdir}

%prep
%setup -q
#%patch0 -p0

%build
cp %{S:2} %{_rabbit_wrapper}
cp %{S:4} %{_rabbit_server_ocf}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install TARGET_DIR=%{_maindir} \
             SBIN_DIR=%{buildroot}%{_rabbit_libdir}/bin \
             MAN_DIR=%{buildroot}%{_mandir} \
             DOC_INSTALL_DIR=/tmp

mkdir -p %{buildroot}%{_localstatedir}/lib/rabbitmq/mnesia
mkdir -p %{buildroot}%{_localstatedir}/log/rabbitmq

#Copy all necessary lib files etc.
install -p -D -m 0755 %{S:1} %{buildroot}%{_initrddir}/rabbitmq-server
install -p -D -m 0755 %{_rabbit_wrapper} %{buildroot}%{_sbindir}/rabbitmqctl
install -p -D -m 0755 %{_rabbit_wrapper} %{buildroot}%{_sbindir}/rabbitmq-server
install -p -D -m 0755 %{_rabbit_wrapper} %{buildroot}%{_sbindir}/rabbitmq-multi
install -p -D -m 0755 %{_rabbit_wrapper} %{buildroot}%{_sbindir}/rabbitmq-plugins
install -p -D -m 0755 %{_rabbit_server_ocf} %{buildroot}%{_exec_prefix}/lib/ocf/resource.d/rabbitmq/rabbitmq-server

install -p -D -m 0644 %{S:3} %{buildroot}%{_sysconfdir}/logrotate.d/rabbitmq-server

mkdir -p %{buildroot}%{_sysconfdir}/rabbitmq

rm %{_maindir}/LICENSE %{_maindir}/LICENSE-MPL-RabbitMQ %{_maindir}/INSTALL

# Install plugins
#cp -v %{S:5} %{buildroot}%{_rabbit_erllibdir}/plugins
#cp -v %{S:6} %{buildroot}%{_rabbit_erllibdir}/plugins
#cp -v %{S:7} %{buildroot}%{_rabbit_erllibdir}/plugins
#cp -v %{S:8} %{buildroot}%{_rabbit_erllibdir}/plugins
#cp -v %{S:9} %{buildroot}%{_rabbit_erllibdir}/plugins
#cp -v %{S:10} %{buildroot}%{_rabbit_erllibdir}/plugins

#Build the list of files
#rm -f %{_builddir}/%{name}.files
#echo '%defattr(-,root,root, -)' >> %{_builddir}/%{name}.files 
#(cd %{buildroot}; \
#    find . -type f ! -regex '\.%{_sysconfdir}.*' \
#        ! -regex '\.\(%{_rabbit_erllibdir}\|%{_rabbit_libdir}\).*' \
#        | sed -e 's/^\.//' >> %{_builddir}/%{name}.files)

#Build the list of files
echo '%defattr(-,root,root, -)' >%{_builddir}/%{name}.files
find %{buildroot} -path %{buildroot}%{_sysconfdir} -prune -o '!' -type d -printf "/%%P\n" >>%{_builddir}/%{name}.files

%pre

if [ $1 -gt 1 ]; then
   #Upgrade - stop previous instance of rabbitmq-server init.d script
  /sbin/service rabbitmq-server stop
fi

# create rabbitmq group
if ! getent group rabbitmq >/dev/null; then
        groupadd -r rabbitmq
fi

# create rabbitmq user
if ! getent passwd rabbitmq >/dev/null; then
        useradd -r -g rabbitmq -d %{_localstatedir}/lib/rabbitmq rabbitmq \
            -c "RabbitMQ messaging server"
fi

%post
/sbin/chkconfig --add %{name}
if [ -f %{_sysconfdir}/rabbitmq/rabbitmq.conf ] && [ ! -f %{_sysconfdir}/rabbitmq/rabbitmq-env.conf ]; then
    mv %{_sysconfdir}/rabbitmq/rabbitmq.conf %{_sysconfdir}/rabbitmq/rabbitmq-env.conf
fi

%preun
if [ $1 = 0 ]; then
  #Complete uninstall
  /sbin/service rabbitmq-server stop
  /sbin/chkconfig --del rabbitmq-server
  # We do not remove /var/log and /var/lib directories
  # Leave rabbitmq user and group
fi

# Clean out plugin activation state, both on uninstall and upgrade
rm -rf %{_plugins_state_dir}
for ext in rel script boot ; do
    rm -f %{_rabbit_erllibdir}/ebin/rabbit.$ext
done

%files -f ../%{name}.files
%defattr(-,root,root,-)
%attr(0750, rabbitmq, rabbitmq) %dir %{_localstatedir}/lib/rabbitmq
%attr(0750, rabbitmq, rabbitmq) %dir %{_localstatedir}/log/rabbitmq
%dir %{_sysconfdir}/rabbitmq
%{_rabbit_erllibdir}
%{_rabbit_libdir}
%{_initrddir}/rabbitmq-server
%config(noreplace) %{_sysconfdir}/logrotate.d/rabbitmq-server
%doc LICENSE LICENSE-MPL-RabbitMQ
%doc docs/rabbitmq.config.example

%clean
rm -rf %{buildroot}

%changelog
* Tue Jan 21 2014 Ivan Polonevich <joni @ wargaming dot net> - 3.2.2-1
- Update upstream

* Fri Jul 20 2012 Polonevich Ivan <i_polonevih at wargaming dot net> - 2.8.4-1
- New Upstream Release

* Mon May 7 2012 Polonevich Ivan <i_polonevih at wargaming dot net> - 2.8.2-1
- New Upstream Release

* Thu Oct 27 2011 Polonevich Ivan <i_polonevih at wargaming dot net> - 2.6.1-1
- New Upstream Release

* Fri Feb 25 2011 Maksim Melnikau <m_melnikau@wargaming.net> 2.3.1
- New Upstream Release
- Management plugins included

* Sat Jan 15 2011 Hubert Plociniczak <hubert.plociniczak@gmail.com> 2.2.0-1
- New Upstream Release
- Fixes #646861

* Mon Nov 1 2010 Hubert Plociniczak <hubert.plociniczak@gmail.com> 2.1.1-1
- New Upstream Release

* Tue Oct 5 2010 Hubert Plociniczak <hubert.plociniczak@gmail.com> 2.1.0-1
- New Upstream Release

* Mon Aug 23 2010 Mike Bridgen <mikeb@rabbitmq.com> 2.0.0-1
- New Upstream Release
- Skip validation for xsltproc and xmlto since versions available have bugs

* Mon Jun 28 2010 Hubert Plociniczak <hubert@lshift.net> 1.8.0-1
- New Upstream Release
- Backported fix for bug 22871, fixes issues with erlang >= R14A

* Mon Feb 15 2010 Matthew Sackman <matthew@lshift.net> 1.7.2-1
- New Upstream Release

* Fri Jan 22 2010 Matthew Sackman <matthew@lshift.net> 1.7.1-1
- New Upstream Release

* Mon Oct 5 2009 David Wragg <dpw@lshift.net> 1.7.0-1
- New upstream release

* Wed Jun 17 2009 Matthias Radestock <matthias@lshift.net> 1.6.0-1
- New upstream release

* Tue May 26 2009 Hubert Plociniczak <hubert@lshift.net> 1.5.5-2
- Include dist macro in the release number

* Tue May 19 2009 Matthias Radestock <matthias@lshift.net> 1.5.5-1
- Maintenance release for the 1.5.x series

* Mon Apr 6 2009 Matthias Radestock <matthias@lshift.net> 1.5.4-1
- Maintenance release for the 1.5.x series

* Tue Feb 24 2009 Tony Garnock-Jones <tonyg@lshift.net> 1.5.3-1
- Maintenance release for the 1.5.x series

* Mon Feb 23 2009 Tony Garnock-Jones <tonyg@lshift.net> 1.5.2-1
- Maintenance release for the 1.5.x series

* Mon Jan 19 2009 Ben Hood <0x6e6562@gmail.com> 1.5.1-1
- Maintenance release for the 1.5.x series

* Wed Dec 17 2008 Matthias Radestock <matthias@lshift.net> 1.5.0-1
- New upstream release

* Thu Jul 24 2008 Tony Garnock-Jones <tonyg@lshift.net> 1.4.0-1
- New upstream release

* Mon Mar 3 2008 Adrien Pierard <adrian@lshift.net> 1.3.0-1
- New upstream release

* Wed Sep 26 2007 Simon MacMullen <simon@lshift.net> 1.2.0-1
- New upstream release

* Wed Aug 29 2007 Simon MacMullen <simon@lshift.net> 1.1.1-1
- New upstream release

* Mon Jul 30 2007 Simon MacMullen <simon@lshift.net> 1.1.0-1.alpha
- New upstream release

* Tue Jun 12 2007 Hubert Plociniczak <hubert@lshift.net> 1.0.0-1.20070607
- Building from source tarball, added starting script, stopping

* Mon May 21 2007 Hubert Plociniczak <hubert@lshift.net> 1.0.0-1.alpha
- Initial build of server library of RabbitMQ package
