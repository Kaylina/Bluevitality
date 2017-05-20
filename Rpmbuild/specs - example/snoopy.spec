Name:           snoopy
Version:        1.9.0
Release:        2%{?dist}
Summary:        A preload library to send shell commands to syslog

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://sourceforge.net/projects/snoopylogger/
Source0:        http://downloads.sourceforge.net/snoopylogger/snoopy-%{version}.tar.gz
Source1:        README.Fedora
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Snoopy is designed to aid a sysadmin by providing a log of commands 
executed. Snoopy is completely transparent to the user and applications.
It is linked into programs to provide a wrapper around calls to execve().
Logging is done via syslog.  

%prep
%setup -q
cp -p %{SOURCE1} .

%build
%configure --enable-root-only
make %{?_smp_mflags}

%post  
/sbin/ldconfig

%postun 
/sbin/ldconfig

%install
rm -rf %{buildroot}
# Make install does not respect DESTDIR.
# so do by hand.
mkdir -p %{buildroot}/%{_lib}
install -m 755 snoopy.so %{buildroot}/%{_lib}/snoopy.so

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/%{_lib}/snoopy.so
%doc COPYING README.md ChangeLog README.Fedora

%changelog
* Mon Feb 03 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.9.0-1
- Update upstream. Use --enable-root-only.

* Mon Jan 14 2011 Steve Traylen <steve.traylen@cern.ch> - 1.7.10-1
- New upstream 1.7.10

* Mon Jan 10 2011 Steve Traylen <steve.traylen@cern.ch> - 1.7.9-1
- New upstream 1.7.9

* Mon Nov 1 2010 Steve Traylen <steve.traylen@cern.ch> - 1.7.6-1
- New upstream 1.7.6

* Thu Aug 6 2010 Steve Traylen <steve.traylen@cern.ch> - 1.7.1-2
- Move lib from /usr/lib64 to /lib64 since a preload over glibc.

* Thu Aug 6 2010 Steve Traylen <steve.traylen@cern.ch> - 1.7.1-1
- New upstream 1.7.1-1

* Wed Aug 4 2010 Steve Traylen <steve.traylen@cern.ch> - 1.6.1-3
- Don't edit /etc/ld.so.preload, instead provide README.Fedora

* Tue Aug 3 2010 Steve Traylen <steve.traylen@cern.ch> - 1.6.1-2
- Call ldconfig in post and preun

* Tue Aug 3 2010 Steve Traylen <steve.traylen@cern.ch> - 1.6.1-1
- Initial packaging.

