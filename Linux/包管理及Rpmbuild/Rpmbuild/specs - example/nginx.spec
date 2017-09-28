%if 0%{?rhel} > 5
%global _default_patch_fuzz 2
%endif 

%define nginx_user      nginx
%define nginx_group     %{nginx_user}
%define nginx_home      %{_localstatedir}/lib/nginx
%define nginx_home_tmp  %{nginx_home}/tmp
%define nginx_logdir    %{_localstatedir}/log/nginx
%define nginx_confdir   %{_sysconfdir}/nginx
%define nginx_datadir   %{_datadir}/nginx
%define nginx_webroot   %{nginx_datadir}/html
%define real_name	    nginx
%define openssl_ver 	1.0.1j

Name:           nginx
Version:        1.6.2
Release:        1%{?dist}
Summary:        Robust, small and high performance http and reverse proxy server
Group:          System Environment/Daemons

License:        BSD
URL:            http://nginx.net/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      pam-devel,pcre-devel,zlib-devel,perl(ExtUtils::Embed)
BuildRequires:      GeoIP-devel, zlib
BuildRequires:      luajit-devel, expat-devel

Requires: 	    luajit
Requires:           pcre,zlib,openssl
Requires:           GeoIP
Requires:           perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires(pre):      shadow-utils
Requires(post):     chkconfig
Requires(preun):    chkconfig
Requires:           initscripts >= 8.36
Requires(postun):   initscripts

Source0:        http://nginx.org/download/nginx-%{version}.tar.gz
Source1:        %{real_name}.init
Source2:        %{real_name}.logrotate
Source3:        virtual.conf
Source4:        ssl.conf
Source5:        nginx-upstream-fair.tar.gz
Source6:        upstream-fair.conf
Source7:        %{real_name}.sysconfig
Source8: 	%{real_name}.conf.src

Source20:	Mod_ustats-r32.tar.gz
Source21:       GeoIPCountryCSV.zip
Source22: 	nginx_accept_language_module.tar.gz
# Download from 	https://github.com/simpl/ngx_devel_kit/archive/v0.2.19.tar.gz
Source23: 	ngx_devel_kit-0.2.19.tar.gz
# Download from   	https://github.com/openresty/lua-nginx-module/archive/v0.9.11.tar.gz
Source24: 	lua-nginx-module-0.9.11.tar.gz
Source25: 	nginx-dav-ext-module.tar.gz
# Download from 	https://github.com/FRiCKLE/ngx_cache_purge/archive/2.1.zip
#Source26: 	ngx_cache_purge-2.1.zip
# Download from         https://github.com/nbs-system/naxsi/archive/0.53-2.tar.gz
Source26: 	naxsi-0.53-2.tar.gz
Source27: 	http://people.freebsd.org/~osa/ngx_http_redis-0.3.7.tar.gz

# Download from 	https://github.com/openresty/echo-nginx-module/archive/master.zip
Source28: 	echo-nginx-module-0.56.tar.gz
Source100:      index.html
Source101:      poweredby.png
Source102:      nginx-logo.png
Source103:      50x.html
Source104:      404.html
Source105:	error_page.include
Source106:	default.conf
Source107:      https://www.openssl.org/source/openssl-%{openssl_ver}.tar.gz
Source108:	server_param.conf


Patch0:         nginx-auto-cc-gcc.patch
Patch1:         nginx_config.patch
Patch2:		nginx_ustats.patch
Patch3:		ngx_http_ustats_module.c.diff
Patch4:		nginx_mime.patch

%description
Nginx [engine x] is an HTTP(S) server, HTTP(S) reverse proxy and IMAP/POP3
proxy server written bOCy Igor Sysoev.

Following third party modules added:
* openssl %{openssl_ver}
* nginx ustats 
* lua-nginx-module with luajit 2.0.3
* nginx devel kit
* nginx accept language module
* nginx dav ext module
* nginx naxsi module
* nginx redis module
* nginx echo module

