Summary: Perforce Software Configuration Management System
Name: perforce
Version: r14.1
Release: 1
Group: Development/Version Control
License: Commercial
Url: http://www.perforce.com/
Packager: Ivan Polonevich <joni @ wargaming . net>
%define p4ver  807760
%define p4dver 807760
#Source0: ftp://ftp.perforce.com/perforce/%{version}/bin.linux24x86_64/p4
#Source1: ftp://ftp.perforce.com/perforce/%{version}/bin.linux24x86_64/p4d
Source0: http://filehost.perforce.com/perforce/%{version}/bin.linux26x86_64/p4
Source1: http://filehost.perforce.com/perforce/%{version}/bin.linux26x86_64/p4d
Source2: http://www.perforce.com/perforce/doc.011/man/p4.1
Source3: http://www.perforce.com/perforce/doc.011/man/p4d.1
Source5: p4d.init
Source6: p4d.sysconfig
BuildRoot: /var/tmp/%{name}-root

%description
Perforce, the Fast Software Configuration Management System.

P4  version: %p4ver
P4D version: %p4dver

This package includes the "Linux 2.4.0 Intel x86_64 (Centos 5)"
version which supports database files larger than 2GB when running
with Linux kernels 2.4.0 or higher.


%prep


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/{bin,sbin,lib,man/man1}
install -p -m0755 %{SOURCE0} $RPM_BUILD_ROOT/usr/bin
install -p -m0755 %{SOURCE1} $RPM_BUILD_ROOT/usr/sbin
install -p -m0644 %{SOURCE2} $RPM_BUILD_ROOT/usr/man/man1
install -p -m0644 %{SOURCE3} $RPM_BUILD_ROOT/usr/man/man1

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -p -m0755 %{SOURCE5} $RPM_BUILD_ROOT/etc/rc.d/init.d/p4d

mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
install -p -m0644 %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/p4d

mkdir -p $RPM_BUILD_ROOT/var/lib/perforce


%pre
if [ $1 = 1 ]; then
    /usr/sbin/groupadd -g 120 -r -f p4admin
    /usr/sbin/useradd -c "Perforce Server" -r -n -s /bin/bash -u 120 \
	-g p4admin -d /var/lib/perforce perforce 2>/dev/null || :
fi

%post
#if [ $1 = 1 ]; then
#    /sbin/chkconfig --add p4d
#fi

%preun
if [ $1 = 0 ]; then
    /sbin/chkconfig --del p4d
fi

%postun
if [ $1 = 0 ]; then
    /usr/sbin/userdel perforce 2>/dev/null || :
    /usr/sbin/groupdel p4admin 2>/dev/null || :
fi


%files
%defattr(-,root,root)
%config /etc/rc.d/init.d/p4d
%config /etc/sysconfig/p4d
/usr/bin/*
/usr/sbin/*
/usr/man/man1/*
%attr(0750,perforce,p4admin) /var/lib/perforce


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Feb 8 2012 Ivan Polonevich <joni at wargaming dot net> - r11.1
- update core
