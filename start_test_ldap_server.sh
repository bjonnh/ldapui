#!/usr/bin/env bash

docker run -d --rm --name ldapui_test_openldap \
           -p 127.0.1.1:389:389 \
           -e DEBUG_LEVEL=1 \
           -e DOMAIN=test.nprod.net \
           -e ORGANIZATION="Test Instance LDAP" \
           -e PASSWORD=1234567890 \
           -v $PWD/test_data.ldif:/test_data.ldif \
           mwaeckerlin/openldap

sleep 5

docker exec ldapui_test_openldap ldapadd -x -w 1234567890 -D'cn=admin,dc=test,dc=nprod,dc=net' -f /test_data.ldif -c
