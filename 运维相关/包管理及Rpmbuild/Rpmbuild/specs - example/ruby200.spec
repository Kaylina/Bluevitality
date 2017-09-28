%define rubyver         2.0.0
%define rubyminorver    p247

Name:           ruby20
Version:        %{rubyver}%{rubyminorver}
Release:        2%{?dist}
License:        Ruby License/GPL - see COPYING
URL:            http://www.ruby-lang.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  readline readline-devel ncurses ncurses-devel gdbm gdbm-devel glibc-devel tcl-devel gcc unzip openssl-devel db4-devel byacc make libyaml-devel
Source0:        ftp://ftp.ruby-lang.org/pub/ruby/ruby-%{rubyver}-%{rubyminorver}.tar.gz
Summary:        An interpreter of object-oriented scripting language
Group:          Development/Languages
#Provides: ruby(abi) = 2.0
#Provides: ruby-irb
#Provides: ruby-rdoc
#Provides: ruby-libs
#Provides: ruby-devel
#Provides: rubygems
#Obsoletes: ruby
#Obsoletes: ruby-libs
#Obsoletes: ruby-irb
#Obsoletes: ruby-rdoc
#Obsoletes: ruby-devel
#Obsoletes: rubygems

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%prep
%setup -n ruby-%{rubyver}-%{rubyminorver}

%build
export CFLAGS="$RPM_OPT_FLAGS -Wall -fno-strict-aliasing"

./configure --prefix=/opt/rubies/ruby-%{rubyver}-%{rubyminorver} \
  --enable-shared \
  --disable-rpath \

make %{?_smp_mflags}

%install
# installing binaries ...
make install DESTDIR=$RPM_BUILD_ROOT

#we don't want to keep the src directory
rm -rf $RPM_BUILD_ROOT/usr/src

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
#%{_bindir}
#%{_includedir}
#%{_datadir}
#%{_libdir}
/opt/rubies/ruby-%{rubyver}-%{rubyminorver}

%changelog
* Thu May 08 2014 Ivan Polonevich <joni @ wargaming dot net> - 2.0.0p247-2
- Initial build for WG

* Wed May 22 2013 Takehiro Matsushima <takehiro.dreamizm@gmail.com> - 2.0.0-p195
- Update ruby version to 2.0.0-p195
* Wed Jan 18 2012 Mandi Walls <mandi.walls@gmail.com> - 1.9.3-p0
- Update ruby version to 1.9.3-p0
* Mon Aug 29 2011 Gregory Graf <graf.gregory@gmail.com> - 1.9.2-p290
- Update ruby version to 1.9.2-p290
* Sat Jun 25 2011 Ian Meyer <ianmmeyer@gmail.com> - 1.9.2-p180-2
- Remove non-existant --sitearchdir and --vedorarchdir from %configure
- Replace --sitedir --vendordir with simpler --libdir
- Change %{_prefix}/share to %{_datadir}

* Tue Mar 7 2011 Robert Duncan <robert@robduncan.co.uk> - 1.9.2-p180-1
- Update prerequisites to include make
- Update ruby version to 1.9.2-p180
- Install /usr/share documentation
- (Hopefully!?) platform agnostic

* Sun Jan 2 2011 Ian Meyer <ianmmeyer@gmail.com> - 1.9.2-p136-1
- Initial spec to replace system ruby with 1.9.2-p136
