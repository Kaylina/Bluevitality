# Define the version of the Linux Kernel Archive tarball.
%define LKAver 3.2.53

# Define the buildid, if required.
#define buildid .

# The following build options are enabled by default.
# Use either --without <option> on your rpmbuild command line
# or force the values to 0, here, to disable them.

# standard kernel
%define with_std %{?_without_std:0} %{?!_without_std:1}
# kernel-PAE
%define with_pae %{?_without_pae:0} %{?!_without_pae:1}
# kernel-doc
%define with_doc %{?_without_doc:0} %{?!_without_doc:1}
# kernel-headers
%define with_hdr %{?_without_hdr:0} %{?!_without_hdr:1}

# Build only the kernel-doc package.
%ifarch noarch
%define with_std 0
%define with_pae 0
%define with_hdr 0
%endif

# Build only the 32-bit kernel-headers package.
%ifarch i386
%define with_std 0
%define with_pae 0
%define with_doc 0
%endif

# Build just the 32-bit kernel & kernel-PAE packages.
%ifarch i686
%define with_doc 0
%define with_hdr 0
%endif

# Build just the 64-bit kernel & kernel-headers packages.
%ifarch x86_64
%define with_pae 0
%define with_doc 0
%endif

# Define the correct buildarch.
%define buildarch x86_64
%ifarch i386 i686
%define buildarch i386
%endif

# Packages that need to be installed before the kernel because the %post scripts make use of them.
%define kernel_prereq fileutils, module-init-tools, initscripts >= 8.11.1-1, mkinitrd >= 4.2.21-1

# Determine the sublevel number and set pkg_version.
%define sublevel %(echo %{LKAver} | %{__awk} -F\. '{ print $3 }')
%if "%{sublevel}" == ""
%define pkg_version %{LKAver}.0
%else
%define pkg_version %{LKAver}
%endif

# Set pkg_release.
%define pkg_release 3%{?buildid}%{?dist}

Name: kernel-lt
Summary: The Linux kernel. (The core of any Linux-based operating system.)
Group: System Environment/Kernel
License: GPLv2
URL: http://www.kernel.org/
Version: %{pkg_version}
Release: %{pkg_release}
ExclusiveArch: noarch i386 i686 x86_64
ExclusiveOS: Linux
Provides: kernel = %{version}
Provides: kernel-%{_target_cpu} = %{version}-%{release}
Provides: kernel-lt = %{version}
Provides: kernel-lt-%{_target_cpu} = %{version}-%{release}
Prereq: %{kernel_prereq}
# We can't let RPM do the dependencies automatically because it'll then pick up
# a correct but undesirable perl dependency from the module headers which
# isn't required for the kernel proper to function.
AutoReq: no
AutoProv: yes

# List the packages used during the kernel build.
BuildPreReq: module-init-tools, patch >= 2.5.4, bash >= 2.03, sh-utils, tar
BuildPreReq: bzip2, findutils, gzip, m4, perl, make >= 3.78, diffutils
BuildRequires: gcc >= 3.4.2, binutils >= 2.12, redhat-rpm-config, unifdef
BuildConflicts: rhbuildsys(DiskFree) < 500Mb

# Sources.
Source0: ftp://ftp.kernel.org/pub/linux/kernel/v3.x/linux-%{LKAver}.tar.xz
Source1: config-%{version}-i686
Source2: config-%{version}-i686-PAE
Source3: config-%{version}-x86_64
Source4: initscripts-rc.sysinit-rtc.el5.elrepo.patch

# Do not package the source tarball.
#NoSource: 0 

%define KVERREL %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}

BuildRoot: %{_tmppath}/%{name}-%{KVERREL}-root-%(%{__id_u} -n)

# Disable the building of the debug package.
%define	debug_package %{nil}

%description
This package provides the Linux kernel (vmlinuz), the core of any
Linux-based operating system. The kernel handles the basic functions
of the OS: memory allocation, process allocation, device I/O, etc.

%package devel
Summary: Development package for building kernel modules to match the kernel.
Group: System Environment/Kernel
Provides: kernel-devel = %{version}
Provides: kernel-devel-%{_target_cpu} = %{version}-%{release}
Provides: kernel-lt-devel = %{version}
Provides: kernel-lt-devel-%{_target_cpu} = %{version}-%{release}
Prereq: /usr/bin/find
AutoReqProv: no

