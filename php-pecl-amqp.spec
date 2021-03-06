# centos/sclo spec file for php-pecl-amqp, from:
#
# remirepo spec file for php-pecl-amqp
# with SCL compatibility, from:
#
# Fedora spec file for php-pecl-amqp
#
# Copyright (c) 2012-2019 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%global sub_prefix  %{scl_prefix}
%if "%{scl}" == "rh-php70"
%global sub_prefix sclo-php70-
%endif
%if "%{scl}" == "rh-php71"
%global sub_prefix sclo-php71-
%endif
%if "%{scl}" == "rh-php72"
%global sub_prefix sclo-php72-
%endif
%if "%{scl}" == "rh-php73"
%global sub_prefix sclo-php73-
%endif
%scl_package        php-pecl-amqp
%endif

%global pecl_name   amqp
%global ini_name    40-%{pecl_name}.ini

Summary:       Communicate with any AMQP compliant server
Name:          %{?sub_prefix}php-pecl-amqp
Version:       1.9.4
Release:       2%{?dist}
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/amqp
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}%{?prever}.tgz

BuildRequires: %{?scl_prefix}php-devel > 5.6
BuildRequires: %{?scl_prefix}php-pear
# Upstream requires 0.5.2, set 0.8.0 to ensure proper version is used.
BuildRequires: librabbitmq-devel   >= 0.8.0

Requires:         %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:         %{?scl_prefix}php(api) = %{php_core_api}

Provides:         %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:         %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:         %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:         %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:         %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:         %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This extension can communicate with any AMQP spec 0-9-1 compatible server,
such as RabbitMQ, OpenAMQP and Qpid, giving you the ability to create and
delete exchanges and queues, as well as publish to any exchange and consume
from any queue.


%prep
%setup -q -c

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

mv %{pecl_name}-%{version}%{?prever} NTS

cd NTS
sed -e 's/CFLAGS="-I/CFLAGS="-fPIC -I/' -i config.m4

# Upstream often forget to change this
extver=$(sed -n '/#define PHP_AMQP_VERSION/{s/.* "//;s/".*$//;p}' php_amqp.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension = %{pecl_name}.so

; Whether calls to AMQPQueue::get() and AMQPQueue::consume()
; should require that the client explicitly acknowledge messages. 
; Setting this value to 1 will pass in the AMQP_AUTOACK flag to
; the above method calls if the flags field is omitted.
;amqp.auto_ack = 0

; The host to which to connect.
;amqp.host = localhost

; The login to use while connecting to the broker.
;amqp.login = guest

; The password to use while connecting to the broker.
;amqp.password = guest

; The port on which to connect.
;amqp.port = 5672

; The number of messages to prefect from the server during a 
; call to AMQPQueue::get() or AMQPQueue::consume() during which
; the AMQP_AUTOACK flag is not set.
;amqp.prefetch_count = 3

; The virtual host on the broker to which to connect.
;amqp.vhost = /

; Timeout
;amqp.timeout =
;amqp.read_timeout = 0
;amqp.write_timeout = 0
;amqp.connect_timeout = 0

;amqp.channel_max = 256
;amqp.frame_max = 131072
;amqp.heartbeat = 0

;amqp.cacert = ''
;amqp.cert = ''
;amqp.key = ''
;amqp.verify = ''
;amqp.sasl_method = 0
EOF


%build
cd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}


%install
make -C NTS install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -Dpm 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# Documentation
cd NTS
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    -m | grep %{pecl_name}


# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so


%changelog
* Fri Oct 25 2019 Remi Collet <remi@remirepo.net> - 1.9.4-2
- build for sclo-php72

* Wed Jan  2 2019 Remi Collet <remi@remirepo.net> - 1.9.4-1
- update to 1.9.4
- drop patch merged upstream
- raise minimal PHP version to 5.6

* Thu Nov 15 2018 Remi Collet <remi@remirepo.net> - 1.9.3-3
- build for sclo-php72

* Tue May 15 2018 Remi Collet <remi@remirepo.net> - 1.9.3-2
- rebuild against librabbitmq 0.8.0 in RHEL 7.5

* Thu Oct 19 2017 Remi Collet <remi@remirepo.net> - 1.9.3-1
- Update to 1.9.3 (stable)

* Fri Jun 16 2017 Remi Collet <remi@remirepo.net> - 1.9.1-1
- cleanup for SCLo build

* Mon Jun 12 2017 Remi Collet <remi@remirepo.net> - 1.9.1-1
- Update to 1.9.1 (stable)

* Tue Mar 21 2017 Remi Collet <remi@remirepo.net> - 1.9.0-1
- update to 1.9.0 (stable)

* Mon Mar 13 2017 Remi Collet <remi@remirepo.net> - 1.9.0-0.2.beta2
- Update to 1.9.0beta2
- drop patch merged upstream

