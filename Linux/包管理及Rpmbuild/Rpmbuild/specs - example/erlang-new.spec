%define ver 17.1
%define rel 1
#%define real_ver %{ver}-%{rel}
%define real_ver %{ver}

Name:           erlang
Version:        %{ver}
Release:        0%{?dist}
Summary:        General-purpose programming language and runtime environment

Group:          Development/Languages
License:        ERPL
URL:            http://www.erlang.org
Source:         http://www.erlang.org/download/otp_src_%{real_ver}.tar.gz
Source1:	http://www.erlang.org/download/otp_doc_html_%{real_ver}.tar.gz
Source2:	http://www.erlang.org/download/otp_doc_man_%{real_ver}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{real_ver}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  unixODBC-devel
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:  gd-devel
%if 0%{?el4}%{?el5}
BuildRequires:	java-1.4.2-gcj-compat-devel
%else
BuildRequires:	java-1.5.0-gcj-devel
#BuildRequires:  java-1.7.0-openjdk-devel
%endif
BuildRequires:  flex
BuildRequires:	m4

Requires:	tk

# Added virtual Provides for each erlang module
Provides: erlang-appmon = %{real_ver}-%{release}
Provides: erlang-asn1 = %{real_ver}-%{release}
Provides: erlang-common_test = %{real_ver}-%{release}
Provides: erlang-compiler = %{real_ver}-%{release}
Provides: erlang-cosEvent = %{real_ver}-%{release}
Provides: erlang-cosEventDomain = %{real_ver}-%{release}
Provides: erlang-cosFileTransfer = %{real_ver}-%{release}
Provides: erlang-cosNotification = %{real_ver}-%{release}
Provides: erlang-cosProperty = %{real_ver}-%{release}
Provides: erlang-cosTime = %{real_ver}-%{release}
Provides: erlang-cosTransactions = %{real_ver}-%{release}
Provides: erlang-crypto = %{real_ver}-%{release}
Provides: erlang-debugger = %{real_ver}-%{release}
Provides: erlang-dialyzer = %{real_ver}-%{release}
Provides: erlang-docbuilder = %{real_ver}-%{release}
Provides: erlang-edoc = %{real_ver}-%{release}
Provides: erlang-erts = %{real_ver}-%{release}
Provides: erlang-et = %{real_ver}-%{release}
Provides: erlang-eunit = %{real_ver}-%{release}
Provides: erlang-gs = %{real_ver}-%{release}
Provides: erlang-hipe = %{real_ver}-%{release}
Provides: erlang-ic = %{real_ver}-%{release}
Provides: erlang-inets = %{real_ver}-%{release}
Provides: erlang-inviso = %{real_ver}-%{release}
Provides: erlang-kernel = %{real_ver}-%{release}
Provides: erlang-megaco = %{real_ver}-%{release}
Provides: erlang-mnesia = %{real_ver}-%{release}
Provides: erlang-observer = %{real_ver}-%{release}
Provides: erlang-odbc = %{real_ver}-%{release}
Provides: erlang-orber = %{real_ver}-%{release}
Provides: erlang-os_mon = %{real_ver}-%{release}
Provides: erlang-otp_mibs = %{real_ver}-%{release}
Provides: erlang-parsetools = %{real_ver}-%{release}
Provides: erlang-percept = %{real_ver}-%{release}
Provides: erlang-pman = %{real_ver}-%{release}
Provides: erlang-public_key = %{real_ver}-%{release}
Provides: erlang-runtime_tools = %{real_ver}-%{release}
Provides: erlang-sasl = %{real_ver}-%{release}
Provides: erlang-snmp = %{real_ver}-%{release}
Provides: erlang-ssh = %{real_ver}-%{release}
Provides: erlang-ssl = %{real_ver}-%{release}
Provides: erlang-stdlib = %{real_ver}-%{release}
Provides: erlang-syntax_tools = %{real_ver}-%{release}
Provides: erlang-test_server = %{real_ver}-%{release}
Provides: erlang-toolbar = %{real_ver}-%{release}
Provides: erlang-tools = %{real_ver}-%{release}
Provides: erlang-tv = %{real_ver}-%{release}
Provides: erlang-typer = %{real_ver}-%{release}
Provides: erlang-webtool = %{real_ver}-%{release}
Provides: erlang-xmerl = %{real_ver}-%{release}