%prep
%setup -q -n %{real_name}-%{version}
%patch0 -p0
#%patch1 -p0
%patch2 -p0
%setup -T -D -a 20 -n %{real_name}-%{version}
%setup -T -D -a 21 -n %{real_name}-%{version}
%setup -T -D -a 22 -n %{real_name}-%{version}
%setup -T -D -a 23 -n %{real_name}-%{version}
%setup -T -D -a 24 -n %{real_name}-%{version}
%setup -T -D -a 25 -n %{real_name}-%{version}
%setup -T -D -a 26 -n %{real_name}-%{version}
%setup -T -D -a 27 -n %{real_name}-%{version}
%setup -T -D -a 28 -n %{real_name}-%{version}
%setup -T -D -a 107 -n %{real_name}-%{version}
%patch3 -p0
%patch4 -p0

%build

# Convert GeoIP
perl contrib/geo2nginx.pl < GeoIPCountryWhois.csv > geo.data

# nginx does not utilize a standard configure script.  It has its own
# and the standard configure options cause the nginx configure script
# to error out.  This is is also the  for the DESTDIR environment
# variable.  The configure script(s) have been patched (Patch1 and
# Patch2) in order to support installing into a build environment.
export LUAJIT_LIB=/usr/lib64/
export LUAJIT_INC=/usr/include/luajit-2.0/

export DESTDIR=%{buildroot}
./configure \
    --user=%{nginx_user} \
    --group=%{nginx_group} \
    --prefix=%{nginx_datadir} \
    --sbin-path=%{_sbindir}/%{real_name} \
    --conf-path=%{nginx_confdir}/%{real_name}.conf \
    --error-log-path=%{nginx_logdir}/error.log \
    --http-log-path=%{nginx_logdir}/access.log \
    --http-client-body-temp-path=%{nginx_home_tmp}/client_body \
    --http-proxy-temp-path=%{nginx_home_tmp}/proxy \
    --http-fastcgi-temp-path=%{nginx_home_tmp}/fastcgi \
    --pid-path=%{_localstatedir}/run/%{real_name}.pid \
    --lock-path=%{_localstatedir}/lock/subsys/%{real_name} \
    --with-openssl="%{_builddir}/nginx-%{version}/openssl-%{openssl_ver}" \
    --with-openssl-opt="enable-tlsext" \
    --with-http_secure_link_module \
    --with-http_random_index_module \
    --with-http_ssl_module \
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_gzip_static_module \
    --with-http_stub_status_module \
    --with-http_geoip_module \
    --with-http_spdy_module \
    --with-debug \
    --with-file-aio \
    --with-cc-opt="%{optflags} $(pcre-config --cflags)" \
    --add-module=%{_builddir}/nginx-%{version}/mod_ustats \
    --add-module=%{_builddir}/nginx-%{version}/ngx_devel_kit-0.2.19 \
    --add-module=%{_builddir}/nginx-%{version}/nginx_accept_language_module \
    --add-module=%{_builddir}/nginx-%{version}/lua-nginx-module-0.9.11 \
    --add-module=%{_builddir}/nginx-%{version}/nginx-dav-ext-module \
    --add-module=%{_builddir}/nginx-%{version}/naxsi-0.53-2/naxsi_src \
    --add-module=%{_builddir}/nginx-%{version}/ngx_http_redis-0.3.7 \
    --add-module=%{_builddir}/nginx-%{version}/echo-nginx-module-0.56 \

