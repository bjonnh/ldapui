#!/usr/bin/env bash

docker run -it --rm --name ldapui_test_openldap \
           -p 127.0.1.1:389:389 \
           -e DEBUG_LEVEL=1 \
           -e DOMAIN=test.nprod.net \
           -e ORGANIZATION="Test Instance LDAP" \
           -e PASSWORD=1234567890 \
           mwaeckerlin/openldap
