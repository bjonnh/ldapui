#!/usr/bin/env bash
source ./venv/bin/activate

export LDAP_HOST=127.0.1.1
export LDAP_PORT=389
export SECRET_KEY=foo
export WTF_CSRF_SECRET_KEY=bar
export MANAGER_USER=admin
export MANAGER_PW=1234567890
export MANAGER_PATH=dc=test,dc=nprod,dc=net
export DC=dc=test,dc=nprod,dc=net
export OU=dc=test,dc=nprod,dc=net
export EMAIL_SERVER=""
export EMAIL_LOGIN=""
export EMAIL_PASSWORD=""
export EMAIL_NAME="LDAP Test instance"
export EMAIL_EMAIL=test@test.com
export SITE_NAME="LDAP Test instance"
export SITE_URL="https://test.nprod.net"
export DEBUG=True

python run.py
