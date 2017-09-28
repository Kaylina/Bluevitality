# libintl.jar requires gcj >= 4.3 to build
%define buildjar 0

Summary: GNU libraries and utilities for producing multi-lingual messages
Name: gettext
Version: 0.18.3.2
Release: 1%{?dist}
Summary: MySQL client programs and shared libraries
Group: Applications/Databases
License: GPLv3 and LGPLv2+
Group: Development/Tools
URL: http://www.gnu.org/software/gettext/
Source: ftp://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.gz
Source2: msghack.py
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
%ifarch x86_64 ppc64 s390x
BuildRequires: automake >= 1.8
%endif
BuildRequires: autoconf >= 2.5
BuildRequires: libtool, bison, gcc-c++
# need expat for xgettext on glade
Buildrequires: expat-devel
%if %{buildjar}
BuildRequires: %{_bindir}/fastjar
# require zip and unzip for brp-java-repack-jars
BuildRequires: zip, unzip
%endif
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Patch5: gettext-0.17-open-args.patch

%description
The GNU gettext package provides a set of tools and documentation for
producing multi-lingual messages in programs. Tools include a set of
conventions about how programs should be written to support message
catalogs, a directory and file naming organization for the message
catalogs, a runtime library which supports the retrieval of translated
messages, and stand-alone programs for handling the translatable and
the already translated strings. Gettext provides an easy to use
library and tools for creating, using, and modifying natural language
catalogs and is a powerful and simple method for internationalizing
programs.


%package devel
Summary: Development files for %{name}
Group: Development/Tools
License: LGPLv2+
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: cvs
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description devel
This package contains all development related files necessary for
developing or compiling applications/libraries that needs
internationalization capability. You also need this package if you
want to add gettext support for your project.


%package libs
Summary: Libraries for %{name}
Group: System Environment/Libraries
License: LGPLv2+

%description libs
This package contains libraries used internationalization support.


%prep
%setup -q
#%patch5 -p0 -b .5-open-args~


%build
[ -f  %{_datadir}/automake/depcomp ] && cp -f %{_datadir}/automake/{depcomp,ylwrap} .

export JAVAC=gcj
%if %{buildjar}
export JAR=fastjar
%endif
%configure --without-included-gettext --enable-nls --disable-static \
    --enable-shared --with-pic-=yes --disable-csharp --disable-java
make %{?_smp_mflags} GCJFLAGS="-findirect-dispatch"


%install
rm -rf %{buildroot}
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="%{__install} -p" \
    lispdir=%{_datadir}/emacs/site-lisp \
    aclocaldir=%{_datadir}/aclocal EXAMPLESFILES=""

# move gettext to /bin
mkdir -p ${RPM_BUILD_ROOT}/bin
mv ${RPM_BUILD_ROOT}%{_bindir}/gettext ${RPM_BUILD_ROOT}/bin
ln -s ../../bin/gettext ${RPM_BUILD_ROOT}%{_bindir}/gettext

install -pm 755 %SOURCE2 ${RPM_BUILD_ROOT}/%{_bindir}/msghack

# make preloadable_libintl.so executable
chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/preloadable_libintl.so

rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir

