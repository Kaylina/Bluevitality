%global _default_patch_fuzz 2
Name:          rtorrent
# OpenSSL exception, see README
License:       GPLv2+ with exceptions
Group:         Applications/Internet
Version:       0.9.2
Release:       5%{?dist}
Summary:       BitTorrent client based on libtorrent 
URL:           http://rtorrent.rakshasa.no/
Source0:       http://libtorrent.rakshasa.no/downloads/%{name}-%{version}.tar.gz
Source1:       rtorrent.rc.example
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libstdc++-devel, pkgconfig, libsigc++20-devel, libtorrent-devel >= 0.13.2-2, libcurl-devel >= 7.27 , ncurses-devel
Requires:      libtorrent >= 0.13.2-4, curl >= 7.27

%description
A BitTorrent client using libtorrent, which on high-bandwidth connections is 
able to seed at 3 times the speed of the official client. Using
ncurses its ideal for use with screen or dtach. It supports 
saving of sessions and allows the user to add and remove torrents and scanning
of directories for torrent files to seed and/or download.

%prep
%setup -q

%build
# work around a bug thats triggered by gcc 4.1                                                           
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | %{__sed} s/-O2/-Os/`
export CFLAGS=$RPM_OPT_FLAGS
export CXXFLAGS=$RPM_OPT_FLAGS
install -m 644 %{SOURCE1} .
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT
		  
%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL README rtorrent.rc.example 
%{_bindir}/rtorrent
#%{_mandir}/man1/rtorrent*

%changelog
* Thu Aug 15 2013 Ivan Polonevich <joni @ wargaming dot net> - 0.9.2-4
- recompile with curl >=7.21

* Sat May 25 2013 Ivan Polonevich <joni @ wargaming dot net> - 0.9.2-3
- one more recompile libtorrent

* Fri May 24 2013 Ivan Polonevich <joni @ wargaming dot net> - 0.9.2-2
- Recompile libtorrent

* Tue May 21 2013 Ivan Polonevich <joni @ wargaming dot net> - 0.9.2-1
- New upstream

* Mon Apr 16 2012 Polonevich Ivan <joni at wargaming dot net> - 0.9.1-0
- New upstream version

* Tue Sep 18 2007 Marek Mahut <mmahut fedoraproject.org> - 0.7.8-1
- New upstream release

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.7.4-3
- Rebuild for selinux ppc32 issue.

* Thu Jun 28 2007 Chris Chabot <chabotc@xs4all.nl> - 0.7.4-2
- Fixed BR

* Thu Jun 28 2007 Chris Chabot <chabotc@xs4all.nl> - 0.7.4-1
- New upstream release

* Sun Nov 26 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.4-1
- New upstream version
- Compile with -Os to work around a gcc 4.1 incompatibility

* Mon Nov 06 2006 Jindrich Novy <jnovy@redhat.com> - 0.6.2-5
- rebuild against new curl

* Fri Sep 29 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.2-4
- re-tag

* Fri Sep 29 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.2-3
- re-tag

* Fri Sep 29 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.2-2
- New upstream version

* Mon Sep 11 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.0-2
- FC6 rebuild

* Sun Aug 13 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.0-1
- Upgrade to 0.6.0

* Sat Jun 17 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.5.3-1
- Upgrade to new upstream version 0.5.3
- And changed libtorrent dependency to >= 0.9.3

* Sat Jan 14 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.4.2-3
- Added ncurses-devel to buildrequirements

* Sat Jan 14 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.4.2-2
- Improved summary & description
- Removed explicit requires, leaving to rpm
- Changed mode of rtorrent.rc.example to 644

* Wed Jan 11 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.4.2-1
- Initial version