%description
Erlang is a general-purpose programming language and runtime
environment. Erlang has built-in support for concurrency, distribution
and fault tolerance. Erlang is used in several large telecommunication
systems from Ericsson.


%package doc
Summary:	Erlang documentation
Group:		Development/Languages

%description doc
Documentation for Erlang.


%prep
%setup -q -n otp_src_%{ver}


# enable dynamic linking for ssl
sed -i 's|SSL_DYNAMIC_ONLY=no|SSL_DYNAMIC_ONLY=yes|' erts/configure
# fix for newer glibc version
sed -i 's|__GLIBC_MINOR__ <= 7|__GLIBC_MINOR__ <= 8|' erts/emulator/hipe/hipe_x86_signal.c


%build
# WARN: --enable-dynamic-ssl-lib needed for preventing strange messages about missing dependencies on EPEL
# see https://bugzilla.redhat.com/458646 and https://bugzilla.redhat.com/499525
#%ifarch sparcv9 sparc64
#CFLAGS="$RPM_OPT_FLAGS -mcpu=ultrasparc -fno-strict-aliasing" %configure --enable-dynamic-ssl-lib --enable-kernel-poll --enable-smp-support --enable-hipe
#%else
# CentOS 6.5 disables EC GF2m curves.
#FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -DOPENSSL_NO_EC=1"
# Bourne Shell
export ERL_TOP=$PWD
export PATH=$ERL_TOP/bin:$PATH
# C Shell
#setenv ERL_TOP $PWD
#setenv PATH $ERL_TOP/bin:$PATH

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure \
	--enable-dynamic-ssl-lib \
	--enable-kernel-poll \
	--enable-smp-support \
	--enable-hipe
#%endif


chmod -R u+w .
make


%install
rm -rf $RPM_BUILD_ROOT
make INSTALL_PREFIX=$RPM_BUILD_ROOT install

# clean up
find $RPM_BUILD_ROOT%{_libdir}/erlang -perm 0775 | xargs chmod 755
find $RPM_BUILD_ROOT%{_libdir}/erlang -name Makefile | xargs chmod 644
find $RPM_BUILD_ROOT%{_libdir}/erlang -name \*.o | xargs chmod 644
find $RPM_BUILD_ROOT%{_libdir}/erlang -name \*.bat | xargs rm -f
find $RPM_BUILD_ROOT%{_libdir}/erlang -name index.txt.old | xargs rm -f

# doc
mkdir -p erlang_doc
tar -C erlang_doc -zxf %{SOURCE1}
tar -C $RPM_BUILD_ROOT/%{_libdir}/erlang -zxf %{SOURCE2}

# make links to binaries
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cd $RPM_BUILD_ROOT/%{_bindir}
for file in erl erlc escript dialyzer
do
  ln -sf ../%{_lib}/erlang/bin/$file .
done

