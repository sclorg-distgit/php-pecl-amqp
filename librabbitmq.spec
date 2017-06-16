# CentOS SCLo spec file for librabbitmq
# Only static library
#
# Fedora spec file for librabbitmq
#
# Copyright (c) 2012-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_commit   caad0ef1533783729c7644a226c989c79b4c497b
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    alanxz
%global gh_project  rabbitmq-c
%global libname     librabbitmq

Name:      %{libname}
Summary:   Client library for AMQP
Version:   0.8.0
Release:   2%{?dist}
License:   MIT
Group:     System Environment/Libraries
URL:       https://github.com/alanxz/rabbitmq-c

Source0:   https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRequires: cmake > 2.8
BuildRequires: popt-devel
BuildRequires: openssl-devel
# For man page
BuildRequires: xmlto


%description
This is a C-language AMQP client library for use with AMQP servers
speaking protocol versions 0-9-1.


%package devel
Summary:    Header files and development libraries for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and development libraries
for %{name}.


%package tools
Summary:    Example tools built using the librabbitmq package
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}

%description tools
This package contains example tools built using %{name}.

It provides:
amqp-consume        Consume messages from a queue on an AMQP server
amqp-declare-queue  Declare a queue on an AMQP server
amqp-delete-queue   Delete a queue from an AMQP server
amqp-get            Get a message from a queue on an AMQP server
amqp-publish        Publish a message on an AMQP server


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Copy sources to be included in -devel docs.
cp -pr examples Examples


%build
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
%cmake \
  -DBUILD_TOOLS_DOCS:BOOL=ON \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
  -DBUILD_STATIC_LIBS:BOOL=ON

make %{_smp_mflags}


%install
make install  DESTDIR="%{buildroot}"


%check
: check .pc is usable
grep @ %{buildroot}%{_libdir}/pkgconfig/librabbitmq.pc && exit 1

: upstream tests
make test



%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE-MIT


%files devel
%doc AUTHORS THANKS TODO *.md
%doc Examples
%{_libdir}/%{libname}.a
%{_includedir}/amqp*
%{_libdir}/pkgconfig/%{libname}.pc

%files tools
%defattr (-,root,root,-)
%{_bindir}/amqp-*
%doc %{_mandir}/man1/amqp-*.1*
%doc %{_mandir}/man7/librabbitmq-tools.7*


%changelog
* Fri Jun 16 2017 Remi Collet <remi@remirepo.net> - 0.8.0-2
- build with --fPIC

* Fri Jun 16 2017 Remi Collet <remi@remirepo.net> - 0.8.0-1
- cleanup for SCLo build
- provide only the static library

* Tue Apr 12 2016 Remi Collet <remi@fedoraproject.org> - 0.8.0-1
- update to 0.8.0

* Tue Oct 13 2015 Remi Collet <remi@fedoraproject.org> - 0.7.1-1
- update to 0.7.1

* Fri Jul  3 2015 Remi Collet <remi@fedoraproject.org> - 0.7.0-1
- update to 0.7.0
- swicth to cmake
- switch from upstream tarball to github sources

* Mon Apr 20 2015 Remi Collet <remi@fedoraproject.org> - 0.6.0-1
- update to 0.6.0
- soname changed to .4
- rename to librabbitmq-last (except F23+)

* Mon Sep 15 2014 Remi Collet <remi@fedoraproject.org> - 0.5.2-1
- update to 0.5.2

* Wed Aug 13 2014 Remi Collet <remi@fedoraproject.org> - 0.5.1-1
- update to 0.5.1
- fix license handling
- move all documentation in devel subpackage

* Mon Feb 17 2014 Remi Collet <remi@fedoraproject.org> - 0.5.0-1
- update to 0.5.0
- open https://github.com/alanxz/rabbitmq-c/issues/169 (version is 0.5.1-pre)
- open https://github.com/alanxz/rabbitmq-c/issues/170 (amqp_get_server_properties)

* Mon Jan 13 2014 Remi Collet <remi@fedoraproject.org> - 0.4.1-4
- drop BR python-simplejson

* Tue Jan  7 2014 Remi Collet <remi@fedoraproject.org> - 0.4.1-3
- fix broken librabbitmq.pc, #1039555
- add check for usable librabbitmq.pc

* Thu Jan  2 2014 Remi Collet <remi@fedoraproject.org> - 0.4.1-2
- fix Source0 URL

* Sat Sep 28 2013 Remi Collet <remi@fedoraproject.org> - 0.4.1-1
- update to 0.4.1
- add ssl support

* Thu Aug  1 2013 Remi Collet <remi@fedoraproject.org> - 0.3.0-3
- cleanups

* Wed Mar 13 2013 Remi Collet <remi@fedoraproject.org> - 0.3.0-2
- remove tools from main package

* Wed Mar 13 2013 Remi Collet <remi@fedoraproject.org> - 0.3.0-1
- update to 0.3.0
- create sub-package for tools

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-0.2.git2059570
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 01 2012 Remi Collet <remi@fedoraproject.org> - 0.2-0.1.git2059570
- update to latest snapshot (version 0.2, moved to github)
- License is now MIT

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.3.hgfb6fca832fd2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 11 2012 Remi Collet <remi@fedoraproject.org> - 0.1-0.2.hgfb6fca832fd2
- add %%check (per review comment)

* Sat Mar 10 2012 Remi Collet <remi@fedoraproject.org> - 0.1-0.1.hgfb6fca832fd2
- Initial RPM

