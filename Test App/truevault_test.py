"""Cloud Foundry test"""
from flask import Flask
import cf_deployment_tracker
import os
import requests





# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

# On Bluemix, get the port number from the environment variable VCAP_APP_PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('VCAP_APP_PORT', 8080))

data = {
  'username': 'python_user',
  'password': 'python',
  'attributes': ''
}

result = requests.post('https://api.truevault.com/v1/users', data=data, auth=('94b53cf5-72ca-4478-85bf-3c3fbdf7a78b', ''))

@app.route('/')
def hello_world():
    return 'Created User ' + result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

