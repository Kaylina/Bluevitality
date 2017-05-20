Name:		sys_basher
Version:	1.1.23
Release:	2%{?dist}
Summary:	A multithreaded hardware exerciser

Group:		Applications/System
License:	BSD
URL:		http://www.polybus.com/sys_basher_web/	
Source0:	http://www.polybus.com/sys_basher/%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	tcsh
BuildRequires:	lm_sensors-devel
BuildRequires:	help2man

ExcludeArch: ppc

%description
sys_basher is a multithreaded system exerciser. It tests the CPU, RAM and Disks
under conditions of maximum stress by running CPU, Memory and Disk tests on all
Cores simultaneously. In addition to reliablity testing, sys_basher measures
low level functions including memory bandwidth, disk IO bandwidth and integer
and floating point operations using unrolled loops.

%prep
%setup -q


%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT BINDIR=%{_bindir} MANDIR=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README COPYRIGHT
%{_bindir}/sys_basher
%{_mandir}/man1/sys_basher.1.*


%changelog
* Thu Aug 20 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.22-2
- Added ExcludeArch: ppc
* Wed Aug 19 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.22-1
- Added finer grained control over the memory tests. Added support for >8G in Bit reverse address tests.
* Tue Aug 18 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.22-1
- Added voltage and fan speed reporting, added bit reverse addr test
* Thu Aug 13 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.21-1
- Improved random number test, added memory refresh test, increased MAX_CORES from 16 to 32, Changed BuildRoot
* Wed Aug 12 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.20-1
- Added a prototype for the open call in sys_disk
* Wed Aug 12 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.19-2
- Spec file clean up
* Wed Aug 12 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.19-1
- Cleaned up lint errors.
* Wed Aug 12 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.18-2
- Changed the build_sensors.csh script so that it's Ubuntu compatible.
* Tue Aug 11 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.18-1
- Changed -help output, added man file
* Tue Aug 11 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.17-6
- Changed sbinder to binder, added CFLAGS="$RPM_OPT_FLAGS" to make statement, removed -lform from Makefile
* Tue Aug 11 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.17-5
- Removed ncurses from the includes
* Mon Aug 10 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.17-4
- Changed Makefile to be Fedora friendly. Removed ncurses dependency
* Mon Aug 10 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.17-3
- Changed license from original BSD to New BSD
* Mon Aug 10 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.17-2
- Some fixes suggested by Fedora packagers
* Mon Aug 10 2009 Joshua Rosen <bjrosen@polybus.com>
- 1.1.17-1
- First package release

