
%global pybasever 2.6
%global pyver 26
%global real_name mod_wsgi

%global __os_install_post %{__python26_os_install_post}
%global __python %{_bindir}/python%{pybasever}

Name:           python%{pyver}-mod_wsgi
Version:        3.4
Release:        2%{?dist}
Summary:        A WSGI interface for Python web applications in Apache

Group:          System Environment/Libraries
License:        ASL 2.0
URL:            http://modwsgi.org
Source0:        http://modwsgi.googlecode.com/files/%{real_name}-%{version}.tar.gz 
Source1:        python26-mod_wsgi.conf
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  httpd-devel
BuildRequires:  python%{pyver} python%{pyver}-devel

Obsoletes:      mod_wsgi-python26 < 3.2-2
Provides:       mod_wsgi-python26 = %{version}-%{release}


%description
The mod_wsgi adapter is an Apache module that provides a WSGI compliant
interface for hosting Python based web applications within Apache. The
adapter is written completely in C code against the Apache C runtime and
for hosting WSGI applications within Apache has a lower overhead than using
existing WSGI adapters for mod_python or CGI.

This package is built against python26.

%prep
%setup -q -n %{real_name}-%{version}


%build
%configure --enable-shared --with-python=%{__python}
make LDFLAGS="-L%{_libdir}" %{?_smp_mflags} 


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf

mv  %{buildroot}%{_libdir}/httpd/modules/mod_wsgi.so \
    %{buildroot}%{_libdir}/httpd/modules/%{name}.so 

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENCE README
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_libdir}/httpd/modules/%{name}.so


%changelog
* Wed Sep 19 2012 Ivan Polonevich <joni @ wargaming dot net> - 3.4-2
- Update to 3.4

* Fri Oct 10 2010 BJ Dierkes <wdierkes@rackspace.com> 3.3-1
- Porting to python26, renamed as python26-mod_wsgi
- Latest sources from upstream.  ChangeLog available at:
  http://code.google.com/p/modwsgi/wiki/ChangesInVersion0303
- Modified Apache config to only load python26-mod_wsgi if mod_python
  and mod_wsgi are not already loaded.

* Tue Mar  9 2010 Josh Kayse <josh.kayse@gtri.gatech.edu> 3.2-1
- update to 3.2
- explicitly enable shared libraries
- add a comment block to the configuration informing the administrator of 
  incompatibilities between mod_python and mod_wsgi
- update the configuration to disable mod_wsgi until the administrator enables

* Thu Jul 02 2009 James Bowes <jbowes@redhat.com> 2.5-1
- Update to 2.5

* Wed Oct 08 2008 James Bowes <jbowes@redhat.com> 2.1-2
- Remove requires on httpd-devel

* Wed Jul 02 2008 James Bowes <jbowes@redhat.com> 2.1-1
- Update to 2.1

* Mon Jun 16 2008 Ricky Zhou <ricky@fedoraproject.org> 1.3-4
- Build against the shared python lib.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3-3
- Autorebuild for GCC 4.3

* Sun Jan 06 2008 James Bowes <jbowes@redhat.com> 1.3-2
- Require httpd

* Sat Jan 05 2008 James Bowes <jbowes@redhat.com> 1.3-1
- Update to 1.3

* Sun Sep 30 2007 James Bowes <jbowes@redhat.com> 1.0-1
- Initial packaging for Fedora