%description devel
This package provides the kernel header files and makefiles
sufficient to build modules against the kernel package.

%package PAE
Summary: The Linux kernel for PAE capable processors.
Group: System Environment/Kernel
Provides: kernel = %{version}
Provides: kernel-%{_target_cpu} = %{version}-%{release}PAE
Provides: kernel-PAE = %{version}
Provides: kernel-PAE-%{_target_cpu} = %{version}-%{release}PAE
Provides: kernel-lt = %{version}
Provides: kernel-lt-%{_target_cpu} = %{version}-%{release}PAE
Provides: kernel-lt-PAE = %{version}
Provides: kernel-lt-PAE-%{_target_cpu} = %{version}-%{release}PAE
Prereq: %{kernel_prereq}
# We can't let RPM do the dependencies automatically because it'll then pick up
# a correct but undesirable perl dependency from the module headers which
# isn't required for the kernel proper to function.
AutoReq: no
AutoProv: yes

%description PAE
This package provides a version of the Linux kernel with support for up to 16GB of memory.
It requires processors with Physical Address Extension (PAE) ability.
The non-PAE kernel can only address up to 4GB of memory.

%package PAE-devel
Summary: Development package for building kernel modules to match the PAE kernel.
Group: System Environment/Kernel
Provides: kernel-PAE-devel = %{version}
Provides: kernel-PAE-devel-%{_target_cpu} = %{version}-%{release}PAE
Provides: kernel-lt-PAE-devel = %{version}
Provides: kernel-lt-PAE-devel-%{_target_cpu} = %{version}-%{release}PAE
Prereq: /usr/bin/find
AutoReqProv: no

%description PAE-devel
This package provides the kernel header files and makefiles
sufficient to build modules against the PAE kernel package.

%package doc
Summary: Various bits of documentation found in the kernel source.
Group: Documentation
Provides: kernel-lt-doc = %{version}-%{release}

%description doc
This package provides documentation files from the kernel source.
Various bits of information about the Linux kernel and the device
drivers shipped with it are documented in these files.

You'll want to install this package if you need a reference to the
options that can be passed to the kernel modules at load time.

%package headers
Summary: Kernel C header files for use by glibc.
Group: Development/System
Conflicts: kernel-headers < %{version}-%{release}
Provides: kernel-lt-headers = %{version}-%{release}

%description headers
This package provides the C header files that specify the interface
between the Linux kernel and userspace libraries & programs. The
header files define structures and constants that are needed when
building most standard programs. They are also required when
rebuilding the glibc package.

%prep
%setup -q -n %{name}-%{version} -c
%{__mv} linux-%{LKAver} linux-%{version}.%{_target_cpu}
pushd linux-%{version}.%{_target_cpu} > /dev/null
%{__cp} %{SOURCE1} .
%{__cp} %{SOURCE2} .
%{__cp} %{SOURCE3} .
popd > /dev/null

