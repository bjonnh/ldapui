# LdapUI

A Python (>=3.6), Flask based LDAP administration interface. It is light and easy to deploy. It authenticates
with the LDAP and allows to edit groups and users. It is highly tailored to the needs I had and may not have any fancy 
function. But it is used in production (internally) since 2017 or so. There is a docker-compose that should get you
a working local version (it will spin up an LDAP server and a fake mail server that will allow you to test the reset
by email function).

![A screenshot of the menu visible when logged in as admin](https://raw.githubusercontent.com/bjonnh/ldapui/main/img/admin.png)

## Deployment on a docker host

Look at the [docker-compose.yml](docker-compose.yml) file, it starts an example LDAP server with data already loaded.

To run it just do:
````
docker-compose up --build 
````

The service is accessible at: [http://127.0.0.1:8080](http://127.0.0.1:8080)

Users are admin (password admin) and user (password user).

The email functionality is emulated with [maildev](https://github.com/maildev/maildev) that is accessible on port 1080:
[http://127.0.0.1:1080](http://127.0.0.1:1080).

Sometimes the openldap server crashes for an unknown reason (it gets SIGKILLED somehow) and you have to restart it. As
I am not using a dockerized LDAP server using this image in production, I didn't dig deeper into that.

## Deployment on bare-metal (deprecated)

Install everything in requirements.txt

On debian (maybe not necessary anymore since we use ldap3 now):
libsasl2-dev python-dev libldap2-dev libssl-dev   
are necessary for compiling python-ldap