make


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALLDIRS=vendor
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} \;
find %{buildroot} -type f -empty -exec rm -f {} \;
find %{buildroot} -type f -exec chmod 0644 {} \;
find %{buildroot} -type f -name '*.so' -exec chmod 0755 {} \;
chmod 0755 %{buildroot}%{_sbindir}/nginx
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{real_name}
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{real_name}
%{__install} -p -D -m 0644 %{SOURCE7} %{buildroot}%{_sysconfdir}/sysconfig/%{real_name}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_confdir}/conf.d
%{__install} -p -d -m 0755 %{buildroot}%{nginx_confdir}/sites-enabled
%{__install} -p -d -m 0755 %{buildroot}%{nginx_confdir}/sites-available
%{__install} -p -D -m 0644 geo.data %{buildroot}%{nginx_confdir}/conf.d/geo.data
%{__install} -p -m 0644 %{SOURCE106} %{buildroot}%{nginx_confdir}/sites-available
%{__install} -p -m 0644 %{SOURCE3} %{SOURCE4} %{SOURCE6} %{SOURCE105} %{SOURCE108} %{buildroot}%{nginx_confdir}/conf.d
%{__install} -p -d -m 0755 %{buildroot}%{nginx_home_tmp}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_logdir}
%{__install} -p -d -m 0755 %{buildroot}%{nginx_webroot}
%{__install} -p -m 0644 %{SOURCE100} %{SOURCE101} %{SOURCE102} %{SOURCE103} %{SOURCE104} %{buildroot}%{nginx_webroot}
%{__install} -p -m 0644 %{SOURCE8} %{buildroot}%{nginx_confdir}/nginx.conf 


# convert to UTF-8 all files that give warnings.
for textfile in CHANGES
do
    mv $textfile $textfile.old
    iconv --from-code ISO8859-1 --to-code UTF-8 --output $textfile $textfile.old
    rm -f $textfile.old
done

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/useradd -c "Nginx user" -s /bin/false -r -d %{nginx_home} %{nginx_user} 2>/dev/null || :

%post
/sbin/chkconfig --add %{real_name}
/sbin/chkconfig %{real_name} on
%{__ln_s} -f %{nginx_confdir}/sites-available/default.conf %{nginx_confdir}/sites-enabled/default.conf


