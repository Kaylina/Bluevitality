%define realname iperf
%define realver  2.0.5
%define srcext   gz

# Common info
Name:          %{realname}
Version:       %{realver}
Release:       5.4
License:       UI License
Group:         Productivity/Networking/Other
URL:           http://sourceforge.net/projects/iperf/
Summary:       A tool for measuring network bandwidth performance

# Build-time parameters
BuildRequires: gcc-c++
BuildRoot:     %{_tmppath}/%{name}-root
Source:        %{realname}-%{realver}%{?extraver:%{extraver}}.tar.%{srcext}

%description
Iperf was developed by NLANR/DAST as a modern alternative for measuring maximum
TCP and UDP bandwidth performance. Iperf allows the tuning of various parameters
and UDP characteristics. Iperf reports bandwidth, delay jitter, datagram loss.

# Preparation step (unpackung and patching if necessary)
%prep
%setup -q -n %{realname}-%{realver}%{?extraver:%{extraver}}

%build
%configure \
 LDFLAGS="-Wl,--as-needed -Wl,--strip-all"
%__make %{?_smp_mflags}

%install
%__make install DESTDIR=%{buildroot}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README doc/*.html doc/dast.gif
%{_bindir}/*
%doc %{_mandir}/man1/*

%changelog