# remove buildroot from installed files
cd $RPM_BUILD_ROOT/%{_libdir}/erlang
sed -i "s|$RPM_BUILD_ROOT||" erts*/bin/{erl,start} releases/RELEASES bin/{erl,start}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc AUTHORS EPLICENCE
%{_bindir}/*
%{_libdir}/erlang


%files doc
%defattr(-,root,root)
%doc erlang_doc/*


%post
%{_libdir}/erlang/Install -minimal %{_libdir}/erlang >/dev/null 2>/dev/null


%changelog
* Fri Feb 25 2011 Maksim Melnikau <m_melnikau@wargaming.net> - R14B01

* Mon Jun  7 2010 Peter Lemenkov <lemenkov@gmail.com> - R12B-5.10
- Added missing virtual provides erlang-erts

* Tue May 25 2010 Peter Lemenkov <lemenkov@gmail.com> - R12B-5.9
- Use java-1.4.2 only for EL-[45]
- Added virtual provides for each erlang module
- Small typo fix

* Mon Apr 19 2010 Peter Lemenkov <lemenkov@gmail.com> - R12B-5.8
- Patches rebased
- Added patches 6,7 from trunk
- Use %%configure

* Tue Apr 21 2009 Debarshi Ray <rishi@fedoraproject.org> R12B-5.7
- Updated rpath patch.
- Fixed configure to respect $RPM_OPT_FLAGS.

* Sun Mar  1 2009 Gerard Milmeister <gemi@bluewin.ch> - R12B-5.6
- new release R12B-5
- link escript and dialyzer to %{_bindir}

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - R12B-5.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Dennis Gilmore <dennis@ausil.us> - R12B-4.5
- fix sparc arches to compile

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - R12B-4.4
- rebuild with new openssl

* Sat Oct 25 2008 Gerard Milmeister <gemi@bluewin.ch> - R12B-4.1
- new release R12B-4

* Fri Sep  5 2008 Gerard Milmeister <gemi@bluewin.ch> - R12B-3.3
- fixed sslrpath patch

* Thu Jul 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> - R12B-3.2
- fix license tag

* Sun Jul  6 2008 Gerard Milmeister <gemi@bluewin.ch> - R12B-3.1
- new release R12B-3

* Thu Mar 27 2008 Gerard Milmeister <gemi@bluewin.ch> - R12B-1.1
- new release R12B-1

* Sat Feb 23 2008 Gerard Milmeister <gemi@bluewin.ch> - R12B-0.3
- disable strict aliasing optimization

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - R12B-0.2
- Autorebuild for GCC 4.3

* Sat Dec  8 2007 Gerard Milmeister <gemi@bluewin.ch> - R12B-0.1
- new release R12B-0

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - R11B-6
 - Rebuild for deps

* Sun Aug 19 2007 Gerard Milmeister <gemi@bluewin.ch> - R11B-5.3
- fix some permissions

* Sat Aug 18 2007 Gerard Milmeister <gemi@bluewin.ch> - R11B-5.2
- enable dynamic linking for ssl

* Sat Aug 18 2007 Gerard Milmeister <gemi@bluewin.ch> - R11B-5.1
- new release R11B-5

* Sat Mar 24 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - R11B-2.4
- Require java-1.5.0-gcj-devel for build.

* Sun Dec 31 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-2.3
- remove buildroot from installed files

* Sat Dec 30 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-2.2
- added patch for compiling with glibc 2.5

* Sat Dec 30 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-2.1
- new version R11B-2

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-0.3
- Rebuild for FE6

* Wed Jul  5 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-0.2
- add BR m4

* Thu May 18 2006 Gerard Milmeister <gemi@bluewin.ch> - R11B-0.1
- new version R11B-0

* Wed May  3 2006 Gerard Milmeister <gemi@bluewin.ch> - R10B-10.3
- added patch for run_erl by Knut-Håvard Aksnes

* Mon Mar 13 2006 Gerard Milmeister <gemi@bluewin.ch> - R10B-10.1
- new version R10B-10

* Thu Dec 29 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-9.1
- New Version R10B-9

* Sat Oct 29 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-8.2
- updated rpath patch

* Sat Oct 29 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-8.1
- New Version R10B-8

* Sat Oct  1 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-6.4
- Added tk-devel and tcl-devel to buildreq
- Added tk to req

* Tue Sep  6 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-6.3
- Remove perl BuildRequires

* Tue Aug 30 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-6.2
- change /usr/lib to %%{_libdir}
- redirect output in %%post to /dev/null
- add unixODBC-devel to BuildRequires
- split doc off to erlang-doc package

* Sat Jun 25 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-6.1
- New Version R10B-6

* Sun Feb 13 2005 Gerard Milmeister <gemi@bluewin.ch> - R10B-3.1
- New Version R10B-3

* Mon Dec 27 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:R10B-2-0.fdr.1
- New Version R10B-2

* Wed Oct  6 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:R10B-0.fdr.1
- New Version R10B

* Thu Oct 16 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:R9B-1.fdr.1
- First Fedora release