%preun
if [ $1 = 0 ]; then
    /sbin/service %{real_name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{real_name}
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service %{real_name} condrestart > /dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc LICENSE CHANGES README

%{nginx_datadir}/
%{_sbindir}/%{real_name}
%{_initrddir}/%{real_name}
%dir %{nginx_confdir}
%dir %{nginx_confdir}/conf.d
%dir %{nginx_confdir}/sites-enabled
%dir %{nginx_confdir}/sites-available
%config(noreplace) %{nginx_confdir}/conf.d/*
%config(noreplace) %{nginx_confdir}/sites-available/*
%config(noreplace) %{nginx_confdir}/sites-enabled/
%config(noreplace) %{nginx_confdir}/win-utf
%config(noreplace) %{nginx_confdir}/%{real_name}.conf.default
%config(noreplace) %{nginx_confdir}/mime.types.default
%config(noreplace) %{nginx_confdir}/fastcgi_params
%config(noreplace) %{nginx_confdir}/fastcgi_params.default
%config(noreplace) %{nginx_confdir}/fastcgi.conf
%config(noreplace) %{nginx_confdir}/fastcgi.conf.default
%config(noreplace) %{nginx_confdir}/uwsgi_params
%config(noreplace) %{nginx_confdir}/uwsgi_params.default
%config(noreplace) %{nginx_confdir}/scgi_params
%config(noreplace) %{nginx_confdir}/scgi_params.default
%config(noreplace) %{nginx_confdir}/koi-win
%config(noreplace) %{nginx_confdir}/koi-utf
%config(noreplace) %{nginx_confdir}/%{real_name}.conf
%config(noreplace) %{nginx_confdir}/mime.types
%config(noreplace) %{_sysconfdir}/logrotate.d/%{real_name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{real_name}
%attr(-,%{nginx_user},%{nginx_group}) %dir %{nginx_home}
%attr(-,%{nginx_user},%{nginx_group}) %dir %{nginx_home_tmp}
%attr(-,%{nginx_user},%{nginx_group}) %dir %{nginx_logdir}


%changelog
* Mon Oct 20 2014 Anton Samets <a_samets@wargaming.net> - 1.6.2-1
- New upstram release
- Updated openssl to 1.0.1j due a lot of CVE

* Fri Oct 03 2014 Alexandr Tselobyonock <a_tselobyonock @ wargaming dot net> - 1.6.1-3
- Updated echo module to 0.56

* Wed Aug 27 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.6.1-2
- Use LuaJit for lua-nginx-module
- Updated lua-nginx-module to 0.9.11

* Mon Aug 11 2014 Anton Samets <a_samets@wargaming.net> - 1.6.1-1
- New upstream release
- Added module echo-nginx-module
- Updated openssl to 1.0.1i due a lot of CVE

* Mon Jul 07 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.6.0-4
- Add redis module
- Remove ngx_cache_purge module

* Fri Jun 27 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.6.0-3
- Add naxsi module

* Mon Jun 23 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.6.0-2
- Add ngx_cache_purge module

* Tue Jun 10 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.6.0-1
- Update upstream

* Mon Jun 09 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.4.7-3
- Update openssl to 1.0.1h for fix CVE-2014-0224

* Tue Apr 08 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.4.7-1
- Update to 1.4.7
- Update OpenSSL to 1.0.1g for fix CVE-2014-0160

* Tue Feb 04 2014 Ivan Polonevich <joni @ wargaming dot net> - 1.4.4-4
- Merge nginx-lua nginx-webdav nginx-lang to one nginx package

* Wed Dec 04 2013 Ivan Polonevich <joni @ wargaming dot net> - 1.4.4-3
- Disable ipv6

* Wed Dec 04 2013 Ivan Polonevich <joni @ wargaming dot net> - 1.4.4-2
- Disable ipv6

* Wed Nov 20 2013 Ivan Polonevich <joni @ wargaming dot net> - 1.4.4-1
- new upstream release 1.4.4

* Fri Aug 30 2013 Ivan Polonevich <joni @ wargaming dot net> - 1.4.2-1
- Add xrds mimetype, add configtest in reload section init script

* Wed Aug 1 2013 Anton Samets <a_samets @ wargaming dot net> - 1.4.2-0
- new upstream release 1.4.2

* Thu May 7 2013 Ivan Polonevich <joni @ wargaming dot net> - 1.4.1-0
- Безопасность: при обработке специально созданного запроса мог
  перезаписываться стек рабочего процесса, что могло приводить к
  выполнению произвольного кода (CVE-2013-2028); ошибка появилась в 1.3.9.

* Fri Apr 26 2013 Ivan Polonevich <joni @ wargaming dot net> - 1.4.0-2
- Add spdy_module

* Thu Apr 25 2013 Ivan Polonevich <joni @ wargaming dot net> - 1.4.0-1
- Update upstream 

* Mon Apr 15 2013 Ivan Polonevich <joni @ wargaming dot net> - 1.3.15-1
- Update to 1.3.15, update openssl to 1.0.1e

* Wed Feb 20 2013 Ivan Polonevich <joni @ wargaming dot net> - 1.2.7-2
- Update to 1.2.7

* Mon Jan 21 2013 Ivan Polonevich <joni @ wargaming dot net> - 1.2.6-1
- Update to 1.2.6

* Mon Sep 10 2012 Ivan Polonevich <joni @ wargaming dot net> - 1.2.4-0
- Update to 1.2.4

* Mon Sep 10 2012 Ivan Polonevich <joni @ wargaming dot net> - 1.2.3-2
- Add GeoIP module

* Mon Sep 03 2012 mockbuild - 1.2.3-1
- Update to 1.2.3 

* Mon Jul 16 2012 Polonevich Ivan <joni at wargaming dot net> - 1.2.2-0
- Update to 1.2.2

* Fri May 18 2012 Polonevich Ivan <joni at wargaming dot net> - 1.1.20-6
- Add ustats module and patch for it

* Fri May 11 2012 Polonevich Ivan <joni at wargaming dot net> - 1.1.20-4
- Delete ustats module http://code.google.com/p/ustats/issues/detail?id=5

* Thu Apr 26 2012 Polonevich Ivan <joni at wargaming dot net> - 1.1.20-0
- Update to 1.1.20

* Thu Mar 20 2012 Polonevich Ivan <joni at wargaming dot net> - 1.1.18-0
- Update to 1.1.18
- Remove server version header

* Thu Mar 20 2012 Polonevich Ivan <joni at wargaming dot net> - 1.1.17-0
- Update to 1.1.17

* Wed Feb 29 2012 Polonevich Ivan <joni at wargaming dot net> - 1.1.16-1
- Update to 1.1.16

* Wed Feb 29 2012 Polonevich Ivan <joni at wargaming dot net> - 1.1.15-4
- Correct fastcgi_busy_buffers_size fastcgi_buffers directive

* Fri Feb 17 2012 Polonevich Ivan <joni at wargaming dot net> - 1.1.15-2
- Enable TLS SNI support on centos 5 with openssl-0.9.8t 
- correct limit_conn directive
- disable mail

* Thu Feb 16 2012 Polonevich Ivan <joni at wargaming dot net> - 1.1.15-1
- update to 1.1.15

* Mon Nov 14 2011 Polonevich Ivan <joni at wargaming dot net> - 1.1.7-1
- update to 1.1.7

* Wed Oct 19 2011 Polonevich Ivan <joni at wargaming dot net> - 1.1.6-1
- update to 1.1.6
- add in defaul.conf php-status location

* Wed Oct 12 2011 Polonevich Ivan <joni at wargaming dot net> - 1.1.5-1
- update to 1.1.5

* Sun Oct 04 2011 Polonevich Ivan <joni at wargaming dot net> - 1.1.4-1
- update to 1.1.4
- update config file 

* Mon Aug 22 2011 Polonevich Ivan <joni at wargaming dot net> - 1.1.1-1
- update to 1.1.1
- add custom error page and conf file 

* Thu May 10 2011 Polonevich Ivan  <joni at wargaming dot net> - 1.0.2-1
- update to 1.0.2
- add module ustats 

* Fri Apr 15 2011 Polonevich Ivan <joni at wargaming dot net> - 1.0.0-4
-  del modules upload, zip, h264

* Fri Apr 15 2011 Denis Frolov <d.frolov81 at mail dot ru> - 1.0.0-3
- add module mod_strip
- update http://www.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip

* Wed Apr 13 2011 Denis Frolov <d.frolov81 at mail dot ru> - 1.0.0-2
- add ipv6-fix patch

* Thu Apr 12 2011 Denis Frolov <d.frolov81 at mail dot ru> - 1.0.0-1
- update to 1.0.0

* Wed Apr 06 2011 Denis Frolov <d.frolov81 at mail dot ru> - 0.9.7-1
- update to 0.9.7

* Mon Mar 21 2011 Denis Frolov <d.frolov81 at mail dot ru> - 0.9.6-1
- update to 0.9.6

* Mon Feb 21 2011 Denis Frolov <d.frolov81 at mail dot ru> - 0.9.5-1
- update to 0.9.5

* Sun Jan 23 2011 Denis Frolov <d.frolov81 at mail dot ru> - 0.9.4-1
- update to 0.9.4

* Thu Dec 14 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.9.3-1
- update to 0.9.3

* Thu Dec 07 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.9.2-1
- update to 0.9.2

* Thu Nov 30 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.9.1-1
- update to 0.9.1

* Thu Nov 02 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.53-5
- add --with-file-aio
- add 2 aio patch

* Mon Oct 25 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.53-4
- fix geo.conf

* Thu Oct 19 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.53-1
- update to 0.8.53-1
- add --with-http_geoip_module

* Wed Sep 28 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.52-1
- update to 0.8.52-1

* Wed Sep 28 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.51-1
- update to 0.8.51-1
- update nginx-upload-module to 2.2.0
- update mod_zip to 1.1.6

* Wed Sep 03 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.50-1
- update to 0.8.50-1

* Tue Aug 10 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.49-1
- update to 0.8.49-1
- add --with-ipv6

* Thu Aug 03 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.48-1
- update to 0.8.48-1

* Thu Jul 28 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.47-1
- update to 0.8.47-1

* Tue Jul 20 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.46-1
- update to 0.8.46-1

* Thu Jul 15 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.45-1
- update to 0.8.45-1

* Mon Jul 05 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.44-1
- update to 0.8.44-1

* Fri Jul 02 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.43-1
- update to 0.8.43-1

* Wed Jun 23 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.42-1
- update to 0.8.42-1

* Wed Jun 16 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.41-1
- update to 0.8.41-1

* Thu Jun 08 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.40-1
- update to 0.8.40-1

* Sun Jun 06 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.39-1
- update to 0.8.39-1

* Thu May 25 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.38-1
- update to 0.8.38-1
- add nginx_mod_h264_streaming-2.2.7.patch

* Wed May 19 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.37-1
- update to 0.8.37-1

* Fri Apr 23 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.35-1
- update to 0.8.36-1

* Fri Apr 02 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.35-1
- update to 0.8.35-1

* Tue Mar 04 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.34-1
- update to 0.8.34-1

* Wed Mar 03 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.33-4
- update nginx_upload_module to 2.0.12

* Wed Feb 18 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.33-3
- Add nginx_mod_h264_streaming
- Add nginx.xs.patch http://nginx.org/pipermail/nginx-ru/2010-February/032233.html

* Wed Feb 10 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.33-2
- update to 0.8.33-2

* Wed Feb 02 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.33-1
- update to 0.8.33

* Wed Jan 13 2010 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.32-1
- update to 0.8.32

* Wed Dec 23 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.31-1
- update to 0.8.31
- remove nginx-proxy-cache-empty patch

* Mon Dec 15 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.30-1
- update to 0.8.30

* Tue Dec 03 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.29-2
- add nginx-proxy-cache-empty patch

* Thu Dec 01 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.29-1
- update to 0.8.29

* Thu Nov 24 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.28-1
- update to 0.8.28
- update nginx_upload_module to 2.0.11

* Sat Nov 21 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.27-2
- Add nginx_upload_module-2.0.10-compat-nginx-0.8.27.patch patch

* Wed Nov 18 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.27-1
- update to 0.8.27

* Fri Nov 13 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.24-1
- update to 0.8.24

* Wed Nov 05 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.22-1
- update to 0.8.22

* Thu Oct 27 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.21-1
- update to 0.8.21

* Thu Oct 15 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.20-1
- update to 0.8.20

* Wed Oct 07 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.19-1
- update to 0.8.19

* Mon Sep 28 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.17-1
- update to 0.8.17

* Wed Sep 23 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.16-1
- update to 0.8.16

* Thu Sep 15 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.15-3
- update nginx-upstream-fair

* Thu Sep 15 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.15-2
- update nginx-upload-progress-module to 0.6
- update mod_zip to 1.1.5

* Thu Sep 15 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.15-1
- update to 0.8.15

* Mon Sep 07 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.14-1
- update to 0.8.14

* Thu Sep 03 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.13-4
- add nginx_uploadprogress_module
- add mod_zip

* Thu Sep 03 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.13-3
- add --with-http_secure_link_module in configure
- add --with-http_random_index_module in configure

* Thu Sep 03 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.13-2
- add --with-file-aio in configure
- add nginx_upload_module

* Tue Sep 01 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.13-1
- update to 0.8.13

* Mon Aug 31 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.11-2
- add memcached patch

* Mon Aug 31 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.11-1
- rebuild to 0.8.11

* Thu Aug 25 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.10-1
- rebuild to 0.8.10

* Thu Aug 18 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.9-1
- rebuild to 0.8.9

* Mon Aug 10 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.8-1
- rebuild to 0.8.8

* Thu Jul 28 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.7-1
- rebuild to 0.8.7

* Mon Jul 20 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.6-1
- rebuild to 0.8.6

* Wed Jul 15 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.5-1
- rebuild to 0.8.5

* Mon Jun 22 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.4-1
- rebuild to 0.8.4

* Sat Jun 19 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.3-1
- rebuild to 0.8.3

* Wed Jun 16 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.2-1
- rebuild to 0.8.2

* Sat Jun 13 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.8.1-1
- rebuild to 0.8.1

* Sat Jun 13 2009 Denis Frolov <d.frolov81 at mail dot ru> - 0.7.59-1
- rebuild to 0.7.59

* Thu Feb 19 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.35-2
- rebuild

* Thu Feb 19 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.35-1
- update to 0.6.35

* Tue Dec 30 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.34-1
- update to 0.6.34
- Fix inclusion of /usr/share/nginx tree => no unowned directories [mschwendt]

* Sun Nov 23 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.33-1
- update to 0.6.33

* Sun Jul 27 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.32-1
- update to 0.6.32
- nginx now supports DESTDIR so removed the patches that enabled it

* Mon May 26 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.31-3
- update init script
- remove 'default' listen parameter

* Tue May 13 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.31-2
- added missing Source files

* Mon May 12 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.6.31-1
- update to new upstream stable branch 0.6
- added 3rd party module nginx-upstream-fair
- add /etc/nginx/conf.d support [#443280]
- use /etc/sysconfig/nginx to determine nginx.conf [#442708]
- added default webpages
- add Requires for versioned perl (libperl.so) (via Tom "spot" Callaway)
- drop silly file Requires (via Tom "spot" Callaway)

* Sat Jan 19 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.5.35-1
- update to 0.5.35

* Sun Dec 16 2007 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.5.34-1
- update to 0.5.34

* Mon Nov 12 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.33-2
- bump build number - source wasn't update

* Mon Nov 12 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.33-1
* update to 0.5.33

* Mon Sep 24 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.32-1
- updated to 0.5.32
- fixed rpmlint UTF-8 complaints.

* Sat Aug 18 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.31-3
- added --with-http_stub_status_module build option.
- added --with-http_sub_module build option.
- add in pcre-config --cflags

* Sat Aug 18 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.31-2
- remove BuildRequires: perl-devel

* Fri Aug 17 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.31-1
- Update to 0.5.31
- specify license is BSD

* Sat Aug 11 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.30-2
- Add BuildRequires: perl-devel - fixing rawhide build

* Mon Jul 30 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.30-1
- Update to 0.5.30

* Tue Jul 24 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.29-1
- Update to 0.5.29

* Wed Jul 18 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.28-1
- Update to 0.5.28

* Mon Jul 09 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.27-1
- Update to 0.5.27

* Mon Jun 18 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.26-1
- Update to 0.5.26

* Sat Apr 28 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.19-1
- Update to 0.5.19

* Mon Apr 02 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.17-1
- Update to 0.5.17

* Mon Mar 26 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.16-1
- Update to 0.5.16
- add ownership of /usr/share/nginx/html (#233950)

* Fri Mar 23 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.15-3
- fixed package review bugs (#235222) given by ruben@rubenkerkhof.com

* Thu Mar 22 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.15-2
- fixed package review bugs (#233522) given by kevin@tummy.com

* Thu Mar 22 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 0.5.15-1
- create patches to assist with building for Fedora
- initial packaging for Fedora