%build
BuildKernel() {
    Flavour=$1

    # Select the correct flavour configuration file and set the development directory / symbolic link.
    if [ -n "$Flavour" ]; then
      Config=config-%{version}-%{_target_cpu}-$Flavour
      DevelDir=/usr/src/kernels/%{KVERREL}-$Flavour-%{_target_cpu}
      DevelLink=/usr/src/kernels/%{KVERREL}$Flavour-%{_target_cpu}
    else
      Config=config-%{version}-%{_target_cpu}
      DevelDir=/usr/src/kernels/%{KVERREL}-%{_target_cpu}
      DevelLink=
    fi

    KernelVer=%{version}-%{release}$Flavour

    # Set the EXTRAVERSION string in the main Makefile.
    %{__perl} -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}$Flavour/" Makefile

    %{__make} -s distclean
    %{__cp} $Config .config

    %{__make} -s CONFIG_DEBUG_SECTION_MISMATCH=y ARCH=%{buildarch} %{?_smp_mflags} bzImage
    %{__make} -s CONFIG_DEBUG_SECTION_MISMATCH=y ARCH=%{buildarch} %{?_smp_mflags} modules

    # Install the results into the RPM_BUILD_ROOT directory.
    %{__mkdir_p} $RPM_BUILD_ROOT/boot
    %{__install} -m 644 .config $RPM_BUILD_ROOT/boot/config-$KernelVer
    touch $RPM_BUILD_ROOT/boot/initrd-$KernelVer.img
    %{__gzip} -c9 < Module.symvers > $RPM_BUILD_ROOT/boot/symvers-$KernelVer.gz
    %{__install} -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-$KernelVer
    %{__cp} arch/%{buildarch}/boot/bzImage $RPM_BUILD_ROOT/boot/vmlinuz-$KernelVer
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/$KernelVer
    %{__make} -s INSTALL_MOD_PATH=$RPM_BUILD_ROOT KERNELRELEASE=$KernelVer ARCH=%{buildarch} modules_install

    # Set the modules to be executable, so that they will be stripped when packaged.
    find $RPM_BUILD_ROOT/lib/modules/$KernelVer -type f -name "*.ko" -exec %{__chmod} u+x "{}" ";"

    # Remove all the files that will be auto generated by depmod at the kernel install time.
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.*

    # Remove the two symbolic links.
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/source

    # Create the four directories and the one symbolic link.
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/$KernelVer/extra
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/$KernelVer/updates
    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/$KernelVer/weak-updates
    pushd $RPM_BUILD_ROOT/lib/modules/$KernelVer > /dev/null
    %{__ln_s} build source
    popd > /dev/null

    # Collect the required development files.
    %{__cp} -a --parents `find -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    %{__cp} -a --parents kernel/bounds.[cs] $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    %{__cp} -a --parents arch/x86/kernel/*.[cs] $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    %{__cp} -a --parents `find security -type f -name "*.h"` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    %{__cp} -a Kbuild $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    %{__cp} -a .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    %{__cp} -a Module.* $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    %{__rm} -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Documentation
    %{__rm} -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    %{__rm} -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts

    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include

    %{__cp} -a --parents arch/x86/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    %{__cp} -a --parents include/generated/*.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    pushd include > /dev/null
    %{__cp} -a * $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    popd > /dev/null
    %{__rm} -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/Kbuild

    %{__cp} -a include/generated/*.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/linux

    %{__mkdir_p} $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts

    %{__cp} -a scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    find $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts -type f -name "*.o" -exec %{__rm} -f "{}" ";"

    # Now ensure that the Makefile, Kbuild, .config, version.h, autoconf.h and auto.conf files
    # all have matching timestamps so that external modules can be built.
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Kbuild
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/.config
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/linux/version.h
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/linux/autoconf.h
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/generated/autoconf.h
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/config/auto.conf

    # Move the development files out of the /lib/modules/ file system.
    %{__mkdir_p} $RPM_BUILD_ROOT/usr/src/kernels
    %{__mv} $RPM_BUILD_ROOT/lib/modules/$KernelVer/build $RPM_BUILD_ROOT$DevelDir
    %{__ln_s} -f ../../..$DevelDir $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    [ -z "$DevelLink" ] || %{__ln_s} -f `basename $DevelDir` $RPM_BUILD_ROOT$DevelLink
}

%{__rm} -rf $RPM_BUILD_ROOT
pushd linux-%{version}.%{_target_cpu} > /dev/null
%if %{with_std}
BuildKernel
%endif
%if %{with_pae}
BuildKernel PAE
%endif
popd > /dev/null

%install
pushd linux-%{version}.%{_target_cpu} > /dev/null
%if %{with_doc}
%{__mkdir_p} $RPM_BUILD_ROOT/usr/share/doc/%{name}-doc-%{version}/Documentation
# Sometimes non-world-readable files sneak into the kernel source tree.
%{__chmod} -R a+r *
# Copy the documentation over.
%{__tar} cf - Documentation | %{__tar} xf - -C $RPM_BUILD_ROOT/usr/share/doc/%{name}-doc-%{version}
# Remove the unrequired file.
%{__rm} -f $RPM_BUILD_ROOT/usr/share/doc/%{name}-doc-%{version}/Documentation/.gitignore
%endif

%if %{with_hdr}
# Install the kernel headers.
%{__make} -s INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr ARCH=%{buildarch} headers_install
find $RPM_BUILD_ROOT/usr/include -type f ! -name "*.h" -exec %{__rm} -f "{}" ";"
# For now, glibc provides the scsi headers.
%{__rm} -rf $RPM_BUILD_ROOT/usr/include/scsi
%endif
popd > /dev/null

# copy patch to rc.sysinit
mkdir -p $RPM_BUILD_ROOT/etc/
%{__cp} %{SOURCE4} $RPM_BUILD_ROOT/etc/initscripts-rc.sysinit-rtc.el5.elrepo.patch

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
/sbin/new-kernel-pkg --package kernel-lt --mkinitrd --depmod --install %{KVERREL} || exit $?
if [ -x /sbin/weak-modules ]; then
    /sbin/weak-modules --add-kernel %{KVERREL} || exit $?
fi
cd /etc/
patch -p0 < /etc/initscripts-rc.sysinit-rtc.el5.elrepo.patch

%post devel
if [ -f /etc/sysconfig/kernel ]; then
    . /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ]; then
    pushd /usr/src/kernels/%{KVERREL}-%{_target_cpu} > /dev/null
    /usr/bin/find . -type f | while read f; do hardlink -c /usr/src/kernels/*FC*/$f $f; done
    popd > /dev/null
fi

%post PAE
/sbin/new-kernel-pkg --package kernel-lt-PAE --mkinitrd --depmod --install %{KVERREL}PAE || exit $?
if [ -x /sbin/weak-modules ]; then
    /sbin/weak-modules --add-kernel %{KVERREL}PAE || exit $?
fi

%post PAE-devel
if [ -f /etc/sysconfig/kernel ]; then
    . /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ]; then
    pushd /usr/src/kernels/%{KVERREL}-PAE-%{_target_cpu} > /dev/null
    /usr/bin/find . -type f | while read f; do hardlink -c /usr/src/kernels/*FC*/$f $f; done
    popd > /dev/null
fi

%preun
/sbin/new-kernel-pkg --rminitrd --rmmoddep --remove %{KVERREL} || exit $?
if [ -x /sbin/weak-modules ]; then
    /sbin/weak-modules --remove-kernel %{KVERREL} || exit $?
fi

%preun PAE
/sbin/new-kernel-pkg --rminitrd --rmmoddep --remove %{KVERREL}PAE || exit $?
if [ -x /sbin/weak-modules ]; then
    /sbin/weak-modules --remove-kernel %{KVERREL}PAE || exit $?
fi

# Files section.
%if %{with_doc}
%files doc
%defattr(-,root,root)
%{_datadir}/doc/%{name}-doc-%{version}/Documentation/*
%dir %{_datadir}/doc/%{name}-doc-%{version}/Documentation
%dir %{_datadir}/doc/%{name}-doc-%{version}
%endif

%if %{with_hdr}
%files headers
%defattr(-,root,root)
/usr/include/*
%endif

%if %{with_std}
%files
%defattr(-,root,root)
/etc/initscripts-rc.sysinit-rtc.el5.elrepo.patch
/boot/vmlinuz-%{KVERREL}
/boot/System.map-%{KVERREL}
/boot/symvers-%{KVERREL}.gz
/boot/config-%{KVERREL}
/lib/firmware
%dir /lib/modules/%{KVERREL}
/lib/modules/%{KVERREL}/kernel
/lib/modules/%{KVERREL}/build
/lib/modules/%{KVERREL}/source
/lib/modules/%{KVERREL}/extra
/lib/modules/%{KVERREL}/updates
/lib/modules/%{KVERREL}/weak-updates
%ghost /boot/initrd-%{KVERREL}.img

%files devel
%defattr(-,root,root)
%dir /usr/src/kernels
%verify(not mtime) /usr/src/kernels/%{KVERREL}-%{_target_cpu}
%endif

%if %{with_pae}
%files PAE
%defattr(-,root,root)
/boot/vmlinuz-%{KVERREL}PAE
/boot/System.map-%{KVERREL}PAE
/boot/symvers-%{KVERREL}PAE.gz
/boot/config-%{KVERREL}PAE
/lib/firmware
%dir /lib/modules/%{KVERREL}PAE
/lib/modules/%{KVERREL}PAE/kernel
/lib/modules/%{KVERREL}PAE/build
/lib/modules/%{KVERREL}PAE/source
/lib/modules/%{KVERREL}PAE/extra
/lib/modules/%{KVERREL}PAE/updates
/lib/modules/%{KVERREL}PAE/weak-updates
%ghost /boot/initrd-%{KVERREL}PAE.img

%files PAE-devel
%defattr(-,root,root)
%dir /usr/src/kernels
%verify(not mtime) /usr/src/kernels/%{KVERREL}-PAE-%{_target_cpu}
/usr/src/kernels/%{KVERREL}PAE-%{_target_cpu}
%endif

%changelog
* Tue Dec 03 2013 Ivan Polonevich <joni @ wargaming dot net> - 3.2.53-1.1
- Add patch for fix hardware clock http://elrepo.org/tiki/kernel-lt 

* Fri Nov 29 2013 Alan Bartlett <ajb@elrepo.org> - 3.2.53-1
- Updated with the 3.2.53 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.2.53]

* Sun Oct 27 2013 Alan Bartlett <ajb@elrepo.org> - 3.2.52-1
- Updated with the 3.2.52 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.2.52]
- First release in the kernel-lt-3.2 series for EL5.

* Tue Oct 22 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.101-1
- Updated with the 3.0.101 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.101]

* Mon Oct 14 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.100-1
- Updated with the 3.0.100 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.100]

* Sat Oct 05 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.99-1
- Updated with the 3.0.99 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.99]

* Wed Oct 02 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.98-1
- Updated with the 3.0.98 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.98]

* Fri Sep 27 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.97-1
- Updated with the 3.0.97 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.97]

* Sat Sep 14 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.96-1
- Updated with the 3.0.96 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.96]

* Sun Sep 08 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.95-1
- Updated with the 3.0.95 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.95]

* Thu Aug 29 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.94-1
- Updated with the 3.0.94 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.94]

* Tue Aug 20 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.93-1
- Updated with the 3.0.93 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.93]

* Tue Aug 20 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.92-1
- Updated with the 3.0.92 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.92]
- Never released due to an bug in the source code.

* Thu Aug 15 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.91-1
- Updated with the 3.0.91 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.91]

* Mon Aug 12 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.90-1
- Updated with the 3.0.90 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.90]

* Sun Aug 04 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.89-1
- Updated with the 3.0.89 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.89]

* Mon Jul 29 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.88-1
- Updated with the 3.0.88 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.88]

* Mon Jul 22 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.87-1
- Updated with the 3.0.87 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.87]

* Sun Jul 14 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.86-1
- Updated with the 3.0.86 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.86]

* Thu Jul 04 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.85-1
- Updated with the 3.0.85 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.85]

* Thu Jun 27 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.84-1
- Updated with the 3.0.84 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.84]

* Fri Jun 21 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.83-1
- Updated with the 3.0.83 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.83]

* Thu Jun 13 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.82-1
- Updated with the 3.0.82 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.82]

* Sat Jun 08 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.81-1
- Updated with the 3.0.81 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.81]

* Fri May 24 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.80-1
- Updated with the 3.0.80 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.80]

* Sun May 19 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.79-1
- Updated with the 3.0.79 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.79]

* Sat May 11 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.78-1
- Updated with the 3.0.78 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.78]

* Thu May 09 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.77-2
- CONFIG_DEVTMPFS=y and CONFIG_DEVTMPFS_MOUNT=y [http://elrepo.org/bugs/view.php?id=381]

* Wed May 08 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.77-1
- Updated with the 3.0.77 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.77]

* Wed May 01 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.76-1
- Updated with the 3.0.76 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.76]

* Fri Apr 26 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.75-1
- Updated with the 3.0.75 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.75]
- CONFIG_REGULATOR_DUMMY disabled. [https://bugzilla.kernel.org/show_bug.cgi?id=50711]
- Reset CONFIG_NUMA=y for 32-bit.

* Wed Apr 17 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.74-1
- Updated with the 3.0.74 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.74]

* Sat Apr 13 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.73-1
- Updated with the 3.0.73 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.73]

* Sat Apr 06 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.72-1
- Updated with the 3.0.72 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.72]
- Never released due to an bug in the source code.

* Thu Mar 28 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.71-1
- Updated with the 3.0.71 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.71]

* Thu Mar 21 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.70-1
- Updated with the 3.0.70 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.70]

* Thu Mar 14 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.69-1
- Updated with the 3.0.69 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.69]

* Mon Mar 04 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.68-1
- Updated with the 3.0.68 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.68]

* Fri Mar 01 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.67-2
- CONFIG_IPV6_PIMSM_V2=y [http://elrepo.org/bugs/view.php?id=354]

* Thu Feb 28 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.67-1
- Updated with the 3.0.67 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.67]
- CONFIG_IPV6_SIT_6RD=y, CONFIG_IPV6_SUBTREES=y and
- CONFIG_IPV6_MROUTE_MULTIPLE_TABLES=y [http://elrepo.org/bugs/view.php?id=354]

* Thu Feb 21 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.66-1
- Updated with the 3.0.66 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.66]

* Mon Feb 18 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.65-1
- Updated with the 3.0.65 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.65]

* Fri Feb 15 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.64-1
- Updated with the 3.0.64 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.64]

* Mon Feb 11 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.63-1
- Updated with the 3.0.63 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.63]

* Mon Feb 04 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.62-1
- Updated with the 3.0.62 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.62]

* Tue Jan 29 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.61-1
- Updated with the 3.0.61 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.61]

* Tue Jan 22 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.60-1
- Updated with the 3.0.60 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.60]

* Thu Jan 17 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.59-1
- Updated with the 3.0.59 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.59]

* Sat Jan 12 2013 Alan Bartlett <ajb@elrepo.org> - 3.0.58-1
- Updated with the 3.0.58 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.58]
- CONFIG_UFS_FS=m [http://elrepo.org/bugs/view.php?id=342]

* Tue Dec 18 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.57-1
- Updated with the 3.0.57 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.57]

* Tue Dec 11 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.56-1
- Updated with the 3.0.56 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.56]

* Fri Dec 07 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.55-1
- Updated with the 3.0.55 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.55]

* Tue Dec 04 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.54-1
- Updated with the 3.0.54 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.54]

* Mon Nov 26 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.53-1
- Updated with the 3.0.53 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.53]
- CONFIG_MAC80211_DEBUGFS=y, CONFIG_ATH_DEBUG=y [http://elrepo.org/bugs/view.php?id=326]
- CONFIG_ATH9K_RATE_CONTROL disabled. [http://elrepo.org/bugs/view.php?id=327]

* Sun Nov 18 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.52-1
- Updated with the 3.0.52 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.52]

* Thu Nov 08 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.51-2
- CONFIG_ARPD=y [Steve Clark]

* Tue Nov 06 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.51-1
- Updated with the 3.0.51 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.51]

* Wed Oct 31 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.50-1
- Updated with the 3.0.50 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.50]

* Sun Oct 28 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.49-1
- Updated with the 3.0.49 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.49]
- CONFIG_MAC80211_MESH=y [Jonathan Bither]
- CONFIG_LIBERTAS_MESH=y

* Tue Oct 23 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.48-1
- Updated with the 3.0.48 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.48]

* Mon Oct 22 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.47-1
- Updated with the 3.0.47 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.47]
- Reconfigured as kernel-lt. [http://lists.elrepo.org/pipermail/elrepo/2012-October/001441.html]

* Sat Oct 13 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.46-1
- Updated with the 3.0.46 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.46]
- CONFIG_FHANDLE=y

* Mon Oct 08 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.45-1
- Updated with the 3.0.45 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.45]
- CONFIG_RTC_DRV_CMOS=y [Dag Wieers]

* Wed Oct 03 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.44-1
- Updated with the 3.0.44 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.44]

* Sat Sep 15 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.43-1
- Updated with the 3.0.43 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.43]

* Mon Aug 27 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.42-1
- Updated with the 3.0.42 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.42]

* Thu Aug 16 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.41-1
- Updated with the 3.0.41 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.41]

* Thu Aug 09 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.40-1
- Updated with the 3.0.40 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.40]

* Thu Aug 02 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.39-1
- Updated with the 3.0.39 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.39]

* Tue Jul 31 2012 Alan Bartlett <ajb@elrepo.org> - 3.0.38-1
- Updated with the 3.0.38 source tarball.
- [https://www.kernel.org/pub/linux/kernel/v3.x/ChangeLog-3.0.38]
- General availability.
