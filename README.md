# Requirements
Python >=3.6 (works with 3.9)

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

## Deployment on bare-metal

Everything in requirements.txt

On debian (maybe not necessary since we use ldap3):
libsasl2-dev python-dev libldap2-dev libssl-dev   
are necessary for compiling python-ldap
