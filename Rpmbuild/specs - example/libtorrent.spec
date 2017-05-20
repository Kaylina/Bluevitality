%global _default_patch_fuzz 2

Name:          libtorrent
License:       GPL
Group:         System Environment/Libraries
Version:       0.13.2
Release:       4%{?dist}
Summary:       BitTorrent library with a focus on high performance & good code
URL:           http://libtorrent.rakshasa.no/
Source0:       http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
Patch1: libtorrent_interval1.pach
Patch2: libtorrent_interval2.pach
Patch3: tracker_dht.cc.diff
Patch4: tracker_udp.cc.diff
Patch5: tracker.cc.diff
Patch6: tracker.h.diff
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig, openssl-devel, libsigc++20-devel

%description
LibTorrent is a BitTorrent library written in C++ for *nix, with a focus 
on high performance and good code. The library differentiates itself 
from other implementations by transfering directly from file pages to 
the network stack. On high-bandwidth connections it is able to seed at 
3 times the speed of the official client.

%package devel
Summary: Libtorrent development environment
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Header and library definition files for developing applications                                               
with the libtorrent libraries.

%prep
%setup -q
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0


%build

# work around a bug thats triggered by gcc 4.1
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | %{__sed} s/-O2/-Os/`
export CFLAGS=$RPM_OPT_FLAGS
export CXXFLAGS=$RPM_OPT_FLAGS

%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL README NEWS
%{_libdir}/libtorrent.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libtorrent.pc
%{_includedir}/torrent
%{_libdir}/*.so

%changelog
* Thu Aug 15 2013 Ivan Polonevich <joni @ wargaming dot net> - 0.13.2-4
- recompile with curl >=7.21

* Sat May 25 2013 Ivan Polonevich <joni @ wargaming dot net> - 0.13.2-3
- Fix using patch

* Fri May 24 2013 Ivan Polonevich <joni @ wargaming dot net> - 0.13.2-2
- Use patch

* Tue May 21 2013 Ivan Polonevich <joni @ wargaming dot net> - 0.13.2-1
- New upstream

* Mon Apr 16 2012 Polonevich Ivan <joni at wargaming dot net> - 0.13.1-1
- New upstream version

* Tue Sep 18 2007 Marek Mahut <mmahut at fedoraproject dot org> - 0.11.8-1
- New upstream version

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.11.4-2
- Rebuild for selinux ppc32 issue.

* Thu Jun 28 2007 Chris Chabot <chabotc@xs4all.nl> - 0.11.4-1
- New upstream version

* Sun Nov 26 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.4-1
- New upstream version
- Compile with -Os to work around a gcc 4.1 incompatibility

* Mon Oct 02 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.2-3
- Bump EVR to fix broken upgrade path (BZ #208985)

* Fri Sep 29 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.2-1
- New upstream release

* Mon Sep 11 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.0-3
- FC6 rebuild, re-tag

* Mon Sep 11 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.0-2
- FC6 rebuild

* Sun Aug 13 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.0-1
- Upgrade to 0.10.0

* Sat Jun 17 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.9.3-1
- Upgrade to new upstream version 0.9.3

* Sat Jan 14 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.8.2-2
- Improved general summary & devel package description 
- Simplified devel package includedir files section
- Removed openssl as requires, its implied by .so dependency
- Correct devel package Group

* Wed Jan 11 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.8.2-1
- Initial version
