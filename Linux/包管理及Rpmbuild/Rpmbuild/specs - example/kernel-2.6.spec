Summary: The Linux kernel (the core of the Linux operating system)

# What parts do we want to build?  We must build at least one kernel.
# These are the kernels that are built IF the architecture allows it.
# All should default to 1 (enabled) and be flipped to 0 (disabled)
# by later arch-specific checks

# The following build options are enabled by default.
# Use either --without <opt> in your rpmbuild command or force values
# to 0 in here to disable them
#
# standard kernel
%define with_up        %{?_without_up:        0} %{?!_without_up:        1}
# kernel-smp (only valid for ppc 32-bit, sparc64)
%define with_smp       %{?_without_smp:       0} %{?!_without_smp:       1}
# kernel-PAE (only valid for i686)
%define with_pae       %{?_without_pae:       0} %{?!_without_pae:       1}
# kernel-xen (only valid for i686, x86_64 and ia64)
#%define with_xen       %{?_without_xen:       0} %{?!_without_xen:       1}
%define with_xen       0
# kernel-kdump (only valid for ppc64)
%define with_kdump     %{?_without_kdump:     0} %{?!_without_kdump:     1}
# kernel-debug
%define with_debug     0
# kernel-doc
%define with_doc       %{?_without_doc:       0} %{?!_without_doc:       1}
# kernel-headers
%define with_headers   %{?_without_headers:   0} %{?!_without_headers:   1}
# kernel-debuginfo
%define with_debuginfo 0

# Control whether we perform a compat. check against published ABI.
#%define with_kabichk   %{?_without_kabichk:   0} %{?!_without_kabichk:   1}
%define with_kabichk   0

# Additional options for user-friendly one-off kernel building:
#
# Only build the base kernel (--with baseonly):
%define with_baseonly  %{?_with_baseonly:     1} %{?!_with_baseonly:     0}
# Only build the smp kernel (--with smponly):
%define with_smponly   %{?_with_smponly:      1} %{?!_with_smponly:      0}
# Only build the xen kernel (--with xenonly):
%define with_xenonly   %{?_with_xenonly:      1} %{?!_with_xenonly:      0}

# Whether to apply the Xen patches -- leave this enabled.
%define includexen 0

# Set debugbuildsenabled to 1 for production (build separate debug kernels)
#  and 0 for rawhide (all kernels are debug kernels).
# See also 'make debug' and 'make release'.
%define debugbuildsenabled 1

# Versions of various parts

# After branching, please hardcode these values as the
# %dist and %rhel tags are not reliable yet
# For example dist -> .el5 and rhel -> 5
%define dist .el5
%define rhel 5

# Values used for RHEL version info in version.h
%define rh_release_major %{rhel}
%define rh_release_minor 3

#
# Polite request for people who spin their own kernel rpms:
# please modify the "buildid" define in a way that identifies
# that the kernel isn't the stock distribution kernel, for example,
# by setting the define to ".local" or ".bz123456"
#
%define buildid .wg
#
%define sublevel 25
%define kversion 2.6.%{sublevel}
%define rpmversion 2.6.%{sublevel}
%define release 129.1.6%{?dist}%{?buildid}
%define signmodules 0
%define xen_hv_cset 15502
%define xen_abi_ver 3.1
%define make_target bzImage
%define kernel_image x86
%define xen_flags verbose=y crash_debug=y XEN_VENDORVERSION=-%{PACKAGE_RELEASE}
%define xen_target vmlinuz
%define xen_image vmlinuz

%define KVERREL %{PACKAGE_VERSION}-%{PACKAGE_RELEASE}
%define hdrarch %_target_cpu

%if !%{debugbuildsenabled}
%define with_debug 0
%endif

%if !%{with_debuginfo}
%define _enable_debug_packages 0
%endif
%define debuginfodir /usr/lib/debug

# if requested, only build base kernel
%if %{with_baseonly}
%define with_smp 0
%define with_pae 0
%define with_xen 0
%define with_kdump 0
%define with_debug 0
%endif

# if requested, only build smp kernel
%if %{with_smponly}
%define with_up 0
%define with_pae 0
%define with_xen 0
%define with_kdump 0
%define with_debug 0
%endif

# if requested, only build xen kernel
%if %{with_xenonly}
%define with_up 0
%define with_smp 0
%define with_pae 0
%define with_kdump 0
%define with_debug 0
%endif

# groups of related archs
#OLPC stuff
%if 0%{?olpc}
%define with_xen 0
%endif
# Don't build 586 kernels for RHEL builds.
%if 0%{?rhel}
%define all_x86 i386 i686
# we differ here b/c of the reloc patches
%ifarch i686 x86_64
%define with_kdump 0
%endif
%else
%define all_x86 i386 i586 i686
%endif

# Overrides for generic default options

# Only ppc and sparc64 need separate smp kernels
%ifnarch ppc sparc64
%define with_smp 0
%endif

# pae is only valid on i686
%ifnarch i686
%define with_pae 0
%endif

# xen only builds on i686, x86_64 and ia64
%ifnarch i686 x86_64 ia64
%define with_xen 0
%endif

# only build kernel-kdump on i686, x86_64 and ppc64
%ifnarch i686 x86_64 ppc64 ppc64iseries s390x
%define with_kdump 0
%endif

# only package docs noarch
%ifnarch noarch
%define with_doc 0
%endif

# no need to build headers again for these arches,
# they can just use i386 and ppc64 headers
%ifarch i586 i686 ppc64iseries
%define with_headers 0
%endif

# obviously, don't build noarch kernels or headers
%ifarch noarch
%define with_up 0
%define with_headers 0
%define with_debug 0
%define all_arch_configs kernel-%{kversion}-*.config
%endif

# Per-arch tweaks

%ifarch %{all_x86}
%define all_arch_configs kernel-%{kversion}-i?86*.config
%define image_install_path boot
%define signmodules 0
%define hdrarch i386
%endif

%ifarch i686
# we build always xen i686 HV with pae
%define xen_flags verbose=y crash_debug=y pae=y XEN_VENDORVERSION=-%{PACKAGE_RELEASE}
%endif

%ifarch x86_64
%define all_arch_configs kernel-%{kversion}-x86_64*.config
%define image_install_path boot
%define signmodules 0
%define xen_flags verbose=y crash_debug=y max_phys_cpus=128 XEN_VENDORVERSION=-%{PACKAGE_RELEASE}
%endif

%ifarch ppc64 ppc64iseries
%define all_arch_configs kernel-%{kversion}-ppc64*.config
%define image_install_path boot
%define signmodules 0
%define make_target vmlinux
%define kernel_image vmlinux
%define kernel_image_elf 1
%define hdrarch powerpc
%endif

%ifarch s390
%define all_arch_configs kernel-%{kversion}-s390*.config
%define image_install_path boot
%define make_target image
%define kernel_image arch/s390/boot/image
%endif

%ifarch s390x
%define all_arch_configs kernel-%{kversion}-s390x*.config
%define image_install_path boot
%define make_target image
%define kernel_image arch/s390/boot/image
%define hdrarch s390
%endif

%ifarch sparc
%define all_arch_configs kernel-%{kversion}-sparc.config
%define make_target image
%define kernel_image image
%endif

%ifarch sparc64
%define all_arch_configs kernel-%{kversion}-sparc64*.config
%define make_target image
%define kernel_image image
%endif

%ifarch ppc
%define all_arch_configs kernel-%{kversion}-ppc{-,.}*config
%define image_install_path boot
%define make_target vmlinux
%define kernel_image vmlinux
%define kernel_image_elf 1
%define hdrarch powerpc
%endif

%ifarch ia64
%define all_arch_configs kernel-%{kversion}-ia64*.config
%define image_install_path boot/efi/EFI/redhat
%define signmodules 0
%define make_target compressed
%define kernel_image vmlinux.gz
# ia64 xen HV doesn't build with debug=y at the moment
%define xen_flags verbose=y crash_debug=y XEN_VENDORVERSION=-%{PACKAGE_RELEASE}
%define xen_target compressed
%define xen_image vmlinux.gz
%endif

# To temporarily exclude an architecture from being built, add it to
# %nobuildarches. Do _NOT_ use the ExclusiveArch: line, because if we
# don't build kernel-headers then the new build system will no longer let
# us use the previous build of that package -- it'll just be completely AWOL.
# Which is a BadThing(tm).

# We don't build a kernel on i386 or s390x or ppc -- we only do kernel-headers there.
%define nobuildarches i386 s390 s390x ppc ppc64 ppc64iseries ia64 sparc sparc64

%ifarch %nobuildarches
%define with_up 0
%define with_smp 0
%define with_pae 0
%define with_xen 0
%define with_kdump 0
%define with_debug 0
%define with_debuginfo 0
%define _enable_debug_packages 0
%endif

#
# Three sets of minimum package version requirements in the form of Conflicts:
# to versions below the minimum
#

#
# First the general kernel 2.6 required versions as per
# Documentation/Changes
#
%define kernel_dot_org_conflicts  ppp < 2.4.3-3, isdn4k-utils < 3.2-32, nfs-utils < 1.0.7-12, e2fsprogs < 1.37-4, util-linux < 2.12, jfsutils < 1.1.7-2, reiserfs-utils < 3.6.19-2, xfsprogs < 2.6.13-4, procps < 3.2.5-6.3, oprofile < 0.9.1-2

#
# Then a series of requirements that are distribution specific, either
# because we add patches for something, or the older versions have
# problems with the newer kernel or lack certain things that make
# integration in the distro harder than needed.
#
%define package_conflicts initscripts < 7.23, udev < 063-6, iptables < 1.3.2-1, ipw2200-firmware < 2.4, selinux-policy-targeted < 1.25.3-14, ecryptfs-utils < 44, cpuspeed < 1.2.1-5

#
# The ld.so.conf.d file we install uses syntax older ldconfig's don't grok.
#
%define xen_conflicts glibc < 2.3.5-1, xen < 3.0.1

#
# Packages that need to be installed before the kernel is, because the %post
# scripts use them.
#
%define kernel_prereq  fileutils, module-init-tools, initscripts >= 8.11.1-1, mkinitrd >= 4.2.21-1

Name: kernel
Group: System Environment/Kernel
License: GPLv2
URL: http://www.kernel.org/
Version: %{rpmversion}
Release: %{release}
%if 0%{?olpc}
ExclusiveArch: i386 i586
%else
# DO NOT CHANGE THIS LINE TO TEMPORARILY EXCLUDE AN ARCHITECTURE BUILD.
# SET %nobuildarches (ABOVE) INSTEAD
ExclusiveArch: noarch %{all_x86} x86_64 ppc ppc64 ia64 sparc sparc64 s390 s390x
%endif
ExclusiveOS: Linux
Provides: kernel = %{version}
Provides: kernel-drm = 4.3.0
Provides: kernel-%{_target_cpu} = %{rpmversion}-%{release}
Prereq: %{kernel_prereq}
Conflicts: %{kernel_dot_org_conflicts}
Conflicts: %{package_conflicts}
# We can't let RPM do the dependencies automatic because it'll then pick up
# a correct but undesirable perl dependency from the module headers which
# isn't required for the kernel proper to function
AutoReq: no
AutoProv: yes


#
# List the packages used during the kernel build
#
BuildPreReq: module-init-tools, patch >= 2.5.4, bash >= 2.03, sh-utils, tar
BuildPreReq: bzip2, findutils, gzip, m4, perl, make >= 3.78, diffutils
%if %{signmodules}
BuildPreReq: gnupg
%endif
BuildRequires: gcc >= 3.4.2, binutils >= 2.12, redhat-rpm-config
%if %{with_headers}
BuildRequires: unifdef
%endif
BuildConflicts: rhbuildsys(DiskFree) < 500Mb


Source0: ftp://ftp.kernel.org/pub/linux/kernel/v2.6/linux-%{kversion}.tar.bz2
#Source1: xen-%{xen_hv_cset}.tar.bz2
Source2: Config.mk

Source10: COPYING.modules
Source11: genkey
Source12: kabitool
Source14: find-provides
Source15: merge.pl

Source20: kernel-%{kversion}-i586.config
Source21: kernel-%{kversion}-i686.config
Source22: kernel-%{kversion}-i686-debug.config
Source23: kernel-%{kversion}-i686-PAE.config

Source24: kernel-%{kversion}-x86_64.config
Source25: kernel-%{kversion}-x86_64-debug.config
#Source26: kernel-%{kversion}-x86_64-kdump.config

#Source27: kernel-%{kversion}-ppc.config
#Source28: kernel-%{kversion}-ppc-smp.config
#Source29: kernel-%{kversion}-ppc64.config
#Source30: kernel-%{kversion}-ppc64-debug.config
#Source31: kernel-%{kversion}-ppc64-kdump.config
#Source31: kernel-%{kversion}-ppc64iseries.config

#Source32: kernel-%{kversion}-s390.config
#Source33: kernel-%{kversion}-s390x.config
#Source34: kernel-%{kversion}-s390x-debug.config
#Source35: kernel-%{kversion}-s390x-kdump.config

#Source36: kernel-%{kversion}-ia64.config
#Source37: kernel-%{kversion}-ia64-debug.config

Source38: kernel-%{kversion}-i686-xen.config
Source39: kernel-%{kversion}-x86_64-xen.config
#Source40: kernel-%{kversion}-i686-kdump.config
#Source41: kernel-%{kversion}-ia64-xen.config
#Source42: kernel-%{kversion}-ppc64iseries-kdump.config

#Source66: kernel-%{kversion}-sparc.config
#Source67: kernel-%{kversion}-sparc64.config
#Source68: kernel-%{kversion}-sparc64-smp.config

Source80: config-rhel-generic
#Source82: config-rhel-ppc64-generic
Source83: config-olpc-generic

Source100: kabi_whitelist_i686
Source101: kabi_whitelist_i686PAE
Source102: kabi_whitelist_i686xen
#Source103: kabi_whitelist_ia64
#Source104: kabi_whitelist_ia64xen
#Source105: kabi_whitelist_ppc64
#Source106: kabi_whitelist_ppc64kdump
#Source107: kabi_whitelist_ppc64iseries
#Source108: kabi_whitelist_ppc64iserieskdump
#Source109: kabi_whitelist_s390x
Source110: kabi_whitelist_x86_64
Source111: kabi_whitelist_x86_64xen

Source120: Module.kabi_i686
Source121: Module.kabi_i686PAE
Source122: Module.kabi_i686xen
#Source123: Module.kabi_ia64
#Source124: Module.kabi_ia64xen
#Source125: Module.kabi_ppc64
#Source126: Module.kabi_ppc64kdump
#Source127: Module.kabi_s390x
Source128: Module.kabi_x86_64
Source129: Module.kabi_x86_64xen

Source130: check-kabi

#
# Patches 0 through 100 are meant for core subsystem upgrades
#
Patch1: patch-2.6.25.20.bz2

#
# Patches 800 through 899 are reserved for bugfixes to the core system
# and patches related to how RPMs are build
#
Patch800: linux-2.6-build-nonintconfig.patch
#Patch801: linux-2.6-build-userspace-headers-warning.patch
#Patch802: linux-2.6-build-deprecate-configh-include.patch

# Exec-shield.
#Patch810: linux-2.6-execshield.patch
#Patch811: linux-2.6-warn-c-p-a.patch

# Module signing infrastructure.
#Patch900: linux-2.6-modsign-core.patch
#Patch901: linux-2.6-modsign-crypto.patch
#Patch902: linux-2.6-modsign-ksign.patch
#Patch903: linux-2.6-modsign-mpilib.patch
#Patch904: linux-2.6-modsign-script.patch
#Patch905: linux-2.6-modsign-include.patch


# adds rhel version info to version.h
Patch99990: linux-2.6-rhel-version-h.patch
# empty final patch file to facilitate testing of kernel patches
Patch99999: linux-kernel-test.patch

# END OF PATCH DEFINITIONS




BuildRoot: %{_tmppath}/kernel-%{KVERREL}-root

# Override find_provides to use a script that provides "kernel(symbol) = hash".
# Pass path of the RPM temp dir containing kabideps to find-provides script.
%global _use_internal_dependency_generator 0
%define __find_provides %_sourcedir/find-provides %{_tmppath}
%define __find_requires /usr/lib/rpm/redhat/find-requires kernel

%ifarch x86_64
Obsoletes: kernel-smp
%endif
Obsoletes: kernel-modules-rhel5-0
Obsoletes: kernel-modules-rhel5-1
Obsoletes: kernel-modules-rhel5-2

%description
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

%package devel
Summary: Development package for building kernel modules to match the kernel.
Group: System Environment/Kernel
AutoReqProv: no
Provides: kernel-devel-%{_target_cpu} = %{rpmversion}-%{release}
Prereq: /usr/bin/find

%description devel
This package provides kernel headers and makefiles sufficient to build modules
against the kernel package.


%package doc
Summary: Various documentation bits found in the kernel source.
Group: Documentation

%description doc
This package contains documentation files from the kernel
source. Various bits of information about the Linux kernel and the
device drivers shipped with it are documented in these files.

You'll want to install this package if you need a reference to the
options that can be passed to Linux kernel modules at load time.

%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Obsoletes: glibc-kernheaders
Provides: glibc-kernheaders = 3.0-46

%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package PAE
Summary: The Linux kernel compiled for PAE capable machines.

Group: System Environment/Kernel
Provides: kernel = %{version}
Provides: kernel-drm = 4.3.0
Provides: kernel-%{_target_cpu} = %{rpmversion}-%{release}PAE
Prereq: %{kernel_prereq}
Conflicts: %{kernel_dot_org_conflicts}
Conflicts: %{package_conflicts}
Obsoletes: kernel-smp < 2.6.17
Obsoletes: kernel-modules-rhel5-0
Obsoletes: kernel-modules-rhel5-1
Obsoletes: kernel-modules-rhel5-2
# We can't let RPM do the dependencies automatic because it'll then pick up
# a correct but undesirable perl dependency from the module headers which
# isn't required for the kernel proper to function
AutoReq: no
AutoProv: yes

%description PAE
This package includes a version of the Linux kernel with support for up to
16GB of high memory. It requires a CPU with Physical Address Extensions (PAE).
The non-PAE kernel can only address up to 4GB of memory.
Install the kernel-PAE package if your machine has more than 4GB of memory.

%package PAE-devel
Summary: Development package for building kernel modules to match the PAE kernel.
Group: System Environment/Kernel
Provides: kernel-PAE-devel-%{_target_cpu} = %{rpmversion}-%{release}
Provides: kernel-devel-%{_target_cpu} = %{rpmversion}-%{release}PAE
Provides: kernel-devel = %{rpmversion}-%{release}PAE
AutoReqProv: no
Prereq: /usr/bin/find

%description PAE-devel
This package provides kernel headers and makefiles sufficient to build modules
against the PAE kernel package.

%package smp
Summary: The Linux kernel compiled for SMP machines.

Group: System Environment/Kernel
Provides: kernel = %{version}
Provides: kernel-drm = 4.3.0
Provides: kernel-%{_target_cpu} = %{rpmversion}-%{release}smp
Prereq: %{kernel_prereq}
Conflicts: %{kernel_dot_org_conflicts}
Conflicts: %{package_conflicts}
# upto and including kernel 2.4.9 rpms, the 4Gb+ kernel was called kernel-enterprise
# now that the smp kernel offers this capability, obsolete the old kernel
Obsoletes: kernel-enterprise < 2.4.10
Obsoletes: kernel-modules-rhel5-0
Obsoletes: kernel-modules-rhel5-1
Obsoletes: kernel-modules-rhel5-2
# We can't let RPM do the dependencies automatic because it'll then pick up
# a correct but undesirable perl dependency from the module headers which
# isn't required for the kernel proper to function
AutoReq: no
AutoProv: yes

%description smp
This package includes a SMP version of the Linux kernel. It is
required only on machines with two or more CPUs as well as machines with
hyperthreading technology.

Install the kernel-smp package if your machine uses two or more CPUs.

%package smp-devel
Summary: Development package for building kernel modules to match the SMP kernel.
Group: System Environment/Kernel
Provides: kernel-smp-devel-%{_target_cpu} = %{rpmversion}-%{release}
Provides: kernel-devel-%{_target_cpu} = %{rpmversion}-%{release}smp
Provides: kernel-devel = %{rpmversion}-%{release}smp
AutoReqProv: no
Prereq: /usr/bin/find

%description smp-devel
This package provides kernel headers and makefiles sufficient to build modules
against the SMP kernel package.

%package debug
Summary: The Linux kernel compiled with extra debugging enabled.
Group: System Environment/Kernel
Provides: kernel = %{version}
Provides: kernel-drm = 4.3.0
Provides: kernel-%{_target_cpu} = %{rpmversion}-%{release}-debug
Prereq: %{kernel_prereq}
Conflicts: %{kernel_dot_org_conflicts}
Conflicts: %{package_conflicts}
AutoReq: no
AutoProv: yes
%description debug
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.

%package debug-debuginfo
Summary: Debug information for package %{name}-debug
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{KVERREL}
Provides: %{name}-debug-debuginfo-%{_target_cpu} = %{KVERREL}
%description debug-debuginfo
This package provides debug information for package %{name}-debug

%package debug-devel
Summary: Development package for building kernel modules to match the kernel.
Group: System Environment/Kernel
AutoReqProv: no
Prereq: /usr/bin/find
%description debug-devel
This package provides kernel headers and makefiles sufficient to build modules
against the kernel package.

%package xen
Summary: The Linux kernel compiled for Xen VM operations

Group: System Environment/Kernel
Provides: kernel = %{version}
Provides: kernel-%{_target_cpu} = %{rpmversion}-%{release}xen
Provides: xen-hypervisor-abi = %{xen_abi_ver}
Prereq: %{kernel_prereq}
Conflicts: %{kernel_dot_org_conflicts}
Conflicts: %{package_conflicts}
Conflicts: %{xen_conflicts}
Obsoletes: kernel-modules-rhel5-0
Obsoletes: kernel-modules-rhel5-1
Obsoletes: kernel-modules-rhel5-2
# We can't let RPM do the dependencies automatic because it'll then pick up
# a correct but undesirable perl dependency from the module headers which
# isn't required for the kernel proper to function
AutoReq: no
AutoProv: yes

%description xen
This package includes a Xen hypervisor and a version of the Linux kernel which
can run Xen VMs for privileged hosts and unprivileged paravirtualized hosts.

%package xen-devel
Summary: Development package for building kernel modules to match the kernel.
Group: System Environment/Kernel
AutoReqProv: no
Provides: kernel-xen-devel-%{_target_cpu} = %{rpmversion}-%{release}
Provides: kernel-devel-%{_target_cpu} = %{rpmversion}-%{release}xen
Provides: kernel-devel = %{rpmversion}-%{release}xen
Prereq: /usr/bin/find

%description xen-devel
This package provides kernel headers and makefiles sufficient to build modules
against the kernel package.

%package kdump
Summary: A minimal Linux kernel compiled for kernel crash dumps.

Group: System Environment/Kernel
Provides: kernel = %{version}
Provides: kernel-drm = 4.3.0
Provides: kernel-%{_target_cpu} = %{rpmversion}-%{release}kdump
Prereq: %{kernel_prereq}
Conflicts: %{kernel_dot_org_conflicts}
Conflicts: %{package_conflicts}
Obsoletes: kernel-modules-rhel5-0
Obsoletes: kernel-modules-rhel5-1
Obsoletes: kernel-modules-rhel5-2
# We can't let RPM do the dependencies automatic because it'll then pick up
# a correct but undesirable perl dependency from the module headers which
# isn't required for the kernel proper to function
AutoReq: no
AutoProv: yes

%description kdump
This package includes a kdump version of the Linux kernel. It is
required only on machines which will use the kexec-based kernel crash dump
mechanism.

%package kdump-devel
Summary: Development package for building kernel modules to match the kdump kernel.
Group: System Environment/Kernel
Provides: kernel-kdump-devel-%{_target_cpu} = %{rpmversion}-%{release}
Provides: kernel-devel-%{_target_cpu} = %{rpmversion}-%{release}kdump
Provides: kernel-devel = %{rpmversion}-%{release}kdump
AutoReqProv: no
Prereq: /usr/bin/find

%description kdump-devel
This package provides kernel headers and makefiles sufficient to build modules
against the kdump kernel package.


%prep
# do a few sanity-checks for --with *only builds
%if %{with_baseonly}
%if !%{with_up}
echo "Cannot build --with baseonly, up build is disabled"
exit 1
%endif
%endif

%if %{with_smponly}
%if !%{with_smp}
echo "Cannot build --with smponly, smp build is disabled"
exit 1
%endif
%endif

%if %{with_xenonly}
%if !%{with_xen}
echo "Cannot build --with xenonly, xen build is disabled"
exit 1
%endif
%endif

# First we unpack the kernel tarball.
# If this isn't the first make prep, we use links to the existing clean tarball
# which speeds things up quite a bit.
if [ ! -d kernel-%{kversion}/vanilla ]; then
  # Ok, first time we do a make prep.
  rm -f pax_global_header
%setup -q -n %{name}-%{version} -c
  mv linux-%{kversion} vanilla
else
  # We already have a vanilla dir.
  cd kernel-%{kversion}
  if [ -d linux-%{kversion}.%{_target_cpu} ]; then
     # Just in case we ctrl-c'd a prep already
     rm -rf deleteme
     # Move away the stale away, and delete in background.
     mv linux-%{kversion}.%{_target_cpu} deleteme
     rm -rf deleteme &
  fi
fi
cp -rl vanilla linux-%{kversion}.%{_target_cpu}

cd linux-%{kversion}.%{_target_cpu}

# Update to latest upstream.
%patch1 -p1


# This patch adds a "make nonint_oldconfig" which is non-interactive and
# also gives a list of missing options at the end. Useful for automated
# builds (as used in the buildsystem).
%patch800 -p1

# Warn if someone tries to build userspace using kernel headers
#%patch801 -p1
# Warn if someone #include's <linux/config.h>
#%patch802 -p1

# Exec shield
#%patch810 -p1
# #%patch811 -p1

#
# GPG signed kernel modules
#
#%patch900 -p1
#%patch901 -p1
#%patch902 -p1
#%patch903 -p1
#%patch904 -p1
#%patch905 -p1


# correction of SUBLEVEL/EXTRAVERSION in top-level source tree Makefile
# patch the Makefile to include rhel version info
%patch99990 -p1
perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{sublevel}/" Makefile
perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -prep/" Makefile
perl -p -i -e "s/^RHEL_MAJOR.*/RHEL_MAJOR = %{rh_release_major}/" Makefile
perl -p -i -e "s/^RHEL_MINOR.*/RHEL_MINOR = %{rh_release_minor}/" Makefile

# conditionally applied test patch for debugging convenience
%if %([ -s %{PATCH99999} ] && echo 1 || echo 0)
%patch99999 -p1
%endif

# END OF PATCH APPLICATIONS



cp %{SOURCE10} Documentation/

mkdir configs

for cfg in %{all_arch_configs}; do
  cp -f $RPM_SOURCE_DIR/$cfg .
done

#if a rhel kernel, apply the rhel config options
#%if 0%{?rhel}
#  for i in %{all_arch_configs}
#  do
#    mv $i $i.tmp
#    $RPM_SOURCE_DIR/merge.pl $RPM_SOURCE_DIR/config-rhel-generic $i.tmp > $i
#    rm $i.tmp
#  done
#%ifarch ppc64 noarch
#  #CONFIG_FB_MATROX is disabled for rhel generic but needed for ppc64 rhel
#  for i in kernel-%{kversion}-ppc64.config
#  do
#    mv $i $i.tmp
#    $RPM_SOURCE_DIR/merge.pl $RPM_SOURCE_DIR/config-rhel-ppc64-generic $i.tmp > $i
#    rm $i.tmp
#  done
#%endif
#%endif
#if a olpc kernel, apply the olpc config options
%if 0%{?olpc}
  for i in %{all_arch_configs}
  do
    mv $i $i.tmp
    $RPM_SOURCE_DIR/merge.pl $RPM_SOURCE_DIR/config-olpc-generic $i.tmp > $i
    rm $i.tmp
  done
%endif


%if 0%{?rhel}
# don't need these for relocatable kernels
rm -f kernel-%{kversion}-{i686,x86_64}-kdump.config
# don't need these in general
rm -f kernel-%{kversion}-i586.config
%endif

%if 0%{?olpc}
# don't need these for OLPC
rm -f kernel-%{kversion}-*PAE*.config
rm -f kernel-%{kversion}-*xen*.config
rm -f kernel-%{kversion}-*kdump*.config
%endif

%if !%{with_debug}
rm -f kernel-%{kversion}-*-debug.config
%endif

# now run oldconfig over all the config files
for i in *.config
do
  mv $i .config
  Arch=`head -1 .config | cut -b 3-`
  make ARCH=$Arch nonint_oldconfig > /dev/null
  echo "# $Arch" > configs/$i
  cat .config >> configs/$i
done

# If we don't have many patches to apply, sometimes the deleteme
# trick still hasn't completed, and things go bang at this point
# when find traverses into directories that get deleted.
# So we serialise until the dir has gone away.
cd ..
while [ -d deleteme ];
do
	sleep 1
done

# get rid of unwanted files resulting from patch fuzz
find . \( -name "*.orig" -o -name "*~" \) -exec rm -f {} \; >/dev/null


# Unpack the Xen tarball.
%if %{includexen}
cp %{SOURCE2} .
if [ -d xen ]; then
  rm -rf xen
fi
%setup -D -T -q -n %{name}-%{version} -a1
cd xen
%endif


###
### build
###
%build
#
# Create gpg keys for signing the modules
#

%if %{signmodules}
gpg --homedir . --batch --gen-key %{SOURCE11}
gpg --homedir . --export --keyring ./kernel.pub CentOS > extract.pub
make linux-%{kversion}.%{_target_cpu}/scripts/bin2c
linux-%{kversion}.%{_target_cpu}/scripts/bin2c ksign_def_public_key __initdata < extract.pub > linux-%{kversion}.%{_target_cpu}/crypto/signature/key.h
%endif

BuildKernel() {
    MakeTarget=$1
    KernelImage=$2
    Flavour=$3

    # Pick the right config file for the kernel we're building
    if [ -n "$Flavour" ] ; then
      Config=kernel-%{kversion}-%{_target_cpu}-$Flavour.config
      DevelDir=/usr/src/kernels/%{KVERREL}-$Flavour-%{_target_cpu}
      DevelLink=/usr/src/kernels/%{KVERREL}$Flavour-%{_target_cpu}
    else
      Config=kernel-%{kversion}-%{_target_cpu}.config
      DevelDir=/usr/src/kernels/%{KVERREL}-%{_target_cpu}
      DevelLink=
    fi

    KernelVer=%{version}-%{release}$Flavour
    echo BUILDING A KERNEL FOR $Flavour %{_target_cpu}...

    # make sure EXTRAVERSION says what we want it to say
    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}$Flavour/" Makefile

    # and now to start the build process

    make -s mrproper
    cp configs/$Config .config

    Arch=`head -1 .config | cut -b 3-`
    echo USING ARCH=$Arch

    if [ "$KernelImage" == "x86" ]; then
       KernelImage=arch/$Arch/boot/bzImage
    fi
    if [ "$Arch" == "s390" -a "$Flavour" == "kdump" ]; then
      pushd arch/s390/boot
      gcc -static -o zfcpdump zfcpdump.c
      popd
    fi

    make -s ARCH=$Arch nonint_oldconfig > /dev/null
    make -s ARCH=$Arch %{?_smp_mflags} $MakeTarget
    if [ "$Arch" != "s390" -o "$Flavour" != "kdump" ]; then
      make -s ARCH=$Arch %{?_smp_mflags} modules || exit 1
    fi

    # Start installing the results

%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/boot
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/%{image_install_path}
%endif
    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}
    install -m 644 .config $RPM_BUILD_ROOT/boot/config-$KernelVer
    install -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-$KernelVer
    touch $RPM_BUILD_ROOT/boot/initrd-$KernelVer.img
    cp $KernelImage $RPM_BUILD_ROOT/%{image_install_path}/vmlinuz-$KernelVer
    if [ -f arch/$Arch/boot/zImage.stub ]; then
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/%{image_install_path}/zImage.stub-$KernelVer || :
    fi

    if [ "$Flavour" == "kdump" -a "$Arch" != "s390" ]; then
        cp vmlinux $RPM_BUILD_ROOT/%{image_install_path}/vmlinux-$KernelVer
        rm -f $RPM_BUILD_ROOT/%{image_install_path}/vmlinuz-$KernelVer
    fi

    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer
    if [ "$Arch" != "s390" -o "$Flavour" != "kdump" ]; then
      make -s ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install KERNELRELEASE=$KernelVer
    else
      touch Module.symvers
    fi

    # Create the kABI metadata for use in packaging
    echo "**** GENERATING kernel ABI metadata ****"
    gzip -c9 < Module.symvers > $RPM_BUILD_ROOT/boot/symvers-$KernelVer.gz
%if %{with_kabichk}
    chmod 0755 %_sourcedir/kabitool
    if [ ! -e $RPM_SOURCE_DIR/kabi_whitelist_%{_target_cpu}$Flavour ]; then
        echo "**** No KABI whitelist was available during build ****"
        %_sourcedir/kabitool -b $RPM_BUILD_ROOT/$DevelDir -k $KernelVer -l $RPM_BUILD_ROOT/kabi_whitelist
    else
	cp $RPM_SOURCE_DIR/kabi_whitelist_%{_target_cpu}$Flavour $RPM_BUILD_ROOT/kabi_whitelist
    fi
    rm -f %{_tmppath}/kernel-$KernelVer-kabideps
    %_sourcedir/kabitool -b . -d %{_tmppath}/kernel-$KernelVer-kabideps -k $KernelVer -w $RPM_BUILD_ROOT/kabi_whitelist
    echo "**** kABI checking is enabled in kernel SPEC file. ****"
    chmod 0755 $RPM_SOURCE_DIR/check-kabi
    if [ -e $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Flavour ]; then
	cp $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Flavour $RPM_BUILD_ROOT/Module.kabi
	$RPM_SOURCE_DIR/check-kabi -k $RPM_BUILD_ROOT/Module.kabi -s Module.symvers || exit 1
    else
	echo "**** NOTE: Cannot find reference Module.kabi file. ****"
    fi
%endif
    touch %{_tmppath}/kernel-$KernelVer-kabideps

    # And save the headers/makefiles etc for building modules against
    #
    # This all looks scary, but the end result is supposed to be:
    # * all arch relevant include/ files
    # * all Makefile/Kconfig files
    # * all script/ files

    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/source
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    (cd $RPM_BUILD_ROOT/lib/modules/$KernelVer ; ln -s build source)
    # dirs for additional modules per module-init-tools, kbuild/modules.txt
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/extra
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/updates
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/weak-updates

    # first copy everything
    cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp Module.symvers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp Module.markers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
%if %{with_kabichk}
    mv $RPM_BUILD_ROOT/kabi_whitelist $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -e $RPM_BUILD_ROOT/Module.kabi ]; then
	mv $RPM_BUILD_ROOT/Module.kabi $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi
    cp symsets-$KernelVer.tar.gz $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
%endif
    # then drop all but the needed Makefiles/Kconfig files
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Documentation
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    cp .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -d arch/%{_arch}/scripts ]; then
      cp -a arch/%{_arch}/scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch} || :
    fi
    if [ -f arch/%{_arch}/*lds ]; then
      cp -a arch/%{_arch}/*lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch}/ || :
    fi
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*.o
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*/*.o
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    cd include
    cp -a acpi config keys linux math-emu media mtd net pcmcia rdma rxrpc scsi sound video asm asm-generic $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    cp -a `readlink asm` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include

    # not needed in 25 kernel
    #if [ "$Arch" = "x86_64" ]; then
    #  cp -a asm-i386 $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    #fi

    # While arch/powerpc/include/asm is still a symlink to the old
    # include/asm-ppc{64,} directory, include that in kernel-devel too.
    if [ "$Arch" = "powerpc" -a -r ../arch/powerpc/include/asm ]; then
      cp -a `readlink ../arch/powerpc/include/asm` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
      mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/$Arch/include
      pushd $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/$Arch/include
      ln -sf ../../../include/asm-ppc* asm
      popd
    fi
%if %{includexen}
    cp -a xen $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
%endif

    # Make sure the Makefile and version.h have a matching timestamp so that
    # external modules can be built
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/linux/version.h
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/.config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/linux/autoconf.h
    # Copy .config to include/config/auto.conf so "make prepare" is unnecessary.
    cp $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/.config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/config/auto.conf
    cd ..

    #
    # save the vmlinux file for kernel debugging into the kernel-debuginfo rpm
    #
%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    cp vmlinux $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
%endif

    find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name "*.ko" -type f >modnames

    # gpg sign the modules
%if %{signmodules}
    gcc -o scripts/modsign/mod-extract scripts/modsign/mod-extract.c -Wall
    KEYFLAGS="--no-default-keyring --homedir .."
    KEYFLAGS="$KEYFLAGS --secret-keyring ../kernel.sec"
    KEYFLAGS="$KEYFLAGS --keyring ../kernel.pub"
    export KEYFLAGS

    for i in `cat modnames`
    do
      sh ./scripts/modsign/modsign.sh $i CentOS
      mv -f $i.signed $i
    done
    unset KEYFLAGS
%endif

    # mark modules executable so that strip-to-file can strip them
    for i in `cat modnames`
    do
      chmod u+x $i
    done

    # detect missing or incorrect license tags
    for i in `cat modnames`
    do
      echo -n "$i "
      /sbin/modinfo -l $i >> modinfo
    done
    cat modinfo |\
      grep -v "^GPL" |
      grep -v "^Dual BSD/GPL" |\
      grep -v "^Dual MPL/GPL" |\
      grep -v "^GPL and additional rights" |\
      grep -v "^GPL v2" && exit 1
    rm -f modinfo
    rm -f modnames
    # remove files that will be auto generated by depmod at rpm -i time
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.*

    # Move the devel headers out of the root file system
    mkdir -p $RPM_BUILD_ROOT/usr/src/kernels
    mv $RPM_BUILD_ROOT/lib/modules/$KernelVer/build $RPM_BUILD_ROOT/$DevelDir
    ln -sf ../../..$DevelDir $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    [ -z "$DevelLink" ] || ln -sf `basename $DevelDir` $RPM_BUILD_ROOT/$DevelLink

	# Temporary fix for upstream "make prepare" bug.
#	pushd $RPM_BUILD_ROOT/$DevelDir > /dev/null
#	if [ -f Makefile ]; then
#		make prepare
#	fi
#	popd > /dev/null
}

###
# DO it...
###

# prepare directories
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/boot

%if %{includexen}
%if %{with_xen}
  cd xen
  mkdir -p $RPM_BUILD_ROOT/%{image_install_path} $RPM_BUILD_ROOT/boot
  make %{?_smp_mflags} %{xen_flags}
  install -m 644 xen.gz $RPM_BUILD_ROOT/%{image_install_path}/xen.gz-%{KVERREL}
  install -m 755 xen-syms $RPM_BUILD_ROOT/boot/xen-syms-%{KVERREL}
  cd ..
%endif
%endif

cd linux-%{kversion}.%{_target_cpu}

%if %{with_up}
BuildKernel %make_target %kernel_image
%endif

%if %{with_pae}
BuildKernel %make_target %kernel_image PAE
%endif

%if %{with_smp}
BuildKernel %make_target %kernel_image smp
%endif

%if %{includexen}
%if %{with_xen}
BuildKernel %xen_target %xen_image xen
%endif
%endif

%if %{with_kdump}
BuildKernel %make_target %kernel_image kdump
%endif

%if %{with_debug}
BuildKernel %make_target %kernel_image debug
%endif

###
### Special hacks for debuginfo subpackages.
###

# This macro is used by %%install, so we must redefine it before that.
%define debug_package %{nil}

%if %{with_debuginfo}
%ifnarch noarch
%global __debug_package 1
%package debuginfo-common
Summary: Kernel source files used by %{name}-debuginfo packages
Group: Development/Debug
Provides: %{name}-debuginfo-common-%{_target_cpu} = %{KVERREL}

%description debuginfo-common
This package is required by %{name}-debuginfo subpackages.
It provides the kernel source files common to all builds.

%files debuginfo-common
%defattr(-,root,root)
/usr/src/debug/%{name}-%{version}/linux-%{kversion}.%{_target_cpu}
%if %{includexen}
%if %{with_xen}
/usr/src/debug/%{name}-%{version}/xen
%endif
%endif
%dir /usr/src/debug
%dir %{debuginfodir}
%dir %{debuginfodir}/%{image_install_path}
%dir %{debuginfodir}/lib
%dir %{debuginfodir}/lib/modules
%dir %{debuginfodir}/usr/src/kernels
%endif
%endif

###
### install
###

%install

cd linux-%{kversion}.%{_target_cpu}
%ifnarch %nobuildarches noarch
mkdir -p $RPM_BUILD_ROOT/etc/modprobe.d
cat > $RPM_BUILD_ROOT/etc/modprobe.d/blacklist-firewire << \EOF
# Comment out the next line to enable the firewire drivers
blacklist firewire-ohci
EOF
%endif

%if %{includexen}
%if %{with_xen}
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
rm -f $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernelcap-%{KVERREL}.conf
cat > $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernelcap-%{KVERREL}.conf <<\EOF
# This directive teaches ldconfig to search in nosegneg subdirectories
# and cache the DSOs there with extra bit 0 set in their hwcap match
# fields.  In Xen guest kernels, the vDSO tells the dynamic linker to
# search in nosegneg subdirectories and to match this extra hwcap bit
# in the ld.so.cache file.
hwcap 0 nosegneg
EOF
chmod 444 $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernelcap-%{KVERREL}.conf
%endif
%endif

%if %{with_doc}
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/kernel-doc-%{kversion}/Documentation

# sometimes non-world-readable files sneak into the kernel source tree
chmod -R a+r *
# copy the source over
tar cf - Documentation | tar xf - -C $RPM_BUILD_ROOT/usr/share/doc/kernel-doc-%{kversion}
%endif

%if %{with_headers}
# Install kernel headers
make ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

# Manually go through the 'headers_check' process for every file, but
# don't die if it fails
chmod +x scripts/hdrcheck.sh
echo -e '*****\n*****\nHEADER EXPORT WARNINGS:\n*****' > hdrwarnings.txt
for FILE in `find $RPM_BUILD_ROOT/usr/include` ; do
    scripts/hdrcheck.sh $RPM_BUILD_ROOT/usr/include $FILE /dev/null >> hdrwarnings.txt || :
done
echo -e '*****\n*****' >> hdrwarnings.txt
if grep -q exist hdrwarnings.txt; then
   sed s:^$RPM_BUILD_ROOT/usr/include/:: hdrwarnings.txt
   # Temporarily cause a build failure if header inconsistencies.
   exit 1
fi

# glibc provides scsi headers for itself, for now
rm -rf $RPM_BUILD_ROOT/usr/include/scsi
rm -f $RPM_BUILD_ROOT/usr/include/asm*/atomic.h
rm -f $RPM_BUILD_ROOT/usr/include/asm*/io.h
rm -f $RPM_BUILD_ROOT/usr/include/asm*/irq.h
%endif
###
### clean
###

%clean
rm -rf $RPM_BUILD_ROOT

###
### scripts
###

%post
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ]; then
  if [ -f /etc/sysconfig/kernel ]; then
    /bin/sed -i -e 's/^DEFAULTKERNEL=kernel-smp$/DEFAULTKERNEL=kernel/' /etc/sysconfig/kernel || exit $?
  fi
fi
/sbin/new-kernel-pkg --package kernel --mkinitrd --depmod --install %{KVERREL} || exit $?
if [ -x /sbin/weak-modules ]
then
    /sbin/weak-modules --add-kernel %{KVERREL} || exit $?
fi

%post devel
if [ -f /etc/sysconfig/kernel ]
then
    . /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ] ; then
  pushd /usr/src/kernels/%{KVERREL}-%{_target_cpu} > /dev/null
  /usr/bin/find . -type f | while read f; do hardlink -c /usr/src/kernels/*FC*/$f $f ; done
  popd > /dev/null
fi

%post smp
/sbin/new-kernel-pkg --package kernel-smp --mkinitrd --depmod --install %{KVERREL}smp || exit $?
if [ -x /sbin/weak-modules ]
then
    /sbin/weak-modules --add-kernel %{KVERREL}smp || exit $?
fi

%post smp-devel
if [ -f /etc/sysconfig/kernel ]
then
    . /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ] ; then
  pushd /usr/src/kernels/%{KVERREL}-smp-%{_target_cpu} > /dev/null
  /usr/bin/find . -type f | while read f; do hardlink -c /usr/src/kernels/*FC*/$f $f ; done
  popd > /dev/null
fi

%post PAE
if [ -f /etc/sysconfig/kernel ]; then
    /bin/sed -i -e 's/^DEFAULTKERNEL=kernel-smp$/DEFAULTKERNEL=kernel-PAE/' /etc/sysconfig/kernel
fi
/sbin/new-kernel-pkg --package kernel-PAE --mkinitrd --depmod --install %{KVERREL}PAE || exit $?
if [ -x /sbin/weak-modules ]
then
    /sbin/weak-modules --add-kernel %{KVERREL}PAE || exit $?
fi

%post PAE-devel
if [ -f /etc/sysconfig/kernel ]
then
    . /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ] ; then
  pushd /usr/src/kernels/%{KVERREL}-PAE-%{_target_cpu} > /dev/null
  /usr/bin/find . -type f | while read f; do hardlink -c /usr/src/kernels/*FC*/$f $f ; done
  popd > /dev/null
fi

%post debug
/sbin/new-kernel-pkg --package kernel-debug --mkinitrd --depmod --install %{KVERREL}debug || exit $?
if [ -x /sbin/weak-modules ]
then
    /sbin/weak-modules --add-kernel %{KVERREL}debug || exit $?
fi

%post debug-devel
if [ -f /etc/sysconfig/kernel ]
then
    . /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ] ; then
  pushd /usr/src/kernels/%{KVERREL}-debug-%{_target_cpu} > /dev/null
  /usr/bin/find . -type f | while read f; do hardlink -c /usr/src/kernels/*FC*/$f $f ; done
  popd > /dev/null
fi

%post xen
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ]; then
  if [ -f /etc/sysconfig/kernel ]; then
    /bin/sed -i -e 's/^DEFAULTKERNEL=kernel-xen[0U]/DEFAULTKERNEL=kernel-xen/' /etc/sysconfig/kernel || exit $?
  fi
fi
if [ -e /proc/xen/xsd_kva -o ! -d /proc/xen ]; then
	/sbin/new-kernel-pkg --package kernel-xen --mkinitrd --depmod --install --multiboot=/%{image_install_path}/xen.gz-%{KVERREL} %{KVERREL}xen || exit $?
else
	/sbin/new-kernel-pkg --package kernel-xen --mkinitrd --depmod --install %{KVERREL}xen || exit $?
fi
if [ -x /sbin/ldconfig ]
then
    /sbin/ldconfig -X || exit $?
fi
if [ -x /sbin/weak-modules ]
then
    /sbin/weak-modules --add-kernel %{KVERREL}xen || exit $?
fi

%post xen-devel
if [ -f /etc/sysconfig/kernel ]
then
    . /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ] ; then
  pushd /usr/src/kernels/%{KVERREL}-xen-%{_target_cpu} > /dev/null
  /usr/bin/find . -type f | while read f; do hardlink -c /usr/src/kernels/*FC*/$f $f ; done
  popd > /dev/null
fi

%post kdump
/sbin/new-kernel-pkg --package kernel-kdump --mkinitrd --depmod --install %{KVERREL}kdump || exit $?
if [ -x /sbin/weak-modules ]
then
    /sbin/weak-modules --add-kernel %{KVERREL}kdump || exit $?
fi

%post kdump-devel
if [ -f /etc/sysconfig/kernel ]
then
    . /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ] ; then
  pushd /usr/src/kernels/%{KVERREL}-kdump-%{_target_cpu} > /dev/null
  /usr/bin/find . -type f | while read f; do hardlink -c /usr/src/kernels/*FC*/$f $f ; done
  popd > /dev/null
fi

%preun
/sbin/new-kernel-pkg --rminitrd --rmmoddep --remove %{KVERREL} || exit $?
if [ -x /sbin/weak-modules ]
then
    /sbin/weak-modules --remove-kernel %{KVERREL} || exit $?
fi

%preun smp
/sbin/new-kernel-pkg --rminitrd --rmmoddep --remove %{KVERREL}smp || exit $?
if [ -x /sbin/weak-modules ]
then
    /sbin/weak-modules --remove-kernel %{KVERREL}smp || exit $?
fi

%preun PAE
/sbin/new-kernel-pkg --rminitrd --rmmoddep --remove %{KVERREL}PAE || exit $?
if [ -x /sbin/weak-modules ]
then
    /sbin/weak-modules --remove-kernel %{KVERREL}PAE || exit $?
fi

%preun kdump
/sbin/new-kernel-pkg --rminitrd --rmmoddep --remove %{KVERREL}kdump || exit $?
if [ -x /sbin/weak-modules ]
then
    /sbin/weak-modules --remove-kernel %{KVERREL}kdump || exit $?
fi

%preun debug
/sbin/new-kernel-pkg --rminitrd --rmmoddep --remove %{KVERREL}debug || exit $?
if [ -x /sbin/weak-modules ]
then
    /sbin/weak-modules --remove-kernel %{KVERREL}debug || exit $?
fi

%preun xen
/sbin/new-kernel-pkg --rminitrd --rmmoddep --remove %{KVERREL}xen || exit $?
if [ -x /sbin/weak-modules ]
then
    /sbin/weak-modules --remove-kernel %{KVERREL}xen || exit $?
fi

###
### file lists
###

# This is %{image_install_path} on an arch where that includes ELF files,
# or empty otherwise.
%define elf_image_install_path %{?kernel_image_elf:%{image_install_path}}

%if %{with_up}
%if %{with_debuginfo}
%ifnarch noarch
%package debuginfo
Summary: Debug information for package %{name}
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{KVERREL}
Provides: %{name}-debuginfo-%{_target_cpu} = %{KVERREL}
%description debuginfo
This package provides debug information for package %{name}
This is required to use SystemTap with %{name}-%{KVERREL}.
%files debuginfo
%defattr(-,root,root)
%if "%{elf_image_install_path}" != ""
%{debuginfodir}/%{elf_image_install_path}/*-%{KVERREL}.debug
%endif
%{debuginfodir}/lib/modules/%{KVERREL}
%{debuginfodir}/usr/src/kernels/%{KVERREL}-%{_target_cpu}
%endif
%endif

%files
%defattr(-,root,root)
/%{image_install_path}/vmlinuz-%{KVERREL}
/boot/System.map-%{KVERREL}
/boot/symvers-%{KVERREL}.gz
/boot/config-%{KVERREL}
%dir /lib/modules/%{KVERREL}
/lib/modules/%{KVERREL}/kernel
/lib/modules/%{KVERREL}/build
/lib/modules/%{KVERREL}/source
/lib/modules/%{KVERREL}/extra
/lib/modules/%{KVERREL}/updates
/lib/modules/%{KVERREL}/weak-updates
%ghost /boot/initrd-%{KVERREL}.img
%config(noreplace) /etc/modprobe.d/blacklist-firewire

%files devel
%defattr(-,root,root)
%verify(not mtime) /usr/src/kernels/%{KVERREL}-%{_target_cpu}
%endif

%if %{with_headers}
%files headers
%defattr(-,root,root)
/usr/include/*
%endif

%if %{with_pae}
%if %{with_debuginfo}
%ifnarch noarch
%package PAE-debuginfo
Summary: Debug information for package %{name}-PAE
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{KVERREL}
Provides: %{name}-%PAE-debuginfo-%{_target_cpu} = %{KVERREL}
%description PAE-debuginfo
This package provides debug information for package %{name}-PAE
This is required to use SystemTap with %{name}-PAE-%{KVERREL}.
%files PAE-debuginfo
%defattr(-,root,root)
%if "%{elf_image_install_path}" != ""
%{debuginfodir}/%{elf_image_install_path}/*-%{KVERREL}PAE.debug
%endif
%{debuginfodir}/lib/modules/%{KVERREL}PAE
%{debuginfodir}/usr/src/kernels/%{KVERREL}-PAE-%{_target_cpu}
%endif
%endif

%files PAE
%defattr(-,root,root)
/%{image_install_path}/vmlinuz-%{KVERREL}PAE
/boot/System.map-%{KVERREL}PAE
/boot/symvers-%{KVERREL}PAE.gz
/boot/config-%{KVERREL}PAE
%dir /lib/modules/%{KVERREL}PAE
/lib/modules/%{KVERREL}PAE/kernel
/lib/modules/%{KVERREL}PAE/build
/lib/modules/%{KVERREL}PAE/source
/lib/modules/%{KVERREL}PAE/extra
/lib/modules/%{KVERREL}PAE/updates
/lib/modules/%{KVERREL}PAE/weak-updates
%ghost /boot/initrd-%{KVERREL}PAE.img
%config(noreplace) /etc/modprobe.d/blacklist-firewire

%files PAE-devel
%defattr(-,root,root)
%verify(not mtime) /usr/src/kernels/%{KVERREL}-PAE-%{_target_cpu}
/usr/src/kernels/%{KVERREL}PAE-%{_target_cpu}
%endif

%if %{with_smp}
%if %{with_debuginfo}
%ifnarch noarch
%package smp-debuginfo
Summary: Debug information for package %{name}-smp
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{KVERREL}
Provides: %{name}-%smp-debuginfo-%{_target_cpu} = %{KVERREL}
%description smp-debuginfo
This package provides debug information for package %{name}-smp
This is required to use SystemTap with %{name}-smp-%{KVERREL}.
%files smp-debuginfo
%defattr(-,root,root)
%if "%{elf_image_install_path}" != ""
%{debuginfodir}/%{elf_image_install_path}/*-%{KVERREL}smp.debug
%endif
%{debuginfodir}/lib/modules/%{KVERREL}smp
%{debuginfodir}/usr/src/kernels/%{KVERREL}-smp-%{_target_cpu}
%endif
%endif

%files smp
%defattr(-,root,root)
/%{image_install_path}/vmlinuz-%{KVERREL}smp
/boot/System.map-%{KVERREL}smp
/boot/symvers-%{KVERREL}smp.gz
/boot/config-%{KVERREL}smp
%dir /lib/modules/%{KVERREL}smp
/lib/modules/%{KVERREL}smp/kernel
/lib/modules/%{KVERREL}smp/build
/lib/modules/%{KVERREL}smp/source
/lib/modules/%{KVERREL}smp/extra
/lib/modules/%{KVERREL}smp/updates
/lib/modules/%{KVERREL}smp/weak-updates
%ghost /boot/initrd-%{KVERREL}smp.img
%config(noreplace) /etc/modprobe.d/blacklist-firewire

%files smp-devel
%defattr(-,root,root)
%verify(not mtime) /usr/src/kernels/%{KVERREL}-smp-%{_target_cpu}
/usr/src/kernels/%{KVERREL}smp-%{_target_cpu}
%endif

%if %{with_debug}
%if %{with_debuginfo}
%ifnarch noarch
%files debug-debuginfo
%defattr(-,root,root)
%if "%{elf_image_install_path}" != ""
%{debuginfodir}/%{elf_image_install_path}/*-%{KVERREL}debug.debug
%endif
%{debuginfodir}/lib/modules/%{KVERREL}debug
%{debuginfodir}/usr/src/kernels/%{KVERREL}-debug-%{_target_cpu}
%endif
%endif

%files debug
%defattr(-,root,root)
/%{image_install_path}/vmlinuz-%{KVERREL}debug
/boot/System.map-%{KVERREL}debug
/boot/symvers-%{KVERREL}debug.gz
/boot/config-%{KVERREL}debug
%dir /lib/modules/%{KVERREL}debug
/lib/modules/%{KVERREL}debug/kernel
/lib/modules/%{KVERREL}debug/build
/lib/modules/%{KVERREL}debug/source
/lib/modules/%{KVERREL}debug/extra
/lib/modules/%{KVERREL}debug/updates
/lib/modules/%{KVERREL}debug/weak-updates
%ghost /boot/initrd-%{KVERREL}debug.img
%config(noreplace) /etc/modprobe.d/blacklist-firewire

%files debug-devel
%defattr(-,root,root)
%verify(not mtime) /usr/src/kernels/%{KVERREL}-debug-%{_target_cpu}
/usr/src/kernels/%{KVERREL}debug-%{_target_cpu}
%endif

%if %{includexen}
%if %{with_xen}
%if %{with_debuginfo}
%ifnarch noarch
%package xen-debuginfo
Summary: Debug information for package %{name}-xen
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{KVERREL}
Provides: %{name}-xen-debuginfo-%{_target_cpu} = %{KVERREL}
%description xen-debuginfo
This package provides debug information for package %{name}-xen
This is required to use SystemTap with %{name}-xen-%{KVERREL}.
%files xen-debuginfo
%defattr(-,root,root)
%if "%{elf_image_install_path}" != ""
%{debuginfodir}/%{elf_image_install_path}/*-%{KVERREL}xen.debug
%endif
%{debuginfodir}/lib/modules/%{KVERREL}xen
%{debuginfodir}/usr/src/kernels/%{KVERREL}-xen-%{_target_cpu}
%{debuginfodir}/boot/xen*-%{KVERREL}.debug
%endif
%endif

%files xen
%defattr(-,root,root)
/%{image_install_path}/vmlinuz-%{KVERREL}xen
/boot/System.map-%{KVERREL}xen
/boot/symvers-%{KVERREL}xen.gz
/boot/config-%{KVERREL}xen
/%{image_install_path}/xen.gz-%{KVERREL}
/boot/xen-syms-%{KVERREL}
%dir /lib/modules/%{KVERREL}xen
/lib/modules/%{KVERREL}xen/kernel
%verify(not mtime) /lib/modules/%{KVERREL}xen/build
/lib/modules/%{KVERREL}xen/source
/etc/ld.so.conf.d/kernelcap-%{KVERREL}.conf
/lib/modules/%{KVERREL}xen/extra
/lib/modules/%{KVERREL}xen/updates
/lib/modules/%{KVERREL}xen/weak-updates
%ghost /boot/initrd-%{KVERREL}xen.img
%config(noreplace) /etc/modprobe.d/blacklist-firewire

%files xen-devel
%defattr(-,root,root)
%verify(not mtime) /usr/src/kernels/%{KVERREL}-xen-%{_target_cpu}
/usr/src/kernels/%{KVERREL}xen-%{_target_cpu}
%endif

%endif

%if %{with_kdump}
%if %{with_debuginfo}
%ifnarch noarch
%package kdump-debuginfo
Summary: Debug information for package %{name}-kdump
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{KVERREL}
Provides: %{name}-kdump-debuginfo-%{_target_cpu} = %{KVERREL}
%description kdump-debuginfo
This package provides debug information for package %{name}-kdump
This is required to use SystemTap with %{name}-kdump-%{KVERREL}.
%files kdump-debuginfo
%defattr(-,root,root)
%ifnarch s390x
%if "%{image_install_path}" != ""
%{debuginfodir}/%{image_install_path}/*-%{KVERREL}kdump.debug
%endif
%else
%if "%{elf_image_install_path}" != ""
%{debuginfodir}/%{elf_image_install_path}/*-%{KVERREL}kdump.debug
%endif
%endif
%{debuginfodir}/lib/modules/%{KVERREL}kdump
%{debuginfodir}/usr/src/kernels/%{KVERREL}-kdump-%{_target_cpu}
%endif
%endif

%files kdump
%defattr(-,root,root)
%ifnarch s390x
/%{image_install_path}/vmlinux-%{KVERREL}kdump
%else
/%{image_install_path}/vmlinuz-%{KVERREL}kdump
%endif
/boot/System.map-%{KVERREL}kdump
/boot/symvers-%{KVERREL}kdump.gz
/boot/config-%{KVERREL}kdump
%dir /lib/modules/%{KVERREL}kdump
/lib/modules/%{KVERREL}kdump/build
/lib/modules/%{KVERREL}kdump/source
%ifnarch s390x
/lib/modules/%{KVERREL}kdump/kernel
/lib/modules/%{KVERREL}kdump/extra
/lib/modules/%{KVERREL}kdump/updates
/lib/modules/%{KVERREL}kdump/weak-updates
%endif
%ghost /boot/initrd-%{KVERREL}kdump.img
%config(noreplace) /etc/modprobe.d/blacklist-firewire

%files kdump-devel
%defattr(-,root,root)
%verify(not mtime) /usr/src/kernels/%{KVERREL}-kdump-%{_target_cpu}
/usr/src/kernels/%{KVERREL}kdump-%{_target_cpu}
%endif

# only some architecture builds need kernel-doc

%if %{with_doc}
%files doc
%defattr(-,root,root)
%{_datadir}/doc/kernel-doc-%{kversion}/Documentation/*
%dir %{_datadir}/doc/kernel-doc-%{kversion}/Documentation
%dir %{_datadir}/doc/kernel-doc-%{kversion}
%endif

%changelog
* Tue Dec 24 2013 Ivan Polonevich <joni @ wargaming dot net> - 2.6.25-129.1.6.el5.binp
- Rebuild for wargaming.net

* Wed Apr  1 2009 Karanbir Singh <kbsingh@centos.org> [2.6.18-128.1.6.el5]
- Roll in CentOS Branding

* Tue Mar 24 2009 Jiri Pirko <jpirko@redhat.com> [2.6.18-128.1.6.el5]
- [x86] add nonstop_tsc flag in /proc/cpuinfo (Luming Yu ) [489310 474091]

* Tue Mar 17 2009 Don Howard <dhoward@redhat.com> [2.6.18-128.1.5.el5]
- Revert: [x86_64] fix gettimeoday TSC overflow issue (Prarit Bhargava ) [489847 467942]

* Mon Mar 16 2009 Jiri Pirko <jpirko@redhat.com> [2.6.18-128.1.4.el5]
- [x86_64] mce: do not clear an unrecoverable error status (Aristeu Rozanski ) [490433 489692]
- [wireless] iwlwifi: booting with RF-kill switch enabled (John W. Linville ) [489846 482990]
- [x86_64] fix gettimeoday TSC overflow issue (Prarit Bhargava ) [489847 467942]
- [misc] signal: modify locking to handle large loads (AMEET M. PARANJAPE ) [489457 487376]
- [x86] TSC keeps running in C3+ (Luming Yu ) [489310 474091]
- [net] fix icmp_send and icmpv6_send host re-lookup code (Jiri Pirko ) [489253 439670] {CVE-2009-0778}

* Mon Mar 09 2009 Jiri Pirko <jpirko@redhat.com> [2.6.18-128.1.3.el5]
- [net] skfp_ioctl inverted logic flaw (Eugene Teo ) [486539 486540] {CVE-2009-0675}
- [net] memory disclosure in SO_BSDCOMPAT gsopt (Eugene Teo ) [486517 486518] {CVE-2009-0676}
- [x86] limit max_cstate to use TSC on some platforms (Tony Camuso ) [488239 470572]
- [ptrace] correctly handle ptrace_update return value (Jerome Marchand ) [487394 483814]
- [misc] minor signal handling vulnerability (Oleg Nesterov ) [479963 479964] {CVE-2009-0028}
- [firmware] dell_rbu: prevent oops (Don Howard ) [482941 482942]
- [gfs2] panic in debugfs_remove when unmounting (Abhijith Das ) [485910 483617]

* Thu Feb 19 2009 Jiri Pirko <jpirko@redhat.com> [2.6.18-128.1.2.el5]
- [scsi] libata: sas_ata fixup sas_sata_ops (David Milburn ) [485909 483171]
- [fs] ecryptfs: readlink flaw (Eric Sandeen ) [481606 481607] {CVE-2009-0269}
- [qla2xxx] correct endianness during flash manipulation (Marcus Barrow ) [485908 481691]
- [net] ixgbe: frame reception and ring parameter issues (Andy Gospodarek ) [483210 475625]
- [misc] fix memory leak during pipe failure (Benjamin Marzinski ) [481576 478643]
- [block] enforce a minimum SG_IO timeout (Eugene Teo ) [475405 475406] {CVE-2008-5700}
- [nfs] handle attribute timeout and u32 jiffies wrap (Jeff Layton ) [483201 460133]
-  [fs] ext[234]: directory corruption DoS (Eugene Teo ) [459601 459604] {CVE-2008-3528}
- [net] deadlock in Hierarchical token bucket scheduler (Neil Horman ) [481746 474797]
- [wireless] iwl: fix BUG_ON in driver (Neil Horman ) [483206 477671]

* Mon Jan 26 2009 Jiri Pirko <jpirko@redhat.com> [2.6.18-128.1.1.el5]
- [security] introduce missing kfree (Jiri Pirko ) [480597 480598] {CVE-2009-0031}
- [sched] fix clock_gettime monotonicity (Peter Zijlstra ) [481122 477763]
- [nfs] create rpc clients with proper auth flavor (Jeff Layton ) [481119 465456]
- [net] sctp: overflow with bad stream ID in FWD-TSN chunk (Eugene Teo ) [478804 478805] {CVE-2009-0065}
- [md] fix oops with device-mapper mirror target (Heinz Mauelshagen ) [481120 472558]
- [openib] restore traffic in connected mode on HCA (AMEET M. PARANJAPE ) [479812 477000]
- [net] add preemption point in qdisc_run (Jiri Pirko ) [477746 471398] {CVE-2008-5713}
- [x86_64] copy_user_c assembler can leave garbage in rsi (Larry Woodman ) [481117 456682]
- [misc] setpgid returns ESRCH in some situations (Oleg Nesterov ) [480576 472433]
- [s390] zfcp: fix hexdump data in s390dbf traces (Hans-Joachim Picht ) [480996 470618]
- [fs] hfsplus: fix buffer overflow with a corrupted image (Anton Arapov ) [469637 469638] {CVE-2008-4933}
- [fs] hfsplus: check read_mapping_page return value (Anton Arapov ) [469644 469645] {CVE-2008-4934}
- [fs] hfs: fix namelength memory corruption (Anton Arapov ) [470772 470773] {CVE-2008-5025}

* Wed Dec 17 2008 Don Zickus <dzickus@redhat.com> [2.6.18-128.el5]
- [cifs] cifs_writepages may skip unwritten pages (Jeff Layton ) [470267]

* Mon Dec 15 2008 Don Zickus <dzickus@redhat.com> [2.6.18-127.el5]
- Revert: [i386]: check for dmi_data in powernow_k8 driver (Prarit Bhargava ) [476184]
- [xen] re-enable using xenpv in boot path for FV guests (Don Dutile ) [473899]
- [xen] pv_hvm: guest hang on FV save/restore (Don Dutile ) [475778]
- [openib] fix ipoib oops in unicast_arp_send (Doug Ledford ) [476005]
- [scsi] fnic: remove link down count processing (mchristi@redhat.com ) [474935]
- Revert: [x86] disable hpet on machine_crash_shutdown (Neil Horman ) [475652]
- [scsi] ibmvscsi: EH fails due to insufficient resources (AMEET M. PARANJAPE ) [475618]
- [x86_64] proc: export GART region through /proc/iomem (Neil Horman ) [475507]
- [acpi] add xw8600 and xw6600 to GPE0 block blacklist (Prarit Bhargava ) [475418]
- [net] cxgb3: fixup embedded firmware problems take 2 (Andy Gospodarek ) [469774]

* Mon Dec 08 2008 Don Zickus <dzickus@redhat.com> [2.6.18-126.el5]
- [scsi] mpt fusion: disable msi by default (Tomas Henzl ) [474465]
- [scsi] fcoe: update drivers (mchristi@redhat.com ) [474089]
- [scsi] fix error handler to call scsi_decide_disposition (Tom Coughlan ) [474345]
- [scsi] lpfc: fix cancel_retry_delay (Tom Coughlan ) [470610]
- [x86] disable hpet on machine_crash_shutdown (Neil Horman ) [473038]
- Revert [mm] keep pagefault from happening under pagelock (Don Zickus ) [473150]
- [net] enic: update to version 1.0.0.648 (Andy Gospodarek ) [473871]
- [scsi] qla4xxx: increase iscsi session check to 3-tuple (Marcus Barrow ) [474736]
- [agp] update the names of some graphics drivers (John Villalovos ) [472438]
- [net] atm: prevent local denial of service (Eugene Teo ) [473701] {CVE-2008-5079}
- [scsi] remove scsi_dh_alua (mchristi@redhat.com ) [471920]
- [scsi] qla2xx/qla84xx: occasional panic on loading (Marcus Barrow ) [472382]
- [net] cxgb3: eeh and eeprom fixups (Andy Gospodarek ) [441959]
- [net] cxgb3: fixup embedded firmware problems (Andy Gospodarek ) [469774]
- [wireless] iwlwifi/mac80211: various small fixes (John W. Linville ) [468967]
- [x86_64] fix AMD IOMMU boot issue (Joachim Deguara ) [473464]
- [x86_64] limit num of mce sysfs files removed on suspend (Prarit Bhargava ) [467725]
- [xen] console: make LUKS passphrase readable (Bill Burns ) [466240]
- [x86_64] Calgary IOMMU sysdata fixes (Prarit Bhargava ) [474047]
- [alsa] select 3stack-dig model for SC CELSIUS R670 (Jaroslav Kysela ) [470449]
- [ata] libata: lba_28_ok sector off by one (David Milburn ) [464868]
- [ppc64] fix system calls on Cell entered with XER.SO=1 (Jesse Larrew ) [474196]
- [block] fix max_segment_size, seg_boundary mask setting (Milan Broz ) [471639]
- [fs] jbd: alter EIO test to avoid spurious jbd aborts (Eric Sandeen ) [472276]
- [acpi] acpi_cpufreq: fix panic when removing module (Prarit Bhargava ) [472844]
- [openib] ehca: fix generating flush work completions (AMEET M. PARANJAPE ) [472812]
- [ata] libata: sata_nv hard reset mcp55 (David Milburn ) [473152]
- [misc] fix add return signal to ptrace_report_exec (AMEET M. PARANJAPE ) [471112]
- [misc] utrace: prevent ptrace_induce_signal() crash (Oleg Nesterov ) [469754]
- [misc] utrace: make ptrace_state refcountable (Oleg Nesterov ) [469754]
- [net] virtio_net: mergeable receive buffers (Mark McLoughlin ) [473120]
- [net] virtio_net: jumbo frame support (Mark McLoughlin ) [473114]
- [net] tun: jumbo frame support (Mark McLoughlin ) [473110]
- [net] fix unix sockets kernel panic (Neil Horman ) [470436] {CVE-2008-5029}
- [xen] x86: emulate movzwl with negative segment offsets (Chris Lalancette ) [471801]

* Mon Dec 01 2008 Don Zickus <dzickus@redhat.com> [2.6.18-125.el5]
- [net] cxgb3: embed firmware in driver (Andy Gospodarek ) [469774]
- [net] cxgb3: eeh, lro, and multiqueue fixes (Andy Gospodarek ) [441959]
- [misc] support for Intel's Ibex Peak (peterm@redhat.com ) [472961]
- [audit] race between inotify watch removal and unmount (Josef Bacik ) [472329] {CVE-2008-5182}
- [net] mlx4: panic when inducing pci bus error (AMEET M. PARANJAPE ) [472769]
- [s390] cio: DASD device driver times out (Hans-Joachim Picht ) [459803]
- [misc] hugepages: ia64 stack overflow and corrupt memory (Larry Woodman ) [472802]
- [net] niu: fix obscure 64-bit read issue (Andy Gospodarek ) [472849]
- [x86] nmi_watchdog: call do_nmi_callback from traps-xen (Aristeu Rozanski ) [471111]
- [GFS2] recovery stuck (Abhijith Das ) [465856]
- [misc] fix check_dead_utrace vs do_wait() race (Oleg Nesterov ) [466774]
- [scsi] cciss: add two new PCI IDs (Tom Coughlan ) [471679]
- [x86] fix memory-less NUMA node booting (Prarit Bhargava ) [471424]
- [pci] generic fix for EEH restore all registers (Jesse Larrew ) [470580]
- [net] e1000e: remove fix for EEH restore all registers (Jesse Larrew ) [470580]
- [agp] use contiguous memory to support xen (Rik van Riel ) [412691]
- [edac] i5000_edac: fix misc/thermal error messages (Aristeu Rozanski ) [471933]
- [alsa] fix PCM write blocking (Jaroslav Kysela ) [468202]
- [xen] build xen-platform-pci as a module (Don Dutile ) [472504]
- [scsi] qla2xx/qla84xx: failure to establish link (Marcus Barrow ) [472382]
- [acpi] add systems to GPE register blacklist (Prarit Bhargava ) [471341]
- [ia64] replace printk with mprintk in MCA/INIT context (Kei Tokunaga ) [471970]
- [usb] add support for dell keyboard 431c:2003 (Mauro Carvalho Chehab ) [471469]
- [net] e1000e: enable ECC correction on 82571 silicon (Andy Gospodarek ) [472095]
- [dlm] fix up memory allocation flags (David Teigland ) [471871]
- [xen] x86: fix highmem-xen.c BUG() (Chris Lalancette ) [452175]
- [xen] guest crashes if RTL8139 NIC is only one specified (Don Dutile ) [471110]
- [net] bnx2: fix oops on call to poll_controller (Neil Horman ) [470625]
- [scsi] update fcoe drivers (mchristi@redhat.com ) [436051]
- [net] bnx2: add support for 5716s (Andy Gospodarek ) [471903]
- [openib] IPoIB: fix oops on fabric events (Doug Ledford ) [471890]
- [libata] force sb600/700 ide mode into ahci on resume (David Milburn ) [466422]
- [xen] increase maximum DMA buffer size (Rik van Riel ) [412691]
- [xen] fix physical memory address overflow (Rik van Riel ) [412691]

* Mon Nov 17 2008 Don Zickus <dzickus@redhat.com> [2.6.18-124.el5]
- [s390] qeth: EDDP for large TSO skb fragment list (Hans-Joachim Picht ) [468068]
- [s390] missing bits for audit-fork (Alexander Viro ) [461831]
- [net] ixgbe: add support for 82598AT (Andy Gospodarek ) [454910]
- [libata] avoid overflow in ata_tf_read_block (David Milburn ) [471576]
- [md] dm-mpath: NULL ptr access in path activation code (Milan Broz ) [471393]
- [scsi] qla2xxx: no NPIV for loop connections (Marcus Barrow ) [471269]
- [ppc64] spufs: clean up page fault error checking (AMEET M. PARANJAPE ) [470301]
- [fs] cifs: corrupt data due to interleaved write calls (Jeff Layton ) [470267]
- [misc] lots of interrupts with /proc/.../hz_timer=0 (Hans-Joachim Picht ) [470289]
- [selinux] recognize addrlabel netlink messages (Thomas Graf ) [446063]
- [acpi] thinkpad: fix autoloading (Matthew Garrett ) [466816]
- [net] bnx2x: eeh, unload, probe, and endian fixes (Andy Gospodarek ) [468922]
- [firewire] various bug and module unload hang fixes (Jay Fenlason ) [469710 469711]

* Mon Nov 10 2008 Don Zickus <dzickus@redhat.com> [2.6.18-123.el5]
- [s390] cio: reduce cpu utilization during device scan (Hans-Joachim Picht ) [459793]
- [s390] cio: fix double unregistering of subchannels (Hans-Joachim Picht ) [456087]
- [video] uvc: buf overflow in format descriptor parsing (Jay Fenlason ) [470427] {CVE-2008-3496}
- [usb] add HID_QUIRK_RESET_LEDS to some keyboards (mchehab@infradead.org ) [434538]
- [acpi] always use 32 bit value for GPE0 on HP xw boxes (Prarit Bhargava ) [456638]
- [wireless] iwlagn/mac80211 IBSS fixes (John W. Linville ) [438388]
- [ppc64] cell: fix page fault error checking in spufs (AMEET M. PARANJAPE ) [470301]
- [input] atkbd: cancel delayed work before freeing struct (Jiri Pirko ) [461233]
- [openib] ehca: deadlock race when creating small queues (Jesse Larrew ) [470137]
- [openib] mthca: fix dma mapping leak (AMEET M. PARANJAPE ) [469902]
- [openib] ib_core: use weak ordering for user memory (AMEET M. PARANJAPE ) [469902]
- [ppc64] dma-mapping: provide attributes on cell platform (AMEET M. PARANJAPE ) [469902]
- [net] bnx2: prevent ethtool -r EEH event (AMEET M. PARANJAPE ) [469962]
- [net] bonding: update docs for arp_ip_target behavior (Andy Gospodarek ) [468870]
- [xen] uninitialized watch structure can lead to crashes (Don Dutile ) [465849]
- [openib] ehca: remove ref to QP if port activation fails (AMEET M. PARANJAPE ) [469941]
- [usb] fix locking for input devices (James Paradis ) [468915]
- [nfs] oops in direct I/O error handling (Steve Dickson ) [466164]
- [md] crash in device mapper if the user removes snapshot (Mikulas Patocka ) [468473]
- [openib] config update: enable some debugging (Doug Ledford ) [469410]
- [sata] libata is broken with large disks (David Milburn ) [469715]
- [md] dm-raid1: support extended status output (Jonathan Brassow ) [437177]
- [s390] qdio: repair timeout handling for qdio_shutdown (Hans-Joachim Picht ) [463164]
- [openib] race in ipoib_cm_post_receive_nonsrq (AMEET M. PARANJAPE ) [463485]
- [xen] remove contiguous_bitmap (Chris Lalancette ) [463500]
- [xen] ia64: backport check_pages_physically_contiguous (Chris Lalancette ) [463500]
- [ppc64] cell: corrupt SPU coredump notes (AMEET M. PARANJAPE ) [431881]
- [ppc64] spufs: missing context switch notification log-2 (AMEET M. PARANJAPE ) [462622]
- [ppc64] spufs: missing context switch notification log-1 (AMEET M. PARANJAPE ) [462622]
- [misc] spec: add generic Obsoletes for 3rd party drivers (Jon Masters ) [460047]
- [x86] vDSO: use install_special_mapping (Peter Zijlstra ) [460276] {CVE-2008-3527}
- [xen] limit node poking to available nodes (Joachim Deguara ) [449803]
- [xen] live migration of PV guest fails (Don Dutile ) [469230]

* Mon Nov 03 2008 Don Zickus <dzickus@redhat.com> [2.6.18-122.el5]
- [acpi] check common dmi tables on systems with acpi (Andy Gospodarek ) [469444]
- [scsi] qla3xxx, qla4xxx: update/use new version format (Marcus Barrow ) [469414]
- [md] dm-stripe.c: RAID0 event handling (Heinz Mauelshagen ) [437173]
- [md] dm-raid45.c: add target to makefile (Heinz Mauelshagen ) [437180]
- [md] dm-raid45.c: revert to RHEL5 dm-io kabi (Heinz Mauelshagen ) [437180]
- [wireless] iwlwifi: avoid sleep in softirq context (John W. Linville ) [467831]
- [net] bonding: allow downed interface before mod remove (Andy Gospodarek ) [467244]
- [acpi] fix boot hang on old systems without _CST methods (Matthew Garrett ) [467927]
- [scsi] qla2xxx: fix entries in class_device_attributes (Marcus Barrow ) [468873]
- [ppc64] clock_gettime is not incrementing nanoseconds (AMEET M. PARANJAPE ) [469073]
- [scsi] add fnic driver (mchristi@redhat.com ) [462385]
- [scsi] add libfc and software fcoe driver (mchristi@redhat.com ) [436051]
- [openib] ppc64: fix using SDP on 64K page systems (AMEET M. PARANJAPE ) [468872]
- [fs] ext4: delay capable checks to avoid avc denials (Eric Sandeen ) [467216]
- [fs] ext3: fix accessing freed memory in ext3_abort (Eric Sandeen ) [468547]
- [fs] autofs4: correct offset mount expire check (Ian Kent ) [468187]
- [fs] autofs4: cleanup autofs mount type usage (Ian Kent ) [468187]
- [openib] ehca: queue and completion pair setup problem (AMEET M. PARANJAPE ) [468237]
- [xen] PV: dom0 hang when device re-attached to in guest (Don Dutile ) [467773]
- [scsi] qla2xxx: correct Atmel flash-part handling (Marcus Barrow ) [468573]
- [scsi] qla2xxx: 84xx show FW VER and netlink code fixes (Marcus Barrow ) [464681]
- [scsi] qla2xxx: restore disable by default of MSI, MSI-X (Marcus Barrow ) [468555]
- [scsi] lpfc: Emulex RHEL-5.3 bugfixes (Tom Coughlan ) [461795]
- [s390] qdio: speedup multicast on full HiperSocket queue (Hans-Joachim Picht ) [463162]
- [ppc64] kexec/kdump: disable ptcal on QS21 (AMEET M. PARANJAPE ) [462744]
- [ppc64] ptcal has to be disabled to use kexec on QS21 (AMEET M. PARANJAPE ) [462744]
- [net] ixgbe: bring up device without crashing fix (AMEET M. PARANJAPE ) [467777]
- [fs] ecryptfs: storing crypto info in xattr corrupts mem (Eric Sandeen ) [468192]
- [misc] rtc: disable SIGIO notification on close (Vitaly Mayatskikh ) [465747]
- [net] allow rcv on inactive slaves if listener exists (Andy Gospodarek ) [448144]
- [net] e1000e: update driver to support recovery (AMEET M. PARANJAPE ) [445299]
- [xen] virtio_net: some relatively minor fixes (Mark McLoughlin ) [468034]
- [kabi] add dlm_posix_set_fsid (Jon Masters ) [468538]
- [wireless] iwlwifi: fix busted tkip encryption _again_ (John W. Linville ) [467831]
- [x86] make halt -f command work correctly (Ivan Vecera ) [413921]
- [ppc64] EEH PCI-E: recovery fails E1000; support MSI (AMEET M. PARANJAPE ) [445299]
- [x86_64] create a fallback for IBM Calgary (Pete Zaitcev ) [453680]
- [drm] i915 driver arbitrary ioremap (Eugene Teo ) [464509] {CVE-2008-3831}
- [xen] x86: allow the kernel to boot on pre-64 bit hw (Chris Lalancette ) [468083]

* Mon Oct 27 2008 Don Zickus <dzickus@redhat.com> [2.6.18-121.el5]
- [net] tun: fix printk warning (Mark McLoughlin ) [468536]
- [xen] FV: fix lockdep warnings when running debug kernel (Don Dutile ) [459876]
- [xen] fix crash on IRQ exhaustion (Bill Burns ) [442736]
- [net] ipv4: fix byte value boundary check (Jiri Pirko ) [468148]
- [ia64] fix ptrace hangs when following threads (Denys Vlasenko ) [461456]
- [net] tcp: let skbs grow over a page on fast peers (Mark McLoughlin ) [467845]
- [md] random memory corruption in snapshots (Mikulas Patocka ) [465825]
- [misc] ptrace: fix exec report (Jerome Marchand ) [455060]
- [gfs2] set gfp for data mappings to GFP_NOFS (Steven Whitehouse ) [467689]
- [nfs] remove recoverable BUG_ON (Steve Dickson ) [458774]
- [openib] ehca: attempt to free srq when none exists (AMEET M. PARANJAPE ) [463487]
- [fs] don't allow splice to files opened with O_APPEND (Eugene Teo ) [466710] {CVE-2008-4554}
- [fs] ext4: add missing aops (Eric Sandeen ) [466246]
- [ppc64] add missing symbols to vmcoreinfo (Neil Horman ) [465396]
- [net] sctp: INIT-ACK indicates no AUTH peer support oops (Eugene Teo ) [466082] {CVE-2008-4576}
- [ppc64] fix race for a free SPU (AMEET M. PARANJAPE ) [465581]
- [ppc64] SPUs hang when run with affinity-2 (AMEET M. PARANJAPE ) [464686]
- [ppc64] SPUs hang when run with affinity-1 (AMEET M. PARANJAPE ) [464686]
- [openib] ehca: add flush CQE generation (AMEET M. PARANJAPE ) [462619]
- [x86] PAE: limit RAM to 64GB/PAE36 (Larry Woodman ) [465373]
- [nfs] portmap client race (Steve Dickson ) [462332]
- [input] atkbd: delay executing of LED switching request (Jiri Pirko ) [461233]
- [x86] powernow_k8: depend on newer version of cpuspeed (Brian Maly ) [468764]
- [fs] ext4: fix warning on x86_64 build (Eric Sandeen ) [463277]
- [crypto] fix ipsec crash with MAC longer than 16 bytes (Neil Horman ) [459812]
- [fs] ecryptfs: depend on newer version of ecryptfs-utils (Eric Sandeen ) [468772]
- [ppc64] support O_NONBLOCK in /proc/ppc64/rtas/error_log (Vitaly Mayatskikh ) [376831]
- [xen] ia64: make viosapic SMP-safe by adding lock/unlock (Tetsu Yamamoto ) [466552]
- [xen] ia64: VT-i2 performance restoration (Bill Burns ) [467487]

* Fri Oct 17 2008 Don Zickus <dzickus@redhat.com> [2.6.18-120.el5]
- [misc] futex: fixup futex compat for private futexes (Peter Zijlstra ) [467459]
- [pci] set domain/node to 0 in PCI BIOS enum code path (Prarit Bhargava ) [463418]
- [scsi] qla2xxx: prevent NPIV conf for older hbas (Marcus Barrow ) [467153]
- [scsi] fix oops after trying to removing rport twice (Marcus Barrow ) [465945]
- [agp] re-introduce 82G965 graphics support (Prarit Bhargava ) [466307]
- [agp] correct bug in stolen size calculations (Dave Airlie ) [463853]
- [scsi] qla2xxx: merge errors caused initialize failures (Marcus Barrow ) [442946]
- [dm] mpath: moving path activation to workqueue panics (Milan Broz ) [465570]
- [scsi] aacraid: remove some quirk AAC_QUIRK_SCSI_32 bits (Tomas Henzl ) [453472]
- Revert: [ppc64] compile and include the addnote binary (Don Zickus ) [462663]
- [scsi] cciss: the output of LUN size and type wrong (Tomas Henzl ) [466030]
- [misc] posix-timers: event vs dequeue_signal() race (Mark McLoughlin ) [466167]
- [ata] libata: ahci enclosure management support (David Milburn ) [437190]
- [gfs2] fix jdata page invalidation (Steven Whitehouse ) [437803]
- [net] sky2: fix hang resulting from link flap (Neil Horman ) [461681]
- [ata] libata: ata_piix sata/ide combined mode fix (David Milburn ) [463716]
- [gfs2] fix for noatime support (Steven Whitehouse ) [462579]
- [fs] remove SUID when splicing into an inode (Eric Sandeen ) [464452]
- [fs] open() allows setgid bit when user is not in group (Eugene Teo ) [463687] {CVE-2008-4210}
- [dlm] add old plock interface (David Teigland ) [462354]
- [audit] fix NUL handling in TTY input auditing (Miloslav Trmač ) [462441]
- [xen] ia64: fix INIT injection (Tetsu Yamamoto ) [464445]

* Fri Oct 10 2008 Don Zickus <dzickus@redhat.com> [2.6.18-119.el5]
- [ppc64] compile and include the addnote binary (Don Zickus ) [462663]
- [scsi] qla2xxx: new version string defintion (Marcus Barrow ) [465023]
- [acpi] configs update for acpi-cpufreq driver (Matthew Garrett ) [449787]

* Sat Oct 04 2008 Don Zickus <dzickus@redhat.com> [2.6.18-118.el5]
- [scsi] fix QUEUE_FULL retry handling (mchristi@redhat.com ) [463709]
- [drm] support for Intel Cantiga and Eaglelake (Dave Airlie ) [438400]
- [agp] add support for Intel Cantiga and Eaglelake (Dave Airlie ) [463853]
- Revert: [mm] fix support for fast get user pages (Dave Airlie ) [447649]
- [ppc64] netboot image too large (Ameet Paranjape ) [462663]
- [scsi] scsi_error: retry cmd handling of transport error (mchristi@redhat.com ) [463206]
- [net] correct mode setting for extended sysctl interface (Neil Horman ) [463659]
- [net] e1000e: protect ICHx NVM from malicious write/erase (Andy Gospodarek ) [463503]
- [s390] qdio: fix module ref counting in qdio_free (Hans-Joachim Picht ) [458074]
- [scsi] qla2xxx: use the NPIV table to instantiate port (Marcus Barrow ) [459015]
- [scsi] qla2xxx: use the Flash Layout Table (Marcus Barrow ) [459015]
- [scsi] qla2xxx: use the Flash Descriptor Table (Marcus Barrow ) [459015]
- [net] enic: add new 10GbE device (Andy Gospodarek ) [462386]
- [net] ipt_CLUSTERIP: fix imbalanced ref count (Neil Horman ) [382491]
- [scsi] qla2xxx: update 24xx,25xx firmware for RHEL-5.3 (Marcus Barrow ) [442946]
- [net] bnx2: fix problems with multiqueue receive (Andy Gospodarek ) [441964]
- [net] e1000: add module param to set tx descriptor power (Andy Gospodarek ) [436966]
- [misc] preempt-notifier fixes (Eduardo Habkost ) [459838]
- [tty] termiox support missing mutex lock (aris ) [445211]
- [fs] ecryptfs: off-by-one writing null to end of string (Eric Sandeen ) [463478]
- [misc] add tracepoints to activate/deactivate_task (Jason Baron ) [461966]
- [scsi] qla2xxx: use rport dev loss timeout consistently (Marcus Barrow ) [462109]
- [ata] libata: rmmod pata_sil680 hangs (David Milburn ) [462743]
- [scsi] qla2xxx: support PCI Enhanced Error Recovery (Marcus Barrow ) [462416]
- [ppc64] subpage protection for pAVE (Brad Peters ) [439489]
- [ppc64] edac: enable for cell platform (Brad Peters ) [439507]

* Mon Sep 29 2008 Don Zickus <dzickus@redhat.com> [2.6.18-117.el5]
- [mm] filemap: fix iov_base data corruption (Josef Bacik ) [463134]
- Revert: [misc] create a kernel checksum file per FIPS140-2 (Don Zickus ) [444632]
- [x86_64] NMI wd: clear perf counter registers on P4 (Aristeu Rozanski ) [461671]
- [scsi] failfast bit setting in dm-multipath/multipath (mchristi@redhat.com ) [463470]
- [scsi] fix hang introduced by failfast changes (Mark McLoughlin ) [463416]
- [x86_64] revert time syscall changes (Prarit Bhargava ) [461184]

* Thu Sep 18 2008 Don Zickus <dzickus@redhat.com> [2.6.18-116.el5]
- [x86] mm: fix endless page faults in mount_block_root (Larry Woodman ) [455491]
- [mm] check physical address range in ioremap (Larry Woodman ) [455478]
- [scsi] modify failfast so it does not always fail fast (mchristi@redhat.com ) [447586]
- Revert: [mm] NUMA: system is slow when over-committing memory (Larry Woodman ) [457264]
- [docs] update kernel-parameters with tick-divider (Chris Lalancette ) [454792]
- [openib] add an enum for future RDS support (Doug Ledford ) [462551]
- [pci] allow multiple calls to pcim_enable_device (John Feeney ) [462500]
- [xen] virtio: include headers in kernel-headers package (Eduardo Pereira Habkost ) [446214]
- [scsi] libiscsi: data corruption when resending packets (mchristi@redhat.com ) [460158]
- [gfs2] glock deadlock in page fault path (Bob Peterson ) [458684]
- [gfs2] panic if you misspell any mount options (Abhijith Das ) [231369]
- [xen] allow guests to hide the TSC from applications (Chris Lalancette ) [378481] {CVE-2007-5907}

* Sat Sep 13 2008 Don Zickus <dzickus@redhat.com> [2.6.18-115.el5]
- [scsi] qla2xxx: additional residual-count correction (Marcus Barrow ) [462117]
- [audit] audit-fork patch (Alexander Viro ) [461831]
- [net] ipv6: extra sysctls for additional TAHI tests (Neil Horman ) [458270]
- [nfs] disable the fsc mount option (Steve Dickson ) [447474]
- [acpi] correctly allow WoL from S4 state (Neil Horman ) [445890]
- [ia64] procfs: show the size of page table cache (Takao Indoh ) [458410]
- [ia64] procfs: reduce the size of page table cache (Takao Indoh ) [458410]
- [fs] ecryptfs: disallow mounts on nfs, cifs, ecryptfs (Eric Sandeen ) [435115]
- [md] add device-mapper message parser interface (heinzm@redhat.com ) [437180]
- [md] add device-mapper RAID4/5 stripe locking interface (heinzm@redhat.com ) [437180]
- [md] add device-mapper dirty region hash file (heinzm@redhat.com ) [437180]
- [md] add device-mapper object memory cache interface (heinzm@redhat.com ) [437180]
- [md] add device-mapper object memory cache (heinzm@redhat.com ) [437180]
- [md] export dm_disk and dm_put (heinzm@redhat.com ) [437180]
- [md] add device-mapper RAID4/5 target (heinzm@redhat.com ) [437180]
- [md] add device-mapper message parser (heinzm@redhat.com ) [437180]
- [md] add device mapper dirty region hash (heinzm@redhat.com ) [437180]
- [md] add config option for dm RAID4/5 target (heinzm@redhat.com ) [437180]
- [scsi] qla2xxx: update 8.02.00-k5 to 8.02.00-k6 (Marcus Barrow ) [459722]
- [kabi] add vscnprintf, down_write_trylock to whitelist (Jon Masters ) [425341]
- [kabi] add dlm_posix_get/lock/unlock to whitelist (Jon Masters ) [456169]
- [kabi] add mtrr_add and mtrr_del to whitelist (Jon Masters ) [437129]
- [kabi] add iounmap to whitelist (Jon Masters ) [435144]
- [x86] make powernow_k8 a module (Brian Maly ) [438835]
- [fs] ecryptfs: delay lower file opens until needed (Eric Sandeen ) [429142]
- [fs] ecryptfs: unaligned access helpers (Eric Sandeen ) [457143]
- [fs] ecryptfs: string copy cleanup (Eric Sandeen ) [457143]
- [fs] ecryptfs: discard ecryptfsd registration messages (Eric Sandeen ) [457143]
- [fs] ecryptfs: privileged kthread for lower file opens (Eric Sandeen ) [457143]
- [fs] ecryptfs: propagate key errors up at mount time (Eric Sandeen ) [440413]
- [fs] ecryptfs: update to 2.6.26 codebase (Eric Sandeen ) [449668]
- Revert [misc] fix wrong test in wait_task_stopped (Anton Arapov ) [382211]

* Sat Sep 13 2008 Don Zickus <dzickus@redhat.com> [2.6.18-114.el5]
- [xen] cpufreq: fix Nehalem/Supermicro systems (Rik van Riel ) [458894]
- [net] enable TSO if supported by at least one device (Herbert Xu ) [461866]
- [crypto] fix panic in hmac self test (Neil Horman ) [461537]
- [scsi] qla2xxx/qla84xx: update to upstream for RHEL-5.3 (Marcus Barrow ) [461414]
- [misc] hpilo: cleanup device_create for RHEL-5.3 (tcamuso@redhat.com ) [437212]
- [misc] hpilo: update driver to 0.5 (tcamuso@redhat.com ) [437212]
- [misc] hpilo: update to upstream 2.6.27 (tcamuso@redhat.com ) [437212]
- [misc] futex: private futexes (Peter Zijlstra ) [460593]
- [misc] preempt-notifiers implementation (Eduardo Habkost ) [459838]
- [scsi] fusion: update to version 3.04.07 (Tomas Henzl ) [442025]
- [fs] ext4/vfs/mm: core delalloc support (Eric Sandeen ) [455452]
- [net] r8169: add support and fixes (Ivan Vecera ) [251252 441626 442635 443623 452761 453563 457892]
- [md] LVM raid-1 performance fixes (Mikulas Patocka ) [438153]
- [md] LVM raid-1 performance fixes (Mikulas Patocka ) [438153]
- [xen] kdump: ability to use makedumpfile with vmcoreinfo (Neil Horman ) [454498]
- [scsi] aic79xx: reset HBA on kdump kernel boot (Neil Horman ) [458620]
- [fs] implement fallocate syscall (Eric Sandeen ) [450566]
- [misc] better clarify package descriptions (Don Zickus ) [249726]
- [audit] audit TTY input (Miloslav Trmač ) [244135]
- [scsi] qla2xxx - mgmt. API for FCoE, NetLink (Marcus Barrow ) [456900]
- [scsi] qla2xxx - mgmt. API, CT pass thru (Marcus Barrow ) [455900]
-  [misc] hrtimer optimize softirq (George Beshers ) [442148]
- [misc] holdoffs in hrtimer_run_queues (George Beshers ) [442148]
- [xen] netfront xenbus race (Markus Armbruster ) [453574]
- [gfs2] NFSv4 delegations fix for cluster systems (Brad Peters ) [433256]
- [scsi] qla2xxx: update 8.02.00-k1 to 8.02.00.k4 (Marcus Barrow ) [455264]
- [scsi] qla2xxx: upstream changes from 8.01.07-k7 (Marcus Barrow ) [453685]
- [scsi] qla2xxx: add more statistics (Marcus Barrow ) [453441]
- [scsi] qla2xxx: add ISP84XX support (Marcus Barrow ) [442083]
- [ia64] set default max_purges=1 regardless of PAL return (Luming Yu ) [451593]
- [ia64] param for max num of concurrent global TLB purges (Luming Yu ) [451593]
- [ia64] multiple outstanding ptc.g instruction support (Luming Yu ) [451593]
- [scsi] ST: buffer size doesn't match block size panics (Ivan Vecera ) [443645]
- [scsi] fix medium error handling with bad devices (Mike Christie ) [431365]
- [xen] ia64: VT-i2 performance addendum (Bill Burns ) [437096]
- [xen] HV: ability to use makedumpfile with vmcoreinfo (Neil Horman ) [454498]
- [xen] ia64: vps save restore patch (Bill Burns ) [437096]

* Fri Sep 12 2008 Don Zickus <dzickus@redhat.com> [2.6.18-113.el5]
- [xen] remove /proc/xen*/* from bare-metal and FV guests (Don Dutile ) [461532]

* Fri Sep 12 2008 Don Zickus <dzickus@redhat.com> [2.6.18-112.el5]
- [fs] jbd: test BH_write_EIO to detect errors on metadata (Hideo AOKI ) [439581]
- [wireless] rt2x00: avoid NULL-ptr deref when probe fails (John W. Linville ) [448763]
- [x86_64] suspend to disk fails with >4GB of RAM (Matthew Garrett ) [459980]
- [char] add range_is_allowed check to mmap_mem (Eugene Teo ) [460857]
- [acpi] add 3.0 _TSD _TPC _TSS _PTC throttling support (Brian Maly ) [440099]
- [scsi] add scsi device handlers config options (Mike Christie ) [438761]
- [scsi] scsi_dh: add ALUA handler (mchristi@redhat.com ) [438761]
- [scsi] scsi_dh: add rdac handler (mchristi@redhat.com ) [438761]
- [md] dm-mpath: use SCSI device handler (mchristi@redhat.com ) [438761]
- [scsi] add infrastructure for SCSI Device Handlers (mchristi@redhat.com ) [438761]
- [misc] driver core: port bus notifiers (mchristi@redhat.com ) [438761]
- [fs] binfmt_misc: avoid potential kernel stack overflow (Vitaly Mayatskikh ) [459463]
- [CRYPTO] tcrypt: Change the XTEA test vectors (Herbert Xu ) [446522]
- [CRYPTO] skcipher: Use RNG instead of get_random_bytes (Herbert Xu ) [446526]
- [CRYPTO] rng: RNG interface and implementation (Herbert Xu ) [446526]
- [CRYPTO] api: Add fips_enable flag (Herbert Xu ) [444634]
- [CRYPTO] cryptomgr - Test ciphers using ECB (Herbert Xu ) [446522]
- [CRYPTO] api - Use test infrastructure (Herbert Xu ) [446522]
- [CRYPTO] cryptomgr - Add test infrastructure (Herbert Xu ) [446522]
- [CRYPTO] tcrypt - Add alg_test interface (Herbert Xu ) [446522]
- [CRYPTO] tcrypt: self test for des3_ebe cipher (Herbert Xu ) [446522]
- [CRYPTO] api: missing accessors for new crypto_alg field (Herbert Xu ) [446522]
- [CRYPTO] tcrypt: Abort and only log if there is an error (Herbert Xu ) [446522]
- [CRYPTO] tcrypt: Avoid using contiguous pages (Herbert Xu ) [446522]
- [CRYPTO] tcrpyt: Remove unnecessary kmap/kunmap calls (Herbert Xu ) [446522]
- [CRYPTO] tcrypt: Catch cipher destination mem corruption (Herbert Xu ) [446522]
- [CRYPTO] tcrypt: Shrink the tcrypt module (Herbert Xu ) [446522]
- [CRYPTO] tcrypt: AES CBC test vector from NIST SP800-38A (Herbert Xu ) [446522]
- [CRYPTO] tcrypt: Change the usage of the test vectors (Herbert Xu ) [446522]
- [CRYPTO] tcrypt: Shrink speed templates (Herbert Xu ) [446522]
- [CRYPTO] tcrypt: Group common speed templates (Herbert Xu ) [446522]
- [fs] jdb: fix error handling for checkpoint I/O (Hideo AOKI ) [439581]
- [fs] ext3: add checks for errors from jbd (Hideo AOKI ) [439581]
- [fs] jbd: fix commit code to properly abort journal (Hideo AOKI ) [439581]
- [fs] jbd: don't dirty original metadata buffer on abort (Hideo AOKI ) [439581]
- [fs] jdb: abort when failed to log metadata buffers (Hideo AOKI ) [439581]
- [fs] ext3: don't read inode block if buf has write error (Hideo AOKI ) [439581]
- [fs] jdb: add missing error checks for file data writes (Hideo AOKI ) [439581]
- [net] tun: add IFF_VNET_HDR, TUNGETFEATURES, TUNGETIFF (Herbert Xu ) [459719]
- [acpi] increase deep idle state residency on platforms-2 (Matthew Garrett ) [455449]
- [acpi] increase deep idle state residency on platforms (Matthew Garrett ) [455447]
- [acpi] cpufreq: update to upstream for RHEL-5.3 (Matthew Garrett ) [449787]
- [acpi] thinkpad_acpi: update to upstream for RHEL-5.3 (Matthew Garrett ) [457101]
- [xen] fix crash on IRQ exhaustion and increase NR_IRQS (Bill Burns ) [442736]
- [ide] enable DRAC4 (John Feeney ) [459197]
- [md] move include files to include/linux for exposure (Jonathan Brassow ) [429337]
- [md] expose dm.h macros (Jonathan Brassow ) [429337]
- [md] remove internal mod refs fields from interface (Jonathan Brassow ) [429337]
- [md] dm-log: move register functions (Jonathan Brassow ) [429337]
- [md] dm-log: clean interface (Jonathan Brassow ) [429337]
- [md] clean up the dm-io interface (Jonathan Brassow ) [429337]
- [md] dm-log: move dirty log into separate module (Jonathan Brassow ) [429337]
- [md] device-mapper interface exposure (Jonathan Brassow ) [429337]
- [cifs] enable SPNEGO and DFS upcalls in config-generic (Jeff Layton ) [453462]
- [fs] cifs: latest upstream for RHEL-5.3 (Jeff Layton ) [453462 431868 443395 445522 446142 447400]
- [fs] introduce a function to register iget failure (Jeff Layton ) [453462]
- [fs] proc: fix ->open'less usage due to ->proc_fops flip (Jeff Layton ) [453462]
- [security] key: fix lockdep warning when revoking auth (Jeff Layton ) [453462]
- [security] key: increase payload size when instantiating (Jeff Layton ) [453462]
- [fs] call flush_disk after detecting an online resize (Jeff Moyer ) [444964]
- [fs] add flush_disk to flush out common buffer cache (Jeff Moyer ) [444964]
- [fs] check for device resize when rescanning partitions (Jeff Moyer ) [444964]
- [fs] adjust block device size after an online resize (Jeff Moyer ) [444964]
- [fs] wrapper for lower-level revalidate_disk routines (Jeff Moyer ) [444964]
- [scsi] sd: revalidate_disk wrapper (Jeff Moyer ) [444964]
- [xen] virtio: add PV network and block drivers for KVM (Mark McLoughlin ) [446214]
- [misc] remove MAX_ARG_PAGES limit: var length argument (Jerome Marchand ) [443659]
- [misc] remove MAX_ARG_PAGES limit: rework execve audit (Jerome Marchand ) [443659]
- [misc] remove MAX_ARG_PAGES limit: independent stack top (Jerome Marchand ) [443659]
- [ia64] kprobes: support kprobe-booster (Masami Hiramatsu ) [438733]
- [audit] fix compile when CONFIG_AUDITSYSCALL is disabled (Prarit Bhargava ) [452577]
- [nfs] v4: handle old format exports gracefully (Brad Peters ) [427424]
- [xen] x86: fix building with max_phys_cpus=128 (Bill Burns ) [447958]
- [xen] Intel EPT 2MB patch (Bill Burns ) [426679]
- [xen] Intel EPT Migration patch (Bill Burns ) [426679]
- [xen] Intel EPT Patch (Bill Burns ) [426679]
- [xen] Intel pre EPT Patch (Bill Burns ) [426679]
- [xen] AMD 2MB backing pages support (Bhavna Sarathy ) [251980]

* Thu Sep 11 2008 Don Zickus <dzickus@redhat.com> [2.6.18-111.el5]
- [ia64] kabi: remove sn symbols from whitelist (Jon Masters ) [455308]
- [net] bnx2x: update to upstream version 1.45.21 (Andy Gospodarek ) [442026]
- [net] cxgb3: updates and lro fixes (Andy Gospodarek ) [441959]
- [net] niu: enable support for Sun Neptune cards (Andy Gospodarek ) [441416]
- [scsi] scsi_host_lookup: error returns and NULL pointers (Tom Coughlan ) [460195]
- [scsi] scsi_netlink: transport/LLD receive/event support (Tom Coughlan ) [460195]
- [misc] install correct kernel chksum file for FIPS140-2 (Chris Lalancette ) [444632]
- [net] ixgbe: update to version 1.3.18-k4 (Andy Gospodarek ) [436044]
- [dlm] fix address compare (David Teigland ) [459585]
- [net] bonding: fix locking in 802.3ad mode (Andy Gospodarek ) [457300]
- [openib] OFED-1.3.2-pre update (Doug Ledford ) [439565 443476 453110 458886 459052 458375 459052 230035 460623]
- [md] dm snapshot: use per device mempools (Mikulas Patocka ) [460846]
- [md] dm kcopyd: private mempool (Mikulas Patocka ) [460845]
- [md] deadlock with nested LVMs (Mikulas Patocka ) [460845]
- [net] skge: don't clear MC state on link down (Andy Gospodarek ) [406051]
- [net] sky2: re-enable 88E8056 for most motherboards (Andy Gospodarek ) [420961]
- [net] update myri10ge 10Gbs ethernet driver (Flavio Leitner ) [357191]
- [net] bnx2: update to upstream version 1.7.9 (Andy Gospodarek ) [441964]
- [net] e1000e: update to upstream version 0.3.3.3-k2 (Andy Gospodarek ) [436045]
- [net] tg3: update to upstream version 3.93 (Andy Gospodarek ) [441975 440958 436686]
- [net] igb: update to upstream version 1.2.45-k2 (Andy Gospodarek ) [436040]
- [misc] intel: new SATA, USB, HD Audio and I2C(SMBUS) ids (John Villalovos ) [433538]
- [net] bnx2x: update to upstream version 1.45.20 (Andy Gospodarek ) [442026]
- [net] ixgb: hardware support and other upstream fixes (Andy Gospodarek ) [441609]
- [x86] amd oprofile: support instruction based sampling (Bhavna Sarathy ) [438385]
- [scsi] cciss: support for sg_ioctl (Tomas Henzl ) [250483]
- [scsi] cciss: support for new controllers (Tomas Henzl ) [437497 447427]
- [net] pppoe: check packet length on all receive paths (Jiri Pirko ) [457013]
- [scsi] iscsi: fix nop timeout detection (mchristi@redhat.com ) [453969]
- [scsi] lpfc: update to version 8.2.0.30 (Tom Coughlan ) [441746]
- [md] fix handling of sense buffer in eh commands (Doug Ledford ) [441640]
- [md] fix error propogation in raid arrays (Doug Ledford ) [430984]
- [md] dm: reject barrier requests (Milan Broz ) [458936]
- [scsi] 3w-9xxx: update to version 2.26.08.003 (Tomas Henzl ) [451946]
- [scsi] 3w-xxxx: update to version 1.26.03.000 (Tomas Henzl ) [451945]
- [scsi] megaraid_sas: update to version 4.01-rh1 (Tomas Henzl ) [442913]
- [md] dm snapshot: fix race during exception creation (Mikulas Patocka ) [459337]
- [md] dm-snapshots: race condition and data corruption (Mikulas Patocka ) [459337]
- [md] dm crypt: use cond_resched (Milan Broz ) [459095]
- [md] dm mpath: fix bugs in error paths (Milan Broz ) [459092]
- [mm] fix support for fast get user pages (Ed Pollard ) [447649]
- [xen] ia64 PV: config file changes to add support (Don Dutile ) [442991]
- [xen] ia64 PV: Kconfig additions (Don Dutile ) [442991]
- [xen] ia64 PV: Makefile changes (Don Dutile ) [442991]
- [xen] ia64 PV: shared used header file changes (Don Dutile ) [442991]
- [IA64] Correct pernodesize calculation (George Beshers ) [455308]
- [IA64] Fix large MCA bootmem allocation (George Beshers ) [455308]
- [IA64] Disable/re-enable CPE interrupts on Altix (George Beshers ) [455308]
- [IA64] Don't set psr.ic and psr.i simultaneously (George Beshers ) [455308]
- [IA64] Support multiple CPUs going through OS_MCA (George Beshers ) [455308]
- [IA64] Remove needless delay in MCA rendezvous (George Beshers ) [455308]
- [IA64] Clean up CPE handler registration (George Beshers ) [455308]
- [IA64] CMC/CPE: Reverse fetching log and checking poll (George Beshers ) [455308]
- [IA64] Force error to surface in nofault code (George Beshers ) [455308]
- [IA64] Fix Altix BTE error return status (George Beshers ) [455308]
- [IA64] BTE error timer fix (George Beshers ) [455308]
- [IA64] Update processor_info features (George Beshers ) [455308]
- [IA64] More Itanium PAL spec updates (George Beshers ) [455308]
- [IA64] Add se bit to Processor State Parameter structure (George Beshers ) [455308]
- [IA64] Add dp bit to cache and bus check structs (George Beshers ) [455308]
- [IA64] PAL calls need physical mode, stacked (George Beshers ) [455308]
- [IA64] Cache error recovery (George Beshers ) [455308]
- [IA64] handle TLB errors from duplicate itr.d dropins (George Beshers ) [455308]
- [IA64] MCA recovery: Montecito support (George Beshers ) [455308]

* Tue Sep 09 2008 Don Zickus <dzickus@redhat.com> [2.6.18-110.el5]
- [x86_64] use strncmp for memmap=exactmap boot argument (Prarit Bhargava ) [450244]
- [wireless] compiler warning fixes for mac80211 update (John W. Linville ) [438391]
- [serial] 8250: support for DTR/DSR hardware flow control (Aristeu Rozanski ) [445215]
- [tty] add termiox support (Aristeu Rozanski ) [445211]
- [vt] add shutdown method (Aristeu Rozanski ) [239604]
- [tty] add shutdown method (Aristeu Rozanski ) [239604]
- [tty] cleanup release_mem (Aristeu Rozanski ) [239604]
- [mm] keep pagefault from happening under page lock (Josef Bacik ) [445433]
- [wireless] iwlwifi: post-2.6.27-rc3 to support iwl5x00 (John W. Linville ) [438388]
- [net] random32: seeding improvement (Jiri Pirko ) [458019]
- [usb] work around ISO transfers in SB700 (Pete Zaitcev ) [457723]
- [x86_64] AMD 8-socket APICID patches (Prarit Bhargava ) [459813]
- [misc] make printk more robust against kexec shutdowns (Neil Horman ) [458368]
- [fs] ext4: backport to rhel5.3 interfaces (Eric Sandeen ) [458718]
- [fs] ext4: Kconfig/Makefile/config glue (Eric Sandeen ) [458718]
- [fs] ext4: fixes from upstream pending patch queue (Eric Sandeen ) [458718]
- [fs] ext4: revert delalloc upstream mods (Eric Sandeen ) [458718]
- [fs] ext4: 2.6.27-rc3 upstream codebase (Eric Sandeen ) [458718]
- [fs] ext4: new s390 bitops (Eric Sandeen ) [459436]
- [usb] wacom: add support for Cintiq 20WSX (Aristeu Rozanski ) [248903]
- [usb] wacom: add support for Intuos3 4x6 (Aristeu Rozanski ) [370471]
- [usb] wacom: fix maximum distance values (Aristeu Rozanski ) [248903]
- [x86] hpet: consolidate assignment of hpet_period (Brian Maly ) [435726]
- [openib] lost interrupt after LPAR to LPAR communication (Brad Peters ) [457838]
- [firmware] fix ibft offset calculation (mchristi@redhat.com ) [444776]
- [block] performance fix for too many physical devices (Mikulas Patocka ) [459527]
- [ide] Fix issue when appending data on an existing DVD (Mauro Carvalho Chehab ) [457025]
- [misc] fix kernel builds on modern userland (Matthew Garrett ) [461540]
- [x86_64] AMD IOMMU driver support (Bhavna Sarathy ) [251970]
- [x86_64] GART iommu alignment fixes (Prarit Bhargava ) [455813]
- [firewire] latest upstream snapshot for RHEL-5.3 (Jay Fenlason ) [449520 430300 429950 429951]
- [net] ipv6: configurable address selection policy table (Neil Horman ) [446063]
- [fs] relayfs: support larger on-memory buffer (Masami Hiramatsu ) [439269]
- [xen] ia64: speed up hypercall for guest domain creation (Tetsu Yamamoto ) [456171]
- [xen] make last processed event channel a per-cpu var (Tetsu Yamamoto ) [456171]
- [xen] process event channel notifications in round-robin (Tetsu Yamamoto ) [456171]
- [xen] use unlocked_ioctl in evtchn, gntdev and privcmd (Tetsu Yamamoto ) [456171]
- [xen] disallow nested event delivery (Tetsu Yamamoto ) [456171]
- [ppc64] spu: add cpufreq governor (Ed Pollard ) [442410]
- [misc] cleanup header warnings and enable header check (Don Zickus ) [458360]
- [mm] NUMA: over-committing memory compiler warnings (Larry Woodman ) [457264]
- [misc] mmtimer: fixes for high resolution timers (George Beshers ) [442186]
- [x86_64] xen: local DOS due to NT bit leakage (Eugene Teo ) [457722] {CVE-2006-5755}
- [xen] ia64: mark resource list functions __devinit (Tetsu Yamamoto ) [430219]
- [xen] ia64: issue ioremap HC in pci_acpi_scan_root (Tetsu Yamamoto ) [430219]
- [xen] ia64: revert paravirt to ioremap /proc/pci (Tetsu Yamamoto ) [430219]
- [xen] ia64: disable paravirt to remap /dev/mem (Tetsu Yamamoto ) [430219]
- [x86_64] kprobe: kprobe-booster and return probe-booster (Masami Hiramatsu ) [438725]
- [xen] NUMA: extend physinfo sysctl to export topo info (Tetsu Yamamoto ) [454711]
- [xen] ia64: kludge for XEN_GUEST_HANDLE_64 (Tetsu Yamamoto ) [454711]
- [xen] ia64: NUMA support (Tetsu Yamamoto ) [454711]
- [misc] pipe support to /proc/sys/net/core_pattern (Neil Horman ) [410871]
- [xen] ia64: fix and cleanup move to psr (Tetsu Yamamoto ) [447453]
- [xen] ia64: turn off psr.i after PAL_HALT_LIGHT (Tetsu Yamamoto ) [447453]
- [xen] ia64: fix ia64_leave_kernel (Tetsu Yamamoto ) [447453]
- [xen] page scrub: serialise softirq with a new lock (Tetsu Yamamoto ) [456171]
- [xen] serialize scrubbing pages (Tetsu Yamamoto ) [456171]
- [xen] ia64: don't warn for EOI-ing edge triggered intr (Tetsu Yamamoto ) [430219]
- [xen] ia64: remove regNaT fault message (Tetsu Yamamoto ) [430219]
- [xen] ia64: suppress warning of __assign_domain_page (Tetsu Yamamoto ) [430219]
- [xen] ia64: remove annoying log message (Tetsu Yamamoto ) [430219]
- [xen] ia64: quieter Xen boot (Tetsu Yamamoto ) [430219]
- [xen] ia64: quiet lookup_domain_mpa when domain is dying (Tetsu Yamamoto ) [430219]
- [xen] ia64: fix XEN_SYSCTL_physinfo to handle NUMA info (Tetsu Yamamoto ) [454711]
- [xen] ia64: fixup physinfo (Tetsu Yamamoto ) [454711]

* Sun Sep 07 2008 Don Zickus <dzickus@redhat.com> [2.6.18-109.el5]
- [misc] cpufreq: fix format string bug (Vitaly Mayatskikh ) [459460]
- [x86_64] perfctr: dont use CCCR_OVF_PMI1 on Pentium 4 Ds (Aristeu Rozanski ) [447618]
- [wireless] iwlwifi: fix busted tkip encryption (John W. Linville ) [438388]
- [wireless] ath5k: fixup Kconfig mess from update (John W. Linville ) [445578]
- [fs] cifs: fix O_APPEND on directio mounts (Jeff Layton ) [460063]
- [ia64] oprofile: recognize Montvale cpu as Itanium2 (Dave Anderson ) [452588]
- [block] aoe: use use bio->bi_idx to avoid panic (Tom Coughlan ) [440506]
- [x86] make bare-metal oprofile recognize other platforms (Markus Armbruster ) [458441]
- [scsi] areca: update for RHEL-5.3 (Tomas Henzl ) [436068]
- [sata] prep work for rhel5.3 (David Milburn ) [439247 445727 450962 451586 455445]
- [sata] update driver to 2.6.26-rc5 (David Milburn ) [439247 442906 445727 450962 451586 455445 459197]
- [openib] race between QP async handler and destroy_qp (Brad Peters ) [446109]
- [mm] don't use large pages to map the first 2/4MB of mem (Larry Woodman ) [455504]
- [mm] holdoffs in refresh_cpu_vm_stats using latency test (George Beshers ) [447654]
- [ppc64] cell spufs: fix HugeTLB (Brad Peters ) [439483]
- [ppc64] cell spufs: update with post 2.6.25 patches (Brad Peters ) [439483]
- [xen] ia64 oprofile: recognize Montvale cpu as Itanium2 (Dave Anderson ) [452588]
- [xen] x86: make xenoprof recognize other platforms (Markus Armbruster ) [458441]

* Wed Sep 03 2008 Don Zickus <dzickus@redhat.com> [2.6.18-108.el5]
- [net] NetXen: remove performance optimization fix (Tony Camuso ) [457958]
- [net] NetXen: update to upstream 2.6.27 (tcamuso@redhat.com ) [457958]
- [net] NetXen: fixes from upstream 2.6.27 (tcamuso@redhat.com ) [457958]
- [net] NetXen: cleanups from upstream 2.6.27 (tcamuso@redhat.com ) [457958]
- [fs] anon_inodes implementation (Eduardo Habkost ) [459835]
- [x86] PCI domain support (Jeff Garzik ) [228290]
- [net] udp: possible recursive locking (Hideo AOKI ) [458909]
- [gfs2] multiple writer performance issue (Abhijith Das ) [459738]
- [alsa] asoc: double free and mem leak in i2c codec (Jaroslav Kysela ) [460103]
- [net] ibmveth: cluster membership problems (Brad Peters ) [460379]
- [net] ipv6: drop outside of box loopback address packets (Neil Horman ) [459556]
- [net] dccp_setsockopt_change integer overflow (Vitaly Mayatskikh ) [459235] {CVE-2008-3276}
- [x86] execute stack overflow warning on interrupt stack (Michal Schmidt ) [459810]
- [ppc] export LPAR CPU utilization stats for use by hv (Brad Peters ) [439516]
- [acpi] error attaching device data (peterm@redhat.com ) [459670]
- [md] fix crashes in iterate_rdev (Doug Ledford ) [455471]
- [utrace] signal interception breaks systemtap uprobes (Roland McGrath ) [459786]
- [misc] markers and tracepoints: config patch (jbaron@redhat.com ) [329821]
- [misc] markers and tracepoints: kabi fix-up patch (jbaron@redhat.com ) [329821]
- [misc] markers and tracepoints: probes (jbaron@redhat.com ) [329821]
- [misc] markers and tracepoints: sched patch (jbaron@redhat.com ) [329821]
- [misc] markers and tracepoints: irq patch (jbaron@redhat.com ) [329821]
- [misc] markers and tracepoints: create Module.markers (jbaron@redhat.com ) [329821]
- [misc] markers and tracepoints: markers docs (jbaron@redhat.com ) [329821]
- [misc] markers and tracepoints: markers samples (jbaron@redhat.com ) [329821]
- [misc] markers and tracepoints: markers (jbaron@redhat.com ) [329821]
- [misc] markers and tracepoints: tracepoint samples (jbaron@redhat.com ) [329821]
- [misc] markers and tracepoints: tracepoints (jbaron@redhat.com ) [329821]
- [misc] markers and tracepoints: samples patch (jbaron@redhat.com ) [329821]
- [misc] markers and tracepoints: rcu-read patch (jbaron@redhat.com ) [329821]
- [x86] nmi: fix disable and enable _timer_nmi_watchdog (Aristeu Rozanski ) [447618]
- [x86] nmi: disable LAPIC/IO APIC on unknown_nmi_panic (Aristeu Rozanski ) [447618]
- [x86] nmi: use lapic_adjust_nmi_hz (Aristeu Rozanski ) [447618]
- [x86] nmi: update check_nmi_watchdog (Aristeu Rozanski ) [447618]
- [x86] nmi: update reserve_lapic_nmi (Aristeu Rozanski ) [447618]
- [x86] nmi: use setup/stop routines in suspend/resume (Aristeu Rozanski ) [447618]
- [x86] nmi: change nmi_active usage (Aristeu Rozanski ) [447618]
- [x86] nmi: update nmi_watchdog_tick (Aristeu Rozanski ) [447618]
- [x86] nmi: introduce do_nmi_callback (Aristeu Rozanski ) [447618]
- [x86] nmi: introduce per-cpu wd_enabled (Aristeu Rozanski ) [447618]
- [x86] nmi: add perfctr infrastructure (Aristeu Rozanski ) [447618]
- [x86_64] nmi: add missing prototypes in xen headers (Aristeu Rozanski ) [447618]
- [x86_64] nmi: kill disable_irq calls (Aristeu Rozanski ) [447618]
- [x86_64] nmi: disable LAPIC/IO APIC on unknown_nmi_panic (Aristeu Rozanski ) [447618]
- [x86_64] nmi: use perfctr functions for probing (Aristeu Rozanski ) [447618]
- [x86_64] nmi: update check_nmi_watchdog (Aristeu Rozanski ) [447618]
- [x86_64] nmi: update reserve_lapic_nmi (Aristeu Rozanski ) [447618]
- [x86_64] nmi: use new setup/stop routines in suspend/resume (Aristeu Rozanski ) [447618]
- [x86_64] nmi: change nmi_active usage (Aristeu Rozanski ) [447618]
- [x86_64] nmi: update nmi_watchdog_tick (Aristeu Rozanski ) [447618]
- [x86_64] nmi: setup apic to handle both IO APIC and LAPIC (Aristeu Rozanski ) [447618]
- [x86_64] nmi: introduce do_nmi_callback (Aristeu Rozanski ) [447618]
- [x86_64] nmi: introduce per-cpu wd_enabled (Aristeu Rozanski ) [447618]
- [x86_64] nmi: add perfctr infrastructure (Aristeu Rozanski ) [447618]
- [mm] drain_node_page: drain pages in batch units (George Beshers ) [442179]
- [mm] optimize ZERO_PAGE in 'get_user_pages' and fix XIP (Anton Arapov ) [452668] {CVE-2008-2372}
- [x86_64] UEFI code support (Brian Maly ) [253295]

* Thu Aug 28 2008 Don Zickus <dzickus@redhat.com> [2.6.18-107.el5]
-  [scsi] mptscsi: check for null device in error handler (Doug Ledford ) [441832]
- [openib] ehca: local CA ACK delay has an invalid value (Brad Peters ) [458378]
- [gfs2] fix metafs (Abhijith Das ) [457798]
- [sound] HDMI Audio: new PCI device ID (Bhavna Sarathy ) [459221]
- [s390] cio: memory leak when ccw devices are discarded (Hans-Joachim Picht ) [459495]
- [openib] ehca: handle two completions for one work req (Brad Peters ) [459142]
- [scsi] cciss: possible race condition during init (Ivan Vecera ) [455663]
- [wireless] rtl818x: add driver from 2.6.26 (John W. Linville ) [448764]
- [wireless] rt2x00: add driver from 2.6.26 (John W. Linville ) [448763]
- [wireless] ath5k: add driver from 2.6.26 (John W. Linville ) [445578]
- [wireless] iwlwifi update to version from 2.6.26 (John W. Linville ) [438395]
- [wireless] mac80211 update to version from 2.6.26 (John W. Linville ) [438391 438464 446076]
- [wireless] infrastructure changes for mac80211 update (John W. Linville ) [438391]
- [xen] xennet: coordinate ARP with backend network status (Herbert Xu ) [458934]
- [x86] oprofile: enable additional perf counters (Markus Armbruster ) [426096]
- [wireless] update zd1211rw to last non-mac80211 version (John W. Linville ) [448762]
- [wireless] update bcm43xx driver to 2.6.25 (John W. Linville ) [448762]
- [wireless] update ipw2x00 driver to 2.6.25 (John W. Linville ) [448762]
- [wireless] update ieee80211 to 2.6.25 (John W. Linville ) [448762]
- [xen] hv: support up to 128 cpus (Bill Burns ) [447958]
- [gfs2] rm on multiple nodes causes panic (Bob Peterson ) [458289]
- [gfs2] d_rwdirectempty fails with short read (Benjamin Marzinski ) [456453]
- [sound] snd_seq_oss_synth_make_info info leak (Eugene Teo ) [458001] {CVE-2008-3272}
- Revert: [mm] add support for fast get user pages (Ed Pollard ) [447649]
- [xen] fix GDT allocation for 128 CPUs (Bill Burns ) [447958]
- [xen] fix building with max_phys_cpus=128 (Bill Burns ) [447958]
- [xen] limit dom0 to 32GB by default (Rik van Riel ) [453467]
- [xen] automatically make heap larger on large mem system (Rik van Riel ) [453467]

* Tue Aug 26 2008 Don Zickus <dzickus@redhat.com> [2.6.18-106.el5]
- [x86_64] resume from s3 in text mode with >4GB of mem (Matthew Garrett ) [452961]
- [x86] kdump: calgary iommu: use boot kernel's TCE tables (Tom Coughlan ) [239272]
- [net] neigh_destroy: call destructor before unloading (Brad Peters ) [449161]
- [usb] removing bus with an open file causes an oops (Pete Zaitcev ) [450786]
- [nfs] missing nfs_fattr_init in nfsv3 acl functions (Jeff Layton ) [453711]
- [xen] x86: fix endless loop when GPF (Chris Lalancette ) [457093]
- [dlm] user.c input validation fixes (David Teigland ) [458760]
- [serial] support for Digi PCI-E 4-8port Async IO adapter (Brad Peters ) [439443]
- [cpufreq] acpi: boot crash due to _PSD return-by-ref (John Villalovos ) [428909]
- [x86] io_apic: check timer with irq off (Brian Maly ) [432407]
- [nfs] v4: don't reuse expired nfs4_state_owner structs (Jeff Layton ) [441884]
- [nfs] v4: credential ref leak in nfs4_get_state_owner (Jeff Layton ) [441884]
- [xen] PVFB probe & suspend fixes fix (Markus Armbruster ) [459107]
- [x86] acpi: prevent resources from corrupting memory (Prarit Bhargava ) [458988]
- [mm] add support for fast get user pages (Ed Pollard ) [447649]
- [ipmi] control BMC device ordering (peterm@redhat.com ) [430157]
- [net] pppoe: fix skb_unshare_check call position (Jiri Pirko ) [459062]
-  [net] ipv6: use timer pending to fix bridge ref count (Jiri Pirko ) [457006]
- [nfs] v4: Poll aggressively when handling NFS4ERR_DELAY (Jeff Layton ) [441884]
- [net] ixgbe: fix EEH recovery time (Brad Peters ) [457466]
- [net] pppoe: unshare skb before anything else (Jiri Pirko ) [457018]
- [ppc64] EEH: facilitate vendor driver recovery (Brad Peters ) [457253]
- [ia64] fix to check module_free parameter (Masami Hiramatsu ) [457961]
- [video] make V4L2 less verbose (Mauro Carvalho Chehab ) [455230]
- [autofs4] remove unused ioctls (Ian Kent ) [452139]
- [autofs4] reorganize expire pending wait function calls (Ian Kent ) [452139]
- [autofs4] fix direct mount pending expire race (Ian Kent ) [452139]
- [autofs4] fix indirect mount pending expire race (Ian Kent ) [452139]
- [autofs4] fix pending checks (Ian Kent ) [452139]
- [autofs4] cleanup redundant readdir code (Ian Kent ) [452139]
- [autofs4] keep most direct and indirect dentrys positive (Ian Kent ) [452139]
- [autofs4] fix waitq memory leak (Ian Kent ) [452139]
- [autofs4] check communication pipe is valid for write (Ian Kent ) [452139]
- [autofs4] fix waitq locking (Ian Kent ) [452139]
- [autofs4] fix pending mount race (Ian Kent ) [452139]
- [autofs4] use struct qstr in waitq.c (Ian Kent ) [452139]
- [autofs4] use lookup intent flags to trigger mounts (Ian Kent ) [448869]
- [autofs4] hold directory mutex if called in oz_mode (Ian Kent ) [458749]
- [autofs4] use rehash list for lookups (Ian Kent ) [458749]
- [autofs4] don't make expiring dentry negative (Ian Kent ) [458749]
- [autofs4] fix mntput, dput order bug (Ian Kent ) [452139]
- [autofs4] bad return from root.c:try_to_fill_dentry (Ian Kent ) [452139]
- [autofs4] sparse warn in waitq.c:autofs4_expire_indirect (Ian Kent ) [452139]
- [autofs4] check for invalid dentry in getpath (Ian Kent ) [452139]
- [misc] create a kernel checksum file per FIPS140-2 (Don Zickus ) [444632]
- [net] h323: Fix panic in conntrack module (Thomas Graf ) [433661]
-  [misc] NULL pointer dereference in kobject_get_path (Jiri Pirko ) [455460]
- [audit] new filter type, AUDIT_FILETYPE (Alexander Viro ) [446707]
-  [ppc64] missed hw breakpoints across multiple threads (Brad Peters ) [444076]
- [net] race between neigh_timer_handler and neigh_update (Brad Peters ) [440555]
- [security] NULL ptr dereference in __vm_enough_memory (Jerome Marchand ) [443659]
- [ppc64] cell: spufs update for RHEL-5.3 (Brad Peters ) [439483]
- [misc] null pointer dereference in register_kretprobe (Jerome Marchand ) [452308]
- [alsa] HDA: update to 2008-07-22 (Jaroslav Kysela ) [456215]
- [ia64] xen: handle ipi case IA64_TIMER_VECTOR (Luming Yu ) [451745]
- [misc] batch kprobe register/unregister (Jiri Pirko ) [437579]
- [ia64] add gate.lds to Documentation/dontdiff (Prarit Bhargava ) [449948]
- [xen] fix netloop restriction (Bill Burns ) [358281]
- [nfs] revert to sync writes when background write errors (Jeff Layton ) [438423]
- [ia64] kdump: implement greater than 4G mem restriction (Doug Chapman ) [446188]
- [nfs] clean up short packet handling for NFSv4 readdir (Jeff Layton ) [428720]
- [nfs] clean up short packet handling for NFSv2 readdir (Jeff Layton ) [428720]
- [nfs] clean up short packet handling for NFSv3 readdir (Jeff Layton ) [428720]

* Thu Aug 14 2008 Don Zickus <dzickus@redhat.com> [2.6.18-105.el5]
- [misc] pnp: increase number of devices (Prarit Bhargava ) [445590]
- [ppc] PERR/SERR disabled after EEH error recovery (Brad Peters ) [457468]
- [ppc] eHEA: update from version 0076-05 to 0091-00 (Brad Peters ) [442409]
- [net] modifies inet_lro for RHEL (Brad Peters ) [442409]
- [net] adds inet_lro module (Brad Peters ) [442409]
- [ppc] adds crashdump shutdown hooks (Brad Peters ) [442409]
- [ppc] xmon: setjmp/longjmp code generically available (Brad Peters ) [442409]
- [xen] PV:  config file changes (Don Dutile ) [442991]
- [xen] PV: Makefile and Kconfig additions (Don Dutile ) [442991]
- [xen] PV: add subsystem (Don Dutile ) [442991]
- [xen] PV: shared used header file changes (Don Dutile ) [442991]
- [xen] PV: shared use of xenbus, netfront, blkfront (Don Dutile ) [442991]
- [fs] backport zero_user_segments and friends (Eric Sandeen ) [449668]
- [fs] backport list_first_entry helper (Eric Sandeen ) [449668]
- [ia64] fix boot failure on ia64/sn2 (Luming Yu ) [451745]
- [ia64] move SAL_CACHE_FLUSH check later in boot (Luming Yu ) [451745]
- [ia64] use platform_send_ipi in check_sal_cache_flush (Luming Yu ) [451745]
- [xen] avoid dom0 hang when tearing down domains (Chris Lalancette ) [347161]
- [xen] ia64: SMP-unsafe with XENMEM_add_to_physmap on HVM (Tetsu Yamamoto ) [457137]

* Tue Aug 12 2008 Don Zickus <dzickus@redhat.com> [2.6.18-104.el5]
- [crypto] IPsec memory leak (Vitaly Mayatskikh ) [455238]
- [ppc] edac: add support for Cell processor (Brad Peters ) [439507]
- [ppc] edac: add pre-req support for Cell processor (Brad Peters ) [439507]
- [scsi] DLPAR remove operation fails on LSI SCSI adapter (Brad Peters ) [457852]
- [net] bridge: eliminate delay on carrier up (Herbert Xu ) [453526]
-  [mm] tmpfs: restore missing clear_highpage (Eugene Teo ) [426083]{CVE-2007-6417}
- [scsi] aic94xx: update to 2.6.25 (Ed Pollard ) [439573]
- [fs] dio: lock refcount operations (Jeff Moyer ) [455750]
- [fs] vfs: fix lookup on deleted directory (Eugene Teo ) [457866]{CVE-2008-3275}
- [fs] jbd: fix races that lead to EIO for O_DIRECT (Brad Peters ) [446599]
- [fs] add percpu_counter_add & _sub (Eric Sandeen ) [443896]
- [xen] event channel lock and barrier (Markus Armbruster ) [457086]
- [ppc] adds DSCR support in sysfs (Brad Peters ) [439567]
- [ppc] oprofile: wrong cpu_type returned (Brad Peters ) [441539]
- [s390] utrace: PTRACE_POKEUSR_AREA corrupts ACR0 (Anton Arapov ) [431183]
- [pci] fix problems with msi interrupt management (Michal Schmidt ) [428696]
- [misc] fix wrong test in wait_task_stopped (Jerome Marchand ) [382211]
- [fs] ecryptfs: use page_alloc to get a page of memory (Eric Sandeen ) [457058]
- [misc]  serial: fix break handling for i82571 over LAN (Aristeu Rozanski ) [440018]
- [xen] blktap: expand for longer busids (Chris Lalancette ) [442723]
- [xen] fix blkfront to accept > 16 devices (Chris Lalancette ) [442723]
- [xen] expand SCSI majors in blkfront (Chris Lalancette ) [442077]
- [misc] core dump: remain dumpable (Jerome Marchand ) [437958]
- [fs] inotify: previous event should be last in list (Jeff Burke ) [453990]
- [block] Enhanced Partition Statistics: documentation (Jerome Marchand ) [224322]
- [block] Enhanced Partition Statistics: retain old stats (Jerome Marchand ) [224322]
- [block] Enhanced Partition Statistics: procfs (Jerome Marchand ) [224322]
- [block] Enhanced Partition Statistics: sysfs (Jerome Marchand ) [224322]
- [block] Enhanced Partition Statistics: cpqarray fix (Jerome Marchand ) [224322]
- [block] Enhanced Partition Statistics: cciss fix (Jerome Marchand ) [224322]
- [block] Enhanced Partition Statistics: aoe fix (Jerome Marchand ) [224322]
- [block] Enhanced Partition Statistics: update statistics (Jerome Marchand ) [224322]
- [block] Enhanced Partition Statistics: core statistics (Jerome Marchand ) [224322]
- [fs] add clear_nlink, drop_nlink (Eric Sandeen ) [443896]
- [fs] add buffer_submit_read and bh_uptodate_or_lock (Eric Sandeen ) [443896]
- [fs] noinline_for_stack attribute (Eric Sandeen ) [443896]
- [fs] i_version updates (Eric Sandeen ) [443896]
- [fs] add an ERR_CAST function (Eric Sandeen ) [443896]
- [fs] introduce is_owner_or_cap (Eric Sandeen ) [443896]
- [fs] add generic_find_next_le_bit (Eric Sandeen ) [443896]
- [fs] add le32_add_cpu and friends (Eric Sandeen ) [443896]
- [net] sctp: export needed data to implement RFC 3873 (Neil Horman ) [277111]
- [xen] x86: xenoprof enable additional perf counters (Markus Armbruster ) [426096]

* Thu Aug 07 2008 Don Zickus <dzickus@redhat.com> [2.6.18-103.el5]
- [fs] dio: use kzalloc to zero out struct dio (Jeff Moyer ) [439918]
- [x86] hugetlb: inconsistent get_user_pages (x86 piece) (Brad Peters ) [456449]
- [fs] fix softlockups when repeatedly dropping caches (Bryn M. Reeves ) [444961]
- [char] add hp-ilo driver (Tony Camuso ) [437212]
- [net] do liberal tracking for picked up connections (Anton Arapov ) [448328]
- [scsi] BusLogic: typedef bool to boolean for compiler (Chip Coldwell ) [445095]
- [misc] ioc4: fixes - pci_put_dev, printks, mem resource (Jonathan Lim ) [442424]

* Tue Aug 05 2008 Don Zickus <dzickus@redhat.com> [2.6.18-102.el5]
- [net] slow_start_after_idle influences cwnd validation (Thomas Graf ) [448918]
- [dlm] fix a couple of races (David Teigland ) [457569]
- [net] NetXen driver update to 3.4.18 (Ed Pollard ) [443619]
- [mm] NUMA: system is slow when over-committing memory (Larry Woodman ) [457264]
- [net] ixgbe: remove device ID for unsupported device (Andy Gospodarek ) [454910]
- [ppc] Event Queue overflow on eHCA adapters (Brad Peters ) [446713]
- [ppc] IOMMU Performance Enhancements (Brad Peters ) [439469]
- [ppc] RAS update for Cell (Brad Peters ) [313731]
- [ppc] fast little endian implementation for System p AVE (Brad Peters ) [439505]
- [net] proc: add unresolved discards stat to ndisc_cache (Neil Horman ) [456732]
- [x86_64] ia32: increase stack size (Larry Woodman ) [442331]
- [mm] fix PAE pmd_bad bootup warning (Larry Woodman ) [455434]
- [video] add uvcvideo module (Jay Fenlason ) [439899]
- [crypto] add tests for cipher types to self test module (Neil Horman ) [446514]
- [mm] fix debug printks in page_remove_rmap() (Larry Woodman ) [457458]
- [mm] fix /proc/sys/vm/lowmem_reserve_ratio (Larry Woodman ) [457471]
- [xen] add VPS sync read/write according to spec (Bill Burns ) [437096]
- [xen] use VPS service to take place of PAL call (Bill Burns ) [437096]
- [xen] enable serial console for new ia64 chip (Bill Burns ) [437096]

* Tue Jul 29 2008 Don Zickus <dzickus@redhat.com> [2.6.18-101.el5]
- [ipmi] restrict keyboard I/O port reservation (peterm@redhat.com ) [456300]
- [mm] xpmem: inhibit page swapping under heavy mem use (George Beshers ) [456574]
- [fs] vfs: wrong error code on interrupted close syscalls (Jeff Layton ) [455729]
- [misc] don't randomize when no randomize personality set (Bryn M. Reeves ) [444611]
- [ia64] holdoffs in sn_ack_irq when running latency tests (Jonathan Lim ) [447838]
- [xen] x86: new vcpu_op call to get physical CPU identity (Bhavana Nagendra ) [434548]
- [xen] HV: memory corruption with large number of cpus (Chris Lalancette ) [449945]
- [xen] save phys addr for crash utility (Bill Burns ) [443618]
- [xen] kexec: allocate correct memory reservation (Bill Burns ) [442661]

* Thu Jul 24 2008 Don Zickus <dzickus@redhat.com> [2.6.18-100.el5]
- [gfs2] glock dumping missing out some glocks (Steven Whitehouse ) [456334]
- [scsi] ibmvscsi: add tape device support (Brad Peters ) [439488]
- [misc] irq: reset stats when installing new handler (Eugene Teo ) [456218]
- [scsi] ibmvscsi: latest 5.3 fixes and enhancements (Brad Peters ) [439487]
- [selinux] prevent illegal selinux options when mounting (Eugene Teo ) [456052]
- [xen] remove blktap sysfs entries before shutdown (Chris Lalancette ) [250104]
- [xen] don't collide symbols with blktap (Chris Lalancette ) [250104]
- [xen] blktap: modify sysfs entries to match blkback (Chris Lalancette ) [250104]
- [xen] don't try to recreate sysfs entries (Chris Lalancette ) [250104]
- [xen] blktap: stats error cleanup (Chris Lalancette ) [250104]
- [xen] blktap: add statistics (Chris Lalancette ) [250104]
- [xen] rename blktap kernel threads to blktap.dom.blkname (Chris Lalancette ) [250104]
- [ia64] xen: incompatibility with HV and userspace tools (Tetsu Yamamoto ) [444589]
- [usb] add ids for WWAN cards (John Feeney ) [253137]
- [ia64] handle invalid ACPI SLIT table (Luming Yu ) [451591]
- [pci] mmconfig: use conf1 for access below 256 bytes (Tony Camuso ) [441615 251493]
- [pci] mmconfig: rm pci_legacy_ops and nommconf blacklist (Tony Camuso ) [441615 251493]
- [pci] mmconfig: remove pci_bios_fix_bus_scan_quirk (Tony Camuso ) [441615 251493]
- [fs] nlm: tear down RPC clients in nlm_shutdown_hosts (Jeff Layton ) [254195]
- [fs] nlm: don't reattempt GRANT_MSG with an inflight RPC (Jeff Layton ) [254195]
- [fs] nlm: canceled inflight GRANT_MSG shouldn't requeue (Jeff Layton ) [254195]
- [fs] potential race in mark_buffer_dirty (Mikulas Patocka ) [442577]

* Tue Jul 22 2008 Don Zickus <dzickus@redhat.com> [2.6.18-99.el5]
- [fs] lockd: nlmsvc_lookup_host called with f_sema held (Jeff Layton ) [453094]
- [x86] don't call MP_processor_info for disabled cpu (Prarit Bhargava ) [455425]
- [x86_64] don't call MP_processor_info for disabled cpu (Prarit Bhargava ) [455427]
- [x86] show apicid in /proc/cpuinfo (Prarit Bhargava ) [455424]
- [acpi] disable lapic timer on C2 states (John Villalovos ) [438409]
- [acpi] enable deep C states for idle efficiency (Matthew Garrett ) [443516]
- [fs] missing check before setting mount propagation (Eugene Teo ) [454393]
- [xen] pvfb: frontend mouse wheel support (Markus Armbruster ) [446235]
- [ppc] use ibm,slb-size from device tree (Brad Peters ) [432127]
- [mm] dio: fix cache invalidation after sync writes (Jeff Moyer ) [445674]
- [misc] fix UP compile in skcipher.h (Prarit Bhargava ) [453038]
- [ia64] softlock: prevent endless warnings in kdump (Neil Horman ) [453200]
- [net] s2io: fix documentation about intr_type (Michal Schmidt ) [450921]
- [net] make udp_encap_rcv use pskb_may_pull (Neil Horman ) [350281]
- [misc] fix compile when selinux is disabled (Prarit Bhargava ) [452535]
- [scsi] update aacraid to 1.1.5-2455 (Chip Coldwell ) [429862]
- [x86_64] ptrace: sign-extend orig_rax to 64 bits (Jerome Marchand ) [437882]
- [x86_64] ia32 syscall restart fix (Jerome Marchand ) [434998]
- [misc] optimize byte-swapping, fix -pedantic compile (Jarod Wilson ) [235699]
- [dm] snapshot: reduce default memory allocation (Milan Broz ) [436494]
- [dm] snapshot: fix chunksize sector conversion (Milan Broz ) [443627]
- [net] ip tunnel can't be bound to another device (Michal Schmidt ) [451196]
- [net] bnx2x: chip reset and port type fixes (Andy Gospodarek ) [441259]
- [audit] records sender of SIGUSR2 for userspace (Eric Paris ) [428277]
- [audit] deadlock under load and auditd takes a signal (Eric Paris ) [429941]
- [audit] send EOE audit record at end of syslog events (Eric Paris ) [428275]
- [x86] brk: fix RLIMIT_DATA check (Vitaly Mayatskikh ) [315681]
- [misc] fix ?!/!? inversions in spec file (Jarod Wilson ) [451008]
- [scsi] fix high I/O wait using 3w-9xxx (Tomas Henzl ) [444759]
- [net] ipv6: fix unbalanced ref count in ndisc_recv_ns (Neil Horman ) [450855]
- [fs] cifs: wait on kthread_stop before thread exits (Jeff Layton ) [444865]
- [net] fix the redirected packet if jiffies wraps (Ivan Vecera ) [445536]
- [nfs] pages of a memory mapped file get corrupted (Peter Staubach ) [435291]
- [net] sunrpc: memory corruption from dead rpc client (Jeff Layton ) [432867]
- [fs] debugfs: fix dentry reference count bug (Josef Bacik ) [445787]
- [acpi] remove processor module errors (John Feeney ) [228836]
- [fs] ext3: make fdatasync not sync metadata (Josef Bacik ) [445649]
- [pci] acpiphp_ibm: let ACPI determine _CID buffer size (Prarit Bhargava ) [428874]
- [fs] need process map reporting for swapped pages (Anton Arapov ) [443749]
- [misc] optional panic on softlockup warnings (Prarit Bhargava ) [445422]
- [net] sctp: support remote address table oid (Neil Horman ) [435110]
- [nfs] knfsd: revoke setuid/setgid when uid/gid changes (Jeff Layton ) [443043]
- [nfs] remove error field from nfs_readdir_descriptor_t (Jeff Layton ) [437479]

* Thu Jul 17 2008 Don Zickus <dzickus@redhat.com> [2.6.18-98.el5]
- [nfs] sunrpc: sleeping rpc_malloc might deadlock (Jeff Layton ) [451317]
- [gfs2] initial write performance very slow (Benjamin Marzinski ) [432826]
- [ia64] avoid unnecessary TLB flushes when allocating mem (Doug Chapman ) [435362]
- [gfs2] lock_dlm: deliver callbacks in the right order (Bob Peterson ) [447748]
- [sound] alsa: HDA driver update from upstream 2008-06-11 (Jaroslav Kysela ) [451007]
- [x86_64] xen: fix syscall return when tracing (Chris Lalancette ) [453394]
- [fs] ext3: lighten up resize transaction requirements (Eric Sandeen ) [425955]
- [xen] PVFB probe & suspend fixes (Markus Armbruster ) [434800]
- [nfs] ensure that options turn off attribute caching (Peter Staubach ) [450184]
- [x86_64] memmap flag results in bogus RAM map output (Prarit Bhargava ) [450244]
- [nfs] sunrpc: fix a race in rpciod_down (Jeff Layton ) [448754]
- [nfs] sunrpc: fix hang due to eventd deadlock (Jeff Layton ) [448754]
- [gfs2] d_doio stuck in readv waiting for pagelock (Bob Peterson ) [432057]
- [fs] ext3: fix lock inversion in direct io (Josef Bacik ) [439194]
- [fs] jbd: fix journal overflow issues (Josef Bacik ) [439193]
- [fs] jbd: fix typo in recovery code (Josef Bacik ) [447742]
- [openib] small ipoib packet can cause an oops (Doug Ledford ) [445731]
- [sched] domain range turnable params for wakeup_idle (Kei Tokunaga ) [426971]
- [edac] k8_edac: fix typo in user visible message (Aristeu Rozanski ) [446068]
- [net] ipv6: don't handle default routes specially (Neil Horman ) [426895 243526]
- [fs] ext3: unmount hang when quota-enabled goes error-RO (Eric Sandeen ) [429054]
- [net] ipv6: no addrconf for bonding slaves (Andy Gospodarek ) [236750]
- [misc] fix race in switch_uid and user signal accounting (Vince Worthington ) [441762 440830]
- [misc] /proc/pid/limits : fix duplicate array entries (Neil Horman ) [443522]
- [nfs] v4: fix ref count and signal for callback thread (Jeff Layton ) [423521]
- [mm] do not limit locked memory when using RLIM_INFINITY (Larry Woodman ) [442426]
- [xen] ia64: add srlz instruction to asm (Aron Griffis ) [440261]
- [nfs] fix transposed deltas in nfs v3 (Jeff Layton ) [437544]
- [x86_64] gettimeofday fixes for HPET, PMTimer, TSC (Prarit Bhargava ) [250708]
- [ia64] remove assembler warnings on head.S (Luming Yu ) [438230]
- [misc] allow hugepage allocation to use most of memory (Larry Woodman ) [438889]
- [edac] k8_edac: add option to report GART errors (Aristeu Rozanski ) [390601]
- [ia64] add TIF_RESTORE_SIGMASK and pselect/ppoll syscall (Luming Yu ) [206806]

* Tue Jul 15 2008 Don Zickus <dzickus@redhat.com> [2.6.18-97.el5]
-  [misc] signaling msgrvc() should not pass back error (Jiri Pirko ) [452533]
- [ia64] properly unregister legacy interrupts (Prarit Bhargava ) [445886]
- [s390] zfcp: status read locking race (Hans-Joachim Picht ) [451278]
- [s390] fix race with stack local wait_queue_head_t. (Hans-Joachim Picht ) [451279]
- [s390] cio: fix system hang with reserved DASD (Hans-Joachim Picht ) [451222]
- [s390] cio: fix unusable zfcp device after vary off/on (Hans-Joachim Picht ) [451223]
- [s390] cio: I/O error after cable pulls (Hans-Joachim Picht ) [451281]
- [s390] tape: race condition in tape block device driver (Hans-Joachim Picht ) [451277]
- [gfs2] cannot use fifo nodes (Steven Whitehouse ) [450276]
- [gfs2] bad subtraction in while-loop can cause panic (Bob Peterson ) [452004]
- [tux] crashes kernel under high load (Anton Arapov ) [448973]
- [dlm] move plock code from gfs2 (David Teigland ) [450138]
- [dlm] fix basts for granted CW waiting PR/CW (David Teigland ) [450137]
- [dlm] check for null in device_write (David Teigland ) [450136]
- [dlm] save master info after failed no-queue request (David Teigland ) [450135]
- [dlm] keep cached master rsbs during recovery (David Teigland ) [450133]
- [dlm] change error message to debug (David Teigland ) [450132]
- [dlm] fix possible use-after-free (David Teigland ) [450132]
- [dlm] limit dir lookup loop (David Teigland ) [450132]
- [dlm] reject normal unlock when lock waits on lookup (David Teigland ) [450132]
- [dlm] validate messages before processing (David Teigland ) [450132]
- [dlm] reject messages from non-members (David Teigland ) [450132]
- [dlm] call to confirm_master in receive_request_reply (David Teigland ) [450132]
- [dlm] recover locks waiting for overlap replies (David Teigland ) [450132]
- [dlm] clear ast_type when removing from astqueue (David Teigland ) [450132]
- [dlm] use fixed errno values in messages (David Teigland ) [450130]
- [dlm] swap bytes for rcom lock reply (David Teigland ) [450130]
- [dlm] align midcomms message buffer (David Teigland ) [450130]
- [dlm] use dlm prefix on alloc and free functions (David Teigland ) [450130]
- [s390] zfcp: memory handling for GID_PN (Hans-Joachim Picht ) [447727]
- [s390] zfcp: out-of-memory handling for status_read req (Hans-Joachim Picht ) [447726]
- [s390] zfcp: deadlock in slave_destroy handler (Hans-Joachim Picht ) [447329]
- [s390] dasd: fix timeout handling in interrupt handler (Hans-Joachim Picht ) [447316]
- [s390] zfcp: fix check for handles in abort handler (Hans-Joachim Picht ) [447331]
- [s390] aes_s390 decrypt may produce wrong results in CBC (Hans-Joachim Picht ) [446191]
- [s390x] CPU Node Affinity (Hans-Joachim Picht ) [447379]
- [gfs2] inode indirect buffer corruption (Bob Peterson ) [345401]
- [s390] cio: avoid machine check vs. not operational race (Hans-Joachim Picht ) [444082]
- [s390] qeth: avoid inconsistent lock state for inet6_dev (Hans-Joachim Picht ) [444077]
- [s390] qdio: missed inb. traffic with online FCP devices (Hans-Joachim Picht ) [444146]
- [s390] qeth: eddp skb buff problem running EDDP guestlan (Hans-Joachim Picht ) [444014]
- [s390] cio: kernel panic in cm_enable processing (Hans-Joachim Picht ) [442032]
- [fs] fix bad unlock_page in pip_to_file() error path (Larry Woodman ) [439917]
- [s390] zfcp: Enhanced Trace Facility (Hans-Joachim Picht ) [439482]
- [s390] dasd: add support for system information messages (Hans-Joachim Picht ) [439441]
- [s390] zcrypt: add support for large random numbers (Hans-Joachim Picht ) [439440]
- [s390] qeth: recovery problems with failing STARTLAN (Hans-Joachim Picht ) [440420]
- [s390] qdio: change in timeout handling during establish (Hans-Joachim Picht ) [440421]
- [s390] lcs: ccl-seq. numbers required for prot. 802.2 (Hans-Joachim Picht ) [440416]
- [s390] dasd: diff z/VM minidisks need a unique UID (Hans-Joachim Picht ) [440402]
- [s390] qeth: ccl-seq. numbers req for protocol 802.2 (Hans-Joachim Picht ) [440227]
- [s390] sclp: prevent console lockup during SE warmstart (Hans-Joachim Picht ) [436967]
- [s390] zcrypt: disable ap polling thread per default (Hans-Joachim Picht ) [435161]
- [s390] zfcp: hold lock on port/unit handle for task cmd (Hans-Joachim Picht ) [434959]
- [s390] zfcp: hold lock on port handle for ELS command (Hans-Joachim Picht ) [434955]
- [s390] zfcp: hold lock on port/unit handle for FCP cmd (Hans-Joachim Picht ) [433537]
- [s390] zfcp: hold lock when checking port/unit handle (Hans-Joachim Picht ) [434953]
- [s390] zfcp: handling of boxed port after physical close (Hans-Joachim Picht ) [434801]
- [s390] dasd: fix ifcc handling (Hans-Joachim Picht ) [431592]
- [s390] cio: introduce timed recovery procedure (Hans-Joachim Picht ) [430593]
- [s390] cio: sense id works with partial hw response (Hans-Joachim Picht ) [430787]
- [s390] zfcp: fix use after free bug (Hans-Joachim Picht ) [412881]
- [s390] cio: add missing reprobe loop end statement (Hans-Joachim Picht ) [412891]
- [s390] zfcp: imbalance in erp_ready_sem usage (Hans-Joachim Picht ) [412831]
- [s390] zfcp: zfcp_erp_action_dismiss will ignore actions (Hans-Joachim Picht ) [409091]
- [s390] zfcp: Units are reported as BOXED (Hans-Joachim Picht ) [412851]
- [s390] zfcp: Reduce flood on hba trace (Hans-Joachim Picht ) [415951]
- [s390] zfcp: Deadlock when adding invalid LUN (Hans-Joachim Picht ) [412841]
- [s390] pav alias disks not detected on lpar (Hans-Joachim Picht ) [416081]

* Thu Jul 10 2008 Don Zickus <dzickus@redhat.com> [2.6.18-96.el5]
- [net] randomize udp port allocation (Eugene Teo ) [454572]
- [tty] add NULL pointer checks (Aristeu Rozanski ) [453154]
- [misc] ttyS1 lost interrupt, stops transmitting v2 (Brian Maly ) [451157]
- [net] sctp: make sure sctp_addr does not overflow (David S. Miller ) [452483]
- [sys] sys_setrlimit: prevent setting RLIMIT_CPU to 0 (Neil Horman ) [437122]
- [net] sit: exploitable remote memory leak (Jiri Pirko ) [446039]
- [x86_64] zero the output of string inst on exception (Jiri Pirko ) [451276] {CVE-2008-2729}
- [net] dccp: sanity check feature length (Anton Arapov ) [447396] {CVE-2008-2358}
- [misc] buffer overflow in ASN.1 parsing routines (Anton Arapov ) [444465] {CVE-2008-1673}
- [x86_64] write system call vulnerability (Anton Arapov ) [433945] {CVE-2008-0598}

* Thu Jul 03 2008 Aristeu Rozanski <arozansk@redhat.com> [2.6.18-95.el5]
- [net] Fixing bonding rtnl_lock screwups (Fabio Olive Leite ) [450219]
- [x86_64]: extend MCE banks support for Dunnington, Nehalem (Prarit Bhargava ) [446673]
- [nfs] address nfs rewrite performance regression in RHEL5 (Eric Sandeen ) [436004]
- [mm] Make mmap() with PROT_WRITE on RHEL5 (Larry Woodman ) [448978]
- [i386]: Add check for supported_cpus in powernow_k8 driver (Prarit Bhargava ) [443853]
- [i386]: Add check for dmi_data in powernow_k8 driver (Prarit Bhargava ) [443853]
- [sata] update sata_svw (John Feeney ) [441799]
- [net] fix recv return zero (Thomas Graf ) [435657]
- [misc] kernel crashes on futex (Anton Arapov ) [435178]

* Wed Jun 04 2008 Don Zickus <dzickus@redhat.com> [2.6.18-94.el5]
- [misc] ttyS1 loses interrupt and stops transmitting (Simon McGrath ) [440121]

* Mon May 19 2008 Don Zickus <dzickus@redhat.com> [2.6.18-93.el5]
- [x86] sanity checking for read_tsc on i386 (Brian Maly ) [443435]
- [xen] netfront: send fake arp when link gets carrier (Herbert Xu ) [441716]
- [net] fix xfrm reverse flow lookup for icmp6 (Neil Horman ) [446250]
- [net] negotiate all algorithms when id bit mask zero (Neil Horman ) [442820]
- [net] 32/64 bit compat MCAST_ sock options support (Neil Horman ) [444582]
- [misc] add CPU hotplug support for relay functions (Kei Tokunaga ) [441523]

* Tue Apr 29 2008 Don Zickus <dzickus@redhat.com> [2.6.18-92.el5]
- [fs] race condition in dnotify (Alexander Viro ) [443440 439759] {CVE-2008-1669 CVE-2008-1375}

* Tue Apr 22 2008 Don Zickus <dzickus@redhat.com> [2.6.18-91.el5]
- [scsi] cciss: allow kexec to work (Chip Coldwell ) [230717]
- [xen] ia64: set memory attribute in inline asm (Tetsu Yamamoto ) [426015]
- [xen] fix VT-x2 FlexPriority (Bill Burns ) [252236]

* Tue Apr 15 2008 Don Zickus <dzickus@redhat.com> [2.6.18-90.el5]
- [x86_64] page faults from user mode are user faults (Dave Anderson ) [442101]
- [ia64] kdump: add save_vmcore_info to INIT path (Neil Horman ) [442368]
- [misc] infinite loop in highres timers (Michal Schmidt ) [440002]
- [net] add aes-ctr algorithm to xfrm_nalgo (Neil Horman ) [441425]
- [x86_64] 32-bit address space randomization (Peter Zijlstra ) [213483]
- Revert: [scsi] qla2xxx: pci ee error handling support (Marcus Barrow ) [441779]
- [pci] revert 'PCI: remove transparent bridge sizing' (Ed Pollard ) [252260]
- [ppc64] eHEA: fixes receive packet handling (Brad Peters ) [441364]

* Tue Apr 08 2008 Don Zickus <dzickus@redhat.com> [2.6.18-89.el5]
- [xen] memory corruption due to VNIF increase (Tetsu Yamamoto ) [441390]
- [crytpo] use scatterwalk_sg_next for xcbc (Thomas Graf ) [439874]
- [video] PWC driver DoS (Pete Zaitcev ) [308531]
- [s390] cio: fix vary off of paths (Hans-Joachim Picht ) [436106]
- [pci] fix MSI interrupts on HT1000 based machines (Doug Ledford ) [438776]
- [s390] cio: CHPID configuration event is ignored (Hans-Joachim Picht ) [431858]
- [x86_64] add phys_base to vmcoreinfo (Muuhh IKEDA ) [439304]
- [wd] disable hpwdt due to nmi problems (Prarit Bhargava ) [438741]
- [nfs] fix the fsid revalidation in nfs_update_inode (Steve Dickson ) [431166]
- [ppc64] SLB shadow buffer error cause random reboots (Brad Peters ) [440085]
- [xen] check num of segments in block backend driver (Bill Burns ) [378291]
- [sata] SB600: add 255-sector limit (Bhavana Nagendra ) [434741]
- [x86_64] fix unprivileged crash on %cs corruption (Jarod Wilson ) [439788]
- [scsi] qla4xxx: update driver version number (Marcus Barrow ) [439316]
- [acpi] only ibm_acpi.c should report bay events (Prarit Bhargava ) [439380]
- [x86] xen: fix SWIOTLB overflows (Stephen C. Tweedie ) [433554]
- [x86] fix mprotect on PROT_NONE regions (Stephen C. Tweedie ) [437412]
- [net] ESP: ensure IV is in linear part of the skb (Thomas Graf ) [427248]
- [x86] fix 4 bit apicid assumption (Geoff Gustafson ) [437820]
- [sata] SB700/SB800 64bit DMA support (Bhavana Nagendra ) [434741]

* Tue Apr 01 2008 Don Zickus <dzickus@redhat.com> [2.6.18-88.el5]
- [pci] hotplug: PCI Express problems with bad DLLPs (Kei Tokunaga ) [433355]
- [net] bnx2x: update 5.2 to support latest firmware (Andy Gospodarek ) [435261]
- [ipsec] use hmac instead of digest_null (Herbert Xu ) [436267]
- [utrace] race crash fixes (Roland McGrath ) [428693 245429 245735 312961]
- [x86_64] EXPORT smp_call_function_single (George Beshers ) [438720]
- [s390] FCP/SCSI write IO stagnates (Jan Glauber ) [437099]
- [net] ipv6: check ptr in ip6_flush_pending_frames (Neil Horman ) [439059]
- [nfs] stop sillyrenames and unmounts from racing (Steve Dickson ) [437302]
- [ppc64] oprofile: add support for Power5+ and later (Brad Peters ) [244719]
- [agp] add cantiga ids (Geoff Gustafson ) [438919]
- [x86] oprofile: support for Penryn-class processors (Geoff Gustafson ) [253056]
- [net] ipv6: fix default address selection rule 3 (Neil Horman ) [438429]
- [audit] fix panic, regression, netlink socket usage (Eric Paris ) [434158]
- [net] eHEA: checksum error fix (Brad Peters ) [438212]
- [s390] fix qeth scatter-gather (Jan Glauber ) [438180]
- [ata] fix SATA IDE mode bug upon resume (Bhavana Nagendra ) [432652]
- [openib] update ipath driver (Doug Ledford ) [253023]
- [openib] update the nes driver from 0.4 to 1.0 (Doug Ledford ) [253023]
- [openib] IPoIB updates (Doug Ledford ) [253023]
- [openib] cleanup of the xrc patch removal (Doug Ledford ) [253023]
- [openib] remove srpt and empty vnic driver files (Doug Ledford ) [253023]
- [openib] enable IPoIB connect mode support (Doug Ledford ) [253023]
- [openib] SDP accounting fixes (Doug Ledford ) [253023]
- [openib] add improved error handling in srp driver (Doug Ledford ) [253023]
- [openib] minor core updates between rc1 and final (Doug Ledford ) [253023]
- [openib] update ehca driver to version 0.25 (Doug Ledford ) [253023]
- [openib] remove xrc support (Doug Ledford ) [253023]
- [ppc64] hardware watchpoints: add DABRX init (Brad Peters ) [438259]
- [ppc64] hardware watchpoints: add DABRX definitions (Brad Peters ) [438259]
- [x86_64] address space randomization (Peter Zijlstra ) [222473]
- [ppc64] fixes removal of virtual cpu from dlpar (Brad Peters ) [432846]
- [mm] inconsistent get_user_pages and memory mapped (Brad Peters ) [408781]
- [s390] add missing TLB flush to hugetlb_cow (Hans-Joachim Picht ) [433799]
- [xen] HV ignoring extended cpu model field (Geoff Gustafson ) [439254]
- [xen] oprofile: support for Penryn-class processors (Geoff Gustafson ) [253056]
- [xen] ia64: HV messages are not shown on VGA console (Tetsu Yamamoto ) [438789]
- [xen] ia64: ftp stress test fixes between HVM/Dom0 (Tetsu Yamamoto ) [426015]
- [xen] ia64: fix kernel panic on systems w/<=4GB RAM (Jarod Wilson ) [431001]

* Tue Mar 25 2008 Don Zickus <dzickus@redhat.com> [2.6.18-87.el5]
- [scsi] qla4xxx: negotiation issues with new switches (Marcus Barrow ) [438032]
- [net] qla3xxx: have link SM use work threads (Marcus Barrow ) [409171]
- [scsi] qla4xxx: fix completion, lun reset code (Marcus Barrow ) [438214]
- [scsi] lpfc: update driver to 8.2.0.22 (Chip Coldwell ) [437050]
- [scsi] lpfc: update driver to 8.2.0.21 (Chip Coldwell ) [437050]
- [block] sg: cap reserved_size values at max_sectors (David Milburn ) [433481]
- Revert: [xen] idle=poll instead of hypercall block (Bill Burns ) [437252]
- [scsi] lpfc: update driver to 8.2.0.20 (Chip Coldwell ) [430600]
- [xen] add warning to 'time went backwards' message (Prarit Bhargava ) [436775]
- [x86] clear df flag for signal handlers (Jason Baron ) [436131]
- [usb] fix iaa watchdog notifications (Bhavana Nagendra ) [435670]
- [usb] new iaa watchdog timer (Bhavana Nagendra ) [435670]

* Tue Mar 18 2008 Don Zickus <dzickus@redhat.com> [2.6.18-86.el5]
- [sound] HDMI device IDs for AMD ATI chipsets (Bhavana Nagendra ) [435658]
- [scsi] fusion: 1078 corrupts data in 36GB mem region (Chip Coldwell ) [436210]
- [GFS2] gfs2_adjust_quota has broken unstuffing code (Abhijith Das ) [434736]
- [docs] add oom_adj and oom_score use to proc.txt (Larry Woodman ) [277151]
- [GFS2] optimise loop in gfs2_bitfit (Bob Peterson ) [435456]
- [crypto] fix SA creation with ESP encryption-only (Thomas Graf ) [436267]
- [crypto] fix SA creation with AH (Thomas Graf ) [435243]
- [ppc64] spufs: invalidate SLB then add a new entry (Brad Peters ) [436336]
- [ppc64] SLB: serialize invalidation against loading (Brad Peters ) [436336]
- [ppc64] cell: remove SPU_CONTEXT_SWITCH_ACTIVE flag (Brad Peters ) [434155]
- Revert: [net] sunrpc: fix hang due to eventd deadlock (Jeff Layton ) [438044]
- [ppc64] broken MSI on cell blades when IOMMU is on (Brad Peters ) [430949]
- [cpufreq] powernow: blacklist bad acpi tables (Chris Lalancette ) [430947]
- [firmware] ibft_iscsi: prevent misconfigured iBFTs (Konrad Rzeszutek ) [430297]
- [xen] HV inside a FV guest, crashes the host (Bill Burns ) [436351]

* Tue Mar 11 2008 Don Zickus <dzickus@redhat.com> [2.6.18-85.el5]
- [xen] ia64: fix kprobes slowdown on single step (Tetsu Yamamoto ) [434558]
- [xen] mprotect performance improvements (Rik van Riel ) [412731]
- [GFS2] remove assertion 'al->al_alloced' failed (Abhijith Das ) [432824]
- [misc] remove unneeded EXPORT_SYMBOLS (Don Zickus ) [295491]
- [net] e1000e: wake on lan fixes (Andy Gospodarek ) [432343]
- [sound] add support for HP-RP5700 model (Jaroslav Kysela ) [433593]
- [scsi] hptiop: fixes buffer overflow, adds pci-ids (Chip Coldwell ) [430662]
- [crypto] xcbc: fix IPsec crash with aes-xcbc-mac (Herbert Xu ) [435377]
- [misc] fix memory leak in alloc_disk_node (Jerome Marchand ) [395871]
- [net] cxgb3: rdma arp and loopback fixes (Andy Gospodarek ) [253449]
- [misc] fix range check in fault handlers with mremap (Vitaly Mayatskikh ) [428971]
- [ia64] fix userspace compile error in gcc_intrin.h (Doug Chapman ) [429074]
- [ppc64] fix xics set_affinity code (Brad Peters ) [435126]
- [scsi] sym53c8xx: use proper struct (Brad Peters ) [434857]
- [ppc64] permit pci error state recovery (Brad Peters ) [434857]
- [misc] fix ALIGN macro (Thomas Graf ) [434940]
- [x86] fix relocate_kernel to not overwrite pgd (Neil Horman ) [346431]
- [net] qla2xxx: wait for flash to complete write (Marcus Barrow ) [434992]
- [ppc64] iommu DMA alignment fix (Brad Peters ) [426875]
- [x86] add HP DL580 G5 to bfsort whitelist (Tony Camuso ) [434792]
- [video] neofb: avoid overwriting fb_info fields (Anton Arapov ) [430254]
- [x86] blacklist systems that need nommconf (Prarit Bhargava ) [433671]
- [sound] add support for AD1882 codec (Jaroslav Kysela ) [429073]
- [scsi] ibmvscsi: set command timeout to 60 seconds (Brad Peters ) [354611]
- [x86] mprotect performance improvements (Rik van Riel ) [412731]
- [fs] nlm: fix refcount leak in nlmsvc_grant_blocked (Jeff Layton ) [432626]
- [net] igb: more 5.2 fixes and backports (Andy Gospodarek ) [252004]
- [net] remove IP_TOS setting privilege checks (Thomas Graf ) [431074]
- [net] ixgbe: obtain correct protocol info on xmit (Andy Gospodarek ) [428230]
- [nfs] fslocations/referrals broken (Brad Peters ) [432690]
- [net] sctp: socket initialization race (Neil Horman ) [426234]
- [net] ipv6: fix IPsec datagram fragmentation (Herbert Xu ) [432314]
- [audit] fix bogus reporting of async signals (Alexander Viro ) [432400]
- [cpufreq] xen: properly register notifier (Bhavana Nagendra ) [430940]
- [x86] fix TSC feature flag check on AMD (Bhavana Nagendra ) [428479]

* Fri Feb 29 2008 Don Zickus <dzickus@redhat.com> [2.6.18-84.el5]
- [xen] x86: revert to default PIT timer (Bill Burns ) [428710]

* Thu Feb 21 2008 Don Zickus <dzickus@redhat.com> [2.6.18-83.el5]
- [xen] x86: fix change frequency hypercall (Bhavana Nagendra ) [430938]
- [xen] resync TSC extrapolated frequency (Bhavana Nagendra ) [430938]
- [xen] new vcpu lock/unlock helper functions (Bhavana Nagendra ) [430938]

* Tue Feb 19 2008 Don Zickus <dzickus@redhat.com> [2.6.18-82.el5]
- [ppc64] X fails to start (Don Zickus ) [433038]

* Tue Feb 12 2008 Don Zickus <dzickus@redhat.com> [2.6.18-81.el5]
- [gfs2] fix calling of drop_bh (Steven Whitehouse ) [432370]
- [nfs] potential file corruption issue when writing (Jeff Layton ) [429755]
- [nfs] interoperability problem with AIX clients (Steve Dickson ) [426804]
- [libata] sata_nv: un-blacklist hitachi drives (David Milburn ) [426044]
- [libata] sata_nv: may send cmds with duplicate tags (David Milburn ) [426044]

* Sun Feb 10 2008 Don Zickus <dzickus@redhat.com> [2.6.18-80.el5]
- [fs] check permissions in vmsplice_to_pipe (Alexander Viro ) [432253] {CVE-2008-0600}

* Fri Feb 08 2008 Don Zickus <dzickus@redhat.com> [2.6.18-79.el5]
- [net] sctp: add bind hash locking to migrate code (Aristeu Rozanski ) [426234]
- [net] ipsec: allow CTR mode use with AES (Aristeu Rozanski ) [430164]
- [net] ipv6: fixes to meet DoD requirements (Thomas Graf ) [431718]
- [module] fix module loader race (Jan Glauber ) [429909]
- [misc] ICH10 device IDs (Geoff Gustafson ) [251083]
- [sound] enable S/PDIF in Fila/Converse - fixlet (John Feeney ) [240783]
- [ide] ide-io: fail request when device is dead (Aristeu Rozanski ) [354461]
- [mm] add sysctl to not flush mmapped pages (Larry Woodman ) [431180]
- [net] bonding: locking fixes and version 3.2.4 (Andy Gospodarek ) [268001]
- [gfs2] reduce memory footprint (Bob Peterson ) [349271]
- [net] e1000e: tweak irq allocation messages (Andy Gospodarek ) [431004]
- [sched] implement a weak interactivity mode (Peter Zijlstra ) [250589]
- [sched] change the interactive interface (Peter Zijlstra ) [250589]
- [ppc] chrp: fix possible strncmp NULL pointer usage (Vitaly Mayatskikh ) [396831]
- [s390] dasd: fix loop in request expiration handling (Hans-Joachim Picht ) [430592]
- [s390] dasd: set online fails if initial probe fails (Hans-Joachim Picht ) [429583]
- [scsi] cciss: update procfs (Tomas Henzl ) [423871]
- [Xen] ia64: stop all CPUs on HV panic part3 (Tetsu Yamamoto ) [426129]

* Tue Feb 05 2008 Don Zickus <dzickus@redhat.com> [2.6.18-78.el5]
- [misc] enable i2c-piix4 (Bhavana Nagendra ) [424531]
- [ide] missing SB600/SB700 40-pin cable support (Bhavana Nagendra ) [431437]
- [isdn] i4l: fix memory overruns (Vitaly Mayatskikh ) [425181]
- [net] icmp: restore pskb_pull calls in receive func (Herbert Xu ) [431293]
- [nfs] reduce number of wire RPC ops, increase perf (Peter Staubach ) [321111]
- [xen] 32-bit pv guest migration can fail under load (Don Dutile ) [425471]
- [ppc] fix mmap of PCI resource with hack for X (Scott Moser ) [229594]
- [md] fix raid1 consistency check (Doug Ledford ) [429747]

* Thu Jan 31 2008 Don Zickus <dzickus@redhat.com> [2.6.18-77.el5]
- [xen] ia64: domHVM with pagesize 4k hangs part2 (Tetsu Yamamoto ) [428124]
- [scsi] qla2xxx: update RH version number (Marcus Barrow ) [431052]
- [ia64] fix unaligned handler for FP instructions (Luming Yu ) [428920]
- [fs] fix locking for fcntl (Ed Pollard ) [430596]
- [isdn] fix possible isdn_net buffer overflows (Aristeu Rozanski ) [392161] {CVE-2007-6063}
- [audit] fix potential SKB invalid truesize bug (Hideo AOKI ) [429417]
- [net] e1000e: disable hw crc stripping (Andy Gospodarek ) [430722]
- [firewire] more upstream fixes regarding rom (Jay Fenlason ) [370421]
- [scsi] qla25xx: incorrect firmware loaded (Marcus Barrow ) [430725]
- [scsi] qla2xxx: updated firmware for 25xxx (Marcus Barrow ) [430729]
- [gfs2] speed up read/write performance (Bob Peterson ) [253990]

* Tue Jan 29 2008 Don Zickus <dzickus@redhat.com> [2.6.18-76.el5]
- [Xen] gnttab: allow more than 3 VNIFs (Tetsu Yamamoto ) [297331]
- [xen] fix /sbin/init to use cpu_possible (Chris Lalancette ) [430310]
- [GFS2] install to root volume should work (Abhijith Das ) [220052]
- [scsi] iscsi: set host template (Mike Christie ) [430130]
- [selinux] harden against null ptr dereference bugs (Eric Paris ) [233021]

* Thu Jan 24 2008 Don Zickus <dzickus@redhat.com> [2.6.18-75.el5]
- [xen] ia64: stop all cpus on hv panic part2 (Tetsu Yamamoto ) [426129]
- [sata] combined mode fix for 5.2 (Peter Martuccelli ) [428945 428708]
- [net] bridge br_if: fix oops in port_carrier_check (Herbert Xu ) [408791]
- [misc] agp: add E7221 pci ids (Dave Airlie ) [216722]
- [ia64] kdump: slave CPUs drop to POD (Jonathan Lim ) [429956]

* Wed Jan 23 2008 Don Zickus <dzickus@redhat.com> [2.6.18-74.el5]
- Revert: [s390] qeth: create copy of skb for modification (Hans-Joachim Picht ) [354861]
- Revert: [xen] allow more than 3 VNIFs (Tetsu Yamamoto ) [297331]
- [nfs] discard pagecache data for dirs on dentry_iput (Jeff Layton ) [364351]
- [net] link_watch: always schedule urgent events (Herbert Xu ) [251527]
- [audit] ratelimit printk messages (Eric Paris ) [428701]
- [misc] kprobes: fix reentrancy (Dave Anderson ) [232489]
- [misc] kprobes: inatomic __get_user and __put_user (Dave Anderson ) [232489]
- [misc] kprobes: support kretprobe blacklist (Dave Anderson ) [232489]
- [misc] kprobes: make probe handler stack unwind correct (Dave Anderson ) [232489]
- [net] ipv6: use correct seed to compute ehash index (Neil Horman ) [248052]
- [scsi] areca: update to latest (Tomas Henzl ) [429877]
- [net] fix potential SKB invalid truesize bug (Hideo AOKI ) [429417]
- [ia64] enable CMCI on hot-plugged processors (Fabio Olive Leite ) [426793]
- [s390] system z large page support (Hans-Joachim Picht ) [318951]
- [mm] introduce more huge pte handling functions (Jan Glauber ) [318951]
- [mm] make page->private usable in compound pages (Jan Glauber ) [318951]
- [net] udp: update infiniband driver (Hideo AOKI ) [223593]
- [net] udp: add memory accounting (Hideo AOKI ) [223593]
- [net] udp: new accounting interface (Hideo AOKI ) [223593]
- [misc] support module taint flag in /proc/modules (Jon Masters ) [253476]
- [scsi] sym53c8xx: add PCI error recovery callbacks (Ed Pollard ) [207977]
- [usb] sierra MC8755: increase HSDPA performance (Ivan Vecera ) [232885]

* Wed Jan 23 2008 Don Zickus <dzickus@redhat.com> [2.6.18-73.el5]
- [xen] ia64: domHVM with pagesize 4k hangs (Tetsu Yamamoto ) [428124]
- [xen] ia64: guest has bad network performance (Tetsu Yamamoto ) [272201]
- [xen] ia64: create 100GB mem guest, HV softlockup (Tetsu Yamamoto ) [251353]
- [xen] ia64: create 100GB mem guest fixes (Tetsu Yamamoto ) [251353]
- [xen] x86-pae: support >4GB memory ia64 fixes (Bhavana Nagendra ) [316371]
- [xen] x86-pae: support >4GB memory (Bhavana Nagendra ) [316371]
- [kABI] RHEL-5.2 updates (Jon Masters ) [282881 284231 252994 371971 403821 264701 422321]
- [ia64] xen: create 100GB mem guest, fix softlockup#2 (Tetsu Yamamoto ) [251353]
- [ia64] xen: create 100GB mem guest, fix softlockup (Tetsu Yamamoto ) [251353]
- [acpi] backport video support from upstream (Dave Airlie ) [428326]
- [audit] break execve records into smaller parts (Eric Paris ) [429692]
- [scsi] qla2xxx fw: driver doesn't login to fabric (Marcus Barrow ) [253477]
- [x86] pci: use pci=norom to disable p2p rom window (Konrad Rzeszutek ) [426033]
- [s390] crypto: new CP assist functions (Hans-Joachim Picht ) [318961]
- [s390] OSA 2 Ports per CHPID support (Hans-Joachim Picht ) [318981]
- [s390] STSI change for capacity provisioning (Hans-Joachim Picht ) [318991]
- [s390] HiperSockets MAC layer routing support (Hans-Joachim Picht ) [319001]
- [scsi] aic94xx: version 1.0.2-2 (Konrad Rzeszutek ) [253301]
- [ppc64] cell: support for Performance Tools part4 (Scott Moser ) [253211]
- [ppc64] cell: support for Performance Tools part3 (Brad Peters ) [253211]
- [ppc64] cell: support for Performance Tools part2 (Scott Moser ) [253211]
- [ppc64] cell: support for Performance Tools part1 (Brad Peters ) [253211]

* Mon Jan 21 2008 Don Zickus <dzickus@redhat.com> [2.6.18-72.el5]
- [ppc64] backport PMI driver for cell blade (Scott Moser ) [279171]
- [fs] ecryptfs: fix dentry handling (Eric Sandeen ) [228341]
- [net] IPV6 SNMP counters fix (Ed Pollard ) [421401]
- [gfs2] lock the page on error (Bob Peterson ) [429168]
- [fs] manually d_move inside of rename() (Peter Staubach ) [427472]
- [dlm] validate lock name length (Patrick Caulfeld ) [409221]
- [net] IPv6 TAHI RH0 RFC5095 update (Thomas Graf ) [426904]
- [mm] using hugepages panics the kernel (Larry Woodman ) [429205]
- [sound] enable HDMI for AMD/ATI integrated chipsets (Bhavana Nagendra ) [428963]
- [net] wireless: introduce WEXT scan capabilities (John W. Linville ) [427528]
- [mm] hugepages: leak due to pagetable page sharing (Larry Woodman ) [428612]
- [nfs] acl support broken due to typo (Steve Dickson ) [429109]
- [ide] hotplug docking support for some laptops (Alan Cox ) [230541]
- [x86] cpufreq: unknown symbol fixes (Rik van Riel ) [427368]
- [mm] prevent cpu lockups in invalidate_mapping_pages (Larry Woodman ) [427798]
- [x86] mmconfig: call pcibios_fix_bus_scan (tcamuso@redhat.com ) [408551]
- [x86] mmconfig: introduce pcibios_fix_bus_scan (tcamuso@redhat.com ) [408551]
- [x86] mmconfig: init legacy pci conf functions (tcamuso@redhat.com ) [408551]
- [x86] mmconfig: add legacy pci conf functions (tcamuso@redhat.com ) [408551]
- [x86] mmconfig: introduce PCI_USING_MMCONF flag (tcamuso@redhat.com ) [408551]
- [x86] mmconfig: remove platforms from the blacklist (tcamuso@redhat.com ) [239673 253288 408551]
- [fs] hfs: make robust to deal with disk corruption (Eric Sandeen ) [213773]
- [acpi] improve reporting of power states (Brian Maly ) [210716]
- [net] e1000: update to lastest upstream (Andy Gospodarek ) [253128]
- [net] e1000e: update to latest upstream (Andy Gospodarek ) [252003]
- [xen] xenoprof: loses samples for passive domains (Markus Armbruster ) [426200]
- [cpufreq] ondemand governor update (Brian Maly ) [309311]
- [input] enable HP iLO2 virtual remote mouse (Alex Chiang ) [250288]
- [misc] ioat: support for 1.9 (John Feeney ) [209411]
- [ppc64] oprofile: power5+ needs unique entry (Scott Moser ) [244719]
- [ppc64] oprofile: distinguish 970MP from other 970s (Scott Moser ) [216458]
- [wd] hpwdt: initial support (pschoell ) [251063]
- [xen] x86: more improved TPR/CR8 virtualization (Bhavana Nagendra ) [251985]
- [xen] domain debugger for VTi (Tetsu Yamamoto ) [426362]
- [xen] virtualize ibr/dbr for PV domains (Tetsu Yamamoto ) [426362]

* Sat Jan 19 2008 Don Zickus <dzickus@redhat.com> [2.6.18-71.el5]
- [scsi] cciss: fix incompatibility with hpacucli (Tomas Henzl ) [426873]
- Revert: [net] udp: update infiniband driver (Hideo AOKI ) [223593]
- Revert: [net] udp: add memory accounting (Hideo AOKI ) [223593]
- Revert: [net] udp: new accounting interface (Hideo AOKI ) [223593]
- Revert: [misc] add a new /proc/modules_taint interface (Jon Masters ) [253476]

* Thu Jan 17 2008 Don Zickus <dzickus@redhat.com> [2.6.18-70.el5]
- [xen] move hvm_maybe_deassert_evtchn_irq early (Don Dutile ) [412721]
- [xen] hvm: tolerate intack completion failure (Don Dutile ) [412721]
- [xen] hvm: evtchn to fake pci interrupt propagation (Don Dutile ) [412721]
- [char] R500 drm support (Dave Airlie ) [429012]
- [x86] correct cpu cache info for Tolapai (Geoff Gustafson ) [426172]
- [ia64] xen: fix bogus IOSAPIC (Doug Chapman ) [246130]
- [misc] enabling a non-hotplug cpu should cause panic (Kei Tokunaga ) [426508]
- [cpufreq] booting with maxcpus=1 panics (Doug Chapman ) [428331]
- [net] fix missing defintions from rtnetlink.h (Neil Horman ) [428143]
- [xen] kdump: fix dom0 /proc/vmcore layout (Neil Horman ) [423731]
- [xen] ia64: access extended I/O spaces from dom0 (Jarod Wilson ) [249629]
- [net] udp: update infiniband driver (Hideo AOKI ) [223593]
- [net] udp: add memory accounting (Hideo AOKI ) [223593]
- [net] udp: new accounting interface (Hideo AOKI ) [223593]
- [xen] idle=poll instead of hypercall block (Markus Armbruster ) [416141]
- [net] get minimum RTO via tcp_rto_min (Anton Arapov ) [427205]
- [xen] fixes a comment only (Bill Burns ) [328321]
- [xen] make dma_addr_to_phys_addr static (Bill Burns ) [328321]
- [xen] allow sync on offsets into dma-mapped region (Bill Burns ) [328321]
- [xen] keep offset in a page smaller than PAGE_SIZE (Bill Burns ) [328321]
- [xen] handle sync invocations on mapped subregions (Bill Burns ) [328321]
- [xen] handle multi-page segments in dma_map_sg (Bill Burns ) [328321]
- [misc] add a new /proc/modules_taint interface (Jon Masters ) [253476]
- [scsi] iscsi: Boot Firmware Table tool support (Konrad Rzeszutek ) [307781]
- [mm] make zonelist order selectable in NUMA (Kei Tokunaga ) [251111]
- [ide] handle DRAC4 hotplug (John Feeney ) [212391]
- [xen] allow more than 3 VNIFs (Tetsu Yamamoto ) [297331]
- [misc] enable support for CONFIG_SUNDANCE (Andy Gospodarek ) [252074]
- [ia64] use thread.on_ustack to determine user stack (Luming Yu ) [253548]
- [xen] export cpu_llc_id as gpl (Rik van Riel ) [429004]
- [md] avoid reading past end of bitmap file (Ivan Vecera ) [237326]
- [acpi] Support external package objs as method args (Luming Yu ) [241899]

* Wed Jan 16 2008 Don Zickus <dzickus@redhat.com> [2.6.18-69.el5]
- [xen] incorrect calculation leads to wrong nr_cpus (Daniel P. Berrange ) [336011]
- [xen] ia64: hv hangs on Corrected Platform Errors (Tetsu Yamamoto ) [371671]
- [xen] ia64: warning fixes when checking EFI memory (Tetsu Yamamoto ) [245566]
- [Xen] ia64: stop all CPUs on HV panic (Tetsu Yamamoto ) [426129]
- [Xen] ia64: failed domHVM creation causes HV hang (Tetsu Yamamoto ) [279831]
- [xen] export NUMA topology info to domains (Bill Burns ) [235848]
- [xen] provide NUMA memory usage information (Bill Burns ) [235850]
- [xen] x86: barcelona hypervisor fixes (Bhavana Nagendra ) [421021]
- [xen] improve checking in vcpu_destroy_pagetables (Bill Burns ) [227614]
- [xen] domain address-size clamping (Bill Burns ) [227614]
- [xen] x86: fix continuation translation for large HC (Bill Burns ) [227614]
- [xen] x86: make HV respect the e820 map < 16M (Chris Lalancette ) [410811]
- [xen] x86: vTPR support and upper address fix (Bill Burns ) [252236]
- [xen] x86: fix hp management support on proliant (Bill Burns ) [415691]
- [xen] x86: improved TPR/CR8 virtualization (Bhavana Nagendra ) [251985]
- [xen] ia64: running java-vm causes dom0 to hang (Tetsu Yamamoto ) [317301]
- [xen] enable nested paging by default on amd-v (Bhavana Nagendra ) [247190]
- [fs] corruption by unprivileged user in directories (Vitaly Mayatskikh ) [428797] {CVE-2008-0001}
- [gfs2] Reduce gfs2 memory requirements (Bob Peterson ) [428291]
- [gfs2] permission denied on first attempt to exec (Abhijith Das ) [422681]
- [openib] OFED 1.3 support (Doug Ledford ) [253023 254027 284861]
- [scsi] qla2xxx: fix bad nvram kernel panic (Marcus Barrow ) [367201]
- [scsi] qla2xxx: fix for infinite-login-retry (Marcus Barrow ) [426327]
- [misc] increase softlockup timeout maximum (George Beshers ) [253124]
- [misc] firewire: latest upstream (Jay Fenlason ) [370421]
- [misc] pci rom: reduce number of failure messages (Jun'ichi "Nick" Nomura ) [217698]
- [s390] pte type cleanup (Hans-Joachim Picht ) [360701]
- [s390] qdio: output queue stall on FCP and net devs (Hans-Joachim Picht ) [354871]
- [s390] qdio: many interrupts on qdio-driven devices (Hans-Joachim Picht ) [360821]
- [s390] qdio: time calculation is wrong (Hans-Joachim Picht ) [360631]
- [s390] crash placing a kprobe on  instruction (Hans-Joachim Picht ) [253275]
- [s390] data corruption on DASD while toggling CHPIDs (Hans-Joachim Picht ) [360611]
- [s390] fix dump on panic for DASDs under LPAR (Hans-Joachim Picht ) [250352]
- [s390] qeth: crash during activation of OSA-cards (Hans-Joachim Picht ) [380981]
- [s390] qeth: hipersockets supports IP packets only (Hans-Joachim Picht ) [329991]
- [s390] cio: Disable chan path measurements on reboot (Hans-Joachim Picht ) [354801]
- [s390] zfcp: remove SCSI devices then adapter (Hans-Joachim Picht ) [382841]
- [s390] zfcp: error messages when LUN 0 is present (Jan Glauber ) [354811]
- [s390] qeth: drop inbound pkt with unknown header id (Hans-Joachim Picht ) [360591]
- [s390] qeth: recognize/handle RC=19 from Hydra 3 OSA (Hans-Joachim Picht ) [354891]
- [char] tpm: cleanups and fixes (Konrad Rzeszutek ) [184784]
- [s390] z/VM monitor stream state 2 (Hans-Joachim Picht ) [253026]
- [s390] support for z/VM DIAG 2FC (Hans-Joachim Picht ) [253034]
- [s390] Cleanup SCSI dumper code part 2 (Hans-Joachim Picht ) [253104]
- [s390] AF_IUCV Protocol support (Jan Glauber ) [228117]
- [s390] z/VM unit-record device driver (Hans-Joachim Picht ) [253121]
- [s390] cleanup SCSI dumper code (Hans-Joachim Picht ) [253104]
- [s390] qeth: skb sg support for large incoming msgs (Hans-Joachim Picht ) [253119]
- [ia64] /proc/cpuinfo of Montecito (Luming Yu ) [251089]

* Sun Jan 13 2008 Don Zickus <dzickus@redhat.com> [2.6.18-68.el5]
- [misc] offline CPU with realtime process running v2 (Michal Schmidt ) [240232]
- Revert: [misc] offlining a CPU with realtime process running (Don Zickus ) [240232]
- [x86] fix build warning for command_line_size (Prarit Bhargava ) [427423]
- [mm] show_mem: include count of pagecache pages (Larry Woodman ) [428094]
- [nfs] Security Negotiation (Steve Dickson ) [253019]
- [net] igb: update to actual upstream version (Andy Gospodarek ) [252004]
- [scsi] cciss: move READ_AHEAD to block layer (Tomas Henzl ) [424371]
- [scsi] cciss: update copyright information (Tomas Henzl ) [423841]
- [scsi] cciss: support new controllers (Tomas Henzl ) [423851]
- [scsi] cciss version change (Tomas Henzl ) [423831]
- [md] dm-mpath: send uevents for path fail/reinstate (dwysocha@redhat.com ) [184778]
- [md] dm-uevent: generate events (Dave Wysochanski ) [184778]
- [md] dm: add uevent to core (dwysocha@redhat.com ) [184778]
- [md] dm: export name and uuid (dwysocha@redhat.com ) [184778]
- [md] dm: kobject backport (Dave Wysochanski ) [184778]
- [sata] rhel5.2 driver update (Jeff Garzik ) [184884 307911]
- [sata] rhel5.2 general kernel prep (Jeff Garzik ) [184884 307911]
- [md] dm: auto loading of dm-mirror log modules (Jonathan Brassow ) [388661]
- [scsi] areca driver update rhel part (Tomas Henzl ) [363961]
- [scsi] areca driver update (Tomas Henzl ) [363961]
- [firewire] limit logout messages in the logs (Jay Fenlason ) [304981]
- - [net] add support for dm9601 (Ivan Vecera ) [251994]
- [ia64] ACPICA: allow Load tables (Luming Yu ) [247596]

* Fri Jan 11 2008 Don Zickus <dzickus@redhat.com> [2.6.18-67.el5]
- [xfrm] drop pkts when replay counter would overflow (Herbert Xu ) [427877]
- [xfrm] rfc4303 compliant auditing (Herbert Xu ) [427877]
- [ipsec] add ICMP host relookup support (Herbert Xu ) [427876]
- [ipsec] added xfrm reverse calls (Herbert Xu ) [427876]
- [ipsec] make xfrm_lookup flags argument a bit-field (Herbert Xu ) [427876]
- [ipv6] esp: discard dummy packets from rfc4303 (Herbert Xu ) [427872]
- [ipv4] esp: discard dummy packets from rfc4303 (Herbert Xu ) [427872]
- [ipsec] add support for combined mode algorithms (Herbert Xu ) [253051]
- [ipsec] allow async algorithms (Herbert Xu ) [253051]
- [ipsec] use crypto_aead and authenc in ESP (Herbert Xu ) [253051]
- [ipsec] add new skcipher/hmac algorithm interface (Herbert Xu ) [253051]
- [ipsec] add async resume support on input (Herbert Xu ) [253051]
- [crypto] aead: add authenc (Herbert Xu ) [253051]
- [ipsec] add async resume support on output (Herbert Xu ) [253051]
- [crypto] xcbc: new algorithm (Herbert Xu ) [253051]
- [crypto] ccm: added CCM mode (Herbert Xu ) [253051]
- [crypto] tcrypt: add aead support (Herbert Xu ) [253051]
- [crypto] ctr: add CTR  block cipher mode (Herbert Xu ) [253051]
- [crypto] hmac: add crypto template implementation (Herbert Xu ) [253051]
- [crypto] tcrypt: hmac template and hash interface (Herbert Xu ) [253051]
- [crypto] tcrypt: use skcipher interface (Herbert Xu ) [253051]
- [crypto] digest: added user api for new hash type (Herbert Xu ) [253051]
- [crypto] cipher: added block ciphers for CBC/ECB (Herbert Xu ) [253051]
- [crypto] cipher: added encrypt_one/decrypt_one (Herbert Xu ) [253051]
- [crypto] seqiv: add seq num IV generator (Herbert Xu ) [253051]
- [crypto] api: add aead crypto type (Herbert Xu ) [253051]
- [crypto] eseqiv: add encrypted seq num IV generator (Herbert Xu ) [253051]
- [crypto] chainiv: add chain IV generator (Herbert Xu ) [253051]
- [crypto] skcipher: add skcipher infrastructure (Herbert Xu ) [253051]
- [crypto] api: add cryptomgr (Herbert Xu ) [253051]
- [crypto] api: add new bottom-level crypto_api (Herbert Xu ) [253051]
- [crypto] api: add new top-level crypto_api (Herbert Xu ) [253051]
- [scsi] mpt fusion: set config_fusion_max=128 (Chip Coldwell ) [426533]
- [xen] ia64: fix ssm_i emulation barrier and vdso pv (Tetsu Yamamoto ) [426015]
- [xen] ia64: cannot create guest having 100GB memory (Tetsu Yamamoto ) [251353]
- [ia64] altix acpi iosapic warning cleanup (George Beshers ) [246130]
- [x86] add pci quirk to HT enabled systems (Neil Horman ) [336371]
- [fs] ecryptfs: check for existing key_tfm at mount (Eric Sandeen ) [228341]
- [fs] ecryptfs: redo dget,mntget on dentry_open fail (Eric Sandeen ) [228341]
- [fs] ecryptfs: upstream fixes (Eric Sandeen ) [228341]
- [fs] ecryptfs: connect sendfile ops (Eric Sandeen ) [228341]
- [fs] ecryptfs: backport to rhel5 netlink api (Eric Sandeen ) [228341]
- [fs] ecryptfs: backport to rhel5 scatterlist api (Eric Sandeen ) [228341]
- [fs] ecryptfs: backport to crypto hash api (Eric Sandeen ) [228341]
- [fs] ecryptfs: backport to rhel5 cipher api (Eric Sandeen ) [228341]
- [fs] ecryptfs: un-constify ops vectors (Eric Sandeen ) [228341]
- [fs] ecryptfs: convert to memclear_highpage_flush (Eric Sandeen ) [228341]
- [fs] ecryptfs: backport to rhel5 memory alloc api (Eric Sandeen ) [228341]
- [fs] ecryptfs: backport sysf API for kobjects/ksets (Eric Sandeen ) [228341]
- [fs] ecryptfs: backport generic_file_aio_read (Eric Sandeen ) [228341]
- [fs] ecryptfs: backport f_path to f_dentry (Eric Sandeen ) [228341]
- [fs] ecryptfs: convert to vfsmount/dentry (Eric Sandeen ) [228341]
- [fs] ecryptfs: stacking functions from upstream vfs (Eric Sandeen ) [228341]
- [fs] ecryptfs: backport from 2.6.24-rc4 (Eric Sandeen ) [228341]
- [firewire] fix uevent to handle hotplug (Jay Fenlason ) [302981]
- [cpufreq] fix non-smp compile and warning (Prarit Bhargava ) [413941]
- [net] r8169: support realtek 8111c and 8101e loms (Ivan Vecera ) [276421 251259 248534 247142 238187]
- specfile: xen - see more than 32 vpcus on x86_64 (Bill Burns) [228572]
- specfile: cleanups, add new build options (Jarod Wilson) [248753 232602 247118]

* Wed Jan 09 2008 Don Zickus <dzickus@redhat.com> [2.6.18-66.el5]
- Fixes: [lockdep] lockstat: core infrastructure (Peter Zijlstra ) [193729]

* Wed Jan 09 2008 Don Zickus <dzickus@redhat.com> [2.6.18-65.el5]
- [audit] add session id to easily correlate records (Eric Paris ) [242813]
- [audit] log uid, auid, and comm in obj_pid records (Eric Paris ) [284531]
- [net] cxgb3: update to latest upstream (Andy Gospodarek ) [253195]
- [net] bnx2x: support Broadcom 10GbE Hardware (Andy Gospodarek ) [253346]
- [misc] enable i2c-piix4 (Bhavana Nagendra ) [424531]
- [net] ixgbe: support for new Intel 10GbE Hardware (Andy Gospodarek ) [252005]
- [net] iwl4965 updates (John W. Linville ) [252981]
- [net] mac80211 updates (John W. Linville ) [253015]
- [net] cfg80211 updates to support mac80211/iwl4965 (John W. Linville ) [252981]
- [net] infrastructure updates to mac80211/iwl4965 (John W. Linville ) [252981 253015 253027 256001]
- [net] NULL dereference in iwl driver (Vitaly Mayatskikh ) [401431] {CVE-2007-5938}
- [scsi] iscsi_tcp update (Mike Christie ) [253989 245823]
- [aio] account for I/O wait properly (Jeff Moyer ) [253337]
- [alsa] disabling microphone in bios panics kernel (John Feeney ) [240783]
- [lockdep] make cli/sti annotation warnings clearer (Peter Zijlstra ) [193729]
- [lockdep] fixup mutex annotations (Peter Zijlstra ) [193729]
- [lockdep] mismatched lockdep_depth/curr_chain_hash (Peter Zijlstra ) [193729]
- [lockdep] avoid lockdep & lock_stat infinite output (Peter Zijlstra ) [193729]
- [lockdep] lockstat: documentation (Peter Zijlstra ) [193729]
- [lockdep] lockstat: better class name representation (Peter Zijlstra ) [193729]
- [lockdep] lockstat: measure lock bouncing (Peter Zijlstra ) [193729]
- [lockdep] fixup sk_callback_lock annotation (Peter Zijlstra ) [193729]
- [lockdep] various fixes (Peter Zijlstra ) [193729]
- [lockdep] lockstat: hook into the lock primitives (Peter Zijlstra ) [193729]
- [lockdep] lockstat: human readability tweaks (Peter Zijlstra ) [193729]
- [lockdep] lockstat: core infrastructure (Peter Zijlstra ) [193729]
- [lockdep] sanitise CONFIG_PROVE_LOCKING (Peter Zijlstra ) [193729]
- [misc] fix raw_spinlock_t vs lockdep (Peter Zijlstra ) [193729]
- [alsa] support for realtek alc888s (Brian Maly ) [251253]
- [xen] save/restore: pv oops when mmap prot_none (Chris Lalancette ) [294811]
- [net] dod ipv6 conformance (Neil Horman ) [253278]
- [audit] log eintr, not erestartsys (Eric Paris ) [234426]
- [misc] ipmi: panic handling enhancement (Geoff Gustafson ) [277121]
- [misc] fix softlockup warnings/crashes (Chris Lalancette ) [250994]
- [misc] core dump masking support (Takahiro Yasui ) [223616]
- [fs] executing binaries with >2GB debug info (Dave Anderson ) [224679]
- [sched] return first time_slice to correct process (Vitaly Mayatskikh ) [238035]

* Tue Jan 08 2008 Don Zickus <dzickus@redhat.com> [2.6.18-64.el5]
- Fixes: [kexec] fix vmcoreinfo patch that breaks kdump (Neil Horman ) [424511]
- Fixes: [fs] nfs: byte-range locking support for cfs (Konrad Rzeszutek ) [196318]

* Mon Jan 07 2008 Don Zickus <dzickus@redhat.com> [2.6.18-63.el5]
- [scsi] lpfc:  update to version 8.2.0.13 (Chip Coldwell ) [426281]
- [scsi] qla2xxx: rediscovering luns takes 5 min (Marcus Barrow ) [413211]
- [misc] edac: add support for intel 5000 mchs (Aristeu Rozanski ) [249335]
- [fs] ext3: error in ext3_lookup if corruption found (Eric Sandeen ) [181662]
- [scsi] stex: use resid for xfer len information (Prarit Bhargava ) [251557]
- [scsi] qla2xxx: msi-x hardware issues on platforms (Marcus Barrow ) [253629]
- [net] ipv6: ip6_mc_input: sense of promiscuous test (Neil Horman ) [390071]
- [x86] Add warning to nmi failure message (Prarit Bhargava ) [401631]
- [misc] enable s/pdif in fila/converse (John Feeney ) [240783]
- [scsi] qla2xxx: add support for npiv - firmware (Marcus Barrow ) [249618]
- [scsi] qla2xxx: pci ee error handling support (Marcus Barrow ) [253267]
- [scsi] qla2xxx: add support for npiv (Marcus Barrow ) [249618]
- [scsi] mpt fusion: fix sas hotplug (Chip Coldwell ) [253122]
- [misc] export radix-tree-preload (George Beshers ) [422321]
- [net] forcedeth: boot delay fix (Andy Gospodarek ) [405521]
- [kexec] fix vmcoreinfo patch that breaks kdump (Neil Horman ) [424511]
- Revert: [misc] add vmcoreinfo support to kernel (Neil Horman ) [253850]
- [scsi] mpt fusion: update to version 3.04.05+ (Chip Coldwell ) [253122]
- [scsi] mpt fusion: add accessor for version 3.04.05+ (Chip Coldwell ) [253122]
- [scsi] mpt fusion: pci ids for version 3.04.05+ (Chip Coldwell ) [253122]
- [misc] offlining a CPU with realtime process running (Michal Schmidt ) [240232]
- [misc] ioat dma: support unisys (Ivan Vecera ) [248767]
- [md] dm ioctl: fix 32bit compat layer (Milan Broz ) [360441]
- [ppc64] enable CONFIG_FB_RADEON (Scott Moser ) [281141]
- [audit] race checking audit_context and loginuid (Eric Paris ) [241728]
- [scsi] update megaraid_sas to version 3.15 (Tomas Henzl ) [243154]
- [x86_64] calioc2 iommu support (Konrad Rzeszutek ) [253302]
- [x86] cpuinfo: list dynamic acceleration technology (Geoff Gustafson ) [252229]
- [ppc64] unequal allocation of hugepages (Scott Moser ) [239790]
- [md] fix bitmap support (Doug Ledford ) [210178]
- [misc] tlclk driver for telco blade systems (Geoff Gustafson ) [233512]
- [fs] nfs: byte-range locking support for cfs (Konrad Rzeszutek ) [196318]
- [x86_64] nmi watchdog: incorrect logic for amd chips (Prarit Bhargava ) [391741]
- [x86] edac: add support for Intel i3000 (Aristeu Rozanski ) [295501]
- [mm] fix hugepage allocation with memoryless nodes (Scott Moser ) [239790]
- [mm] make compound page destructor handling explicit (Scott Moser ) [239790]
- [scsi] qla2xxx: more improvements and cleanups part2 (Marcus Barrow ) [253272]
- [scsi] qla2xxx: 8 GB/S support (Marcus Barrow ) [249796]
- [scsi] qla2xxx: upstream improvements and cleanups (Marcus Barrow ) [253272]
- [ppc64] ehea: sync with upstream (Scott Moser ) [253414]
- [ia64] fix kernel warnings from rpm prep stage (Luming Yu ) [208271]

* Thu Dec 20 2007 Don Zickus <dzickus@redhat.com> [2.6.18-62.el5]
- [xen] ia64: hvm guest memory range checking (Jarod Wilson ) [408711]
- [xen] x86: support for architectural pstate driver (Bhavana Nagendra ) [419171]
- [xen] disable cpu freq scaling when vcpus is small (Rik van Riel ) [251969]
- [xen] hv: cpu frequency scaling (Rik van Riel ) [251969]
- [xen] ia64: vulnerability of copy_to_user in PAL emu (Jarod Wilson ) [425939]
- [net] bonding: documentation update (Andy Gospodarek ) [235711]
- [net] bonding: update to upstream version 3.2.2 (Andy Gospodarek ) [251902 236750 268001]
- [misc] utrace: update for 5.2 (Roland McGrath ) [299941 309461 309551 309761]
- [ia64] ptrace: access to user register backing (Roland McGrath ) [237749]
- [ia64] utrace: forbid ptrace changes psr.ri to 3 (Roland McGrath ) [247174]
- [net] bnx2: update to upstream version 1.6.9 (Andy Gospodarek ) [251109]
- [net] tg3: update to upstream version 3.86 (Andy Gospodarek ) [253344]
- [net] sunrpc: make clients take ref to rpciod workq (Jeff Layton ) [246642]
- [scsi] aacraid: update to 1.1.5-2453 (Chip Coldwell ) [364371]
- [md] dm-mirror: write_callback might deadlock (Jonathan Brassow ) [247877]
- [md] dm-mirror: shedule_timeout call causes slowdown (Jonathan Brassow ) [358881]
- [md] mirror presuspend causing cluster mirror hang (Jonathan Brassow ) [358871]
- [acpi] docking/undocking: oops when _DCK eval fails (John Feeney ) [252214]
- [acpi] docking/undocking: check if parent is on dock (John Feeney ) [252214]
- [acpi] docking/undocking: error handling in init (John Feeney ) [252214]
- [acpi] docking/undocking: add sysfs support (John Feeney ) [252214]
- [acpi] docking/undocking support (John Feeney ) [252214]
- [xen] support for architectural pstate driver (Bhavana Nagendra ) [419171]
- [usb] wacom: fix 'side' and 'extra' mouse buttons (Aristeu Rozanski ) [249415]
- [audit] netmask on xfrm policy configuration changes (Eric Paris ) [410531]
- [xen] rapid block device plug/unplug leads to crash (Don Dutile ) [308971]
- [net] fix refcnt leak in optimistic dad handling (Neil Horman ) [423791]
- [net] ixgb: resync upstream and transmit hang fixes (Andy Gospodarek ) [252002]
- [xen] kernel: cpu frequency scaling (Rik van Riel ) [251969]
- [md] dm snapshot: excessive memory usage (Milan Broz ) [421451]
- [md] dm-crypt: possible max_phys_segments violation (Milan Broz ) [421441]
- [xen] xenbus has use-after-free (Don Dutile ) [249728]
- [fs] cifs: update CHANGES file and version string (Jeff Layton ) [417961]
- [fs] cifs: endian conversion problem in posix mkdir (Jeff Layton ) [417961]
- [fs] cifs: corrupt data with cached dirty page write (Jeff Layton ) [329431]
- [fs] cifs: missing mount helper causes wrong slash (Jeff Layton ) [417961]
- [fs] cifs: fix error message about packet signing (Jeff Layton ) [417961]
- [fs] cifs: shut down cifsd when signing mount fails (Jeff Layton ) [417961]
- [fs] cifs: reduce corrupt list in find_writable_file (Jeff Layton ) [417961]
- [fs] cifs: fix memory leak in statfs to old servers (Jeff Layton ) [417961]
- [fs] cifs: buffer overflow due to corrupt response (Jeff Layton ) [373001]
- [fs] cifs: log better errors on failed mounts (Jeff Layton ) [417961]
- [fs] cifs: oops on second mount to same server (Jeff Layton ) [373741]
- [fs] cifs: fix spurious reconnect on 2nd peek (Jeff Layton ) [417961]
- [fs] cifs: bad handling of EAGAIN on kernel_recvmsg (Jeff Layton ) [336501]
- [fs] cifs: small fixes to make cifs-1.50c compile (Jeff Layton ) [417961]
- [net] cifs: stock 1.50c import (Jeff Layton ) [417961]
- [nfs4] client: set callback address properly (Steve Dickson ) [264721]
- [sched] fair scheduler (Peter Zijlstra ) [250589]
- [net] s2io: correct VLAN frame reception (Andy Gospodarek ) [354451]
- [net] s2io: allow VLAN creation on interfaces (Andy Gospodarek ) [354451]
- [mm] soft lockups when allocing mem on large systems (Doug Chapman ) [281381]
- [md] dm mpath: hp retry if not ready (Dave Wysochanski ) [208261]
- [md] dm mpath: add retry pg init (Dave Wysochanski ) [208261]
- [md] dm mpath: add hp handler (Dave Wysochanski ) [208261]
- [x86] fix race with 'endflag' in NMI setup code (Prarit Bhargava ) [357391]
- [xen] fix behavior of invalid guest page mapping (Markus Armbruster ) [254208]
- [misc] tux: get rid of O_ATOMICLOOKUP (Michal Schmidt ) [358661]
- [misc] Denial of service with wedged processes (Jerome Marchand ) [229882]
- [x86_64] fix race conditions in setup_APIC_timer (Geoff Gustafson ) [251869]

* Sat Dec 15 2007 Don Zickus <dzickus@redhat.com> [2.6.18-61.el5]
- [net] sunhme: fix failures on x86 (John W. Linville ) [254234]
- [ppc64] power6 SPURR support (Scott Moser ) [253114]
- [usb] fix for error path in rndis (Pete Zaitcev ) [236719]
- [ipmi] legacy ioport setup changes (Peter Martuccelli ) [279191]
- [ipmi] add PPC SI support (Peter Martuccelli ) [279191]
- [ipmi] remove superfluous semapahore from watchdog (Peter Martuccelli ) [279191]
- [ipmi] do not enable interrupts too early (Peter Martuccelli ) [279191]
- [ipmi] fix memory leak in try_init_dmi (Peter Martuccelli ) [279191]
- [net] sunrpc: lockd recovery is broken (Steve Dickson ) [240976]
- [fs] core dump file ownership (Don Howard ) [397001]
- [cpufreq] don't take sem in cpufreq_quick_get (Doug Chapman ) [253416]
- [cpufreq] remove hotplug cpu cruft (Doug Chapman ) [253416]
- [cpufreq] governor: use new rwsem locking in work cb (Doug Chapman ) [253416]
- [cpufreq] ondemand governor restructure the work cb (Doug Chapman ) [253416]
- [cpufreq] rewrite lock to eliminate hotplug issues (Doug Chapman ) [253416]
- [ppc64] spufs: context destroy vs readdir race (Scott Moser ) [387841]
- [scsi] update lpfc driver to 8.2.0.8 (Chip Coldwell ) [252989]
- [ppc64] utrace: fix PTRACE_GETVRREGS data (Roland McGrath ) [367221]
- [scsi] ipr: add dual SAS RAID controller support (Scott Moser ) [253398]
- [net] backport of functions for sk_buff manipulation (Andy Gospodarek ) [385681]
- [gfs2] recursive locking on rgrp in gfs2_rename (Abhijith Das ) [404711]
- [gfs2] check kthread_should_stop when waiting (David Teigland ) [404571]
- [dlm] don't print common non-errors (David Teigland ) [404561]
- [dlm] tcp: bind connections from known local address (David Teigland ) [358841]
- [dlm] block dlm_recv in recovery transition (David Teigland ) [358821]
- [dlm] fix memory leak in dlm_add_member (David Teigland ) [358791]
- [dlm] zero unused parts of sockaddr_storage (David Teigland ) [358771]
- [dlm] dump more lock values (David Teigland ) [358751]
- [gfs2] remove permission checks from xattr ops (Ryan O'Hara ) [307431]
- [x86] report_lost_ticks fix up (Prarit Bhargava ) [394581]
- [ppc64] SLB shadow buffer support (Scott Moser ) [253112]
- [ppc64] handle alignment faults on new FP load/store (Scott Moser ) [253111]
- [xen] PVFB frontend can send bogus screen updates (Markus Armbruster ) [370341]
- [nfs] let rpciod finish sillyrename then umount (Steve Dickson ) [253663]
- [nfs] fix a race in silly rename (Steve Dickson ) [253663]
- [nfs] clean up the silly rename code (Steve Dickson ) [253663]
- [nfs] infrastructure changes for silly renames (Steve Dickson ) [253663]
- [nfs] introducde nfs_removeargs and nfs_removeres (Steve Dickson ) [253663]
- [xen] avoid dom0 hang when disabling pirq's (Chris Lalancette ) [372741]
- [ppc64] cell: support for msi on axon (Scott Moser ) [253212]
- [ppc64] cell: enable rtas-based ptcal for xdr memory (Scott Moser ) [253212]
- [ppc64] cell: ddr2 memory driver for axon (Scott Moser ) [253212]
- [ppc64] spu: add temperature and throttling support (Scott Moser ) [279171]
- [ppc64] sysfs: support for add/remove cpu sysfs attr (Scott Moser ) [279171]
- [ppc64] cbe_cpufreq: fixes from 2.6.23-rc7 (Scott Moser ) [279171]
- [ppc64] typo with mmio_read_fixup (Scott Moser ) [253208]
- [ppc64] spufs: feature updates (Scott Moser ) [253208]
- [ppc64] export last_pid (Scott Moser ) [253208]
- [ppc64] cell: support pinhole-reset on blades (Scott Moser ) [253208]
- [s390] use IPL CLEAR for reipl under z/VM (Hans-Joachim Picht ) [386991]
- [net] sunrpc: fix hang due to eventd deadlock (Jeff Layton ) [246642]
- [misc] : misrouted interrupts deadlocks (Dave Anderson ) [247379]
- [fs] ignore SIOCIFCOUNT ioctl calls (Josef Bacik ) [310011]
- [ppc64] fixes PTRACE_SET_DEBUGREG request (Roland McGrath ) [253117]
- [fs] dm crypt: memory leaks and workqueue exhaustion (Milan Broz ) [360621]
- [md] dm: panic on shrinking device size (Milan Broz ) [360151]
- [md] dm: bd_mount_sem counter corruption (Milan Broz ) [360571]
- [fs] udf: fix possible leakage of blocks (Eric Sandeen ) [221282]
- [fs] udf: Fix possible data corruption (Eric Sandeen ) [221282]
- [fs] udf: support files larger than 1G (Eric Sandeen ) [221282]
- [fs] udf: add assertions (Eric Sandeen ) [221282]
- [fs] udf: use get_bh (Eric Sandeen ) [221282]
- [fs] udf: introduce struct extent_position (Eric Sandeen ) [221282]
- [fs] udf: use sector_t and loff_t for file offsets (Eric Sandeen ) [221282]
- [misc] use touch_softlockup_watchdog when no nmi wd (Prarit Bhargava ) [367251]
- [misc] backport upstream softlockup_tick code (Prarit Bhargava ) [367251]
- [misc] pass regs struct to softlockup_tick (Prarit Bhargava ) [336541]
- [misc] fix bogus softlockup warnings (Prarit Bhargava ) [252360]
- [x86] use pci=bfsort for certain boxes (Michal Schmidt ) [242990]
- [x86] Change command line size to 2048 (Prarit Bhargava ) [247477]
- [misc] systemtap uprobes: access_process_vm export (Frank Ch. Eigler ) [424991]
- [nfs] fix ATTR_KILL_S*ID handling on NFS (Jeff Layton ) [222330]
- [mm] oom: prevent from killing several processes (Larry Woodman ) [392351]

* Fri Dec 14 2007 Don Zickus <dzickus@redhat.com> [2.6.18-60.el5]
- [xen] x86: suppress bogus timer warning (Chris Lalancette ) [317201]
- [xen] ia64: saner default mem and cpu alloc for dom0 (Jarod Wilson ) [248967]
- [xen] x86_64: add stratus hooks into memory (Kimball Murray ) [247833]
- [ia64] mm: register backing store bug (Luming Yu ) [310801]
- [serial] irq -1 assigned to serial port (Luming Yu ) [227728]
- [utrace] s390 regs fixes (Roland McGrath ) [325451]
- [x86] use pci=bfsort on Dell R900 (Michal Schmidt ) [242990]
- [nfs] server support 32-bit client and 64-bit inodes (Peter Staubach ) [253589]
- [nfs] support 32-bit client and 64-bit inode numbers (Peter Staubach ) [253589]
- [dlm] Don't overwrite castparam if it's NULL (Patrick Caulfield ) [318061]
- [s390] panic with lcs interface as dhcp server (Hans-Joachim Picht ) [350861]
- [s390] qeth: do not free memory on failed init (Hans-Joachim Picht ) [330211]
- [s390] qeth: default performace_stats attribute to 0 (Hans-Joachim Picht ) [248897]
- [s390] qeth: create copy of skb for modification (Hans-Joachim Picht ) [354861]
- [s390] qeth: up sequence number for incoming packets (Hans-Joachim Picht ) [354851]
- [s390] qeth: use correct MAC address on recovery (Hans-Joachim Picht ) [241276]
- [s390] cio: handle invalid subchannel setid in stsch (Hans-Joachim Picht ) [354831]
- [s390] cio: Dynamic CHPID reconfiguration via SCLP (Hans-Joachim Picht ) [253120]
- [s390] cio: fix memory leak when deactivating (Hans-Joachim Picht ) [213272]
- [s390] cio: Device status validity (Hans-Joachim Picht ) [354821]
- [s390] cio: reipl fails after channel path reset (Hans-Joachim Picht ) [231306]
- [usb] reset LEDs on Dell keyboards (Pete Zaitcev ) [228674]
- [x86] hotplug: PCI memory resource mis-allocation (Konrad Rzeszutek ) [252260]
- [ppc64] Make the vDSO handle C++ unwinding correctly (David Howells ) [420551]
- [ppc64] add AT_NULL terminator to auxiliary vector (Vitaly Mayatskikh ) [231442]
- [x86] Add Greyhound Event based Profiling support (Bhavana Nagendra ) [314611]
- [nfs] reset any fields set in attrmask (Jeff Layton ) [242482]
- [nfs] Set attrmask on NFS4_CREATE_EXCLUSIVE reply (Jeff Layton ) [242482]
- [fs] proc: add /proc/<pid>/limits (Neil Horman ) [253762]
- [xen] ia64: make ioremapping work (Jarod Wilson ) [240006]
- [ia64] bte_unaligned_copy transfers extra cache line (Luming Yu ) [218298]
- [xen] inteface with stratus platform op (Kimball Murray ) [247841]
- [mm] xen: export xen_create_contiguous_region (Kimball Murray ) [247839]
- [mm] xen: memory tracking cleanups (Kimball Murray ) [242514]

* Tue Dec 11 2007 Don Zickus <dzickus@redhat.com> [2.6.18-59.el5]
- [net] ipv6: backport optimistic DAD (Neil Horman ) [246723]
- [crypto] aes: Rename aes to aes-generic (Herbert Xu ) [245954]
- [xen] ia64: fix free_irq_vector: double free (Aron Griffis ) [208599]
- [selinux] don't oops when using non-MLS policy (Eric Paris ) [223827]
- [net] qla3xxx: new 4032 does not work with VLAN (Marcus Barrow ) [253785]
- [ide] SB700 contains two IDE channels (Bhavana Nagendra ) [314571]
- [edac] fix return code in e752x_edac probe function (Aristeu Rozanski ) [231608]
- [scsi] cciss: disable refetch on P600 (Aron Griffis ) [251563]
- [misc] Intel Tolapai SATA and I2C support (Ivan Vecera ) [251086]
- [net] ibmveth: Checksum offload support (Scott Moser ) [254035]
- [misc] Allow a hyphenated range for isolcpus (Jonathan Lim ) [328151]
- [misc] sched: force /sbin/init off isolated cpus (Jonathan Lim ) [328091]
- [ia64] contig: show_mem cleanup output (George Beshers ) [221612]
- [ia64] discontig: show_mem cleanup output (George Beshers ) [221612]
- [ia64] show_mem printk cleanup (George Beshers ) [221612]
- [net] ppp_mppe: avoid using a copy of interim key (Michal Schmidt ) [248716]
- [ppc64] mpstat reports wrong per-processor stats (Scott Moser ) [212234]
- [net] labeled: memory leak calling secid_to_secctx (Eric Paris ) [250442]
- [misc] /proc/<pid>/environ stops at 4k bytes (Anton Arapov ) [308391]
- [net] kernel needs to support TCP_RTO_MIN (Anton Arapov ) [303011]
- [x86_64] kdump: shutdown gart on k8 systems (Prarit Bhargava ) [264601]
- [input] psmouse: add support to 'cortps' protocol (Aristeu Rozanski ) [248759]
- [nfs] nfs_symlink: allocate page with GFP_HIGHUSER (Jeff Layton ) [245042]
- [ia64] enable kprobe's trap code on slot 1 (Masami Hiramatsu ) [207107]
- [misc] Fix relay read start in overwrite mode (Masami Hiramatsu ) [250706]
- [misc] Fix relay read start position (Masami Hiramatsu ) [250706]
- [x86_64] 'ide0=noprobe' crashes the kernel (Michal Schmidt ) [241338]
- [ia64] proc/iomem wiped out on non ACPI kernel (George Beshers ) [257001]
- [net] CIPSO packets generate kernel unaligned access (Luming Yu ) [242955]
- [ia64] ioremap: fail mmaps with incompat attributes (Jarod Wilson ) [240006]
- [ia64] ioremap: allow cacheable mmaps of legacy_mem (Jarod Wilson ) [240006]
- [ia64] ioremap: avoid unsupported attributes (Jarod Wilson ) [240006]
- [ia64] ioremap: rename variables to match i386 (Jarod Wilson ) [240006]
- [ia64] validate and remap mmap requests (Jarod Wilson ) [240006]
- [ia64] kdump: deal with empty image (Doug Chapman ) [249724]
- [net] NetXen: allow module to unload (Konrad Rzeszutek ) [245751]
- [net] clean up in-kernel socket api usage (Neil Horman ) [246851]
- [hotplug] slot poweroff problem on systems w/o _PS3 (Prarit Bhargava ) [410611]
- [PPC64] kdump: fix irq distribution on ppc970 (Jarod Wilson ) [208659]
- [serial] support PCI Express icom devices (Chris Snook ) [243806]
- [xen] Rebase HV to 15502 (Bill Burns) [318891]

* Wed Nov 27 2007 Don Zickus <dzickus@redhat.com> [2.6.18-58.el5]
- Updated: [net] panic when mounting with insecure ports (Anton Arapov ) [294881]
- [kabitool] - fail on missing symbols (Jon Masters)

* Wed Nov 21 2007 Don Zickus <dzickus@redhat.com> [2.6.18-57.el5]
- [misc] lockdep: fix seqlock_init (Peter Zijlstra ) [329851]
- [ppc64] Remove WARN_ON from disable_msi_mode() (Scott Moser ) [354241]
- [GFS2] sysfs  file should contain device id (Bob Peterson ) [363901]
- [x86_64] update IO-APIC dest field to 8-bit for xAPIC (Dave Anderson ) [224373]
- [ia64] add global ACPI OpRegion handler for fw calls (Doug Chapman ) [262281]
- [ia64] add driver for ACPI methods to call native fw (Doug Chapman ) [262281]
- [ppc64] eHEA: ibm,loc-code not unique (Scott Moser ) [271821]
- [ata] SB800 SATA/IDE LAN support (Bhavana Nagendra ) [252961]
- [net] ibmveth: enable large rx buf pool for large mtu (Scott Moser ) [250827]
- [net] ibmveth: h_free_logical_lan err on pool resize (Scott Moser ) [250827]
- [net] ibmveth: fix rx pool deactivate oops (Scott Moser ) [250827]
- [gfs2] Fix ordering of page lock and transaction lock (Steven Whitehouse ) [303351]
- [net] panic when mounting with insecure ports (Anton Arapov ) [294881]
- [ia64] fix vga corruption with term blanking disabled (Jarod Wilson ) [291421]
- [ppc64] panic on DLPAR remove of eHEA (Scott Moser ) [253767]
- [ppc64] boot Cell blades with >2GB memory (Scott Moser ) [303001]
- [x86_64] Add NX mask for PTE entry (Jarod Wilson ) [232748]
- [hotplug] acpiphp: System error during PCI hotplug (Konrad Rzeszutek ) [243003]
- [misc] softirq: remove spurious BUG_ON's (Jarod Wilson ) [221554]
- [audit] collect events for segfaulting programs (Eric Paris ) [239061]
- [misc] cfq-iosched: fix deadlock on nbd writes (Jarod Wilson ) [241540]
- [scsi] stale residual on write following BUSY retry (Jonathan Lim ) [300871]
- ext3: orphan list check on destroy_inode (Eric Sandeen ) [269401]
- [scsi] always update request data_len with resid (George Beshers ) [282781]
- [misc] add vmcoreinfo support to kernel (Neil Horman ) [253850]
- [ia64] remove stack hard limit (Aron Griffis ) [251043]
- [fs] Fix unserialized task->files changing (Vitaly Mayatskikh ) [253866]
- [ide] allow disabling of drivers (Gerd Hoffmann ) [247982]
- [net] fail multicast with connection oriented socket (Anton Arapov ) [259261]
- [net] fix race condition in netdev name allocation (Neil Horman ) [247128]
- [char] tty: set pending_signal on return -ERESTARTSYS (Aristeu Rozanski ) [253873]
- [fs] aio: account for I/O wait properly (Jeff Moyer ) [253337]
- [x86_64] Switching to vsyscall64 causes oops (Jeff Burke ) [224541]
- [net] lvs syncdaemon causes high avg load on system (Anton Arapov ) [245715]
- [i2c] SB600/700/800 use same SMBus controller devID (Bhavana Nagendra ) [252286]
- [acpi] sbs: file permissions set incorrectly (Vitaly Mayatskikh ) [242565]
- [net] ipv6: support RFC4193 local unicast addresses (Neil Horman ) [252264]
- [misc] serial: fix console hang on HP Integrity (Doug Chapman ) [244054]
- [tux] fix crashes during shutdown (Ernie Petrides ) [244439]
- [usb] Support for EPiC-based io_edgeport devices (Jarod Wilson ) [249760]
- [misc] Prevent NMI watchdog triggering during sysrq-T (Konrad Rzeszutek ) [248392]
- [hotplug] acpiphp: 'cannot get bridge info' with PCIe (Konrad Rzeszutek ) [248571]
- [misc] serial: assert DTR for serial console devices (Michal Schmidt ) [244728]
- [net] sctp: rewrite receive buffer management code (Neil Horman ) [246722]
- [net] NetXen: MSI: failed interrupt after fw enabled (Konrad Rzeszutek ) [246019]
- [cifs] make demux thread ignore signals from userspace (Jeff Layton ) [245674]
- [ia64] misc DBS cleanup (Luming Yu ) [245217]
- [misc] Remove non-existing SB600 raid define (Prarit Bhargava ) [244038]

* Tue Nov 13 2007 Don Zickus <dzickus@redhat.com> [2.6.18-56.el5]
- [fs] missing dput in do_lookup error leaks dentries (Eric Sandeen ) [363491] {CVE-2007-5494}
- [ppc] System cpus stuck in H_JOIN after migrating (Scott Moser ) [377901]
- [scsi] ibmvSCSI: Unable to continue migrating lpar after errors (Scott Moser ) [377891]
- [scsi] ibmvSCSI: client can't handle deactive/active device from server (Scott Moser ) [257321]
- [audit] still allocate contexts when audit is disabled (Alexander Viro ) [360841]

* Tue Nov 06 2007 Don Zickus <dzickus@redhat.com> [2.6.18-55.el5]
- Revert [misc] Denial of service with wedged processes (Jerome Marchand ) [229882] {CVE-2006-6921}
- [autofs4] fix race between mount and expire (Ian Kent ) [354621]
- [net] ieee80211: off-by-two integer underflow (Anton Arapov ) [346401] {CVE-2007-4997}
- [fs] sysfs: fix race condition around sd->s_dentry (Eric Sandeen ) [243728] {CVE-2007-3104}
- [fs] sysfs: fix condition check in sysfs_drop_dentry() (Eric Sandeen ) [243728] {CVE-2007-3104}
- [fs] sysfs: store inode nrs in s_ino (Eric Sandeen ) [243728] {CVE-2007-3104}
- [nfs] v4: umounts oops in shrink_dcache_for_umount (Steve Dickson ) [254106]
- [net] tg3: Fix performance regression on 5705 (Andy Gospodarek ) [330181]
- [net] forcedeth: MSI interrupt bugfix (Andy Gospodarek ) [353281]
- [ppc] kexec/kdump kernel hung on Power5+ and Power6 (Scott Moser ) [245346]

* Mon Oct 22 2007 Don Zickus <dzickus@redhat.com> [2.6.18-54.el5]
- [misc] Denial of service with wedged processes (Jerome Marchand ) [229882] {CVE-2006-6921}
- [alsa] Convert snd-page-alloc proc file to use seq_file (Jerome Marchand ) [297771] {CVE-2007-4571}
- [x86] Fixes for the tick divider patch (Chris Lalancette ) [315471]
- [mm] ia64: flush i-cache before set_pte (Luming Yu ) [253356]
- [fs] jbd: wait for t_sync_datalist buffer to complete (Eric Sandeen ) [250537]
- [audit] improper handling of audit_log_start return values (Eric Paris ) [335731]
- [cifs] fix memory corruption due to bad error handling (Jeff Layton ) [336501]
- [net] bnx2: Add PHY workaround for 5709 A1 (Andy Gospodarek ) [317331]

* Wed Oct 10 2007 Don Zickus <dzickus@redhat.com> [2.6.18-53.el5]
- [GFS2] handle multiple demote requests (Wendy Cheng ) [295641]
- [scsi] megaraid_sas: kabi fix for /proc entries (Chip Coldwell ) [323231]
- [sound] allow creation of null parent devices (Brian Maly ) [323771]

* Wed Sep 26 2007 Don Zickus <dzickus@redhat.com> [2.6.18-52.el5]
- [net] iwlwifi: avoid BUG_ON in tx cmd queue processing (John W. Linville ) [306831]
- [GFS2] Get super block a different way (Steven Whitehouse ) [306621]

* Tue Sep 25 2007 Don Zickus <dzickus@redhat.com> [2.6.18-51.el5]
- [GFS2] dlm: schedule during recovery loops (David Teigland ) [250464]
- Revert: [pata] IDE (siimage) panics when DRAC4 reset (John Feeney ) [212391]

* Mon Sep 24 2007 Don Zickus <dzickus@redhat.com> [2.6.18-50.el5]
- Revert: [net] bonding: convert timers to workqueues (Andy Gospodarek ) [210577]
- [pata] enable IDE (siimage) DRAC4 (John Feeney ) [212391]
- [GFS2] gfs2_writepage(s) workaround (Wendy Cheng ) [252392]
- [scsi] aacraid: Missing ioctl() permission checks (Vitaly Mayatskikh ) [298381] {CVE-2007-4308}
- [GFS2] Solve journaling/{release|invalidate}page issues (Steven Whitehouse ) [253008]
- [x86_64] syscall vulnerability (Anton Arapov ) [297881] {CVE-2007-4573}
- [GFS2] Fix i_cache stale entry (Wendy Cheng ) [253756]
- [GFS2] deadlock running revolver load with lock_nolock (Benjamin Marzinski ) [288581]
- [net] s2io: check for error_state in ISR (more) (Scott Moser ) [276871]

* Thu Sep 20 2007 Don Zickus <dzickus@redhat.com> [2.6.18-49.el5]
- [sata] libata probing fixes and other cleanups (Jeff Garzik ) [260281]
- [net] cxgb3: backport fixups and sysfs corrections (Andy Gospodarek ) [252243]

* Mon Sep 17 2007 Don Zickus <dzickus@redhat.com> [2.6.18-48.el5]
- [net] s2io: check for error_state in ISR (Scott Moser ) [276871]
- [fs] ext3: ensure do_split leaves enough free space in both blocks (Eric Sandeen ) [286501]
- [kabi] whitelist GFS2 export symbols to allow driver updates (Jon Masters) [282901]
- [gfs2] allow process to handle multiple flocks on a file (Abhijith Das ) [272021]
- [gfs2] operations hang after mount--RESEND (Bob Peterson ) [276631]
- [scsi] qlogic: fix nvram/vpd update memory corruptions (Marcus Barrow ) [260701]
- [fs] Reset current->pdeath_signal on SUID binary execution (Peter Zijlstra) [251119] {CVE-2007-3848}
- [gfs2] mount hung after recovery (Benjamin Marzinski ) [253089]
- [GFS2] Move inode delete logic out of blocking_cb (Wendy Cheng ) [286821]
- [dlm] Make dlm_sendd cond_resched more (Patrick Caulfield ) [250464]
- [x86_64] fix 32-bit ptrace access to debug registers (Roland McGrath ) [247427]
- [autofs4] fix deadlock during directory create (Ian Kent ) [253231]
- [nfs] enable 'nosharecache' mounts fixes (Steve Dickson ) [243913]
- [usb] usblcd: Locally triggerable memory consumption (Anton Arapov ) [276011] {CVE-2007-3513}
- [misc] Bounds check ordering issue in random driver (Anton Arapov ) [275971] {CVE-2007-3105}

* Tue Sep 11 2007 Don Zickus <dzickus@redhat.com> [2.6.18-47.el5]
- [ppc64] Fix SPU slb size and invalidation on hugepage faults (Scott Moser ) [285981]
- [s390] qdio: Refresh buffer states for IQDIO Asynch output queue (Hans-Joachim Picht ) [222181]
- [scsi] fusion: allow VMWare's emulator to work again (Chip Coldwell ) [279571]

* Mon Sep 10 2007 Don Zickus <dzickus@redhat.com> [2.6.18-46.el5]
- [XEN] x86: 32-bit ASID mode hangs dom0 on AMD (Chris Lalancette ) [275371]
- [scsi] megaraid_sas: intercept cmd timeout and throttle io (Chip Coldwell ) [245184 247581]
- [s390] hypfs: inode corruption due to missing locking (Brad Hinson ) [254169]
- [Xen] Allow 32-bit Xen to kdump >4G physical memory (Stephen C. Tweedie ) [251341]
- [ptrace] NULL pointer dereference triggered by ptrace (Anton Arapov ) [275991] {CVE-2007-3731}
- [XEN] ia64: allocating with GFP_KERNEL in interrupt context fix (Josef Bacik ) [279141]

* Tue Sep 04 2007 Don Zickus <dzickus@redhat.com> [2.6.18-45.el5]
- [XEN] Update spec file to provide specific xen ABI version (Stephen C. Tweedie ) [271981]
- [scsi] qla2xxx: nvram/vpd updates produce soft lockups and system hangs (Marcus Barrow ) [260701]
- [scsi] iscsi: borked kmalloc  (Mike Christie ) [255841]
- [net] qla3xxx: Read iSCSI target disk fail (Marcus Barrow ) [246123]
- [net] igmp: check for NULL when allocating GFP_ATOMIC skbs (Neil Horman ) [252404]
- [mm] madvise call to kernel loops forever (Konrad Rzeszutek ) [263281]

* Mon Aug 27 2007 Don Zickus <dzickus@redhat.com> [2.6.18-44.el5]
- [misc] re-export some symbols as EXPORT_SYMBOL_GPL (Jon Masters ) [252377]
- [xen] ia64: set NODES_SHIFT to 8 (Doug Chapman ) [254050]
- [xen] Fix privcmd to remove nopage handler (Chris Lalancette ) [249409]
- [xen] increase limits to boot on large ia64 platforms (Doug Chapman ) [254062]
- [autofs] autofs4 - fix race between mount and expire (Ian Kent ) [236875]
- [nfs] NFS4: closes and umounts are racing (Steve Dickson ) [245062]
- [GFS2] Fix lock ordering of unlink (Steven Whitehouse ) [253609]
- [openib] Fix two ipath controllers on same subnet (Doug Ledford ) [253005]
- [net] tg3: update to fix suspend/resume problems (Andy Gospodarek ) [253988]
- [GFS2] distributed mmap test cases deadlock (Benjamin Marzinski ) [248480]
- [GFS2] Fix inode meta data corruption (Wendy Cheng ) [253590]
- [GFS2] bad mount option causes panic with NULL superblock pointer (Abhijith Das ) [253921]
- [fs] hugetlb: fix prio_tree unit (Konrad Rzeszutek ) [253930]
- [misc] Microphone stops working (John Feeney ) [240716]
- [GFS2] glock dump dumps glocks for all file systems (Abhijith Das ) [253238]
- [scsi] qla2xxx: disable MSI-X by default (Marcus Barrow ) [252410]

* Tue Aug 21 2007 Don Zickus <dzickus@redhat.com> [2.6.18-43.el5]
- [XEN] remove assumption first numa node discovered is node0 (Jarod Wilson ) [210078]

* Mon Aug 20 2007 Don Zickus <dzickus@redhat.com> [2.6.18-42.el5]
- [GFS2] More problems unstuffing journaled files (Bob Peterson ) [252191]
- [DLM] Reuse connections rather than freeing them (Patrick Caulfield ) [251179]
- [ppc] EEH: better status string detection (Scott Moser ) [252405]
- [scsi] cciss: set max command queue depth (Tomas Henzl ) [251167]
- [audit] Stop multiple messages from being printed (Eric Paris ) [252358]
- [scsi] uninitialized field in gdth.c (Chip Coldwell ) [245550]
- [scsi] SATA RAID 150-4/6 do not support 64-bit DMA (Chip Coldwell ) [248327]
- [gfs2] fix truncate panic (Wendy Cheng ) [251053]
- [gfs2] panic after can't parse mount arguments  (Benjamin Marzinski ) [253289]
- [fs] CIFS: fix deadlock in cifs_get_inode_info_unix (Jeff Layton ) [249394]
- [sound] support ad1984 codec (Brian Maly ) [252373]
- [scsi] fix iscsi write handling regression (Mike Christie ) [247827]
- [ppc] Fix detection of PCI-e based devices (Doug Ledford ) [252085]
- [gfs2] unstuff quota inode (Abhijith Das ) [250772]
- [net] fix DLPAR remove of eHEA logical port (Scott Moser ) [251370]
- [gfs2] hang when using a large sparse quota file (Abhijith Das ) [235299]
- [x86_64] Fix MMIO config space quirks (Bhavana Nagendra ) [252397]
- [misc] Convert cpu hotplug notifiers to use raw_notifier (Peter Zijlstra ) [238571]
- [sound] fix panic in hda_codec (Brian Maly ) [251854]
- [mm] separate mapped file and anonymous pages in show_mem() output. (Larry Woodman ) [252033]
- [misc] Fix broken AltSysrq-F (Larry Woodman ) [251731]
- [scsi] cciss: increase max sectors to 2048 (Tomas Henzl ) [248121]
- Revert [gfs2] remounting w/o acl option leaves acls enabled (Bob Peterson ) [245663]

* Thu Aug 16 2007 Don Zickus <dzickus@redhat.com> [2.6.18-41.el5]
- Revert [ia64] validate and remap mmap requests (Jarod Wilson ) [240006]

* Tue Aug 14 2007 Don Zickus <dzickus@redhat.com> [2.6.18-40.el5]
- [net] s2io: update to driver version 2.0.25.1 (Andy Gospodarek ) [223033]
- [XEN] ia64: use panic_notifier list (Kei Tokunaga ) [250456]
- [XEN] ia64: support nvram (Kei Tokunaga ) [250203]
- [XEN] Allow dom0 to boot with greater than 2 vcpus (Kei Tokunaga ) [250441]
- [XEN] Fix MCE errors on AMD-V (Bhavana Nagendra ) [251435]
- [XEN] set correct paging bit identifier when NP enabled (Chris Lalancette ) [250857]
- [XEN] ia64: fix for hang when running gdb (Doug Chapman ) [246482]
- [XEN] AMD-V fix for W2k3 guest w/ Nested paging (Bhavana Nagendra ) [250850]
- [XEN] blktap tries to access beyond end of disk (Kei Tokunaga ) [247696]
- [ia64] fsys_gettimeofday leaps days if it runs with nojitter (Luming Yu ) [250825]
- [x86] Blacklist for HP DL585G2 and HP dc5700 (Tony Camuso ) [248186]
- [misc] Missing critical phys_to_virt in lib/swiotlb.c (Anton Arapov ) [248102]
- [mm] Prevent the stack growth into hugetlb reserved regions (Konrad Rzeszutek ) [247658]
- [scsi] fix qla4xxx underrun and online handling (Mike Christie ) [242828]
- [sound] Audio playback does not work (John Feeney ) [250269]
- [XEN] ia64: allow guests to vga install (Jarod Wilson ) [249076]
- [net] forcedeth: optimize the tx data path (Andy Gospodarek ) [252034]
- [agp] 945/965GME: bridge id, bug fix, and cleanups (Geoff Gustafson ) [251166]
- [net] tg3: pci ids missed during backport (Andy Gospodarek ) [245135]
- [misc] workaround for qla2xxx vs xen swiotlb (Rik van Riel ) [219216]
- [XEN] netfront: Avoid deref'ing skb after it is potentially freed. (Herbert Xu ) [251905]
- [ia64] validate and remap mmap requests (Jarod Wilson ) [240006]
- [ppc] DLPAR REMOVE I/O resource failed (Scott Moser ) [249617]
- [XEN] ia64: Cannot use e100 and IDE controller (Kei Tokunaga ) [250454]
- [wireless] iwlwifi: update to version 1.0.0 (John W. Linville ) [223560 250675]
- [ppc] make eHCA driver use remap_4k_pfn in 64k kernel (Scott Moser ) [250496]
- [audit] sub-tree signal handling fix (Alexander Viro ) [251232]
- [audit] sub-tree memory leaks (Alexander Viro ) [251160]
- [audit] sub-tree cleanups (Alexander Viro ) [248416]
- [GFS2] invalid metadata block (Bob Peterson ) [248176]
- [XEN] use xencons=xvc by default on non-x86 (Aron Griffis ) [249100]
- [misc] i915_dma: fix batch buffer security bit for i965 chipsets (Aristeu Rozanski ) [251188] {CVE-2007-3851}
- [Xen] Fix restore path for 5.1 PV guests (Chris Lalancette ) [250420]
- [x86] Support mobile processors in fid/did to frequency conversion (Bhavana Nagendra ) [250833]
- [dlm] fix basts for granted PR waiting CW (David Teigland ) [248439]
- [scsi] PCI shutdown for cciss driver (Chip Coldwell ) [248728]
- [scssi] CCISS support for P700m (Chip Coldwell ) [248735]
- [net] forcedeth: fix nic poll (Herbert Xu ) [245191]
- [ppc] 4k page mapping support for userspace 	in 64k kernels (Scott Moser ) [250144]
- [net] tg3: small update for kdump fix (Andy Gospodarek ) [239782]
- [ppc] Cope with PCI host bridge I/O window not starting at 0 (Scott Moser ) [242937]
- [ata]: Add additional device IDs for SB700 (Prarit Bhargava ) [248109]
- [fs] - fix VFAT compat ioctls on 64-bit systems (Eric Sandeen ) [250666] {CVE-2007-2878}
- [fs] - Move msdos compat ioctl to msdos dir (Eric Sandeen ) [250666]

* Thu Aug 09 2007 Don Zickus <dzickus@redhat.com> [2.6.18-39.el5]
- [net] e1000: add support for Bolton NICs (Bruce Allan ) [251221]
- [net] e1000: add support for HP Mezzanine cards (Bruce Allan ) [251214]
- [net] igb: initial support for igb netdriver (Andy Gospodarek ) [244758]
- [net] e1000e: initial support for e1000e netdriver (Andy Gospodarek ) [240086]

* Fri Aug 03 2007 Don Zickus <dzickus@redhat.com> [2.6.18-38.el5]
- [ppc] No Boot/Hang response for PCI-E errors (Scott Moser ) [249667]
- [GFS2] Reduce number of gfs2_scand processes to one (Steven Whitehouse ) [249905]
- [scsi] Adaptec: Add SC-58300 HBA PCI ID (Konrad Rzeszutek ) [249275]
- [GFS2] Fix bug relating to inherit_jdata flag on inodes (Steven Whitehouse ) [248576]
- [ppc] Disable PCI-e completion timeouts on I/O Adapters (Scott Moser ) [232004]
- [x86] Fix tscsync frequency transitions (Bhavana Nagendra ) [245082]
- [CIFS] respect umask when unix extensions are enabled (Jeff Layton ) [246667]
- [CIFS] fix signing sec= mount options (Jeff Layton ) [246595]
- [XEN] netloop: Do not clobber cloned skb page frags (Herbert Xu ) [249683]

* Mon Jul 30 2007 Don Zickus <dzickus@redhat.com> [2.6.18-37.el5]
- [net] Using mac80211 in ad-hoc mode can result in a kernel panic (John W. Linville ) [223558]
- [ppc] Axon memory does not handle double bit errors (Scott Moser ) [249910]
- [xen] x86: HV workaround for invalid PAE PTE clears (Chris Lalancette ) [234375]
- [scsi] Update stex driver (Jeff Garzik ) [241074]
- [scsi] cciss: Re-add missing kmalloc (Prarit Bhargava ) [249104]
- [GFS2] Fix an oops in the glock dumping code (Steven Whitehouse ) [248479]
- [GFS2] locksmith/revolver deadlocks (Steven Whitehouse ) [249406]
- [xen] race loading xenblk.ko and scanning for LVM partitions (Richard Jones ) [247265]

* Fri Jul 20 2007 Don Zickus <dzickus@redhat.com> [2.6.18-36.el5]
- [NFS] Re-enable force umount (Steve Dickson ) [244949]
- [sata] regression in support for third party modules (Jeff Garzik ) [248382]
- [utrace] set zombie leader to EXIT_DEAD before release_task (Roland McGrath ) [248621]

* Wed Jul 18 2007 Don Zickus <dzickus@redhat.com> [2.6.18-35.el5]
- [XEN] fix time going backwards in gettimeofday (Rik van Riel ) [245761]
- [GFS2] soft lockup in rgblk_search (Bob Peterson ) [246114]
- [DLM] fix NULL reference in send_ls_not_ready (David Teigland ) [248187]
- [DLM] Clear othercon pointers when a connection is closed (David Teigland ) [220538]

* Thu Jul 12 2007 Don Zickus <dzickus@redhat.com> [2.6.18-34.el5]
- [wireless] iwlwifi: add driver (John W. Linville ) [223560]
- [XEN] make crashkernel=foo@16m work (Gerd Hoffmann ) [243880]
- [XEN] ia64: HV built with crash_debug=y does not boot on NUMA machine (Kei Tokunaga ) [247843]
- [edac] allow edac to panic with memory corruption on non-kdump kernels (Don Zickus ) [237950]
- [GFS2] Mounted file system won't suspend (Steven Whitehouse ) [192082]
- [GFS2] soft lockup detected in databuf_lo_before_commit (Bob Peterson ) [245832]
- [sata] Add Hitachi HDS7250SASUN500G 0621KTAWSD to NCQ blacklist (Prarit Bhargava ) [247627]
- [PCI] unable to reserve mem region on module reload (Scott Moser ) [247701 247400]
- [PPC] eHEA driver can cause kernel panic on recv of VLAN packets (Scott Moser ) [243009]
- [PPC] Fix 64K pages with kexec on native hash table (Scott Moser ) [242550]
- Reverts: Mambo driver on ppc64 [208320]

* Mon Jul 09 2007 Don Zickus <dzickus@redhat.com> [2.6.18-33.el5]
- [XEN] ia64: Windows guest cannot boot with debug mode (Kei Tokunaga ) [245668]
- [XEN] ia64: SMP Windows guest boot fails sometimes (Kei Tokunaga ) [243870]
- [XEN] ia64: Dom0 boot fails on NUMA hardware (Kei Tokunaga ) [245275]
- [XEN] ia64: Windows guest sometimes panic by incorrect ld4.s emulation (Kei Tokunaga ) [243865]
- [XEN] ia64: boot 46 GuestOS makes Dom0 hang (Kei Tokunaga ) [245667]
- [XEN] ia64: HVM guest hangs on vcpu migration (Kei Tokunaga ) [233971]
- [XEN] ia64: Cannot create guest domain due to rid problem (Kei Tokunaga ) [242040]
- [XEN] ia64: HVM domain creation panics if xenheap is not enough. (Kei Tokunaga ) [240108]
- [XEN] ia64: DomU panics by save/restore (Kei Tokunaga ) [243866]
- [XEN] ia64: Guest OS hangs on IPF montetito (Kei Tokunaga ) [245637]
- [xen] Guest access to MSR may cause system crash/data corruption (Bhavana Nagendra ) [245186]
- [xen] Windows HVM guest image migration causes blue screen (Bhavana Nagendra ) [245169]
- [xen] ia64: enable blktap driver (Jarod Wilson ) [216293]
- [scsi] check portstates before invoking target scan (David Milburn ) [246023]
- [nfs] NFSd oops when exporting krb5p mount (Steve Dickson ) [247120]
- [misc] Overflow in CAPI subsystem (Anton Arapov ) [231072] {CVE-2007-1217}
- [dlm] A TCP connection to DLM port blocks DLM operations (Patrick Caulfield ) [245892] {CVE-2007-3380}
- [dm] allow invalid snapshots to be activated (Milan Broz ) [244215]
- [gfs2] inode size inconsistency (Wendy Cheng ) [243136]
- [gfs2] Remove i_mode passing from NFS File Handle (Wendy Cheng ) [243136]
- [gfs2] Obtaining no_formal_ino from directory entry (Wendy Cheng ) [243136]
- [gfs2] EIO error from gfs2_block_truncate_page (Wendy Cheng ) [243136]
- [gfs2] remounting w/o acl option leaves acls enabled (Bob Peterson ) [245663]
- [GFS2] igrab of inode in wrong state (Steven Whitehouse ) [245646]
- [audit] subtree watching cleanups (Alexander Viro ) [182624]

* Mon Jun 25 2007 Don Zickus <dzickus@redhat.com> [2.6.18-32.el5]
- [ppc64] Data buffer miscompare (Konrad Rzeszutek ) [245332]
- [xen] fix kexec/highmem failure (Gerd Hoffmann ) [245585]
- [audit] kernel oops when audit disabled with files watched (Eric Paris ) [245164]
- [scsi] Update aic94xx and libsas to 1.0.3 (Ryan Powers ) [224694]
- [xen] ia64: kernel-xen panics when dom0_mem is specified(2) (Kei Tokunaga ) [217593]
- [md] fix EIO on writes after log failure (Jonathan Brassow ) [236271]
- [net] bonding: convert timers to workqueues (Andy Gospodarek ) [210577]
- [scsi] cciss driver updates (Tomas Henzl ) [222852]
- [sata] combined mode regression fix (Jeff Garzik ) [245052]
- Reverts: [audit] protect low memory from user mmap operations (Eric Paris ) [233021]

* Thu Jun 21 2007 Don Zickus <dzickus@redhat.com> [2.6.18-31.el5]
- [firewire] New stack technology preview (Jay Fenlason ) [182183]
- [xen] kdump/kexec support (Gerd Hoffmann ) [212843]
- [xen] Add AMD-V support for domain live migration (Chris Lalancette ) [222131]
- [GFS2] assertion failure after writing to journaled file, umount (Bob Peterson ) [243899]
- [pata] IDE (siimage) panics when DRAC4 reset (John Feeney ) [212391]
- [agp] Fix AMD-64 AGP aperture validation (Bhavana Nagendra ) [236826]
- [x86_64] C-state divisor not functioning correctly  (Bhavana Nagendra ) [235404]
- [i2c] SMBus does not work on ATI/AMD SB700 chipset (Bhavana Nagendra ) [244150]
- [ide] Cannot find IDE device with ATI/AMD SB700 (Bhavana Nagendra ) [244150]
- [pci] PCI-X/PCI-Express read control interface (Bhavana Nagendra ) [234335]
- [pata] IDE hotplug support for Promise pata_pdc2027x (Scott Moser ) [184774]

* Thu Jun 21 2007 Don Zickus <dzickus@redhat.com> [2.6.18-30.el5]
- [md] add dm rdac hardware handler (Mike Christie ) [184635]
- [sound]  ALSA update (1.0.14) (Brian Maly ) [227671 240713 223133 238004 223142 244672]
- [xen] : AMD's ASID implementation  (Bhavana Nagendra ) [242932]
- [x86_64] Fix casting issue in tick divider patch (Prarit Bhargava ) [244861]
- [fs] setuid program unable to read own /proc/pid/maps file (Konrad Rzeszutek ) [221173]
- [x86_64] Fixes system panic during boot up with no memory in Node 0 (Bhavana Nagendra ) [218641]
- [nfs] closes and umounts are racing.  (Steve Dickson ) [225515]
- [security] allow NFS nohide and SELinux to work together (Eric Paris ) [219837]
- [ia64] Altix ACPI support (Greg Edwards ) [223577]
- [net] ixgb: update to driver version 1.0.126-k2 (Bruce Allan ) [223380]
- [net] Update netxen_nic driver to version 3.x.x (Konrad Rzeszutek ) [244711]
- [misc] utrace update (Roland McGrath ) [229886 228397 217809 210693]
- [misc] disable pnpacpi on IBM x460 (Brian Maly ) [243730]
- [gfs2] posix lock fixes (David Teigland ) [243195]
- [gfs2] panic in unlink (Steven Whitehouse ) [239737]
- [input] i8042_interrupt() race can deliver bytes swapped to serio_interrupt() (Markus Armbruster ) [240860]
- [s390] qdio: system hang with zfcp in case of adapter problems (Jan Glauber ) [241298]
- [net] Fix tx_checksum flag bug in qla3xxx driver (Marcus Barrow ) [243724]
- [openib] Update OFED code to 1.2 (Doug Ledford ) [225581]
- [openib] kernel backports for OFED 1.2 update (Doug Ledford ) [225581]
- [ppc64] donate cycles from dedicated cpu (Scott Moser ) [242762]
- [scsi] RAID1 goes 'read-only' after resync (Chip Coldwell ) [231040]
- [md] move fn call that could block outside spinlock (Jonathan Brassow ) [242069]
- [fs] FUSE: Minor vfs change (Eric Sandeen ) [193720]
- [net] s2io: Native Support for PCI Error Recovery (Scott Moser ) [228052]
- [xen] x86_64: Fix FS/GS registers for VT bootup (Rik van Riel ) [224671]
- [misc] Add RHEL version info to version.h (Konrad Rzeszutek ) [232534]
- Revert: [mm] memory tracking patch only partially applied to Xen kernel (Kimball Murray ) [242514]
- Revert: [x86_64] Set CONFIG_CALGARY_IOMMU_ENABLED_BY_DEFAULT=n (Konrad Rzeszutek ) [222035]
- Revert: [ppc64] Oprofile kernel module does not distinguish PPC 970MP  (Janice M. Girouard ) [216458]

* Mon Jun 18 2007 Don Zickus <dzickus@redhat.com> [2.6.18-29.el5]
- [xen] Expand VNIF number per guest domain to over four (Kei Tokunaga ) [223908]
- [xen] change interface version for 3.1 (Kei Tokunaga ) [242989]
- [xen] ia64: Fix PV-on-HVM driver (Kei Tokunaga ) [242144]
- [xen] ia64: use generic swiotlb.h header (Kei Tokunaga ) [242138]
- [xen] ia64: xm save/restore does not work (Kei Tokunaga ) [240858]
- [xen] ia64: Skip MCA setup on domU (Kei Tokunaga ) [242143]
- [xen] ia64: Cannot measure process time accurately (Kei Tokunaga ) [240107]
- [xen] Support new xm command: xm trigger (Kei Tokunaga ) [242140]
- [xen] ia64: Fix for irq_desc() missing in new upstream (Kei Tokunaga ) [242137]
- [xen] ia64: Set IRQ_PER_CPU status on percpu IRQs (Kei Tokunaga ) [242136]
- [xen] ia64: improve performance of system call (Kei Tokunaga ) 
- [xen] ia64: para domain vmcore does not work under crash (Kei Tokunaga ) [224047]
- [xen] ia64: kernel-xen panics when dom0_mem=4194304 is specified (Kei Tokunaga ) [217593]
- [xen] ia64: evtchn_callback fix and clean (Kei Tokunaga ) [242126]
- [xen] ia64: changed foreign domain page mapping semantic (Kei Tokunaga ) [242779]
- [xen] Change to new interrupt deliver mechanism (Kei Tokunaga ) [242125]
- [xen] ia64: Uncorrectable error makes hypervisor hung (MCA  support) (Kei Tokunaga ) [237549]
- [xen] Xen0 can not startX in tiger4 (Kei Tokunaga ) [215536]
- [xen] ia64: Fix xm mem-set hypercall on IA64 (Kei Tokunaga ) [241976]
- [xen] ia64: Fix HVM interrupts on IPF (Kei Tokunaga ) [242124]
- [xen] save/restore fix (Gerd Hoffmann ) [222128]
- [xen] blkback/blktap: fix id type (Gerd Hoffmann ) [222128]
- [xen] xen: blktap race #2 (Gerd Hoffmann ) [222128]
- [xen] blktap: race fix #1 (Gerd Hoffmann ) [222128]
- [xen] blktap: cleanups. (Gerd Hoffmann ) [242122]
- [xen] blktap: kill bogous flush (Gerd Hoffmann ) [222128]
- [xen] binmodal drivers: block backends (Gerd Hoffmann ) [222128]
- [xen] bimodal drivers, blkfront driver (Gerd Hoffmann ) [222128]
- [xen] bimodal drivers, pvfb frontend (Gerd Hoffmann ) [222128]
- [xen] bimodal drivers, protocol header (Gerd Hoffmann ) [222128]

* Fri Jun 15 2007 Don Zickus <dzickus@redhat.com> [2.6.18-28.el5]
- [net] netxen: initial support for NetXen 10GbE NIC (Andy Gospodarek ) [231724]
- [net] cxgb3: initial support for Chelsio T3 card (Andy Gospodarek ) [222453]
- [drm] agpgart and drm support for bearlake graphics (Geoff Gustafson ) [229091]
- [acpi] acpi_prt list incomplete (Kimball Murray ) [214439]
- [mm] memory tracking patch only partially applied to Xen kernel (Kimball Murray ) [242514]
- [x86_64] Fix TSC reporting for processors with constant TSC (Bhavana Nagendra ) [236821]
- [pci] irqbalance causes oops during PCI removal (Kimball Murray ) [242517]
- [net] Allow packet drops during IPSec larval state resolution (Vince Worthington ) [240902]
- [net] bcm43xx: backport from 2.6.22-rc1 (John W. Linville ) [213761]
- [net] softmac: updates from 2.6.21 (John W. Linville ) [240354]
- [net] e1000: update to driver version 7.3.20-k2 (Andy Gospodarek ) [212298]
- [net] bnx2: update to driver version 1.5.11 (Andy Gospodarek ) [225350]
- [net] ipw2[12]00: backports from 2.6.22-rc1 (John W. Linville ) [240868]
- [net] b44 ethernet driver update (Jeff Garzik ) [244133]
- [net] sky2: update to version 1.14 from 2.6.21 (John W. Linville ) [223631]
- [net] forcedeth: update to driver version 0.60 (Andy Gospodarek ) [221941]
- [net] bonding: update to driver version 3.1.2 (Andy Gospodarek ) [210577]
- [net] tg3: update to driver version 3.77 (Andy Gospodarek ) [225466 228125]
- [PPC] Update of spidernet to 2.0.A for Cell (Scott Moser ) [227612]
- [scsi] SPI DV fixup (Chip Coldwell ) [237889]
- [audit] audit when opening existing messege queue (Eric Paris ) [223919 ]
- [audit] audit=0 does not disable all audit messages (Eric Paris ) [231371]
- [net] mac80211 inclusion (John W. Linville ) [214982 223558]

* Fri Jun 15 2007 Don Zickus <dzickus@redhat.com> [2.6.18-27.el5]
- [sata] kabi fixes [203781]
- [audit] panic and kabi fixes [233021]

* Thu Jun 14 2007 Don Zickus <dzickus@redhat.com> [2.6.18-26.el5]
- [x86_64] sparsemem memmap allocation above 4G (grgustaf) [227426]
- [net] ip_conntrack_sctp: fix remotely triggerable panic (Don Howard ) [243244] {CVE-2007-2876}
- [usb] Strange URBs and running out IOMMU (Pete Zaitcev ) [230427]
- [audit] broken class-based syscall audit (Eric Paris ) [239887]
- [audit] allow audit filtering on bit & operations (Eric Paris ) [232967]
- [x86_64] Add L3 cache support to some processors (Bhavana Nagendra ) [236835]
- [x86_64] disable mmconf for HP dc5700 Microtower (Prarit Bhargava ) [219389]
- [misc] cpuset information leak (Prarit Bhargava ) [242811] {CVE-2007-2875}
- [audit] stop softlockup messages when loading selinux policy (Eric Paris ) [231392]
- [fs] nfs does not support leases, send correct error (Peter Staubach ) [216750]
- [dlm] variable allocation types (David Teigland ) [237558]
- [GFS2] Journaled data issues (Steven Whitehouse ) [238162]
- [ipsec] Make XFRM_ACQ_EXPIRES proc-tunable (Vince Worthington ) [241798]
- [GFS2] Missing lost inode recovery code (Steven Whitehouse ) [201012]
- [GFS2] Can't mount GFS2 file system on AoE device (Robert Peterson ) [243131]
- [scsi] update aacraid driver to 1.1.5-2437 (Chip Coldwell ) [197337]
- [scsi] cciss: ignore results from unsent commands on kexec boot (Neil Horman ) [239520]
- [scsi] update iscsi_tcp driver (Mike Christie ) [227739]
- [x86_64] Fix regression in kexec (Neil Horman ) [242648]
- [x86] rtc support for HPET legacy replacement mode (Brian Maly ) [220196]
- [scsi] megaraid_sas update (Chip Coldwell ) [225221]
- [fs] fix ext2 overflows on filesystems > 8T (Eric Sandeen ) [237188]
- [x86] MCE thermal throttling (Brian Maly ) [224187]
- [audit] protect low memory from user mmap operations (Eric Paris ) [233021]
- [scsi] Add FC link speeds. (Tom Coughlan ) [231888]
- [pci] I/O space mismatch with P64H2 (Geoff Gustafson ) [220511]
- [scsi] omnibus lpfc driver update (Chip Coldwell ) [227416]
- [scsi] Update qla2xxx firmware (Marcus Barrow ) [242534]
- [ide] Serverworks data corruptor (Alan Cox ) [222653]
- [scsi] update qla4xxx driver (Mike Christie ) [224435 223087 224203]
- [scsi] update iser driver (Mike Christie ) [234352]
- [dlm] fix debugfs ref counting problem (Josef Bacik ) [242807]
- [md] rh_in_sync should be allowed to block (Jonathan Brassow ) [236624]
- [md] unconditionalize log flush (Jonathan Brassow ) [235039]
- [GFS2] Add nanosecond timestamp feature  (Steven Whitehouse ) [216890]
- [GFS2] quota/statfs sign problem and cleanup _host structures (Steven Whitehouse ) [239686]
- [scsi] mpt adds DID_BUS_BUSY host status on scsi BUSY status (Chip Coldwell ) [228108]
- [scsi] fix for slow DVD drive (Chip Coldwell ) [240910]
- [scsi] update MPT Fusion to 3.04.04 (Chip Coldwell ) [225177]
- [GFS2] Fix calculation for spare log blocks with smaller block sizes (Steven Whitehouse ) [240435]
- [gfs2] quotas non-functional (Abhijith Das ) [201011]
- [gfs2] Cleanup inode number handling (Abhijith Das ) [242584]

* Wed Jun 13 2007 Don Zickus <dzickus@redhat.com> [2.6.18-25.el5]
- [s390] fix possible reboot hang on s390 (Jan Glauber ) [222181]
- [cifs] Update CIFS to version 1.48aRH (Jeff Layton ) [238597]
- [audit] Make audit config immutable in kernel (Eric Paris ) [223530]
- [dio] invalidate clean pages before dio write (Jeff Moyer ) [232715]
- [nfs] fixed oops in symlink code.  (Steve Dickson ) [218718]
- [mm] shared page table for hugetlb  page (Larry Woodman ) [222753]
- [nfs] Numerous oops, memory leaks and hangs found in upstream (Steve Dickson ) [242975]
- [misc] include taskstats.h in kernel-headers package (Don Zickus ) [230648]
- [ide] packet command error when installing rpm (John Feeney ) [229701]
- [dasd] export DASD status to userspace (Chris Snook ) [242681]
- [dasd] prevent dasd from flooding the console (Jan Glauber ) [229590]
- [s390] ifenslave -c causes kernel panic with VLAN and OSA Layer2 (Jan Glauber ) [219826]
- [s390] sclp race condition (Jan Glauber ) [230598]
- [audit] SAD/SPD flush have no security check (Eric Paris ) [233387]
- [audit] Add space in IPv6 xfrm audit record (Eric Paris ) [232524]
- [audit] Match proto when searching for larval SA (Eric Paris ) [234485]
- [audit] pfkey_spdget does not audit xrfm policy changes (Eric Paris ) [229720]
- [audit] collect audit inode information for all f*xattr commands (Eric Paris ) [229094]
- [audit] Initialize audit record sid information to zero (Eric Paris ) [223918]
- [audit] xfrm_add_sa_expire return code error (Eric Paris ) [230620]
- [net] NetLabel: Verify sensitivity level has a valid CIPSO mapping (Eric Paris ) [230255]
- [audit] pfkey_delete and xfrm_del_sa audit hooks wrong (Eric Paris ) [229732]
- [block] Fix NULL bio crash in loop worker thread (Eric Sandeen ) [236880]
- [x86]: Add Greyhound performance counter events (Bhavana Nagendra ) [222126]
- [dio] clean up completion phase of direct_io_worker() (Jeff Moyer ) [242116]
- [audit] add subtrees support (Alexander Viro ) [182624]
- [audit] AVC_PATH handling (Alexander Viro ) [224620]
- [audit] auditing ptrace (Alexander Viro ) [228384]
- [x86_64] Fix a cast in the lost ticks code (Prarit Bhargava ) [241781]
- [PPC64] DMA 4GB boundary protection  (Scott Moser ) [239569]
- [PPC64] MSI support for PCI-E (Scott Moser ) [228081]
- [ppc64] Enable DLPAR support for HEA (Scott Moser ) [237858]
- [ppc64] update ehea driver to latest version. (Janice M. Girouard ) [234225]
- [PPC64] spufs move to sdk2.1 (Scott Moser ) [242763]
- [PPC64] Cell SPE and Performance (Scott Moser ) [228128]
- [cpufreq] Identifies correct number of processors in powernow-k8 (Bhavana Nagendra ) [229716]

* Mon Jun 11 2007 Don Zickus <dzickus@redhat.com> [2.6.18-24.el5]
- [ipmi] update to latest (Peter Martuccelli ) [241928 212415 231436]
- [sata] super-jumbo update (Jeff Garzik ) [203781]
- [sata] move SATA drivers to drivers/ata (Jeff Garzik ) [203781]

* Fri Jun 08 2007 Don Zickus <dzickus@redhat.com> [2.6.18-23.el5]
- [dlm] Allow unprivileged users to create the default lockspace (Patrick Caulfield ) [241902]
- [dlm] fix queue_work oops (David Teigland ) [242070]
- [dlm] misc device removed when lockspace removal fails (David Teigland ) [241817]
- [dlm] dumping master locks (David Teigland ) [241821]
- [dlm] canceling deadlocked lock (David Teigland ) [238898]
- [dlm] wait for config check during join (David Teigland ) [206520]
- [dlm] fix new_lockspace error exit (David Teigland ) [241819]
- [dlm] cancel in conversion deadlock (David Teigland ) [238898]
- [dlm] add lock timeouts and time warning (David Teigland ) [238898]
- [dlm] block scand during recovery (David Teigland ) [238898]
- [dlm] consolidate transport protocols (David Teigland ) [219799]
- [audit] log targets of signals (Alexander Viro ) [228366]

* Thu Jun 07 2007 Don Zickus <dzickus@redhat.com> [2.6.18-22.el5]
- [scsi] Add kernel support for Areca RAID controllers (Tomas Henzl ) [205897]
- [s390] runtime switch for qdio performance statistics (Jan Glauber ) [228048]
- [nfs] enable 'nosharecache' mounts. (Steve Dickson ) [209964]
- [scsi] scsi_error.c - Fix lost EH commands (Chip Coldwell ) [227586]
- [s390] zfcp driver fixes (Jan Glauber ) [232002 232006]
- [misc] synclink_gt: fix init error handling  (Eric Sandeen) [210389]
- [edac] k8_edac: don't panic on PCC check (Aristeu Rozanski ) [237950]
- [mm] Prevent OOM-kill of unkillable children or siblings (Larry Woodman ) [222492]
- [aio] fix buggy put_ioctx call in aio_complete (Jeff Moyer ) [219497]
- [scsi] 3ware 9650SE not recognized by updated  3w-9xxx module (Chip Coldwell ) [223465]
- [scsi] megaraid: update version reported by  MEGAIOC_QDRVRVER (Chip Coldwell ) [237151]
- [nfs] NFS/NLM - Fix double free in __nlm_async_call (Steve Dickson ) [223248]
- [ppc] EEH is improperly enabled for some Power4  systems (Scott Moser ) [225481]
- [net] ixgb: update to 1.0.109 to add pci error recovery (Andy Gospodarek ) [211380]
- [ppc] Fix xmon=off and cleanup xmon initialization (Scott Moser ) [229593]
- [mm] reduce MADV_DONTNEED contention (Rik van Riel ) [237677]
- [x86_64] wall time is not compensated for lost timer ticks (Konrad Rzeszutek ) [232666]
- [PPC] handle <.symbol> lookup for kprobes (Scott Moser ) [238465]
- [pci] Dynamic Add and Remove of PCI-E (Konrad Rzeszutek ) [227727]
- [PPC64] Support for ibm,power-off-ups RTAS  call (Scott Moser ) [184681]

* Fri Jun 01 2007 Don Zickus <dzickus@redhat.com> [2.6.18-21.el5]
- [net] Re-enable and update the qla3xxx networking driver (Konrad Rzeszutek ) [225200]
- [misc] xen: kill sys_{lock,unlock} dependency on microcode driver (Gerd Hoffmann ) [219652]
- [acpi] Update ibm_acpi module (Konrad Rzeszutek ) [231176]
- [nfs] NFSv4: referrals support (Steve Dickson ) [230602]
- [misc] random: fix error in entropy extraction (Aristeu Rozanski ) [241718] {CVE-2007-2453}
- [net] fix DoS in PPPOE (Neil Horman ) [239581] {CVE-2007-2525}
- [GFS2] Fixes related to gfs2_grow (Steven Whitehouse ) [235430]
- [gfs2] Shrink size of struct gdlm_lock (Steven Whitehouse ) [240013]
- [misc] Bluetooth setsockopt() information leaks (Don Howard ) [234292] {CVE-2007-1353}
- [net] RPC/krb5 memory leak (Steve Dickson ) [223248]
- [mm] BUG_ON in shmem_writepage() is triggered (Michal Schmidt ) [234447]
- [nfs] protocol V3 :write procedure patch (Peter Staubach ) [228854]
- [fs] invalid segmentation violation during exec (Dave Anderson ) [230339]
- [md] dm io: fix panic on large request (Milan Broz ) [240751]
- [nfs] RPC: when downsizing response buffer, account for checksum (Jeff Layton ) [238687]
- [md] incorrect parameter to dm_io causes read failures (Jonathan Brassow ) [241006]
- [ia64] eliminate potential deadlock on XPC disconnects (George Beshers ) [223837]
- [md] dm crypt: fix possible data corruptions (Milan Broz ) [241272]
- [ia64] SN correctly update smp_affinity mask (luyu ) [223867]
- [mm]fix OOM wrongly killing processes through MPOL_BIND (Larry Woodman ) [222491]
- [nfs] add nordirplus option to NFS client  (Steve Dickson ) [240126]
- [autofs] fix panic on mount fail - missing autofs module (Ian Kent ) [240307]
- [scsi] Fix bogus warnings from SB600 DVD drive (Prarit Bhargava ) [238570]
- [acpi] _CID support for PCI Root Bridge  detection. (Luming Yu ) [230742]
- [ia64] platform_kernel_launch_event is a noop in non-SN kernel (Luming Yu ) [232657]
- [net] high TCP latency with small packets (Thomas Graf ) [229908]
- [misc] xen: fix microcode driver for new firmware (Gerd Hoffmann ) [237434]
- [GFS2] Bring GFS2 uptodate (Steven Whitehouse ) [239777]
- [scsi] update for new SAS RAID  (Scott Moser ) [228538]
- [md] dm: allow offline devices in table (Milan Broz ) [239655]
- [md] dm: fix suspend error path (Milan Broz ) [239645]
- [md] dm multipath: rr path order is inverted (Milan Broz ) [239643]
- [net] RPC: simplify data check, remove BUG_ON (Jeff Layton ) [237374]
- [mm] VM scalability issues (Larry Woodman ) [238901 238902 238904 238905]
- [misc] lockdep: annotate DECLARE_WAIT_QUEUE_HEAD (Chip Coldwell ) [209539]
- [mm] memory-less node support (Prarit Bhargava ) [228564]

* Thu May 17 2007 Don Howard <dhoward@redhat.com> [2.6.18-20.el5]
- [fs] prevent oops in compat_sys_mount (Jeff Layton ) [239767] {CVE-2006-7203}

* Thu May 10 2007 Don Zickus <dzickus@redhat.com> [2.6.18-19.el5]
- [ia64] MCA/INIT issues with printk/messages/console (Kei Tokunaga ) [219158]
- [ia64] FPSWA exceptions take excessive system time  (Erik Jacobson ) [220416]
- [GFS2] flush the glock completely in inode_go_sync (Steven Whitehouse ) [231910]
- [GFS2] mmap problems with distributed test cases (Steven Whitehouse ) [236087]
- [GFS2] deadlock running d_rwdirectlarge (Steven Whitehouse ) [236069]
- [GFS2] panic if you try to rm -rf the lost+found directory (Steven Whitehouse ) [232107]
- [misc] Fix softlockup warnings during sysrq-t (Prarit Bhargava ) [206366]
- [pty] race could lead to double idr index free (Aristeu Rozanski ) [230500]
- [v4l] use __GFP_DMA32 in videobuf_vm_nopage (Aristeu Rozanski ) [221478]
- [scsi] Update QLogic qla2xxx driver to 8.01.07-k6 (Marcus Barrow ) [225249]
- [mm] OOM killer breaks s390 CMM (Jan Glauber ) [217968]
- [fs] stack overflow with non-4k page size (Dave Anderson ) [231312]
- [scsi] scsi_transport_spi: sense buffer size error (Chip Coldwell ) [237889]
- [ppc64] EEH PCI error recovery  support (Scott Moser ) [207968]
- [mm] optimize kill_bdev() (Peter Zijlstra ) [232359]
- [x86] tell sysrq-m to poke the nmi watchdog (Konrad Rzeszutek ) [229563]
- [x86] Use CPUID calls to check for mce (Bhavana Nagendra ) [222123]
- [x86] Fix to nmi to support GH processors (Bhavana Nagendra ) [222123]
- [x86] Fix CPUID calls to support GH processors (Bhavana Nagendra ) [222123]
- [x86] Greyhound cpuinfo output cleanups (Bhavana Nagendra ) [222124]
- [misc] intel-rng: fix deadlock in smp_call_function (Prarit Bhargava ) [227696]
- [net] ixgb: fix early TSO completion (Bruce Allan ) [213642]

* Fri May 04 2007 Don Zickus <dzickus@redhat.com> [2.6.18-18.el5]
- [e1000] fix watchdog timeout panics (Andy Gospodarek ) [217483]
- [net] ipv6_fl_socklist is inadvertently shared (David S. Miller ) [233088] {CVE-2007-1592}
- [dlm] expose dlm_config_info fields in configfs (David Teigland ) [239040]
- [dlm] add config entry to enable log_debug (David Teigland ) [239040]
- [dlm] rename dlm_config_info fields (David Teigland ) [239040]
- [mm] NULL current->mm dereference in grab_swap_token causes oops (Jerome Marchand ) [231639]
- [net] Various NULL pointer dereferences in netfilter code (Thomas Graf ) [234287] {CVE-2007-1496}
- [net] IPv6 fragments bypass in nf_conntrack netfilter code (Thomas Graf ) [234288] {CVE-2007-1497}
- [net] disallow RH0 by default (Thomas Graf ) [238065] {CVE-2007-2242}
- [net] fib_semantics.c out of bounds check (Thomas Graf ) [236386]
- [misc] getcpu system call (luyu ) [233046]
- [ipc] bounds checking for shmmax (Anton Arapov ) [231168]
- [x86_64] GATT pages must be uncacheable (Chip Coldwell ) [238709]
- [gfs2] does a mutex_lock instead of a mutex_unlock (Josef Whiter ) [229376]
- [dm] failures when creating many snapshots (Milan Broz ) [211516 211525]
- [dm] kmirrord: deadlock when dirty log on mirror itself (Milan Broz ) [218068]
- [security] Supress SELinux printk for messages users don't care about (Eric Paris ) [229874]
- [serial] panic in check_modem_status on 8250 (Norm Murray ) [238394]
- [net] Fix user OOPS'able bug in FIB netlink (David S. Miller ) [237913]
- [misc] EFI: only warn on pre-1.00 version (Michal Schmidt ) [223282]
- [autofs4] fix race between mount and expire (Ian Kent ) [236875]
- [GFS2] gfs2_delete_inode: 13 (Steven Whitehouse ) [224480]
- [misc] k8temp (Florian La Roche ) [236205]

* Mon Apr 30 2007 Don Zickus <dzickus@redhat.com> [2.6.18-17.el5]
- [x86_64] Calgary IOMMU cleanups and fixes (Konrad Rzeszutek ) [222035]
- [GFS2] lockdump support (Robert Peterson ) [228540]
- [net] kernel-headers: missing include of types.h (Neil Horman ) [233934]
- [mm] unmapping memory range disturbs page referenced state (Peter Zijlstra ) [232359]
- [IA64] Fix stack layout issues when using ulimit -s (Jarod Wilson ) [234576]
- [CIFS] Windows server bad domain name null terminator fix (Jeff Layton ) [224359]
- [x86_64] Fix misconfigured K8 north bridge (Bhavana Nagendra ) [236759]
- [gfs2] use log_error before LM_OUT_ERROR (David Teigland ) [234338]
- [dlm] fix mode munging (David Teigland ) [234086]
- [dlm] change lkid format (David Teigland ) [237126]
- [dlm] interface for purge (David Teigland ) [237125]
- [dlm] add orphan purging code (David Teigland ) [237125]
- [dlm] split create_message function (David Teigland ) [237125]
- [dlm] overlapping cancel and unlock (David Teigland ) [216113]
- [dlm] zero new user lvbs (David Teigland ) [237124]
- [PPC64] Handle Power6 partition modes (2) (Janice M. Girouard ) [228091]
- [ppc64] Handle Power6 partition modes (Janice M. Girouard ) [228091]
- [mm] oom kills current process on memoryless node. (Larry Woodman ) [222491]
- [x86] Tick Divider (Alan Cox ) [215403]
- [GFS2] hangs waiting for semaphore (Steven Whitehouse ) [217356]
- [GFS2] incorrect flushing of rgrps (Steven Whitehouse ) [230143]
- [GFS2] Clean up of glock code (Steven Whitehouse ) [235349]
- [net] IPsec: panic when large security contexts in ACQUIRE (James Morris ) [235475]
- [ppc64] Cell Platform Base kernel support (Janice M. Girouard ) [228099]
- [s390] fix dasd reservations (Chris Snook ) [230171]
- [x86] Fix invalid write to nmi MSR (Prarit Bhargava ) [221671]

* Fri Apr 20 2007 Don Zickus <dzickus@redhat.com> [2.6.18-16.el5]
- [s390] crypto driver update (Jan Glauber ) [228049]
- [NMI] change watchdog timeout to 30 seconds (Larry Woodman ) [229563]
- [ppc64] allow vmsplice to work in 32-bit mode on ppc64 (Don Zickus ) [235184]
- [nfs] fix multiple dentries pointing to same directory inode (Steve Dickson ) [208862]
- [ipc] mqueue nested locking annotation (Eric Sandeen ) 
- [net] expand in-kernel socket api (Neil Horman ) [213287]
- [XEN] Better fix for netfront_tx_slot_available(). (Herbert Xu ) [224558]
- [fs] make static counters in new_inode and iunique be 32 bits (Jeff Layton ) [215356]
- [ppc64] remove BUG_ON() in hugetlb_get_unmapped_area() (Larry Woodman ) [222926]
- [dm] stalls on resume if noflush is used (Milan Broz ) [221330]
- [misc]: AMD/ATI SB600 SMBus support (Prarit Bhargava ) [232000]
- [mm] make do_brk() correctly return EINVAL for ppc64.   (Larry Woodman ) [224261]
- [agp] agpgart fixes and new pci ids (Geoff Gustafson ) [227391]
- [net] xfrm_policy delete security check misplaced (Eric Paris ) [228557]
- [x86]: Fix mtrr MODPOST warnings (Prarit Bhargava ) [226854]
- [elevator] move clearing of unplug flag  earlier (Eric Sandeen ) [225435]
- [net] stop leak in flow cache code (Eric Paris ) [229528]
- [ide] SB600 ide only has one channel (Prarit Bhargava ) [227908]
- [scsi] ata_task_ioctl should return ata registers (David Milburn ) [218553]
- [pcie]: Remove PCIE warning for devices with no irq pin (Prarit Bhargava ) [219318]
- [x86] ICH9 device IDs  (Geoff Gustafson ) [223097]
- [mm] Some db2 operations cause system to hang (Michal Schmidt ) [222031]
- [security] invalidate flow cache entries after selinux policy reload (Eric Paris ) [229527]
- [net] wait for IPSEC SA resolution in socket contexts. (Eric Paris ) [225328]
- [net] clean up xfrm_audit_log interface (Eric Paris ) [228422]
- [ipv6]: Fix routing regression. (David S. Miller ) [222122]
- [tux] date overflow fix (Jason Baron ) [231561]
- [cifs] recognize when a file is no longer read-only (Jeff Layton ) [231657]
- [module] MODULE_FIRMWARE support (Jon Masters ) [233494]
- [misc] some apps cannot use IPC msgsnd/msgrcv larger than 64K (Jerome Marchand ) [232012]
- [xen] Fix netfront teardown (Glauber de Oliveira Costa ) [219563]

* Fri Apr 13 2007 Don Zickus <dzickus@redhat.com> [2.6.18-15.el5] 
- [x86_64] enable calgary support for x86_64 system (Neil Horman ) [221593]
- [s390] pseudo random number generator (Jan Glauber ) [184809]
- [ppc64] Oprofile kernel module does not distinguish PPC 970MP  (Janice M. Girouard ) [216458]
- [GFS2] honor the noalloc flag during block allocation (Steven Whitehouse ) [235346]
- [GFS2] resolve deadlock when writing and accessing a file (Steven Whitehouse ) [231380]
- [s390] dump on panic support (Jan Glauber ) [228050, 227841]
- [pci] include devices in NIC ordering patch and fix whitespace (Andy Gospodarek ) [226902]
- [ext3] handle orphan inodes vs. readonly snapshots (Eric Sandeen ) [231553]
- [fs] - Fix error handling in check_partition(), again (Eric Sandeen ) [231518]
- [ipv6] /proc/net/anycast6 unbalanced inet6_dev refcnt (Andy Gospodarek ) [231310]
- [s390] kprobes breaks BUG_ON (Jan Glauber ) [231155]
- [edac] add support for revision F processors (Aristeu Rozanski ) [202622]
- [scsi] blacklist touch-up (Chip Coldwell ) [232074]
- [gfs2] remove an incorrect assert (Steven Whitehouse ) [229873]
- [gfs2] inconsistent inode number lookups (Wendy Cheng ) [229395]
- [gfs2] NFS cause recursive locking (Wendy Cheng ) [229349]
- [gfs2] NFS v2 mount failure (Wendy Cheng ) [229345]
- [s390] direct yield for spinlocks on s390 (Jan Glauber ) [228869]
- [s390] crypto support for 3592 tape devices (Jan Glauber ) [228035]
- [cpu-hotplug] make and module insertion script cause a panic (Konrad Rzeszutek ) [217583]
- [s390] runtime switch for dasd erp logging (Jan Glauber ) [228034]
- [suspend] Fix x86_64/relocatable kernel/swsusp breakage. (Nigel Cunningham ) [215954]
- [ext3] buffer: memorder fix (Eric Sandeen ) [225172]
- [scsi] fix incorrect last scatg length (David Milburn ) [219838]
- [usb]: airprime driver corrupts ppp session for EVDO card (Jon Masters ) [222443]
- [misc] Fix race in efi variable delete code (Prarit Bhargava ) [223796]
- [ext3] return ENOENT from ext3_link when racing with unlink (Eric Sandeen ) [219650]
- [scsi] Missing PCI Device in aic79xx driver (Chip Coldwell ) [220603]
- [acpi]: Fix ACPI PCI root bridge querying time (Prarit Bhargava ) [218799]
- [kdump]: Simple bounds checking for crashkernel args (Prarit Bhargava ) [222314]
- [misc] longer CD timeout (Erik Jacobson ) [222362]
- [nfs] Disabling protocols when starting NFS server is broken. (Steve Dickson ) [220894]
- [s390] page_mkclean causes data corruption on s390 (Jan Glauber ) [235373]

* Wed Apr 04 2007 Don Zickus <dzickus@redhat.com> [2.6.18-14.el5]
- [ppc] reduce num_pmcs to 6 for Power6 (Janice M. Girouard ) [220114]
- [sched] remove __cpuinitdata from cpu_isolated_map (Jeff Burke ) [220069]
- [gfs2] corrrectly display revalidated directories (Robert Peterson ) [222302]
- [gfs2] fix softlockups (Josef Whiter ) [229080]
- [gfs2] occasional panic in gfs2_unlink while running bonnie++ (Steven Whitehouse ) [229831]
- [gfs2] Shrink gfs2 in-core inode size (Steven Whitehouse ) [230693]
- [GFS2] Fix list corruption in lops.c (Steven Whitehouse ) [226994]
- [gfs2] fix missing unlock_page() (Steven Whitehouse ) [224686]
- [dlm] make lock_dlm drop_count tunable in sysfs (David Teigland ) [224460]
- [dlm] increase default lock limit (David Teigland ) [224460]
- [dlm] can miss clearing resend flag (David Teigland ) [223522]
- [dlm] fix master recovery (David Teigland ) [222307]
- [dlm] fix user unlocking (David Teigland ) [219388]
- [dlm] saved dlm message can be dropped (David Teigland ) [223102]

* Tue Mar 27 2007 Don Zickus <dzickus@redhat.com> [2.6.18-13.el5]
- [x86_64] Don't leak NT bit into next task (Dave Anderson ) [213313]
- [mm] Gdb does not accurately output the backtrace. (Dave Anderson ) [222826]
- [net] IPV6 security holes in ipv6_sockglue.c - 2 (David S. Miller ) [231517] {CVE-2007-1000}
- [net] IPV6 security holes in ipv6_sockglue.c (David S. Miller ) [231668] {CVE-2007-1388}
- [audit] GFP_KERNEL allocations in non-blocking context fix (Alexander Viro ) [228409]
- [NFS] version 2 over UDP is not working properly (Steve Dickson ) [227718]
- [x86] Fix various data declarations in cyrix.c (Prarit Bhargava ) [226855]
- [sound] Fix various data declarations in sound/drivers (Prarit Bhargava ) [227839]
- [mm] remove __initdata from initkmem_list3 (Prarit Bhargava ) [226865]

* Wed Mar 14 2007 Don Zickus <dzickus@redhat.com> [2.6.18-12.el5]
- [xen] move xen sources out of kernel-xen-devel (Don Zickus ) [212968]
- [net] __devinit & __devexit cleanups for de2104x driver (Prarit Bhargava ) [228736]
- [video] Change rivafb_remove to __deviexit (Prarit Bhargava ) [227838]
- [x86] Reorganize smp_alternatives sections in vmlinuz (Prarit Bhargava ) [226876]
- [atm] Fix __initdata declarations in drivers/atm/he.c (Prarit Bhargava ) [227830]
- [video] Change nvidiafb_remove to __devexit (Prarit Bhargava ) [227837]
- [usb] __init to __devinit in isp116x_probe (Prarit Bhargava ) [227836]
- [rtc] __init to __devinit in rtc drivers' probe functions (Prarit Bhargava ) [227834]
- [x86] remove __init from sysenter_setup (Prarit Bhargava ) [226852]
- [irq] remove __init from noirqdebug_setup (Prarit Bhargava ) [226851]
- [x86] remove __init from efi_get_time (Prarit Bhargava ) [226849]
- [x86] Change __init to __cpuinit data in SMP code (Prarit Bhargava ) [226859]
- [x86] apic probe __init fixes (Prarit Bhargava ) [226875]
- [x86] fix apci related MODPOST warnings (Prarit Bhargava ) [226845]
- [serial] change serial8250_console_setup to __init (Prarit Bhargava ) [226869]
- [init] Break init() into two parts to avoid MODPOST warnings (Prarit Bhargava ) [226829]
- [x86] declare functions __init to avoid  compile warnings (Prarit Bhargava ) [226858]
- [x86] cpu hotplug/smpboot misc MODPOST warning fixes (Prarit Bhargava ) [226826]
- [x86] Fix boot_params and .pci_fixup warnings (Prarit Bhargava ) [226824 226874]
- [xen] Enable Xen booting on machines with > 64G (Chris Lalancette ) [220592]
- [utrace] exploit and unkillable cpu fixes (Roland McGrath ) [229886]
- [pcmcia] buffer overflow in omnikey cardman driver    (Don Howard ) [227478]

* Fri Feb 23 2007 Don Zickus <dzickus@redhat.com> [2.6.18-10.el5]
- [cpufreq] Remove __initdata from tscsync (Prarit Bhargava ) [223017]
- [security] Fix key serial number collision problem (David Howells ) [227497] {CVE-2007-0006}
- [fs] core dump of read-only binarys (Don Howard ) [228886] {CVE-2007-0958}

* Thu Feb 23 2007 Don Zickus <dzickus@redhat.com> [2.6.18-9.el5]
- enable debug options

* Thu Jan 25 2007 Don Zickus <dzickus@redhat.com> [2.6.18-8.el5]
- quiet down the console_loglevel (Don Zickus) [224613]

* Thu Jan 25 2007 Don Zickus <dzickus@redhat.com> [2.6.18-7.el5]
- xen: fix TLB flushing in shadow pagetable mode (Rik van Riel ) [224227]

* Tue Jan 23 2007 Don Zickus <dzickus@redhat.com> [2.6.18-6.el5]
- Update: xen: Add PACKET_AUXDATA cmsg (Herbert Xu ) [223505]

* Tue Jan 23 2007 Don Zickus <dzickus@redhat.com> [2.6.18-5.el5]
- x86: /proc/mtrr interface MTRR bug fix (Bhavana Nagendra ) [223821]
- Revert: bonding: eliminate rtnl assertion spew (Andy Gospodarek ) [210577]
- ia64: Check for TIO errors on shub2 Altix (George Beshers ) [223529]
- nfs: Unable to mount more than 1 Secure NFS mount (Steve Dickson ) [220649]

* Wed Jan 17 2007 Don Zickus <dzickus@redhat.com> [2.6.18-4.el5]
- IPSec: incorrect return code in xfrm_policy_lookup (Eric Paris ) [218591]
- more kabi whitelist updates (Jon Masters)

* Tue Jan 16 2007 Don Zickus <dzickus@redhat.com> [2.6.18-3.el5]
- scsi: fix EX8350 panic (stex.ko) (Jun'ichi Nick Nomura ) [220783]
- Audit: Mask upper bits on 32 bit syscall auditing on ppc64 (Eric Paris ) [213276]

* Mon Jan 15 2007 Don Zickus <dzickus@redhat.com> [2.6.18-2.el5]
- mm: handle mapping of memory without a struct page backing it (Erik Jacobson ) [221029]
- rng: check to see if bios locked device (Erik Jacobson ) [221029]
- sata: support legacy IDE mode of SB600 SATA (Bhavana Nagendra ) [221636]
- xen: quick fix for Cannot allocate memory (Steven Rostedt ) [217056]
- XEN: Register PIT handlers to the correct domain (Herbert Xu ) [222520]
- SATA AHCI: support AHCI class code (Jeff Garzik ) [222674]
- fix vdso in core dumps (Roland McGrath ) [211744]

* Fri Jan 12 2007 Don Zickus <dzickus@redhat.com> [2.6.18-1.3014.el5]
- XEN: Replace inappropriate domain_crash_synchronous use (Herbert Xu ) [221239]
- SATA timeout boot message  (Peter Martuccelli ) [222108]
- Netlabel: off by one and init bug in netlbl_cipsov4_add_common (Eric Paris ) [221648]
- NetLabel: fix locking issues (Eric Paris ) [221504]
- mm: fix statistics in vmscan.c (Peter Zijlstra ) [222030]
- usb: Sun/AMI virtual floppy issue (Pete Zaitcev ) [219628]
- bonding: eliminate rtnl assertion spew (Andy Gospodarek ) [210577]
- Xen: Make HVM hypercall table NR_hypercalls entries big. (Herbert Xu ) [221818]
- xen: Add PACKET_AUXDATA cmsg (Herbert Xu ) [219681]

* Wed Jan 10 2007 Don Zickus <dzickus@redhat.com> [2.6.18-1.3002.el5]
- ppc64: initialization of hotplug memory fixes (Janice M. Girouard ) [220065]
- GFS2: return error for NULL inode (Russell Cattelan ) [217008]
- scsi: prevent sym53c1510 from claiming the wrong pci id (Chip Coldwell ) [218623]
- net: Disable the qla3xxx network driver. (Tom Coughlan ) [221328]
- xen: Disable CONFIG_IDE_GENERIC (Jarod Wilson ) [220099]
- sound: add support for STAC9205 codec (John Feeney ) [219494]
- ipv6: panic when bringing up multiple interfaces (Thomas Graf ) [218039]
- XFRM Audit: correct xfrm auditing panic (Eric Paris ) [222033]
- edac: fix /proc/bus/pci/devices to allow X to start (John Feeney ) [219288]
- x86_64: clear_kernel_mapping: mapping has been split. will leak memory. (Larry Woodman ) [218543]
- xen: >4G guest fix (Steven Rostedt ) [217770]
-  fs: listxattr syscall can corrupt user space programs (Eric Sandeen ) [220119]
- CacheFiles: Fix object struct recycling (David Howells ) [215599]
- Remove capability requirement to reading cap-bound (Eric Paris ) [219230]
- disable building ppc64iseries (Don Zickus) [219185]
- update: utrace fixes (Roland McGrath) [214405 215052 216150 209118]
- PPC config file changes for IPMI and DTLK (Peter Martuccelli ) [210214]
- update: Xen: emulate PIT channels for vbios support (Stephen C. Tweedie ) [215647]
- net: qla3xxx panics when eth1 is sending pings (Konrad Rzeszutek ) [220246]
- s390: inflate spinlock kabi (Jan Glauber ) [219871]
- x86: Add panic on unrecovered NMI (Prarit Bhargava ) [220829]
- ppc64: fix booting kdump env. w/maxcpus=1 on power5 (Jarod Wilson ) [207300]
- netfilter: iptables stop fails because ip_conntrack cannot unload. (Thomas Graf ) [212839]
- gfs: Fix gfs2_rename lock ordering (for local filesystem) (Wendy Cheng ) [221237]
- GFS2: Fix ordering of page disposal vs. glock_dq (Steven Whitehouse ) [220117]
- xen: fix nosegneg detection (Rik van Riel ) [220675]
- mm: Fix for shmem_truncate_range() BUG_ON() (Larry Woodman ) [219821]
- x86_64: enabling lockdep hangs the system (Don Zickus ) [221198]
- dlm: change some log_error to log_debug (David Teigland ) [221326]
- dlm: disable debugging output (David Teigland ) [221326]
- fs: ext2_check_page denial of service (Eric Sandeen ) [217018]
- CPEI - prevent relocating hotplug irqs (Kei Tokunaga ) [218520]
- Networking: make inet->is_icsk assignment binary (Eric Paris ) [220482]
- net: b44: phy reset problem that leads to link flap  (Neil Horman ) [216338]
- autofs - fix panic on mount fail - missing autofs module update (Ian Kent ) [221118]
- net: act_gact: division by zero (Thomas Graf ) [218348]
- ppc64: Avoid panic when taking altivec exceptions from userspace. (David Woodhouse ) [220586]

* Wed Jan 03 2007 Don Zickus <dzickus@redhat.com> [2.6.18-1.2961.el5]
- new set of kabi whitelists (Jon Masters) [218682]
- x86: remove unwinder patches from x86/x86_64 (Don Zickus ) [220238]
- usb: disable ub and libusual (Pete Zaitcev ) [210026]
- NetLabel: stricter configuration checking (Eric Paris ) [219393]
- scsi: fix iscsi sense len handling (Mike Christie ) [217933]
- Xen: emulate PIT channels for vbios support (Stephen C. Tweedie ) [215647]
- VM: Fix nasty and subtle race in shared mmap'ed page writeback (Eric Sandeen ) [220963]
- Audit: Add type for 3rd party, emit key for audit events (Eric Paris ) [217958]
- NFS: system stall on NFS stress under high memory  pressure (Steve Dickson ) [213137]
- netfilter: IPv6/IP6Tables Vulnerabilities (Thomas Graf ) [220483]
- acpi: increase ACPI_MAX_REFERENCE_COUNT (Doug Chapman ) [217741]
- Race condition in mincore can cause ps -ef to hang (Doug Chapman ) [220480]
- Call init_timer() for ISDN PPP CCP reset state timer (Marcel Holtmann ) [220163]
- Race condition concerning VLAPIC interrupts (Bhavana Nagendra ) [213858]

* Tue Jan 02 2007 Don Zickus <dzickus@redhat.com> [2.6.18-1.2943.el5]
- CIFS: Explicitly set stat->blksize (Steve Dickson ) [210608]
- FS-Cache: dueling read/write processes fix (Steve Dickson ) [212831]
- xen: Use swiotlb mask for coherent mappings too (Herbert Xu ) [216472]
- ia64: Kexec, Kdump on SGI IA64 NUMA machines fixes (George Beshers ) [219091]
- splice : Must fully check for fifos (Don Zickus ) [214289]
- Xen: Fix potential grant entry leaks on error (Herbert Xu ) [217993]
- e1000: truncated TSO TCP header with 82544, workaround (Herbert Xu ) [206540]
- scsi: fix bus reset in qla1280 driver (George Beshers ) [219819]
- scsi: add qla4032 and fix some bugs (Mike Christie ) [213807]
- XFRM: Config Change Auditing (Eric Paris ) [209520]
- Xen: ia64 guest networking finally works (Jarod Wilson ) [218895]
- scsi structs for future known features and fixes (Mike Christie ) [220458]
- squashfs fixup (Steve Grubb ) [219534]
- ppc64: DLPAR virtual CPU removal failure - cppr bits (Janice M. Girouard ) [218058]
- ia64: allow HP ZX1 systems to initalize swiotlb in kdump (Neil Horman ) [220064]
- export tasklist_lock (David Howells ) [207992]
- gfs2: Initialization of security/acls (Steven Whitehouse ) [206126]
- x86: handle _PSS object range corectly in speedstep-centrino (Brian Maly ) [211690]
- GFS2 change nlink panic (Wendy Cheng ) [215088]
- scsi: fix oops in iscsi packet transfer path (Mike Christie ) [215381]
- Fix Emulex lpfc ioctl on PPC (Tom Coughlan ) [219194]
- Xen: Fix agp on x86_64 under Xen (Stephen C. Tweedie ) [217715]
- Emulex lpfc update to 8.1.10.2 (Tom Coughlan ) [218243]
- bluetooth: Add packet size checks for CAPI messages (Marcel Holtmann ) [219139]
- x86_64: create Calgary boot knob (Konrad Rzeszutek ) [220078]
- cciss bugfixes (Tom Coughlan ) [185021]
- ia64: Do not call SN_SAL_SET_CPU_NUMBER twice on cpu 0 on booting (Erik Jacobson ) [219722]
- scsi: Empty /sys/class/scsi_host/hostX/config  file (Janice M. Girouard ) [210239]
- refresh: Reduce iommu page size to 4K on 64K page PPC systems (Janice M. Girouard) [212097]
- update: Xen netback: Reenable TX queueing and drop pkts after timeout (Herbert Xu ) [216441]

* Sun Dec 17 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2910.el5]
- xen: Update xen paravirt framebuffer to upstream protocol (fixes) (Stephen C. Tweedie ) [218048]
- xen: Update xen paravirt framebuffer to upstream protocol (Stephen C. Tweedie ) [218048]
- nfs: disable Solaris NFS_ACL version 2  (Steve Dickson ) [215073]
- xen: EXPORT_SYMBOL(zap_page_range) needs to be moved (Stephen C. Tweedie ) [218476]
- ppc64: disable unused drivers that cause oops on insmod/rmmod (Janice M. Girouard ) [206658]
- scsi: GoVault not accessible due to software reset. (Konrad Rzeszutek ) [215567]
- GFS2 fix DIO deadlock (Steven Whitehouse ) [212627]
- dlm: fix lost flags in stub replies (David Teigland ) [218525]
- CacheFiles: Improve/Fix reference counting (David Howells ) [212844]
- gfs2: Fails back to readpage() for stuffed files (Steven Whitehouse ) [218966]
- gfs2: Use try locks in readpages (Steven Whitehouse ) [218966]
- GFS2 Readpages fix (part 2) (Steven Whitehouse ) [218966]
- gfs2: Readpages fix  (Steven Whitehouse ) [218966]
- bonding: Don't release slaves when master is admin down (Herbert Xu ) [215887]
- x86_64: fix execshield randomization for heap (Brian Maly ) [214548]
- x86_64: check and enable NXbit support during resume (Vivek Goyal ) [215954]
- GPL export truncate_complete_page (Eric Sandeen ) [216545]
- mm: reject corrupt swapfiles earlier (Eric Sandeen ) [213118]
- QLogic qla2xxx - add missing PCI device IDs (Tom Coughlan ) [219350]
- mpt fusion bugfix and maintainability improvements (Tom Coughlan ) [213736]
- scsi: make fc transport removal of target configurable (Mike Christie ) [215797]
- gfs2: don't try to lockfs after shutdown (Steven Whitehouse ) [215962]
- xen: emulation for accesses faulting on a page boundary (Stephen C. Tweedie ) [219275]
- gfs2: dirent format compatible with gfs1 (Steven Whitehouse ) [219266]
- gfs2: Fix size caclulation passed to the allocator. (Russell Cattelan ) [218950]
- ia64: PAL_GET_PSTATE implementation (Prarit Bhargava ) [184896]
- CacheFiles: Handle ENOSPC on create/mkdir better (David Howells) [212844]
- connector: exessive unaligned access (Erik Jacobson ) [218882]
- revert: Audit: Add type for 3rd party, emit key for audit events (Eric Paris ) [217958]

* Wed Dec 13 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2876.el5]
- touch softdog during oops (Dave Jones ) [218109]
- selinux: allow quoted commas for certain catagories in context mounts (Eric Paris ) [211857]
- xen: oprofile on Intel CORE (Glauber de Oliveira Costa ) [213964]
- Xen: make ballooning work right (xen part) (Rik van Riel ) [212069]
- Xen: make ballooning work right (Rik van Riel ) [212069]
- Xen: HVM crashes on IA32e SMP (Glauber de Oliveira Costa ) [214774]
- gfs2: Fix uninitialised variable (Steven Whitehouse ) [219212]
- GFS2: Don't flush everything on fdatasync (Steven Whitehouse ) [218770]
- Disable PCI mmconf and segmentation on HP xw9300/9400 (Bhavana Nagendra ) [219159]
- Audit: Add type for 3rd party, emit key for audit events (Eric Paris ) [217958]
- Fix time skew on Intel Core 2 processors (Prarit Bhargava ) [213050]
- Xen : Fix for SMP Xen guest slow boot issue on AMD systems (Bhavana Nagendra ) [213138]
- GFS2: fix mount failure (Josef Whiter ) [218327]
- cramfs: fix zlib_inflate oops with corrupted image (Eric Sandeen ) [214705]
- xen: Fix xen swiotlb for b44 module (xen part) (Stephen C. Tweedie ) [216472]
- xen: Fix xen swiotlb for b44 module (Stephen C. Tweedie ) [216472]
- scsi: fix stex_intr signature (Peter Zijlstra ) [219370]
- GFS2: Fix recursive locking in gfs2_permission (Steven Whitehouse ) [218478]
- GFS2: Fix recursive locking in gfs2_getattr (Steven Whitehouse ) [218479]
- cifs: Fix mount failure when domain not specified (Steve Dickson ) [218322]
- GFS2: Fix memory allocation in glock.c (Steven Whitehouse ) [204364]
- gfs2: Fix journal flush problem (Steven Whitehouse ) [203705]
- gfs2: Simplify glops functions (Steven Whitehouse ) [203705]
- gfs2: Fix incorrect fs sync behaviour (Steven Whitehouse ) [203705]
- fix check_partition routines to continue on errors (David Milburn ) [210234]
- fix rescan_partitions to return errors properly (David Milburn ) [210234]
- gfs2: Tidy up bmap & fix boundary bug (Steven Whitehouse ) [218780]
- Fix bmap to map extents properly (Steven Whitehouse ) [218780]
- ide-scsi/ide-cdrom module load race fix (Alan Cox ) [207248]
- dlm: fix receive_request lvb copying (David Teigland ) [214595]
- dlm: fix send_args lvb copying (David Teigland ) [214595]
- device-mapper mirroring - fix sync status change (Jonathan Brassow ) [217582]
- Xen: Copy shared data before verification (Herbert Xu ) [217992]
- s390: common i/o layer fixes (Jan Glauber ) [217799]
- Spurious interrups from ESB2 in native mode (Alan Cox ) [212060]

* Wed Dec 06 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2839.el5]
- Xen: fix xen/ia64/vti panic when config sets maxmem (Aron Griffis ) [214161]
- Xen: ia64 making it work (Aron Griffis ) [210637]
- Xen: upstream patches to make Windows Vista work (Steven Rostedt) [214780]
- enable PCI express hotplug driver (Kei Tokunaga ) [207203]
- d80211: kABI pre-compatibility (John W. Linville ) [214982]
- Xen: ia64 kernel unaligned access (Aron Griffis ) [212505]
- Xen: getting ia64 working; kernel part (Aron Griffis) [210637]
- Xen: Properly close block frontend on non-existant file (Glauber de Oliveira Costa ) [218037]
- SHPCHP driver doesn't work if the system was under heavy load (Kei Tokunaga ) [215561]
- SHPCHP driver doesn't work in poll mode (Kei Tokunaga) [211679]
- pciehp: free_irq called twice (Kei Tokunaga ) [216940]
- pciehp: pci_disable_msi() called to early (Kei Tokunaga ) [216939]
- pciehp: parallel hotplug operations cause kernel panic (Kei Tokunaga ) [216935]
- pciehp: info messages are confusing (Kei Tokunaga ) [216932]
- pciehp: Trying to enable already enabled slot disables the slot (Kei Tokunaga ) [216930]
- CacheFiles: cachefiles_write_page() shouldn't indicate error twice (David Howells) [204570]
- IPMI - allow multiple Baseboard Management Centers (Konrad Rzeszutek ) [212572]
- nfs - set correct mode during create operation (Peter Staubach ) [215011]
- Xen: blkback: Fix potential grant entry leaks on error (Rik van Riel ) [218355]
- Xen: blkback: Copy shared data before verification (Rik van Riel) [217994]
- revert: Xen: fix SMP HVM guest timer irq delivery (Rik van Riel ) [213138]

* Tue Dec 05 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2817.el5]
- Adding in a kabi_whitelist (Jon Masters) [218402]
- Xen: AMD-V HVM fix for Windows hibernate (Bhavana Nagendra ) [217367]
- Xen: fix SMP HVM guest timer irq delivery (Rik van Riel ) [213138]
- NetLabel: bring current with upstream: cleanup/future work (Eric Paris ) [218097]
- NetLabel: bring current with upstream: performance (Eric Paris ) [218097]
- NetLabel: bring current with upstream: bugs (Eric Paris ) [218097]
- TG3 support Broadcom 5756M/5756ME  Controller (John Feeney ) [213204]
- tg3: BCM5752M crippled after reset (Andy Gospodarek ) [215765]
- sata ata_piix map values (Geoff Gustafson ) [204684]
- e1000: Reset all functions after a PCI error (Janice M. Girouard) [211694]
- prevent /proc/meminfo's HugePages_Rsvd from going negative. (Larry Woodman ) [217910]
- netlabel: disallow editing of ip options on packets with cipso options (Eric Paris ) [213062]
- xen netback: Fix wrap to zero in transmit credit scheduler. (Herbert Xu ) [217574]
- megaraid initialization fix for kdump (Jun'ichi Nick Nomura ) [208451]
- HFS: return error code in case of error (Eric Paris ) [217009]
- Xen: fix 2TB overflow in virtual disk driver (Rik van Riel ) [216556]
- e1000: fix garbled e1000 stats (Neil Horman ) [213939]
- dlm: use recovery seq number to discard old replies (David Teigland ) [215596]
- dlm: resend lock during recovery if master not ready (David Teigland ) [215596]
- dlm: check for incompatible protocol version (David Teigland ) [215596]
- NetLabel: Do not send audit messages if audit is off (Eric Paris ) [216244]
- selinux: give correct response to get_peercon() calls (Eric Paris ) [215006]
- SELinux: Fix oops with non-mls policies (Eric Paris ) [214397]
- Xen blkback: Fix first_sect check. (Rik van Riel ) [217995]
- allow the highest frequency if bios think so. (Dave Jones ) [218106]
- AGP corruption fixes. (Dave Jones ) [218107]

* Mon Dec 04 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2789.el5]
- Xen: fix vcpu hotplug statistics (Rik van Riel ) [209534]
- DLPAR and Hotplug not enabled (Janice M. Girouard ) [207732]
- Reduce iommu page size to 4K on 64K page PPC systems (Janice M. Girouard) [212097]
- e1000: add (2) device ids (Bruce Allan) [184864]
- power6: illegal instruction errors during install (Janice M. Girouard) [216972]
- update_flash is broken across PPC (Janice M. Girouard) [214690]
- write failure on swapout could corrupt data (Peter Zijlstra) [216194]
- IBM veth panic when buffer rolls over (Janice M. Girouard ) [214486]
- Make the x86_64 boot gdt limit exact (Steven Rostedt ) [214736]
- Xen: make netfront device permanent (Glauber de Oliveira Costa ) [216249]
- lockdep: fix ide/proc interaction (Peter Zijlstra ) [210678]
- Xen: fix iSCSI root oops on x86_64 xen domU (Rik van Riel ) [215581]
- Fix flowi clobbering (Chris Lalancette ) [216944]
- Enable netpoll/netconsole for ibmveth (Neil Horman ) [211246]
- dlm: fix size of STATUS_REPLY message (David Teigland ) [215430]
- dlm: fix add_requestqueue checking nodes list (David Teigland ) [214475]
- dlm: don't accept replies to old recovery messages (David Teigland ) [215430]
- x86_64: kdump mptable reservation fix  (Vivek Goyal ) [215417]
- Add Raritan KVM USB dongle to the USB HID blacklist (John Feeney ) [211446]
- Fix bogus warning in [un]lock_cpu_hotplug (Prarit Bhargava ) [211301]
- Xen: Avoid touching the watchdog when gone for too long (Glauber de Oliveira Costa ) [216467]
- add missing ctcmpc Makefile target (Jan Glauber ) [184608]
- remove microcode size check for i386 (Geoff Gustafson ) [214798]

* Thu Nov 30 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2769.el5]
- add the latest 2.6.18.4 security patches (Don Zickus) [217904]
- revert: mspec failures due to memory.c bad pte problem (Erik Jacobson ) [211854]

* Wed Nov 29 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2767.el5]
- disable W1 config (Dave Jones ) [216176]
- Xen netback: Reenable TX queueing and drop pkts after timeout (Herbert Xu ) [216441]
- Xen: fix profiling (Rik van Riel ) [214886]
- bnx2: update firmware to correct rx problem in promisc mode (Neil Horman ) [204534]
- sound-hda: fix typo in patch_realtek.c (John W. Linville) [210691]
- Fix sys_move_pages when a NULL node list is passed. (Dave Jones ) [214295]
- proc: readdir race fix (Nobuhiro Tachino ) [211682]
- device mapper: /sys/block/dm-* entries remain after removal (Milan Broz ) [214905]
- Fix 64k page table problems on ppc specific ehca driver (Doug Ledford ) [199765]
- configfs: mutex_lock_nested() fix (Eric Sandeen ) [211506]
- CIFS: Explicitly set stat->blksize (Eric Sandeen ) [214607]
- Compute checksum properly in netpoll_send_udp (Chris Lalancette ) [214542]
- Noisy stack trace by memory hotplug on memory busy system (Kei Tokunaga ) [213066]
- catch blocks beyond pagecache limit in __getblk_slow (Eric Sandeen ) [214419]
- xen privcmd: Range-check hypercall index. (Herbert Xu ) [213178]
- strange messages around booting and acpi-memory-hotplug (Kei Tokunaga) [212231]
- Fix panic in CPU hotplug on ia64 (Prarit Bhargava ) [213455]
- Fix spinlock bad magic when removing xennet device (Chris Lalancette ) [211684]
- netlabel: various error checking cleanups (Eric Paris ) [210425]
- mspec failures due to memory.c bad pte problem (Erik Jacobson ) [211854]
- Fix autofs creating bad dentries in NFS mount (David Howells ) [216178]

* Thu Nov 09 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2747.el5] 
- Set HZ to 1000 for kernel and 250 for Xen (Don Zickus) [198594] 
- Custom Diagnostics kernel module fails to load on RHEL5 (Janice Girouard) [213020] 
- kernel: FS-Cache: error from cache: -105 (2nd part) (Don Zickus) [214678] 
 
* Mon Nov 06 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2746.el5] 
- configure XPC as a loadable kernel module instead of static (Erik Jacobson) [213903] 
- kernel BUG at drivers/xen/core/evtchn.c:482! (Glauber de Oliveira Costa) [210672] 
- IPv6 MRT: 'lockdep' annotation is missing? (Thomas Graf) [209313] 
- sort PCI device list breadth-first (John Feeney) [209484] 
- reenable xen pae >4GB patch (Don Zickus) 
 
* Sun Nov 05 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2745.el5] 
- disable the xen-pae patch due to compile problems

* Sun Nov 05 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2744.el5] 
- Kernel Panic on Initial boot of guest (Steven Rostedt) [211633] 
- kernel unable to read partition (device busy) (Peter Zijlstra) [212191] 
- QEMU always crashes (Don Zickus) [212625] 
- kernel: FS-Cache: error from cache: -105 (Steve Dickson) [212831] 
- DLM oops in kref_put when umounting (Patrick Caulfield) [213005] 
- gfs umount hung, message size too big (Patrick Caulfield) [213289] 
- CPU hotplug doesn't work trying to BSP offline (Keiichiro Tokunaga) [213324] 
- status messages ping-pong between unmounted nodes (Dave Teigland) [213682] 
- res_recover_locks_count not reset when recover_locks is aborted (Dave Teigland) [213684] 
- disable CONFIG_ISA (Don Zickus) 
 
* Wed Nov 01 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2740.el5] 
- Remove support for ipw3945 driver (Don Zickus) [195534] 
- acpiphp will not load due to unknown symbols (Prarit Bhargava) [209506] 
- Can not install rhel5 b1 on ipr dasd. (Janice Girouard) [210851] 
- Can't make SCTP connections between Xen guests (Don Zickus) [212550] 
- eHEA update to support 64K pages for Power6 (Janice Girouard) [212041] 
- Failure to boot second kernel on HP hardware (Don Zickus) [212578] 
- dlm deadlock during simultaneous mount attempts (Dave Teigland) [211914] 
- CMT-eligible ipw2200/2915 driver (John W. Linville) [184862] 
- CVE-2006-5174 copy_from_user information leak on s390 (Jan Glauber) [213568] 
- NFSv4: fs_locations support (Steve Dickson) [212352] 
- [IPv6] irrelevant rules break ipv6 routing. (Thomas Graf) [209354] 
- [IPv6] blackhole and prohibit rule types not working (Thomas Graf) [210216] 
- [KEXEC] bad offset in icache instruction crashes Montecito systems (Jarod Wilson) [212643] 
- assertion "FALSE" failed in gfs/glock.c (Dave Teigland) [211622] 
- I/O DLPAR and Hotplug not enabled in RHEL5 (Janice Girouard) [207732] 
 
* Thu Oct 26 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2739.el5] 
- SHPCHP driver doesn't work (Keiichiro Tokunaga) [210478] 
- ext3/jbd panic (Eric Sandeen) [209647] 
- Oops in nfs_cancel_commit_list (Jeff Layton) [210679] 
- kernel Soft lockup detected on corrupted ext3 filesystem (Eric Sandeen) [212053] 
- CIFS doesn't work (Steve Dickson) [211070] 
 
* Thu Oct 26 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2738.el5] 
- need to convert bd_mount_mutex on gfs2 also (Peter Zijlstra)

* Wed Oct 25 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2737.el5] 
- Grant table operations unsuitable for guest domains (Rik van Riel) [210489] 
- AMD-V HVM windows guest boot menu timer issue (Steven Rostedt) [209001] 
- iflags.h is not upstream (Steve Whitehouse) [211583] 
- ACPIPHP doesn't work (Keiichiro Tokunaga) [209677] 
- IBMVSCSI does not correctly reenable the CRQ (Janice Girouard) [211304] 
- librdmacm-utils failures (Doug Ledford) [210711] 
- Badness in debug_mutex_unlock at kernel/mutex-debug.c:80 (Janice Girouard) [208500] 
- Stratus memory tracking functionality needed in RHEL5 (Kimball Murray) [209173, 211604] 
 
* Tue Oct 24 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2736.el5] 
- Can't unload gnbd module, 128 references (Peter Zijlstra) [211905]
- ddruid does not recognize dasd drives (Peter Zijlstra) [210030]
 
* Mon Oct 23 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2733.el5]
- disable x86_64 dirty page tracking, it breaks some machines (Don Zickus)

* Tue Oct 17 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2732.el5] 
- possible recursive locking detected: cachefilesd (David Howells) [204615] 
- Stratus memory tracking functionality needed in RHEL5 (Kimball Murray) [209173] 
- nfs handled rpc error incorrectly (Steve Dickson) [207040] 
- cachefiles: inode count maintance (Steve Dickson) [209434] 
- mkinitrd: iSCSI root requires crc32c module (Mike Christie) [210232] 
- implemented sysrq-w to dump all cpus (Larry Woodman) 
- enable panic_on_oops (Dave Anderson) 
- re-enable x86_64 stack unwinder fixes (Don Zickus) 
- disable kernel debug flags (Don Zickus) 
 
* Tue Oct 17 2006 Stephen C. Tweedie <sct@redhat.com>
- Fix up xen blktap merge to restore modular build

* Tue Oct 17 2006 Don Zickus <dzickus@redhat.com> 
- fix xen breakage from last night's incorrect commits

* Mon Oct 16 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2729.el5] 
- revert Kpobes backport from 2.6.19-rc1, it fails to compile

* Mon Oct 16 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2728.el5] 
- Update FC transport and Emulex lpfc Fibre Channel Driver (Tom Coughlan) [207551] 
- NFSv4 using memory after its freed fix (Steve Dickson) [206996] 
- GFS2 dirents are 'unkown' type (Steve Whitehouse) [210493] 
- Cachefs double unlock (Steve Dickson) [210701] 
- tty locking cleanup (Prarit Bhargava) [210249] 
- ibmveth fails in kdump boot (Janice Girouard - IBM on-site partner) [199129] 
- Kpobes backport from 2.6.19-rc1 (Anil S Keshavamurthy) [210555] 
- Ia64 - kprobe opcode must reside on 16 bytes alignment (Anil S Keshavamurthy) [210552] 
- GFS2 forgets to unmap pages (Steve Whitehouse) [207764] 
- DIO needs to avoid using page cache (Jeffrey Moyer) [207061] 
- megaraid_sas: update (Chip Coldwell) [209463] 
- NFS data corruption (Steve Dickson) [210071] 
- page align bss sections on x86_64 (Vivek Goyal) [210499] 
- blkbk/netbk modules don't load (Aron Griffis) [210070] 
- blktap does not build on ia64 (Aron Griffis) [208895] 
- blkbk/netbk modules don't load (Rik van Riel) [202971] 
- patches from xen-ia64-unstable (Rik van Riel) [210637] 
- Xen version strings need to reflect exact Red Hat build number (Stephen Tweedie) [211003] 
- updated to 2.6.18.1 stable series (Don Zickus) 
- updated execshield patch (Don Zickus) 
- revert CONFIG_PCI_CALGARY_IOMMU config (Don Zickus) 
- disable CONFIG_MAMBO (Don Zickus) 
 
* Thu Oct 12 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2727.el5] 
- I/O errors with dm-multipath when adding new path (Alasdair Kergon) [169302] 
- Kdump on i386 fails - Second kernel panics (Vivek Goyal) [207598] 
- patch to qla4xxx for supporting ioctl module (Mike Christie) [207356] 
- lockdep fixes (Peter Zijlstra) [208165 209135 204767] 
- printk cleanup (Dave Jones) 
- spec file cleanup (Dave Jones, Bill Nottingham) 
- gfs-dlm fix (Patrick Caulfield) 
- find-provides fix (Jon Masters) 
 
* Wed Oct 11 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2726.el5] 
- need to disable all cpu frequency scaling drivers in Xen kernel (Rik van Riel) [210336 208942] 
- radeon hangs DMA when CONFIG_CALGARY_IOMMU is build in kernel. (Konrad Rzeszutek) [210380] 
- Got Call Trace message when remove veth module (Janice Girouard) [208938] 
- cannot generate kABI deps unless kernel is installed (Jon Masters) [203926] 
- ctcmpc driver (Jan Glauber) [184608] 
- PTRACE_DETACH doesn't deliver signals under utrace. (Aristeu S. Rozanski F.) [207674] 
- SG_SCATTER_SZ causing Oops during scsi disk microcode update (Doug Ledford) [207146] 
- ia64 kprobe fixes (David Smith) 
 
* Tue Oct 10 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2725.el5] 
- Duplicate dput in sysfs_update_file can cause a panic. (Prarit Bhargava) [209454] 
- Lock issue with 2.6.18-1.2702.el5, NetworkManager and ipw3945 (John W. Linville) [208890] 
- cpqarray module fails to detect arrays (Chip Coldwell) [205653] 
- stex.c driver for Promise SuperTrak EX is missing (Jeff Garzik) [209179] 
- NetLabel does not audit configuration changes (Eric Paris) [208456] 
- NetLabel has a race problem in the cache (Eric Paris) [209324] 
- kernel/lockdep.c:1814/trace_hardirqs_on() (Not tainted) for APM (Peter Zijlstra) [209480] 
-  correct netlabel secid for packets without a known label (Eric Paris) [210032] 
- IPSec information leak with labeled networking (Eric Paris) [209171] 
- NetLabel hot-add memory confict pre-beta2 kenrel x86_64 (Konrad Rzeszutek) [208445] 
- NFS data corruption (Steve Dickson) [210071] 
- kernel dm multipath: ioctl support (Alasdair Kergon) [207575] 
- kernel dm: fix alloc_dev error path (Alasdair Kergon) [209660] 
- kernel dm snapshot: fix invalidation ENOMEM (Alasdair Kergon) [209661] 
- kernel dm snapshot: chunk_size parameter is not required after creation (Alasdair Kergon) [209840] 
- kernel dm snapshot: fix metadata error handling (Alasdair Kergon) [209842] 
- kernel dm snapshot: fix metadata writing when suspending (Alasdair Kergon) [209843] 
- kernel dm: full snapshot removal attempt causes a seg fault/kernel bug (Alasdair Kergon) [204796] 
- dm mirror: remove trailing space from table (Alasdair Kergon) [209848] 
- kernel dm: add uevent change event on resume (Alasdair Kergon) [209849] 
- kernel dm crypt: Provide a mechanism to clear key while device suspended (Milan Broz) [185471] 
- kernel dm: use private biosets to avoid deadlock under memory pressure (Alasdair Kergon) [209851] 
- kernel dm: add feature flags to structures for future kABI compatibility (Alasdair Kergon) [208543] 
- kernel dm: application visible I/O errors with dm-multipath and queue_if_no_path when adding new path (Alasdair Kergon) [169302] 
- refresh ia64-kexec-kdump patch (Don Zickus) 
- update exec-shield patch (Don Zickus) 
- revert x86 unwinder fixes (Don Zickus) 
 
 
* Mon Oct 09 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2722.el5]  
- update utrace patch to fix s390 build problems
- ia64 hotswap cpu patch fixes to compile under xen
- ia64 export fixes

* Mon Oct 09 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2718.el5]  
- Audit Filtering on PPID for = and != is inverted (Eric Paris) [206425] 
- Adding Hitachi SANRISE entries into SCSI white list (Chip Coldwell) [206532] 
- forward port of SCSI blacklist from RHEL4 (Chip Coldwell) [208256] 
- Need to add ALSA support for Broadwater platform (John W. Linville) [184855] 
- /proc/<pid>/smaps doesn't give any data (Alexander Viro) [208589] 
- ACPI based CPU hotplug causes kernel panic (Keiichiro Tokunaga) [208487] 
- New infiniband 12x power driver opensourced from IBM (Janice Girouard) [184791] 
- iscsi oops when connection creation fails (Mike Christie) [209006] 
- nommconf work-around still needed for AMD chipsets (Jim Baker) [207396] 
- ProPack XPMEM exported symbols (Greg Edwards) [206215] 
- PCI error recovery bug in e100 and e1000 cards (John W. Linville) [208187] 
- / on raid fails to boot post-install system (Jan Glauber) [196943] 
- auditctl fails to reject malformed ARCH filter (Eric Paris) [206427] 
- oom-killer updates (Larry Woodman) [208583] 
- NFS is revalidating directory entries too often (Steve Dickson) [205454] 
- kernel-xen cannot reboot (Stephen Tweedie) [209841] 
- Unsupported FS's in RHEL 5 Beta 1 (Don Zickus) [206486] 
 
* Thu Oct 05 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2717.el5] 
- patch fix for RDSCTP (Don Zickus)

* Thu Oct 05 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2715.el5] 
- RDTSCP Support (Bhavana Nagendra) [185057] 
- s390 kprobe on larl instruction crashes system (Jan Glauber) [205738] 
- single stepping is broken when kprobes is configured (Jan Glauber) [205739] 
- autofs kernel patches resulting from Connectathon testing (Ian Kent) [206952] 
- Include the qla3xxx networking driver (Konrad Rzeszutek) [208182] 
- overzealous sanity checking in sys_poll() (Chris Snook) [204705] 
- automounter cannot shutdown when timeout=0 (Ian Kent) [205836] 
- Rewrite of journaling data commit code (Eric Sandeen) [207739] 
- qla4xxx soft lockup when ethernet cable disconnected (Mike Christie) [206063] 
- hypfs_kill_super() check for initialized root inode (Jan Glauber) [207717] 
- The Matrox graphics driver is not built (Janice Girouard) [207200] 
 
* Mon Oct 02 2006 Don Zickus <dzickus@redhat.com> [2.6.18-1.2714.el5] 
- Wrong SELinux context prevents hidd from working (David Woodhouse) [204655] 
- nfs connectathon component basic test 6 fails.... (Steve Dickson) [208637] 
- unstick STICKY bit to fix suspend/resume (Dave Jones) 
 
* Fri Sep 29 2006 Don Zickus <dzickus@redhat.com>
- fix up ipv6 multiple routing table patch

* Thu Sep 28 2006 Don Zickus <dzickus@redhat.com> 
- s390 ccs/ccw subsystem does not have proper uevent support (Pete Zaitcev) [199994] 
- 'Cannot allocate memory' when cat /proc/scsi/scsi (Chip Coldwell) [200299] 
- Add support for Kirkwood and Kirkwood LP NICs (John W. Linville) [207776] 
- remove userspace support from qla4xxx (Mike Christie) [206063] 
- NetLabel interface has changed in the upstream kernels (Eric Paris) [208119] 
- lockdep fixes (Peter Zijlstra) [208304 204795] 
 
* Thu Sep 28 2006 Steven Whitehouse <swhiteho@redhat.com>
- Updated GFS2/DLM patch

* Wed Sep 27 2006 Don Zickus <dzickus@redhat.com> 
-Multiple routing tables for IPv6 (Thomas Graf) [179612] 
-bunch of lockdep fixes (Peter Zijlstra) [200520 208294 208293 208292 208290] 
-rearrange the cachefs patches for easier future maintance (Steve Dickson) 
-enable some TCP congestion algorithms (David Miller) 
-add a test patch (Eric Paris) 
 
* Tue Sep 26 2006 Don Zickus <dzickus@redhat.com>
- Need to add the sata sas bits
 
* Tue Sep 26 2006 Don Zickus <dzickus@redhat.com> 
-Native SAS and SATA device support - SATA/IDE converter (Janice Girouard) [196336] 
-kernel unaligned access messages in rhel5a1 (Prarit Bhargava) [198572] 
-problems with LUNs mapped at LUN0 with iscsi and netapp filers (Mike Christie) [205802] 
-ext3 fails to mount a 16T filesystem due to overflows (Eric Sandeen) [206721] 
-possible recursive locking detected - swapper/1 (Peter Zijlstra) [203098] 
-FS-Cache: error from cache: -28 (David Howells) [204614] 
-aic94xx driver does not recognise SAS drives in x366 (Konrad Rzeszutek) [206526] 
-Support for 3945 driver (John W. Linville) [195534] 
-Memory Hotplug fails due to relocatable kernel patches (Vivek Goyal) [207596] 
-Potential overflow in jbd for filesystems > 8T (Eric Sandeen) [208024] 
-2,4-node x460 halts during bootup after installation (Konrad Rzeszutek) [203971] 
 
* Mon Sep 25 2006 Don Zickus <dzickus@redhat.com>
- fix x86 relocatable patch (again) to build properly

* Mon Sep 25 2006 Dave Jones <davej@redhat.com>
- Disable 31bit s390 kernel builds.

* Mon Sep 25 2006 Jarod Wilson <jwilson@redhat.com>
- Make kernel packages own initrd files

* Mon Sep 25 2006 John W. Linville <linville@redhat.com>
- Add periodic work fix for bcm43xx driver

* Sat Sep 23 2006 Dave Jones <davej@redhat.com>
- Disable dgrs driver.

* Fri Sep 22 2006 David Woodhouse <dwmw2@redhat.com>
- Fix PowerPC audit syscall success/failure check (#204927)
- Remove offsetof() from <linux/stddef.h> (#207569)
- One line per header in Kbuild files to reduce conflicts
- Fix visibility of ptrace operations on ppc32
- Fix ppc32 SECCOMP

* Thu Sep 21 2006 Dave Jones <davej@redhat.com>
- reiserfs: make sure all dentry refs are released before
  calling kill_block_super
- Fix up some compile warnings

* Thu Sep 21 2006 Mike Christie <mchristie@redhat.com>
- clean up spec file.

* Thu Sep 21 2006 Mike Christie <mchristie@redhat.com>
- drop 2.6.18-rc iscsi patch for rebase

* Wed Sep 20 2006 Juan Quintela <quintela@redhat.com>
- xen HV printf rate limit (rostedt).
- xen HV update to xen-unstable cset11540:9837ff37e354
- xen-update:
  * linux-2.6 changeset:   34294:dc1d277d06e0
  * linux-2.6-xen-fedora changeset:   36184:47c098fdce14
  * xen-unstable changeset:   11540:9837ff37e354

* Wed Sep 20 2006 Dave Jones <davej@redhat.com>
- 2.6.18
- i965 AGP suspend support.
- AGP x8 fixes.

* Tue Sep 19 2006 Juan Quintela <quintela@redhat.com>
- xen update to 2.6.18-rc7-git4.
  * linux-2.6 changeset: 34288:3fa5ab23fee7
  * linux-2.6-xen-fedora changeset: 36175:275f8c0b6342
  * xen-unstable changeset: 11486:d8bceca5f07d

* Tue Sep 19 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc7-git4
- Further lockdep fixes. (#207064)

* Tue Sep 19 2006 Don Zickus <dzickus@redhat.com>
- EXT3 overflows at 16TB (#206721)

* Tue Sep 19 2006 Don Zickus <dzickus@redhat.com>
- Increase nodes supported on ia64 (#203184)
- Powernow K8 Clock fix (#204354)
- NetLabel fixes

* Mon Sep 18 2006 Dave Jones <davej@redhat.com>
- Fix RTC lockdep bug. (Peter Zijlstra)

* Mon Sep 18 2006 Juan Quintela <quintela@redhat.com>
- xen HV update (cset 11470:2b8dc69744e3).

* Mon Sep 18 2006 David Woodhouse <dwmw2@redhat.com>
- Fix various Bluetooth compat ioctls

* Sun Sep 17 2006 Juan Quintela <quintela@redhat.com>
- xen update:
  * linux-2.6 changeset: 34228:ea3369ba1e2c
  * linux-2.6-xen-fedora changeset: 36107:47256dbb1583
  * linux-2.6-xen changeset: 22905:d8ae02f7df05
  * xen-unstable changeset: 11460:1ece34466781ec55f41fd29d53f6dafd208ba2fa

* Sun Sep 17 2006 Dave Jones <davej@redhat.com>
- Fix task->mm refcounting bug in execshield. (#191094)
- 2.6.18rc7-git2
- 586 SMP support.

* Sat Sep 16 2006 David Woodhouse <dwmw2@redhat.com>
- Implement futex primitives on IA64 and wire up [gs]et_robust_list again
  (patch from Jakub, #206613)

* Fri Sep 15 2006 Mike Christie <mchristie@redhat.com>
- fix slab corruption when starting qla4xxx with iscsid not started.

* Thu Sep 14 2006 Don Zickus <dzickus@redhat.com>
- add include/asm-x86_64/const.h to exported header file list
  used by the x86 relocatable patch (inside include/asm-x86_64/page.h)
  
* Thu Sep 14 2006 Dave Jones <davej@redhat.com>
- kprobe changes to make systemtap's life easier.

* Thu Sep 14 2006 Don Zickus <dzickus@redhat.com>
- sync up beta1 fixes and patches
   - includes infiniband driver
   - aic9400/adp94xx updates
   - squashfs s390 fix
- include x86 relocatable patch at end of list
- some /proc/kcore changes for x86 relocatable kernel
   
* Thu Sep 14 2006 David Woodhouse <dwmw2@redhat.com>
- 2.6.18rc7-git1
- header file fixups
- use correct arch for 'make headers_install' when cross-building

* Wed Sep 13 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc7

* Tue Sep 12 2006 David Woodhouse <dwmw2@redhat.com>
- Export <linux/netfilter/xt_{CONN,}SECMARK.h> (#205612)

* Tue Sep 12 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc6-git4
- Enable IFB driver. (#204552)
- Export copy_4K_page for ppc64

* Tue Sep 12 2006 David Woodhouse <dwmw2@redhat.com>
- GFS2 update

* Mon Sep 11 2006 Roland McGrath <roland@redhat.com>
- s390 single-step fix

* Mon Sep 11 2006 Dave Jones <davej@redhat.com>
- Add a PCI ID to sata_via
- Intel i965 DRM support.
- Fix NFS/Selinux oops. (#204848)

* Sat Sep  9 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc6-git3

* Fri Sep  8 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc6-git2

* Thu Sep  7 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc6-git1
- GFS2/DLM updates.

* Wed Sep  6 2006 Roland McGrath <roland@redhat.com>
- New utrace patch: fix 32-bit PTRACE_PEEKUSR for FP regs on ppc64. (#205179)

* Wed Sep  6 2006 Juan Quintela <quintela@redhat.com>
- Undo rhel5 xen patch for relocatable.

* Wed Sep  6 2006 Dave Jones <davej@redhat.com>
- AGP support for Intel I965

* Tue Sep  5 2006 Jeremy Katz <katzj@redhat.com>
- Update xenfb based on upstream review

* Tue Sep  5 2006 Dave Jones <davej@redhat.com>
- Numerous sparse fixes to Tux.

* Tue Sep  5 2006 Mike Christie <mchristi@redhat.com>
- update iscsi layer to what will be in 2.6.19-rc1

* Tue Sep  5 2006 Dave Jones <davej@redhat.com>
- NFS lockdep fixes.
- Make ia64 Altix IDE driver built-in instead of modular. (#205282)

* Mon Sep  4 2006 Juan Quintela <quintela@redhat.com>
- xenoprof upstream fix.
- update xen HV to cset 11394.
- xen update (3hypercall incompatibility included)
- linux-2.6 changeset: 34073:b1d36669f98d
- linux-2.6-xen-fedora changeset: 35901:b7112196674e
- xen-unstable changeset: 11204:5fc1fe79083517824d89309cc618f21302724e29
- fix ia64 (xen & net xen).

* Mon Sep  4 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc6
- Drop recent NFS changes completely.

* Sun Sep  3 2006 Dave Jones <davej@redhat.com>
- Fix bogus -EIO's over NFS (#204859)
- Enable ptrace in olpc kernels. (#204958)

* Sun Sep  3 2006 Marcelo Tosatti <mtosatti@redhat.com>
- Remove PAE, xen and kdump configs for olpc case

* Sun Sep  3 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc5-git7

* Sat Sep  2 2006 Dave Jones <davej@redhat.com>
- Fix up typo in tux.patch
- 2.6.18rc5-git6

* Wed Aug 30 2006 Juan Quintela <quintela@redhat.com>
- update xen-hv to cset 11256 (pre 3 hypercall breakage).
- remove debug=y from HV compilation.
- xen update (pre 3 hypercall breakage)
  * linux-2.6 changeset: 33957:421a6d428e95
  * linux-2.6-xen-fedora changeset: 35756:78332fcbe5b0
  * xen-unstable changeset: 11251:5fc1fe79083517824d89309cc618f21302724e29
  * get new irqflags code from linux-2.6.tip-xen.

* Wed Aug 30 2006 Jeremy Katz <katzj@redhat.com>
- Fix up DEFAULTKERNEL for kernel-xen[0U]->kernel-xen change

* Wed Aug 30 2006 Marcelo Tosatti <mtosatti@redhat.com>
- Fixes for DUB-E100 vB1 usb ethernet (backported from James M.)

* Tue Aug 29 2006 Jarod Wilson <jwilson@redhat.com>
- 2.6.18-rc5-git1

* Tue Aug 29 2006 Jeremy Katz <katzj@redhat.com>
- Fix serial console with xen dom0

* Tue Aug 29 2006 Don Zickus <dzickus@redhat.com>
- enabled EHEA driver
- x86 relocatable fixes
- audit code fixes for cachefs

* Mon Aug 28 2006 Jeremy Katz <katzj@redhat.com>
- Add updated pv framebuffer patch for Xen and re-enable the config options

* Mon Aug 28 2006 Juan Quintela <quintela@redhat.com>
- ia64 xen fixing.

* Sun Aug 27 2006 David Woodhouse <dwmw2@redhat.com>
- Fix V4L1 stuff in <linux/videodev.h> (#204225)

* Fri Aug 25 2006 Juan Quintela <quintela@redhat.com>
- update xen HV to xen-unstable cset 11251.
- fix ia64 xen HV compilation.
- linux xen kernel update:
  * linux-2.6 changeset: 33681:2695586981b9
  * linux-2.6-xen-fedora changeset: 35458:b1b8e00e7a17
  * linux-2.6-xen changeset: 22861:0b726fcb6780
  * xen-unstable changeset: 11204:5fc1fe79083517824d89309cc618f21302724e29

* Fri Aug 25 2006 Don Zickus <dzickus@redhat.com>
- build fix for ia64 kdump

* Fri Aug 25 2006 Don Zickus <dzickus@redhat.com>
- update utrace
- more gfs2-dlm fixes
- fix xen-devel build directory issue
- add x86, x86_64 relocatable kernel patch for rhel only (davej, forgive my sins)
  - applied xen relocatable cleanup on top of it
- add ia64 kexec/kdump pieces

* Fri Aug 25 2006 Jesse Keating <jkeating@redhat.com>
- Enable i386 for olpc so that kernel-headers is built

* Thu Aug 24 2006 David Woodhouse <dwmw2@redhat.com>
- Update GFS2 patch (from swhiteho)
- Enable kernel-headers build
- Enable i386 build _only_ for kernel-headers

* Tue Aug 22 2006 Don Zickus <dzickus@redhat.com>
- Another lockdep-fix
- NFS fix for the connectathon test
- Enable mmtimer for ia64
- Add support for iscsi qla4xxx

* Tue Aug 22 2006 Marcelo Tosatti <mtosatti@redhat.com>
- Add Libertas wireless driver

* Mon Aug 21 2006 Roland McGrath <roland@redhat.com>
- New utrace patch: experimental support for ia64, sparc64.

* Sun Aug 20 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc4-git1

* Sat Aug 19 2006 Dave Jones <davej@redhat.com>
- Update to latest upstream from GregKH's git tree.

* Sat Aug 19 2006 Juan Quintela <quintela@redhat.com>
- xen kernel update.
  * linux-2.6 changeset: 33525:dcc321d1340a
  * linux-2.6-xen-fedora changeset: 35247:400b0cf28ee4
  * linux-2.6-xen changeset: 22813:80c2ccf5c330
  * xen-unstable changeset: 11069:0340e579f06544431e915d17596ac144145a077e
- xen big config update.  Every config option is the same than normal kernel
  except MICROCODE, TCG_TPM & CONFIG_DEBUG_SLAB.
- disable XEN_FRAMEBUFFER & XEN_KEYBOARD.
- make sysrq c to "crash" all kernels.

* Thu Aug 17 2006 Don Zickus <dzickus@redhat.com>
- NFS 64-bit inode support
- QLogic firmware
- SELinux support for range transitions
- EHEA ethernet driver
- ppc irq mapping fix

* Wed Aug 16 2006 Roland McGrath <roland@redhat.com>
- New utrace patch:
  - Fix s390 single-step for real this time.
  - Revamp how arch code defines ptrace compatibility.

* Wed Aug 16 2006 Dave Jones <davej@redhat.com>
- Update to latest GregKH tree.
- Reenable debug.

* Tue Aug 15 2006 Don Zickus <dzickus@redhat.com>
- cleanup config-rhel-generic to compile again
- removed useless options in config-rhel-generic

* Tue Aug 15 2006 Don Zickus <dzickus@redhat.com>
- ppc64 spec cleanups

* Mon Aug 14 2006 Dave Jones <davej@redhat.com>
- Update to squashfs 3.1 which should fix stack overflows seen
  during installation.
- Merge framebuffer driver for OLPC.

* Sun Aug 13 2006 Juan Quintela <quintela@redhat.com>
- enable ia64 xen again.
- xen kernel-update linux-2.6-xen-fedora cset 35236:70890e6e4a72.
  * fix ia64 compilation problems.

* Sat Aug 12 2006 Juan Quintela <quintela@redhat.com>
- disable ia64 xen, it doesn't compile.
- xen HV update cset 11057:4ee64035c0a3
  (newer than that don't compile on ia64).
- update linux-2.6-xen patch to fix sort_regions on ia64.
- fix %%setup for xen HV to work at xen HV upgrades.

* Fri Aug 11 2006 Juan Quintela <quintela@redhat.com>
- xen HV update cset 11061:80f364a5662f.
- xen kernel update
  * linux-2.6-xen-fedora cset
  * linux-2.6-xen cset 22809:d4b3aba8876df169ffd9fac1d17bd88d87eb67c5.
  * xen-unstable 11060:323eb29083e6d596800875cafe6f843b5627d77b
  * Integrate xen virtual frame buffer patch.
  * Enable CONFIG_CRASH on xen.

* Fri Aug 11 2006 Dave Jones <davej@redhat.com>
- Yet more lockdep fixes.
- Update to GregKH's daily tree.
- GFS2/DLM locking bugfix

* Thu Aug 10 2006 Roland McGrath <roland@redhat.com>
- New utrace patch: fix ptrace synchronization issues.

* Thu Aug 10 2006 Dave Jones <davej@redhat.com>
- GFS2/DLM update.
- Daily GregKH updates
- More lockdep fixes.

* Wed Aug  9 2006 Roland McGrath <roland@redhat.com>
- Fix utrace_regset nits breaking s390.

* Wed Aug  9 2006 Dave Jones <davej@redhat.com>
- Another lockdep fix for networking.
- Change some hotplug PCI options.
- Daily update from GregKH's git tree.
- Unbreak SMP locking in oprofile.
- Fix hotplug CPU locking in workqueue creation.
- K8 EDAC support.
- IPsec labelling enhancements for MLS
- Netlabel: CIPSO labeled networking

* Tue Aug  8 2006 Roland McGrath <roland@redhat.com>
- Fix utrace/ptrace interactions with SELinux.

* Tue Aug  8 2006 Dave Jones <davej@redhat.com>
- Pull post-rc4 fixes from GregKH's git tree.

* Mon Aug  7 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc4

* Sun Aug  6 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc3-git7

* Fri Aug  4 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc3-git6
- Return of signed modules.

* Thu Aug  3 2006 Roland McGrath <roland@redhat.com>
- New utrace patch:
  - fix s390 single-step
  - first third of ia64 support, enable CONFIG_UTRACE (no ptrace yet)

* Fri Aug  3 2006 Juan Quintela <quintela@anano.mitica>
- Update linux-2.6-xen patch.
  * linux-2.6-xen-fedora cset 34931:a3fda906fb82
  * linux-2.6-xen cset 22777:158b51d317b76ebc94d61c25ad6a01d121dff750
  * xen-unstable cset  10866:4833dc75ce4d08e2adc4c5866b945c930a96f225

* Thu Aug  3 2006 Juan Quintela <quintela@redhat.com>
- xen hv compiled with -O2 through Config.mk
- Update xen HV cset 10294.

* Thu Aug  3 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc3-git3
- Fix PCI ID clash between ipr and dac960

* Thu Aug  3 2006 Jon Masters <jcm@redhat.com>
- Copy .config to include/config/auto.conf to avoid unnecessary "make prepare".
- This should finally fix #197220.
- Pulled in patch-2.6.18-rc3-git2.bz2.sign to fix SRPM build failure.

* Wed Aug  2 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc3-git2
- Readd patch to allow 460800 baud on 16C950 UARTs.
- Fix backtracing for interrupt stacks

* Wed Aug  2 2006 Jeremy Katz <katzj@redhat.com>
- add necessary ia64 hv fixes (#201040)

* Wed Aug  2 2006 Dave Jones <davej@redhat.com>
- More GFS2 bugfixing.

* Tue Aug  1 2006 Dave Jones <davej@redhat.com>
- s390 kprobes support.
- Fix oops in libata ata_device_add()
- Yet more fixes for lockdep triggered bugs.
- Merge numerous patches from -mm to improve software suspend.
- Fix incorrect section usage in MCE code that blew up on resume.

* Tue Aug  1 2006 Roland McGrath <roland@redhat.com>
- fix bogus BUG_ON in ptrace_do_wait

* Tue Aug  1 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc3-git1

* Tue Aug  1 2006 Juan Quintela <quintela@redhat.com>
- disable CONFIG_DEBUG_SLAB for xen (should fix #200127).

* Mon Jul 31 2006 Roland McGrath <roland@redhat.com>
- New utrace patch:
  - fix ptrace_do_wait deadlock (#200822, #200605)
  - arch cleanups

* Mon Jul 31 2006 Juan Quintela <quintela@redhat.com>
- disable blktap for xen-ia64 (don't compile).
- enable ia64-xen (it compiles, but still don't boot).

* Mon Jul 31 2006 Juan Quintela <quintela@redhat.com>
- Fix dlm s/u.generic_ip/i_private/.

* Mon Jul 31 2006 Don Zickus <dzickus@redhat.com>
- IA64 compile fixes

* Mon Jul 31 2006 Juan Quintela <quintela@redhat.com>
- Update xen patch to linux-2.6-xen-fedora cset 34801.
	* linux-2.6 cset 33175
	* no linux-2.6-xen updates.
- Remove xen x86_64 8 cpu limit.

* Mon Jul 31 2006 Dave Jones <davej@redhat.com>
- Numerous GFS2/DLM fixes.

* Mon Jul 31 2006 Jeremy Katz <katzj@redhat.com>
- new ahci suspend patch

* Mon Jul 31 2006 Dave Jones <davej@redhat.com>
- VFS: Destroy the dentries contributed by a superblock on unmounting [try #2]

* Sun Jul 30 2006 Jon Masters <jcm@redhat.com>
- Wasn't calling weak-modules properly.
- kabitool not being picked up (weird).

* Sun Jul 30 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc3

* Sat Jul 29 2006 Dave Jones <davej@redhat.com>
- lockdep fix: ipv6
- 2.6.18rc2-git7

* Fri Jul 28 2006 Don Zickus <dzickus@redhat.com>
- Refreshed NFS caching patches
- tweaked some ppc64 kdump config options

* Fri Jul 28 2006 Jon Masters <jcm@redhat.com>
- Remove make-symsets and built-in-where as now handled by kabitool

* Fri Jul 28 2006 Dave Jones <davej@redhat.com>
- Update futex-death patch.

* Thu Jul 27 2006 Roland McGrath <roland@redhat.com>
- s390 utrace fix

* Thu Jul 27 2006 Don Zickus <dzickus@redhat.com>
- Enable kdump on ppc64iseries.  yeah more rpms..

* Thu Jul 27 2006 Dave Jones <davej@redhat.com>
- Add missing export for ia64 (#200396)

* Thu Jul 27 2006 Juan Quintela <quintela@redhat.com>
- review all xen related patches.
- x86_64 dom0, x86_64 domU and i386 domU should work.
- fix xen i386 dom0 boot (#200382).

* Thu Jul 27 2006 Rik van Riel <riel@redhat.com>
- reduce hypervisor stack use with -O2, this really fixes bug (#198932)

* Wed Jul 26 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc2-git6

* Wed Jul 26 2006 Roland McGrath <roland@redhat.com>
- New utrace patch: unsafe_exec fix; s390 build enabled (but non-working).

* Wed Jul 26 2006 Juan Quintela <quintela@redhat.com>
- new xen patch based on linux-2.6-xen cset 22749.
  and linux-2.6 cset 33089.

* Wed Jul 26 2006 Dave Jones <davej@redhat.com>
- Enable sparsemem on ia64. (#108848)

* Wed Jul 26 2006 Juan Quintela <quintela@redhat.com>
- update xen-hv to 10730 cset, should really fix huge timeout problems.

* Wed Jul 26 2006 Juan Quintela <quintela@redhat.com>
- Workaround the huge timeouts problems on xen HV x86.
- xen update and cleanup/reorgatization of xen patches.

* Tue Jul 25 2006 Rik van Riel <riel@redhat.com>
- disable debug=y hypervisor build option because of stack overflow (#198932)

* Tue Jul 25 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc2-git4 & git5

* Tue Jul 25 2006 Jon Masters <jcm@redhat.com>
- Fix kabitool provided find-provides once again.

* Tue Jul 25 2006 Juan Quintela <quintela@redhat.com>
- Use cset number instead of date for xen hypervisor.
- Update xen hypervisor to cset 10712.

* Mon Jul 24 2006 Dave Jones <davej@redhat.com>
- 2.6.18rc2-git2 & git3
- Fix PI Futex exit crash.
- Fix an inotify locking bug.
- Add device mapper mirroring patches.

* Mon Jul 24 2006 Jon Masters <jcm@redhat.com>
- Change kabideps location.

* Mon Jul 24 2006 Juan Quintela <quintela@redhat.com>
- New xen patch, fixes gso, xenoprof, vDSO.

* Sat Jul 22 2006 Dave Jones <davej@redhat.com>
- Enable connector proc events.
- Enable PPC64 memory hotplug.
- 2.6.18rc2-git1

* Sat Jul 22 2006 Juan Quintela <quintela@redhat.com>
- addia64-xen support, not enabled by default.
- add ia64-xen config

* Fri Jul 21 2006 Jeremy Katz <katzj@redhat.com>
- Patch from jakub to use sysv style hash for VDSO to fix booting
  on ia64 (#199634, #199595)
- Fix e1000 crc calculation for things to work with xen
- Update gfs2 patchset

* Thu Jul 20 2006 Roland McGrath <roland@redhat.com>
- Clean up spec changes for debuginfo generation to cover Xen case.
- New version of utrace patch, fixes /proc permissions. (#199014)

* Thu Jul 20 2006 Juan Quintela <quintela@anano.mitica>
- remove xenPAE option, as now the i686 xen kernel is PAE.

* Thu Jul 20 2006 Juan Quintela <quintela@redhat.com>
- Fix to get xen debug info files in the right position.

* Thu Jul 20 2006 Don Zickus <dzickus@redhat.com>
- apparently I was wrong and was fixed already

* Thu Jul 20 2006 Don Zickus <dzickus@redhat.com>
- fixed build_debuginfo to not collect a stripped kernel

* Wed Jul 19 2006 Don Zickus <dzickus@redhat.com>
- Add in support for nfs superblock sharing and cachefs
  patches from David Howells
- Disable 'make prepare' hack as it is breaking ppc symlinks
- Added tracking dirty pages patch from Peter Zijlstra
- Fix for Opteron timer scaling
- Fix for Calgary pci hang

* Wed Jul 19 2006 Juan Quintela <quintela@redhat>
- big xen patch.
- enable xen again.
- redo xen config.
- i686 kernel for xen uses PAE now.
- new xen Hypervisor cset 10711.

* Wed Jul 19 2006 Roland McGrath <roland@redhat.com>
- New version of utrace patch, might fix #198780.

* Wed Jul 19 2006 Jon Masters <jcm@redhat.com>
- Workaround upstream "make prepare" bug by adding an additional prepare stage.
- Fix kabideps

* Tue Jul 18 2006 Jon Masters <jcm@redhat.com>
- Check in new version of kabitool for kernel deps.
- Fix kabitool for correct location of symvers.
- Various other fixes when things broke.

* Sun Jul 16 2006 Dave Jones <davej@redhat.com>
- Support up to 4GB in the 586 kernel again.
- Drop the FPU optimisation, it may be the reason for
  strange SIGFPE warnings various apps have been getting.

* Sat Jul 15 2006 Dave Jones <davej@redhat.com>
- Cleaned up a bunch of bogons in the config files.
- 2.6.18-rc1-git9,git10 & 2.6.18-rc2
- improvements to linked list debugging.

* Fri Jul 14 2006 Don Zickus <dzickus@redhat.com>
- remove the ppc kdump patches

* Fri Jul 14 2006 Dave Jones <davej@redhat.com>
- 2.6.18-rc1-git8

* Thu Jul 13 2006 Dave Jones <davej@redhat.com>
- 2.6.18-rc1-git7
- More lockdep fixes.
- Fix slab corruption issue.

* Thu Jul 13 2006 Mike Christie <mchristi@redhat.com>
- Add iscsi update being sent upstream for 2.6.18-rc2

* Thu Jul 13 2006 Roland McGrath <roland@redhat.com>
- Fix spec typo that swallowed kdump subpackage.

* Thu Jul 13 2006 Dave Jones <davej@redhat.com>
- 2.6.18-rc1-git6

* Wed Jul 12 2006 Roland McGrath <roland@redhat.com>
- Build separate debuginfo subpackages instead of a single one.

* Wed Jul 12 2006 Dave Jones <davej@redhat.com>
- 2.6.18-rc1-git5
- Make serial console installs on ia64 work again.
- Shrink struct inode.

* Wed Jul 12 2006 David Woodhouse <dwmw2@redhat.com>
- Temporarily disable -headers subpackage until the problems which
  arise from brew not using older package are dealt with.

* Wed Jul 12 2006 David Woodhouse <dwmw2@redhat.com>
- No headers subpackage for noarch build
- Fix PI-futexes to be properly unlocked on unexpected exit

* Wed Jul 12 2006 Dave Jones <davej@redhat.com>
- Add sleazy fpu optimisation.   Apps that heavily
  use floating point in theory should get faster.

* Tue Jul 11 2006 Dave Jones <davej@redhat.com>
- Add utrace. (ptrace replacement).

* Tue Jul 11 2006 David Woodhouse <dwmw2@redhat.com>
- Build iSeries again
- Minor GFS2 update
- Enable kernel-headers subpackage

* Tue Jul 11 2006 Dave Jones <davej@redhat.com>
- 2.6.18-rc1-git4

* Mon Jul 10 2006 Dave Jones <davej@redhat.com>
- 2.6.18-rc1-git3
- Big bunch o' lockdep patches from Arjan.

* Sun Jul  9 2006 Dave Jones <davej@redhat.com>
- 2.6.18-rc1-git2

* Fri Jul  7 2006 Don Zickus <dzickus@redhat.com>
- Unified rhel and fedora srpm

* Fri Jul  7 2006 Dave Jones <davej@redhat.com>
- Add lockdep annotate for bdev warning.
- Enable autofs4 to return fail for revalidate during lookup

* Thu Jul  6 2006 Dave Jones <davej@redhat.com>
- 2.6.18-rc1
- Disable RT_MUTEX_TESTER

* Wed Jul  5 2006 Dave Jones <davej@redhat.com>
- 2.6.17-git25

* Wed Jul  5 2006 Dave Jones <davej@redhat.com>
- Try out sparsemem experiment on x86-64.

* Wed Jul  5 2006 David Woodhouse <dwmw2@redhat.com>
- Fix asm-powerpc/cputime.h for new cputime64_t stuff
- Update GFS2

* Wed Jul  5 2006 Dave Jones <davej@redhat.com>
- Further lockdep improvements.

* Wed Jul  5 2006 David Woodhouse <dwmw2@redhat.com>
- 2.6.17-git24 (yay, headers_install)

* Tue Jul  4 2006 Dave Jones <davej@redhat.com>
- 2.6.17-git21, git22 & git23

* Sun Jul  2 2006 David Woodhouse <dwmw2@redhat.com>
- Add ppoll() and pselect() on x86_64 again

* Sat Jul  1 2006 Dave Jones <davej@redhat.com>
- 2.6.17-git19

* Fri Jun 30 2006 Dave Jones <davej@redhat.com>
- 2.6.17-git16 & git17

* Fri Jun 30 2006 Jeremy Katz <katzj@redhat.com>
- really fix up squashfs

* Thu Jun 29 2006 Dave Jones <davej@redhat.com>
- 2.6.17-git13, git14 & git15
- Hopefully fix up squashfs & gfs2

* Tue Jun 27 2006 Dave Jones <davej@redhat.com>
- 2.6.17-git12
- Disable the signed module patches for now, they need love.

* Mon Jun 26 2006 Dave Jones <davej@redhat.com>
- 2.6.17-git10 & git11
- Enable fake PCI hotplug driver. (#190437)
- Remove lots of 'modprobe loop's from specfile.

* Sun Jun 25 2006 Dave Jones <davej@redhat.com>
- 2.6.17-git8 & git9

* Sat Jun 24 2006 Dave Jones <davej@redhat.com>
- Enable profiling for 586 kernels.
- 2.6.17-git6 & git7
  This required lots of rediffing. SATA suspend, Promise PATA-on-SATA,
  Xen, exec-shield, and more.  Tread carefully, harmful if swallowed etc.

* Fri Jun 23 2006 Dave Jones <davej@redhat.com>
- 2.6.17-git5

* Fri Jun 23 2006 Jeremy Katz <katzj@redhat.com>
- update to squashfs 3.0

* Thu Jun 22 2006 Dave Jones <davej@redhat.com>
- 2.6.17-git4
- Update sysconfig/kernel on x86 %%post - Robert Scheck (#196307)

* Thu Jun 22 2006 David Woodhouse <dwmw2@redhat.com>
- MTD update

* Thu Jun 22 2006 David Woodhouse <dwmw2@redhat.com>
- Update GFS2 patch
- Apply 'make headers_install' unconditionally now Linus has the cleanups

* Wed Jun 21 2006 Dave Jones <davej@redhat.com>
- 2.6.17-git3

* Tue Jun 20 2006 David Woodhouse <dwmw2@redhat.com>
- Update MTD tree, Update and re-enable Geode tree
- Remove AC97 patch obsoleted by Geode tree

* Tue Jun 20 2006 Dave Jones <davej@redhat.com>
- 2.6.17-git1

* Sun Jun 18 2006 Dave Jones <davej@redhat.com>
- 2.6.17

* Sat Jun 17 2006 David Woodhouse <dwmw2@redhat.com>
- Add Geode and MTD git trees (for OLPC)

* Thu Jun 15 2006 Don Zickus <dzickus@redhat.com>
- rhelbuild clean ups
- add back in support for iSeries and s390 (needed internally only)

* Thu Jun 15 2006 Jeremy Katz <katzj@redhat.com>
- fix installation of -xen kernel on baremetal to be dom0 grub config

* Wed Jun 14 2006 Dave Jones <davej@redhat.com>
- 2.6.17-rc6-git7
- Console fixes for suspend/resume
- Drop support for PPC iseries & 31bit s390.

* Wed Jun 14 2006 Juan Quintela <quintela@redhat.com>
- remove xen0/xenU/xen0-PAE/xenU-PAE packages
- disable xen PAE kernel for i386 for now
- create xen-PAE kernel
- remove %%requires xen from xen kernels

* Wed Jun 14 2006 Juan Quintela <quintela@redhat.com>
- rename xen0 & xenU to single xen kernels.

* Tue Jun 13 2006 Dave Jones <davej@redhat.com>
- 2.6.17-rc6-git5
- serial/tty resume fixing.

* Mon Jun 12 2006 Dave Jones <davej@redhat.com>
- 2.6.17-rc6-git3
- autofs4 - need to invalidate children on tree mount expire

* Sun Jun 11 2006 Dave Jones <davej@redhat.com>
- 2.6.17-rc6-git2
- Add MyMusix PD-205 to the unusual USB quirk list.
- Silence noisy unimplemented 32bit syscalls on x86-64.

* Sat Jun 10 2006 Juan Quintela <quintela@redhat.com>
- rebase xen to linux-2.6 cset 27412
- rebase xen to linux-2.6-xen cset 22608
- rebase HV cset 10314

* Fri Jun  9 2006 David Woodhouse <dwmw2@redhat.com>
- Update GFS2 patch, export GFS2 and DLM headers

* Fri Jun  9 2006 Dave Jones <davej@redhat.com>
- Disable KGDB again, it broke serial console :(
- 2.6.17-rc6-git1

* Wed Jun  7 2006 Dave Jones <davej@redhat.com>
- Experiment: Add KGDB.
- AC97 fix for OLPC.

* Tue Jun  6 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc6. Special 6/6/6 edition, what could go wrong?
- Add a kdump kernel for PPC64 (Don Zickus)
- Enable SCHED_STATS

* Mon Jun  5 2006 Dave Jones <davej@redhat.com>
- Do PCI config space restore on resume in reverse.
- Make Powernow-k7 work again.
- Fix the setuid /proc/self/maps fix (#165351, #190128)

* Sun Jun  4 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc5-git11

* Fri Jun  2 2006 Dave Jones <davej@redhat.com>
- Drop previous autofs4 patch, it was broken.

* Fri Jun  2 2006 Juan Quintela <quintela@redhat.com>
- disable PAE for now
- update xen HV to xen-unstable cset 10243
- rebase xen-patch to linux-2.6-xen cset 22568
- rebase xen-patch to linux-2.6 cset 27329

* Thu Jun  1 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc5-git8

* Wed May 31 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc5-git7
- Ressurect V4L1, too much still depends on it.

* Tue May 30 2006 Dave Jones <davej@redhat.com>
- Fix up CFQ locking bug.
- 2.6.17rc5-git6
- Update iscsi to what will be pushed for 2.6.18

* Tue May 30 2006 Jon Masters <jcm@redhat.com>
- Add KMP enablers to kernel spec file.

* Mon May 29 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc5-git5
- autofs4: spoof negative dentries from mount fails on browseable
  indirect map mount points
- Make acpi-cpufreq sticky.

* Sun May 28 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc5-git4

* Sat May 27 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc5-git2 & git3

* Fri May 26 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc5-git1

* Thu May 25 2006 Juan Quintela <quintela@redhat.com>
- enable xen PAE kernels for testing.
- rebase xen patch (linux-2.6-xen cset 22558, linux-2.6 cset 27227)

* Thu May 25 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc5
- Merge GFS2/DLM (Steven Whitehouse)
- Remove .orig's during rpmbuild. (#192982)

* Wed May 24 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc4-git13

* Wed May 24 2006 Juan Quintela <quintela@redhat.com>
- remove xen-irq-patch included upstream.
- rebase xen hipervisor to xen-unstable cset 10140.
- rebase xen patch linux-2.6-xen cset 22552.

* Tue May 23 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc4-git11

* Mon May 22 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc4-git10

* Sat May 20 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc4-git9

* Thu May 18 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc4-git6

* Wed May 17 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc4-git5

* Tue May 16 2006 Juan Quintela <quintela@redhat.com>
- rebase xen to cset 28078.

* Sun May 16 2006 David Woodhouse <dwmw2@redhat.com>
- 2.6.17rc4-git3

* Sun May 14 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc4-git2

* Thu May 11 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc4

* Tue May  9 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc3-git17

* Mon May  8 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc3-git15

* Sat May  6 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc3-git12

* Fri May  5 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc3-git11

* Fri May  5 2006 David Woodhouse <dwmw2@redhat.com>
- Fix #190776 by rediffing the patch so it actually gets applied properly
- Fix the machine check too.

* Fri May  5 2006 David Woodhouse <dwmw2@redhat.com>
- Remove bcm43xx-assoc-on-startup patch. I don't think the original
  problem is fixed upstream yet, but this patch causes BZ #190776.

* Fri May  5 2006 Juan Quintela <quintela@redhat.com>
- fix irq handling on xen Hypervisor.
- rebase to linux-2.6-xen-fedora cset 27866

* Thu May  4 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc3-git10

* Thu May  4 2006 Jeremy Katz <katzj@redhat.com>
- improved ahci suspend patch from Forrest Zhao

* Wed May  3 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc3-git8

* Wed May  3 2006 Juan Quintela <quintela@redhat.com>
- rebase xen-unstable HV 9920"

* Tue May  2 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc3-git6

* Tue May  2 2006 Juan Quintela <quintela@redhat.com>
- rebase on linux-2.6 & linux-2.6-xen as of May,1st.
- new HV from xen-unstable as of 20060428.
- fixed the binaries included on xen tarball :p

* Mon May  1 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc3-git4

* Sun Apr 30 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc3-git3

* Fri Apr 28 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc3-git2

* Fri Apr 28 2006 David Woodhouse <dwmw2@redhat.com>
- Disable Xen on the basis that it doesn't build
- Check for Xen tarball being unclean, abort early even on i386.

* Thu Apr 27 2006 Juan Quintela <quintela@redhat.com>
- Remove figlet by hand again.
- Enable xen again
- rebase linux-2.6-xen linux-2.6-xen
- fix & enable xenoprof

* Wed Apr 26 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc3
- 2.6.17rc2-git8

* Wed Apr 26 2006 David Woodhouse <dwmw2@redhat.com>
- Don't include /usr/include/scsi in kernel-headers for now, because
  glibc ships those for itself. Update header cleanup patches so that
  glibc actually builds against the resulting headers

* Wed Apr 26 2006 Juan Quintela <quintela@redhat.com>
- Delete figlet form xen hypervisor.

* Wed Apr 26 2006 David Woodhouse <dwmw2@redhat.com>
- Include kernel-headers subpackage, conditionally (and off for now)

* Wed Apr 26 2006 Juan Quintela <quintela@redhat.com>
- rebase with last linux-2.6-xen.
- enable xen again.

* Tue Apr 25 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc2-git7

* Tue Apr 25 2006 David Woodhouse <dwmw2@redhat.com>
- Drop the last remnants of the 'make bzImage on all arches' silliness

* Sun Apr 23 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc2-git5

* Sat Apr 22 2006 Dave Jones <davej@redhat.com>
- Ugly SATA suspend/resume hack de jour.

* Sat Apr 22 2006 Juan Quintela <quintela@redhat.com>
- rebase xen.
- fix x86_64 xen (thanks chris).
- enable xen again.

* Fri Apr 21 2006 Dave Jones <davej@redhat.com>
- Make Promise PATA on SATA work again (thanks Jim Bevier)
- 2.6.17rc2-git4

* Thu Apr 20 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc2-git3
- Make AHCI suspend/resume work.

* Wed Apr 19 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc2-git1
- Use unicode VTs by default.

* Tue Apr 18 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc2
- 2.6.17rc1-git13
- Enable DECNET to keep both users happy. (#120628)
- Enable TPM modules. (#189020)
- Enable some SGI specific ia64 options. (#188915)
- Add missing -kdump %%preuninstall (#189100)

* Mon Apr 17 2006 Juan Quintela <quintela@redhat.com>
- enable xen again.

* Sun Apr 16 2006 Dave Jones <davej@redhat.com>
- Big rebase to 2.6.17-rc1-git12

* Fri Apr 14 2006 Juan Quintela <quintela@redhat.com>
- Enable xen again.
- Update xen hypervisor to cset 9638.
- Update xen patch to linux-2.6.tip-xen.hg cset 26602.
- Remove/rediff lots of patches.
- x86_64 xen don't work, fixing that.

* Wed Apr 12 2006 David Woodhouse <dwmw2@redhat.com>
- Add include/{mtd,rdma,keys} directories to kernel-devel package

* Tue Apr 11 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc1-git4

* Mon Apr 10 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc1-git2 & git3
- Enable SMP on all x86 kernels.
  SMP_ALTERNATIVES disables the spinlocks etc at runtime.
- setuid /proc/self/maps fix (#165351)

* Thu Apr  6 2006 Dave Jones <davej@redhat.com>
- Rebuild without a zillion warnings.

* Tue Apr  4 2006 Dave Jones <davej@redhat.com>
- Reenable non-standard serial ports. (#187466)
- Reenable snd-es18xx for x86-32 (#187733)
- Map x86 kernel to 4MB physical address.

* Mon Apr  3 2006 Dave Jones <davej@redhat.com>
- Disable 'quiet' mode.

* Sun Apr  2 2006 Dave Jones <davej@redhat.com>
- 2.6.17rc1

* Sun Apr  2 2006 James Morris <jmorris@redhat.com>
- Rework dom0 sedf scheduler defaults patch, bz # 181856

* Sat Apr  1 2006 Dave Jones <davej@redhat.com>
- 2.6.16-git20

* Fri Mar 31 2006 Dave Jones <davej@redhat.com>
- 2.6.16-git19

* Fri Mar 31 2006 David Woodhouse <dwmw2@redhat.com>
- Send standard WEXT events on softmac assoc/disassociation.
- OFFB udpate

* Thu Mar 30 2006 Dave Jones <davej@redhat.com>
- 2.6.16-git18
- Reenable CONFIG_PCI_MSI

* Wed Mar 29 2006 Dave Jones <davej@redhat.com>
- 2.6.16-git16 & git17

* Tue Mar 28 2006 Dave Jones <davej@redhat.com>
- 2.6.16-git14 & git15
- reenable sky2.

* Mon Mar 27 2006 Dave Jones <davej@redhat.com>
- 2.6.16-git13
- Fix broken x86-64 32bit vDSO (#186924)

* Sat Mar 25 2006 Dave Jones <davej@redhat.com>
- 2.6.16-git10

* Fri Mar 24 2006 Dave Jones <davej@redhat.com>
- 2.6.16-git9

* Fri Mar 24 2006 David Woodhouse <dwmw2@redhat.com>
- Fix lockup when someone takes the bcm43xx device down while it's
  scanning (#180953)

* Thu Mar 23 2006 Juan Quintela <quintela@redhat.com>
- disable sky2 (as it is broken upstream)

* Thu Mar 23 2006 Juan Quintela <quintela@redhat.com>
- fix xen to compile with 2.6.16-git6.

* Thu Mar 23 2006 Dave Jones <davej@redhat.com>
- 2.6.16-git6

* Wed Mar 22 2006 Dave Jones <davej@redhat.com>
- 2.6.16-git5

* Wed Mar 22 2006 David Woodhouse <dwmw2@redhat.com>
- Update the bcm43xx driver to make it work nicely with initscripts
  and NetworkManager without user intervention.
- Fix Tux build

* Tue Mar 21 2006 Dave Jones <davej@redhat.com>
- 2.6.16-git3
- Improve spinlock scalability on big machines.

* Tue Mar 21 2006 Juan Quintela <quintela@redhat.com>
- rebase to xen unstable cset 9334.

* Tue Mar 21 2006 Juan Quintela <quintela@redhat.com>
- buildxen again.

* Mon Mar 20 2006 Juan Quintela <quintela@redhat.com>
- fix xen vmx in 64 bits.

* Mon Mar 20 2006 Dave Jones <davej@redhat.com>
- 2.6.16 & 2.6.16-git1
- Tux 2.6.16-A0 (Just rediffing)
- Update Ingo's latency tracer patch.
- Update exec-shield to Ingo's latest.
  (Incorporates John Reiser's "map the vDSO intelligently" patch
   which increases the efficiency of prelinking - #162797).
- ACPI ecdt uid hack. (#185947)

* Sun Mar 19 2006 Dave Jones <davej@redhat.com>
- 2.6.16rc6-git12
- Enable EFI on x86.

* Sat Mar 18 2006 Dave Jones <davej@redhat.com>
- 2.6.16rc6-git10 & git11

* Fri Mar 17 2006 Dave Jones <davej@redhat.com>
- 2.6.16rc6-git8 & git9

* Thu Mar 16 2006 Dave Jones <davej@redhat.com>
- 2.6.16rc6-git7

* Wed Mar 15 2006 Dave Jones <davej@redhat.com>
- 2.6.16rc6-git5
- Unmark 'print_tainted' as a GPL symbol.

* Tue Mar 14 2006 Dave Jones <davej@redhat.com>
- FC5 final kernel
- 2.6.16-rc6-git3
