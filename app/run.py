from app import app
import os

app.run(debug=os.environ['DEBUG'] == "True", port=8086, host='0.0.0.0')
