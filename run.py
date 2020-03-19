import os

if 'WTF_CSRF_SECRET_KEY' not in os.environ:
    raise ArgumentError("Please set a SECRET string into the WTF_CSRF_SECRET_KEY environment variable")
if 'SECRET_KEY' not in os.environ:
    raise ArgumentError("Please set another SECRET string into SECRET_KEY environment variable")
if 'DC' not in os.environ:
    raise ArgumentError("Please set the DC into DC environment variable")
if 'OU' not in os.environ:
    raise ArgumentError("Please set the OU into OU environment variable")
from app import app

app.run(debug=os.environ['DEBUG'] == "True", port=8086, host='0.0.0.0')
