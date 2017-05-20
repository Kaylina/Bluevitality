Name:           mysql-json-udfs
Version:        0.3.0
Release:        1%{?dist}
Summary: 	mysql plugin json-udfs

Group:          MySQL Database
License:        GPL 
#URL:            http://sourceforge.net/projects/snoopylogger/
Source0: 	http://downloads.mysql.com/snapshots/pb/%{name}-%{version}/%{name}-%{version}-labs-json-udfs-linux-glibc2.5-x86_64.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: 	mysql-server

%description
mysql plugin json-udfs

%prep
%setup -q -n %{name}-%{version}-labs-json-udfs-linux-glibc2.5-x86_64

#%post 
#Need only for Ubuntu and Deb
#ln -s /usr/lib/x86_64-linux-gnu/libpcreposix.so.3 /usr/lib/x86_64-linux-gnu/libpcreposix.so.0
#ln -s /lib/x86_64-linux-gnu/libpcre.so.3 /lib/x86_64-linux-gnu/libpcre.so.0
#%postun
#rm -f /usr/lib/x86_64-linux-gnu/libpcreposix.so.0
#rm -f /lib/x86_64-linux-gnu/libpcre.so.0

%install
rm -rf $RPM_BUILD_ROOT

# Dir fot deb
#mkdir -p %{buildroot}/usr/lib/mysql/plugin

mkdir -p %{buildroot}/usr/lib64/mysql/plugin/
cp -ar libmy_json_udf.so %{buildroot}/usr/lib64/mysql/plugin/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/usr/lib64/mysql/plugin/libmy_json_udf.so

%changelog
* Mon Feb 24 2014 Ivan Polonevich <joni @ wargaming dot net> - 0.3.0-1
- Initial rpm

