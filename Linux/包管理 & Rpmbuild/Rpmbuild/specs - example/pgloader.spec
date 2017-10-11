Summary:            extract, transform and load data into PostgreSQL
Name:               pgloader
Version:            3.0.99
Release:            22%{?dist}
License:            The PostgreSQL Licence
Group:              System Environment/Base
# Download url https://codeload.github.com/dimitri/pgloader/tar.gz/v3.0.99
#Source:             %{name}-%{version}.tar.gz
Source:             %{name}.tar.gz
URL:                https://github.com/dimitri/pgloader
BuildRequires: 	    curl, git, wget, sbcl, openssl, openssl-devel,
%description
pgloader imports data from different kind of sources and COPY it into
PostgreSQL.

The command language is described in the manual page and allows to describe
where to find the data source, its format, and to describe data processing
and transformation.
 
Supported source formats include CSV, fixed width flat files, dBase3 files
(DBF), and SQLite and MySQL databases. In most of those formats, pgloader is
able to auto-discover the schema and create the tables and the indexes in
PostgreSQL. In the MySQL case it's possible to edit CASTing rules from the
pgloader command directly.

%prep
%setup -q -n %{name}

%build

#wget http://downloads.sourceforge.net/project/sbcl/sbcl/1.1.14/sbcl-1.1.14-source.tar.bz2
#tar xfj sbcl-1.1.14-source.tar.bz2
#cd sbcl-1.1.14
#./make.sh --with-sb-thread --with-sb-core-compression 
#> /dev/null 2>&1
#./install.sh
#rpm -e sbcl

%define debug_package %{nil}
make CL=/tmp/ccl/lx86cl64 pgloader

%install
install -m 755 -d %{buildroot}/%{_bindir}
cp build/bin/pgloader %{buildroot}/%{_bindir}/pgloader

%files
%doc README.md pgloader.1.md
%{_bindir}/*

%changelog
* Wed Jul 30 2014 Ivan Polonevich <joni @ wargaming dot net> - 3.0.99-22
- Rebuild for WG

* Tue Apr 29 2014 Dimitri Fontaine <dimitri@2ndQuadrant.fr> 3.0.99
- Assorted fixes, release candidate 9
* Thu Dec 23 2013 Dimitri Fontaine <dimitri@2ndQuadrant.fr> 3.0.98
- Assorted fixes, release candidate 8
* Wed Dec 15 2013 Dimitri Fontaine <dimitri@2ndQuadrant.fr> 3.0.97
- Assorted fixes, release candidate 7
* Tue Dec 10 2013 Dimitri Fontaine <dimitri@2ndQuadrant.fr> 3.0.96
- Package as an RPM

%global __os_install_post %{nil}