* Mon Mar 13 2017 Remi Collet <remi@remirepo.net> - 1.9.0-0.1.beta1
- Update to 1.9.0beta1
- add patch from https://github.com/pdezwart/php-amqp/pull/274

* Sun Feb 19 2017 Remi Collet <remi@remirepo.net> - 1.8.0-2
- ensure proper librabbitmq version is used

* Fri Feb 17 2017 Remi Collet <remi@remirepo.net> - 1.8.0-1
- update to 1.8.0 (stable)

* Thu Dec  1 2016 Remi Collet <remi@fedoraproject.org> - 1.8.0-0.3.beta2
- rebuild with PHP 7.1.0 GA

* Mon Nov  7 2016 Remi Collet <remi@fedoraproject.org> - 1.8.0-0.2.beta2
- update to 1.8.0beta2

* Tue Nov  1 2016 Remi Collet <remi@fedoraproject.org> - 1.8.0-0.1.beta1
- update to 1.8.0beta1

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 1.7.1-2
- rebuild for PHP 7.1 new API version

* Sun Jul 10 2016 Remi Collet <remi@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1 (php 5 and 7, stable)

* Tue Apr 26 2016 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- update to 1.7.0 (php 5 and 7, stable)

* Fri Mar  4 2016 Remi Collet <remi@fedoraproject.org> - 1.7.0-0.3.alpha2
- adapt for F24

* Sat Dec 26 2015 Remi Collet <remi@fedoraproject.org> - 1.7.0-0.2.alpha2
- update to 1.7.0alpha2

* Thu Nov 12 2015 Remi Collet <remi@fedoraproject.org> - 1.7.0-0.1.alpha1
- update to 1.7.0alpha1

* Tue Nov  3 2015 Remi Collet <remi@fedoraproject.org> - 1.6.0-2
- update to 1.6.0 (stable)
- fix typo in config file

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.6.0-0.4.beta4
- open https://github.com/pdezwart/php-amqp/pull/178 - librabbitmq 0.5
- open https://github.com/pdezwart/php-amqp/pull/179 --with-libdir

* Fri Sep 18 2015 Remi Collet <remi@fedoraproject.org> - 1.6.0-0.3.beta4
- update to 1.6.0beta4

* Fri Jun 19 2015 Remi Collet <remi@fedoraproject.org> - 1.6.0-0.2.beta3
- allow build against rh-php56 (as more-php56)

* Mon Apr 20 2015 Remi Collet <remi@fedoraproject.org> - 1.6.0-0.1.beta3
- update to 1.6.0beta3
- drop runtime dependency on pear, new scriptlets
- don't install/register tests

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.4.0-1.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.4.0-1
- improve SCL build

* Tue Apr 15 2014 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- update to 1.6.0 (stable)

* Wed Apr  9 2014 Remi Collet <remi@fedoraproject.org> - 1.4.0-0.3.beta2
- add numerical prefix to extension configuration file

* Sun Mar  9 2014 Remi Collet <remi@fedoraproject.org> - 1.4.0-0.2.beta2
- update to 1.4.0beta2

* Thu Jan 16 2014 Remi Collet <remi@fedoraproject.org> - 1.4.0-0.1.beta1
- update to 1.4.0beta1
- adapt for SCL

* Mon Nov 25 2013 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- update to 1.3.0 (beta)
- cleanups for Copr
- install doc in pecl doc_dir
- install tests in pecl test_dir (in devel)
- add --with tests option to run upstream tests during build

* Sat Sep 28 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-2
- rebuild with librabbitmq 0.4.1

* Thu May 30 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0 (stable)

* Fri Apr 19 2013 Remi Collet <remi@fedoraproject.org> - 1.0.10-1
- Update to 1.0.10 (stable)

* Wed Mar 13 2013 Remi Collet <remi@fedoraproject.org> - 1.0.9-3
- rebuild for new librabbitmq

* Tue Nov 13 2012 Remi Collet <remi@fedoraproject.org> - 1.0.9-1
- update to 1.0.9 (stable)

* Mon Nov 12 2012 Remi Collet <remi@fedoraproject.org> - 1.0.8-1
- update to 1.0.8 (stable)
- build ZTS extension
- also provides php-amqp

* Wed Sep 12 2012 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- update to 1.0.7 (stable)
- cleanups

* Mon Aug 27 2012 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- update to 1.0.5
- LICENSE now provided in upstream tarball

* Wed Aug 01 2012 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 19 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- update to 1.0.3
- add extension version check (and fix)

* Mon Mar 19 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-3
- clean EL-5 stuff as requires php 5.2.0, https://bugs.php.net/61351

* Sat Mar 10 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- rebuild for PHP 5.4

* Sat Mar 10 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Initial RPM release without ZTS extension
- open request for LICENSE file https://bugs.php.net/61337

