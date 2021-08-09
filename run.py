import os

environment_errors = {
    "WTF_CSRF_SECRET_KEY": "Please set a SECRET string into the WTF_CSRF_SECRET_KEY environment variable",
    "SECRET_KEY": "Please set a SECRET string different from the CSRF one into SECRET_KEY environment variable",
    "DC": "Please set the DC into DC environment variable such as: dc=test,dc=nprod,dc=net",
    "OU": "Please set the OU group of users into OU environment variable such as: ou=Users,dc=test,dc=nprod,dc=net"
}

for key, error in environment_errors.items():
    if key not in os.environ:
        raise Exception(error)

from app import app

port = os.getenv("PORT", 8080)
host = os.getenv("HOST", "0.0.0.0")

app.run(debug=os.environ['DEBUG'] == "True", port=port, host=host)