# doc relocations
for i in gettext-runtime/man/*.html; do
  rm ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/`basename $i`
done
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/javadoc*

rm -rf ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/examples

rm -rf htmldoc
mkdir htmldoc
mv ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext/* ${RPM_BUILD_ROOT}/%{_datadir}/doc/libasprintf/* htmldoc
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/libasprintf
rm -r ${RPM_BUILD_ROOT}%{_datadir}/doc/gettext

## note libintl.jar does not build with gcj < 4.3
## since it would not be fully portable
%if %{buildjar}
### this is no longer needed since examples not packaged
## set timestamp of examples ChangeLog timestamp for brp-java-repack-jars
#for i in `find ${RPM_BUILD_ROOT} examples -newer ChangeLog -type f -name ChangeLog`; do
#  touch -r ChangeLog  $i
#done
%else
# in case another java compiler is installed
rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{name}/libintl.jar
%endif

# remove unpackaged files from the buildroot
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/emacs
rm ${RPM_BUILD_ROOT}%{_libdir}/lib*.la

%find_lang %{name}-runtime
%find_lang %{name}-tools
cat %{name}-*.lang > %{name}.lang


%clean
rm -rf ${RPM_BUILD_ROOT}


%check
make check


%define install_info /sbin/install-info
%define remove_install_info /sbin/install-info --delete


%post
/sbin/ldconfig
%{install_info} %{_infodir}/gettext.info.gz %{_infodir}/dir || :


%preun
if [ "$1" = 0 ]; then
    %{remove_install_info} %{_infodir}/gettext.info.gz %{_infodir}/dir || :
fi
exit 0


%postun -p /sbin/ldconfig


%post devel
/sbin/ldconfig
%{install_info} %{_infodir}/autosprintf.info %{_infodir}/dir || :


%preun devel
if [ "$1" = 0 ]; then
    %{remove_install_info} %{_infodir}/autosprintf.info %{_infodir}/dir || :
fi


%postun devel -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc gettext-runtime/ABOUT-NLS AUTHORS gettext-runtime/BUGS
%doc COPYING gettext-tools/misc/DISCLAIM README
%doc NEWS THANKS 
%doc gettext-runtime/man/*.1.html
%doc gettext-runtime/intl/COPYING*
/bin/*
%{_bindir}/*
%{_libdir}/libgettextlib-*.so
%{_libdir}/libgettextsrc-*.so
%{_infodir}/gettext*
%{_mandir}/man1/*
%{_libdir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/archive.dir.tar.xz
%{_datadir}/%{name}/styles
#%{_datadir}/%{name}/gettext.jar
%if %{buildjar}
%{_datadir}/%{name}/libintl.jar
%endif


%files devel
%defattr(-,root,root,-)
%doc gettext-runtime/man/*.3.html ChangeLog
%{_datadir}/%{name}/ABOUT-NLS
%{_datadir}/%{name}/projects/
%{_datadir}/%{name}/config.rpath
%{_datadir}/%{name}/*.h
%{_datadir}/%{name}/intl
%{_datadir}/%{name}/po
%{_datadir}/%{name}/msgunfmt.tcl
%{_datadir}/aclocal/*
%{_includedir}/*
%{_infodir}/autosprintf*
%{_libdir}/libasprintf.so
%{_libdir}/libgettextpo.so
%{_libdir}/libgettextlib.so
%{_libdir}/libgettextsrc.so
%{_libdir}/preloadable_libintl.so
%{_mandir}/man3/*
%{_datadir}/%{name}/javaversion.class
%doc gettext-runtime/intl-java/javadoc*

%files libs
%defattr(-,root,root,-)
%{_libdir}/libasprintf.so.*
%{_libdir}/libgettextpo.so.*


%changelog
* Mon Jan 20 2014 Ivan Polonevich <joni @ wargaming dot net> - 0.18.3.2-1
- Update upstream

* Sat Mar  5 2011 Maksim Melnikau - 0.17-4
- build for Wargaming Extra repo

* Wed Aug 26 2009 David Robaska <techie564@gmail.com> - 0.17-4
- rebuild for centos 5

* Sat Nov 22 2008 Dave Robaska <techie564@gmail.com> - 0.17-4
- rebuild hbfc3

* Mon Feb 18 2008 Jens Petersen <petersen@redhat.com> - 0.17-4
- if %%buildjar is off make sure libintl.jar does not get installed (#433210)

* Mon Feb 18 2008 Jens Petersen <petersen@redhat.com> - 0.17-3
- turn on building of libintl.jar now that we have gcc43

* Thu Feb 14 2008 Jens Petersen <petersen@redhat.com> - 0.17-2
- rebuild with gcc43

* Thu Jan 24 2008 Jens Petersen <petersen@redhat.com> - 0.17-1
- update to 0.17 release
  - update License field to GPLv3
  - add gettext-0.17-open-args.patch to fix build from upstream
  - gettext-tools-tests-lang-gawk-fail.patch, gettext-php-headers.patch,
    gettext-php-prinf-output-237241.patch, and
    gettext-xglade-define-xml-major-version-285701.patch are no longer needed
- drop superfluous po-mode-init.el source
- no need to run autoconf and autoheader when building
- pass -findirect-dispatch to gcj to make java binaries ABI independent
  (jakub,#427796)
- move autopoint, gettextize, and %{_datadir}/%{name}/ to main package
- force removal of emacs/ so install does not fail when no emacs

* Fri Sep 21 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-12
- add a libs subpackage (suggested by Dwayne Bailey, #294891)
- move preloadable_libintl.so to the devel subpackage

* Fri Sep 14 2007 Nils Philippsen <nphilipp@redhat.com> - 0.16.1-11
- remove gettext-xglade-include-expat-285701.patch, add
  gettext-xglade-define-xml-major-version-285701.patch to determine
  XML_MAJOR_VERSION from expat.h and define it in config.h (#285701)

* Wed Sep 12 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-10
- buildrequire expat-devel
- add gettext-xglade-include-expat-285701.patch to include expat.h
  to get xgettext to dl the right libexpat (Nils Philippsen, #285701)

* Thu Aug 16 2007 Jens Petersen <petersen@redhat.com>
- specify license is GPL and LGPL version 2 or later

* Wed Aug  1 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-9
- fix encoding of msghack script (Dwayne Bailey, #250248)

* Mon Apr 30 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-8
- add gettext-php-prinf-output-237241.patch to workaround php test failure
  (#237241)
- add gettext-php-headers.patch to correct php test headers
  (Robert Scheck, #232832)

* Thu Mar 15 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-7
- set preloadable_libintl.so executable in %%install so it gets stripped
- force removal of infodir/dir since it is not there when /sbin is not in path

* Tue Mar 13 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-6
- add buildjar switch for building of libintl.jar
- lots of spec file cleanup (Mamoru Tasaka, #225791):
- preserve timestamps of installed files
- disable building of static library
- use %%find_lang for .mo files
- remove examples from -devel package
- do not own en@*quot locale dirs
- set preloadable_libintl.so executable
- add ChangeLog to -devel package
- add %%check to run make check
- add gettext-tools-tests-lang-gawk-fail.patch to work around gawk test failure

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 0.16.1-5
- rebuild to pick up dependency on libgcj.so.8rh instead libgcj.so.7rh

* Thu Feb  1 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-4
- protect install-info in devel %%post and %%preun too (Ville Skyttä, #223689)
- forward port fix to reset of timestamp of examples ChangeLog for
  brp-java-repack-jars libintl.jar multilib conflict (#205207)

* Mon Jan 22 2007 Jens Petersen <petersen@redhat.com> - 0.16.1-3
- protect install-info in %%post and %%preun (Ville Skyttä, #223689)

* Fri Dec 22 2006 Jens Petersen <petersen@redhat.com> - 0.16.1-1
- update to 0.16.1

* Mon Nov 27 2006 Jens Petersen <petersen@redhat.com> - 0.16-2
- re-enable openmp on ia64

* Thu Nov 23 2006 Jens Petersen <petersen@redhat.com> - 0.16-1
- update to 0.16 release
- disable openmp on ia64 (#216988)

* Fri Oct 27 2006 Jens Petersen <petersen@redhat.com> - 0.15-1
- update to 0.15 release
- mkinstalldirs and libintl.jar are gone
- javaversion.class added

* Mon Oct  2 2006 Jens Petersen <petersen@redhat.com> - 0.14.6-3
- buildrequire zip and unzip to fix libintl.jar multilib conflict (#205207)

* Fri Aug 25 2006 Jens Petersen <petersen@redhat.com> - 0.14.6-2
- move libgettext*.so devel files to devel package (Patrice Dumas, #203622)

* Mon Aug  7 2006 Jens Petersen <petersen@redhat.com> - 0.14.6-1
- update to 0.14.6
- include preloadable_libintl.so again (Roozbeh Pournader, #149809)
- remove .la files (Kjartan Maraas, #172624)
- cleanup spec file

* Tue Jul 25 2006 Thomas Fitzsimmons <fitzsim@redhat.com> - 0.14.5-4
- Bump release number.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.14.5-3.1
- rebuild

* Wed Feb 22 2006 Karsten Hopp <karsten@redhat.de> 0.14.5-3
- --disable-csharp, otherwise it'll build a dll when mono is 
  installed in the buildroot.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.14.5-2.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.14.5-2.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 0.14.5-2.2
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 28 2005 Jindrich Novy <jnovy@redhat.com> 0.14.5-2
- convert spec to UTF-8
- remove old tarballs from sources

* Thu Aug 11 2005 Leon Ho <llch@redhat.com>
- updated to 0.14.5
- Add cvs as Requires for gettext-devel

* Mon Mar 21 2005 Leon Ho <llch@redhat.com>
- updated to 0.14.3
- fixed compiling problem on gcc4 (#150992)
- fixed Group for -devel (#138303)
- moved gettextize and autopoint to -devel (#137542, #145768)
- moved some of the man pages

* Tue Mar 01 2005 Jakub Jelinek <jakub@redhat.com>
- rebuilt with gcc 4.0

* Wed Dec 01 2004 Leon Ho <llch@redhat.com>
- Add env var to redirect use fastjar instead of jar
- BuildRequires fastjar and libgcj

* Mon Nov 01 2004 Leon Ho <llch@redhat.com>
- fix call on phase0_getc()
- fix temp file issue (#136323 - CAN-2004-0966 - mjc)

* Sun Oct 03 2004 Leon Ho <llch@redhat.com>
- fixed typo on %%preun on -devel

* Fri Oct 01 2004 Leon Ho <llch@redhat.com>
- fix install_info
- add gcc-java build requirement

* Mon Sep 13 2004 Leon Ho <llch@redhat.com>
- move java stuff to gettext-devel (#132239)
- add BuildRequires: gcc-c++ (#132518)
- add some missing install-info and ldconfig (#131272)
- fix dir ownership (#133696)
- run autotools for 1.9

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 08 2004 Leon Ho <llch@redhat.com>
- use --without-included-gettext to avoid the need of libintl.so (#125497)
- remove preloadable_libintl.so

* Sun Jun 06 2004 Leon Ho <llch@redhat.com>
- moved some of the shared lib to main pkg
- added more build requires

* Thu Jun 03 2004 Leon Ho <llch@redhat.com>
- add conditionals for patch and requires auto* (#125216)

* Wed Jun 02 2004 Leon Ho <llch@redhat.com>
- packaged lib files for devel
- moved some of the files to different sub-pkg
- fix problem on x86_64 build

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 02 2004 Leon Ho <llch@redhat.com>
- rebuilt to 0.14.1

* Fri Sep 19 2003 Leon Ho <llch@redhat.com>
- rebuilt 0.12.1
- fix including files and excludes some patches

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 14 2003 Leon Ho <llch@redhat.com>
- 0.11.5

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 16 2003 Leon Ho <llch@redhat.com> 0.11.4-6
- add online help for msghack replacement

* Thu Dec  5 2002 Leon Ho <llch@redhat.com> 0.11.4-5
- add patch to fix gettextize (#78720)

* Wed Nov 27 2002 Tim Powers <timp@redhat.com> 0.11.4-4
- remove unpackaged files from the buildroot

* Wed Aug 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.11.4-3
- Use %%{_libdir} instead of /usr/lib (#72524)

* Fri Aug  2 2002 Nalin Dahyabhai <nalin@redhat.com> 0.11.4-2
- install ulonglong.m4, which is required by uintmax_t.m4, which is already
  being installed

* Sun Jul 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.11.4-1
- 0.11.4

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.11.2-1
- 0.11.2
- include some new files

* Fri Apr  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.11.1-2
- Add patch to make it compile with C99 compilers (#62313)

* Wed Mar 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.11.1-1
- 0.11.1

* Sun Feb 17 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update gettext to 0.11
- disable patch4

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Dec  5 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.10.40-3
- improve automake handling

* Wed Nov 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.10.40-2
- Add URL
- Add automake workaround (#56081)

* Sun Sep 16 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.10.40-1
- 0.10.40 - libintl is now LGPLed (it was GPLed). Note that RHL
  uses the glibc version, and don't include libintl from gettext.
- include new man pages
- don't include the elisp mode - bundle it into the main emacs package,
  like we do for XEmacs.
- README-alpha no longer exists, so don't list it as a doc file

* Fri Aug 24 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.10.38-7
- Rebuild - this should fix #52463

* Wed Aug 22 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.10.38-6
- Fix handling of multiline entries (rest of #50065)
- don't use the references of the last entry in a po file
- remove duplicates when inverting
- Own the en@quot and en@boldquot locale dirs (#52164)
- Handle entries with a first line of "" as identical to those
  without

* Thu Aug  9 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Added "--append" and "-o" to msghack, which should address 
  initial concerns in #50065

* Thu Jul 19 2001 Trond Eivind Glomsrød <teg@redhat.com>
- New msghack - from scratch, in python

* Tue Jul 17 2001 Trond Eivind Glomsrød <teg@redhat.com>
- msghack is back

* Mon Jun  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Include some docfiles

* Sun Jun 03 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- 0.10.38
- do not include charset.alias

* Wed May  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- Build statically.

* Mon Apr 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 0.10.37
- Disable all but two patches

* Sun Feb 25 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Initialize proper fonts when entering po-mode (#29152)

* Mon Feb 12 2001 Yukihiro Nakai <ynakai@redhat.com>
- More fix about msgmerge.

* Mon Feb 12 2001 Yukihiro Nakai <ynakai@redhat.com>
- Fix for msgmerge not to break multibyte strings
  at Japanese locale.

* Wed Jan 24 2001 Matt Wilson <msw@redhat.com>
- fixed the %%lang generator to not have "./" in the lang

* Sun Jan 14 2001 Trond Eivind Glomsrød <teg@redhat.com>
- add an init file for the emacs po-mode
- update source URL

* Thu Jan 11 2001 Bill Nottingham <notting@redhat.com>
- put gettext in /bin for initscripts use
- %%langify

* Fri Dec 29 2000 Bill Nottingham <notting@redhat.com>
- prereq /sbin/install-info

* Wed Aug 23 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Added patch from Ulrich Drepper

* Fri Aug 04 2000 Trond Eivind Glomsrød <teg@redhat.com>
- update DESTDIR patch (#12072)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fix problems wrt to DESTDIR (#12072)

* Thu Jun 22 2000 Preston Brown <pbrown@redhat.com>
- use FHS paths
- add buildroot patch for .../intl/Makefile.in, was using abs. install path

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- minor configure tweaks for ia64

* Sun Feb 27 2000 Cristian Gafton <gafton@redhat.com>
- add --comments to msghack

* Thu Feb 10 2000 Cristian Gafton <gafton@redhat.com>
- fix bug #9240 - gettextize has the right aclocal patch

* Wed Jan 12 2000 Cristian Gafton <gafton@redhat.com>
- add the --diff and --dummy options

* Wed Oct 06 1999 Cristian Gafton <gafton@redhat.com>
- add the --missing option to msghack

* Wed Sep 22 1999 Cristian Gafton <gafton@redhat.com>
- updated msghack not to merge in fuzzies in the master catalogs

* Thu Aug 26 1999 Cristian Gafton <gafton@redhat.com>
- updated msghack to understand --append

* Wed Aug 11 1999 Cristian Gafton <gafton@redhat.com>
- updated msghack to correctly deal with sorting files

* Thu May 06 1999 Cristian Gafton <gafton@redhat.com>
- msghack updates

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 8)

* Mon Mar 08 1999 Cristian Gafton <gafton@redhat.com>
- added patch for misc hacks to facilitate rpm translations

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to allow to build on ARM

* Wed Sep 30 1998 Jeff Johnson <jbj@redhat.com>
- add Emacs po-mode.el files.

* Sun Sep 13 1998 Cristian Gafton <gafton@redhat.com>
- include the aclocal support files

* Fri Sep  3 1998 Bill Nottingham <notting@redhat.com>
- remove devel package (functionality is in glibc)

* Tue Sep  1 1998 Jeff Johnson <jbj@redhat.com>
- update to 0.10.35.

* Mon Jun 29 1998 Jeff Johnson <jbj@redhat.com>
- add gettextize.
- create devel package for libintl.a and libgettext.h.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun Nov 02 1997 Cristian Gafton <gafton@redhat.com>
- added info handling
- added misc-patch (skip emacs-lisp modofications)

* Sat Nov 01 1997 Erik Troan <ewt@redhat.com>
- removed locale.aliases as we get it from glibc now
- uses a buildroot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- Built against glibc
