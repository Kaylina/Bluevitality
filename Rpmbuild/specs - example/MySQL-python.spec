Summary: An interface to MySQL
Name: mysql55-python
Version: 1.2.3
Release: 2%{?dist}
License: GPL
Group: Development/Libraries
URL: http://sourceforge.net/projects/mysql-python/
Source0: http://prdownloads.sourceforge.net/mysql-python/MySQL-python-%{version}.tar.gz
# 1.2.2 has adopted python-setuptools in preference to distutils, but since
# we don't (yet?) ship that in Fedora or RHEL, we keep using the setup.py
# script from 1.2.1_p2 for now.
Source1: setup.py
Patch1: sitecfg.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: python mx mysql55
Requires: python
BuildRequires: python-devel
BuildRequires: mysql55-devel
BuildRequires: python Distutils gcc zlib-devel
Conflicts: mysql51-python
Conflicts: MySQL-python

%description
Python interface to MySQL

MySQLdb is an interface to the popular MySQL database server for Python.
The design goals are:

-     Compliance with Python database API version 2.0 
-     Thread-safety 
-     Thread-friendliness (threads will not block each other) 
-     Compatibility with MySQL 3.23 and up

This module should be mostly compatible with an older interface
written by Joe Skinner and others. However, the older version is
a) not thread-friendly, b) written for MySQL 3.21, c) apparently
not actively maintained. No code from that version is used in
MySQLdb. MySQLdb is distributed free of charge under a license
derived from the Python license.

%prep
%setup -q -n  MySQL-python-%{version}

cp -f %{SOURCE1} setup.py

%patch1 -p1

%build
rm -f doc/*~
export libdirname=%{_lib}
CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

export libdirname=%{_lib}
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc README doc/*
%dir %{_libdir}/python?.?/site-packages/MySQLdb
%{_libdir}/python?.?/site-packages/MySQLdb/*.pyo
%{_libdir}/python?.?/site-packages/MySQLdb/constants/*.pyo
%{_libdir}/python?.?/site-packages/*.pyo
%dir /usr/%{_lib}/python?.?/site-packages/MySQLdb/constants

%changelog
* Tue Nov 3 2011 Ivan Polonevich <joni@wargaming.net> 1.2.3-1
- Update core version and support mysql version 5.5.16

* Tue Jun  29 2011 Ivan Polonevich <joni@wargaming.net> 1.2.2-4
- Add rpm in Wargaming.Net repos

* Tue Jul  3 2007 Tom Lane <tgl@redhat.com> 1.2.2-3
- Ooops, previous fix for quoting bug was wrong, because it converted the
  version_info tuple to a string in Python's eyes
Resolves: #246366

* Tue Jun 12 2007 Tom Lane <tgl@redhat.com> 1.2.2-2
- Fix quoting bug in use of older setup.py: need to quote version_info now
Resolves: #243877

* Fri Apr 20 2007 Tom Lane <tgl@redhat.com> 1.2.2-1
- Update to 1.2.2, but not 1.2.2 setup.py (since we don't ship setuptools yet)

* Wed Dec  6 2006 Tom Lane <tgl@redhat.com> 1.2.1_p2-1.el4s1.1
- Update to 1.2.1_p2

* Thu Sep 28 2006 Tom Lane <tgl@redhat.com> 1.2.1-1.el4s1.2
- Rebuild to verify building in brew

* Fri Jul 21 2006 Tom Lane <tgl@redhat.com> 1.2.1-1.el4s1.1
- Update to 1.2.1

* Thu Jul 20 2006 Tom Lane <tgl@redhat.com> 1.2.0-3.el4s1.2
- Rebuild to ensure compatibility with repackaged mysql client library
- Remove hardwired python version number in favor of asking Python

* Thu Feb  9 2006 Tom Lane <tgl@redhat.com> 1.2.0-3.el4s1.1
- Adjust release string to meet convention established by stacks group.

* Wed Feb  8 2006 Tom Lane <tgl@redhat.com> 1.2.0-3.RHEL4S1.1
- rebuild in Stacks branch

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Tom Lane <tgl@redhat.com> 1.2.0-3
- Rebuild due to mysql 5.0 update and openssl library update.

* Wed Aug 03 2005 Karsten Hopp <karsten@redhat.de> 1.2.0-2
- package all python files. INSTALLED_FILES doesn't contain files created
  by the brp-python-bytecompile script

* Thu Apr 21 2005 Tom Lane <tgl@redhat.com> 1.2.0-1
- Update to 1.2.0, per bug #155341
- Link against mysql 4.x not 3.x, per bug #150828

* Sun Mar  6 2005 Tom Lane <tgl@redhat.com> 1.0.0-3
- Rebuild with gcc4.

* Thu Nov 11 2004 Tom Lane <tgl@redhat.com> 1.0.0-2
- bring us to python 2.4

* Thu Nov 11 2004 Tom Lane <tgl@redhat.com> 1.0.0-1
- update to 1.0.0; rebuild against mysqlclient10

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 20 2004 Tom Lane <tgl@redhat.com>
- reinstate (and update) patch for /usr/lib64 compatibility
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Nov 25 2003 Patrick Macdonald <patrickm@redhat.com> 0.9.2-1
- update to 0.9.2
- remove patches (no longer applicable)

* Sat Nov 15 2003 Tom "spot" Callaway <tcallawa@redhat.com> 0.9.1-10
- bring us to python 2.3

* Thu Jul 03 2003 Patrick Macdonald <patrickm@redhat.com> 0.9.1-9
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 0.9.1-8
- rebuilt

* Tue Mar 04 2003 Patrick Macdonald <patrickm@redhat.com> 0.9.1-7
- explicitly define the constants directory in case a more
  restrictive umask is encountered (#74019)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 0.9.1-5
- lib64'ize

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 13 2002 Trond Eivind Glomsrd <teg@redhat.com> 0.9.1-2
- Build for newer python

* Wed Mar 13 2002 Trond Eivind Glomsrd <teg@redhat.com> 0.9.1-1
- 0.9.1

* Tue Feb 26 2002 Trond Eivind Glomsrd <teg@redhat.com> 0.9.0-6
- Rebuild

* Thu Jan 31 2002 Elliot Lee <sopwith@redhat.com> 0.9.0-5
- Change python conflicts to requires
- Use pybasever/pynextver macros.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Sep 14 2001 Trond Eivind Glomsrd <teg@redhat.com> 0.9.0-3
- Build for Python 2.2

* Mon Jul 23 2001 Trond Eivind Glomsrd <teg@redhat.com>
- Add zlib-devel to buildrequires (#49788)

* Tue Jun 19 2001 Trond Eivind Glomsrd <teg@redhat.com>
- Initial build
