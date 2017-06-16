This repository contains sources for RPMs that are used
to build Software Collections for CentOS by SCLo SIG.

This branch is for librabbitmq, dependency of php-pecl-amqp
This package only build the static library

    build -bs *spec --define "dist .el7"
    cbs add-pkg    sclo7-sclo-php70-sclo-candidate --owner=sclo  librabbitmq
    cbs add-pkg    sclo7-sclo-php56-sclo-candidate --owner=sclo  librabbitmq
    cbs build      sclo7-sclo-php70-sclo-el7       <above>.src.rpm
 	cbs tag-build  sclo7-sclo-php56-sclo-candidate <above build>

    build -bs *spec --define "dist .el6"
    cbs add-pkg    sclo6-sclo-php70-sclo-candidate --owner=sclo  librabbitmq
    cbs add-pkg    sclo6-sclo-php56-sclo-candidate --owner=sclo  librabbitmq
    cbs build      sclo6-sclo-php70-sclo-el6       <above>.src.rpm
 	cbs tag-build  sclo6-sclo-php56-sclo-candidate <above build>

