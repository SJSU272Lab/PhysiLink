from flask import Flask, render_template, Response, request, flash, redirect
import requests
import base64
import json
import database
import cf_deployment_tracker
import os
import datetime

# Emit Bluemix deployment event
cf_deployment_tracker.track()


VAULT_ID = "cada6e4e-39e6-4dbf-b550-3dda6f3e7e9a"
USERNAME = '4920249b-5f3d-4983-94b1-bc4d4a91a2f5-bluemix'
PASSWD = 'c3020144543af9ec9f68d1d35e130fada3233d3dd2c82f7c0991709b147ad0fb'
URL = 'https://4920249b-5f3d-4983-94b1-bc4d4a91a2f5-bluemix.cloudant.com'
CURRENT_USER_EMAIL = "Kristina"
API_KEY = "a4fced3b-820d-488c-b429-884798f5d5c8"


class Sent_Emails:
    def __init__(self, name, receiver, doc_id, provider, subject, vault_id):
        self.name = name
        self.receiver = receiver
        self.doc_id = doc_id
        self.provider = provider
        self.subject = subject
        self.vault_id = vault_id


UPLOAD_FOLDER = '/Home/Downloads'
ALLOWED_EXTENSIONS = set(['csv','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)

# On Bluemix, get the port number from the environment variable VCAP_APP_PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('VCAP_APP_PORT', 8080))


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = database.ConnectDB(USERNAME, PASSWD, URL, 'physician')


@app.route('/showSignUp', methods=['GET', 'POST'])
def showSignUp():
    return render_template('sent.html', sender1 = CURRENT_USER_EMAIL)

@app.route('/showSentBox')
def showSentBox():
    list = database.getSentEmail(db, "Kristina")
    sent_list = []
    for item in list:
        sent_list.append(Sent_Emails(item["sender"], item["receiver"], item["document_id"], item["provider"], item["subject"], VAULT_ID))
    log_file = open("log.txt", "a")
    log_file.write("User viewed outgoing mailbox at %s\n" % datetime.datetime.now())
    return render_template( 'link1.html', result = sent_list)

@app.route('/sentItems/<key>', methods=['GET', 'POST'])
#@app.route('/hello')
def sentItems(key):
    resp = requests.get(
        'https://api.truevault.com/v1/vaults/cada6e4e-39e6-4dbf-b550-3dda6f3e7e9a/documents/'+ key , auth=('a4fced3b-820d-488c-b429-884798f5d5c8', ''))
    document = base64.b64decode(resp.text).decode('utf-8')
    email_obj = database.getEmailDocID(db, key)
    sender = email_obj[0]["sender"]
    provid_num = email_obj[0]["provider"]
    sub = email_obj[0]["subject"]
    id = email_obj[0]["_id"]
    filename = email_obj[0]["filename"]
    doc_id = email_obj[0]["document_id"]
    result = [sender, provid_num, sub, document, id, filename, doc_id]
    return render_template("message.html", result = result)


@app.route('/sentItems/attachments/<doc>/<key>/<filename>', methods = ['GET', 'POST'])
def attachment(key, filename, doc):
    print(key)
    #key = '5c7d886a84f4c2101d7836a1a159caff'
    success = database.getRecvAttachment(db, key, filename)
    flash("Success")
    return redirect("/", code=302)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      file = request.files['file']
      return render_template("sent.html")

@app.route('/createEmail', methods=['GET', 'POST'])
def createEmail():
    if request.method == 'POST':
        file = request.files['file']
    else:
        file = None

    name = request.form['name']
    sender = request.form['sender']
    subject = request.form['title']
    message = request.form['document']
    provider = request.form['provider']

    s = json.dumps(message)
    message_document = base64.b64encode(s.encode('utf-8'))
    data = {
       'document': message_document,
        #schema_id': '00000000-0000-0000-0000-000000000000',
        #'owner_id': 'dae9ccbf-085d-4fc3-a4ff-e97e1ccc6736'
    }

    resp = requests.post('https://api.truevault.com/v1/vaults/cada6e4e-39e6-4dbf-b550-3dda6f3e7e9a/documents', data=data,
                  auth=('a4fced3b-820d-488c-b429-884798f5d5c8', ''))

    json_data = json.loads(resp.text)
    list = [sender, name, subject, message, json_data['document_id'], provider, VAULT_ID]
    if file is not None:
        fo = open(file.filename, "r")
        extension = os.path.splitext(file.filename)[1][1:]
        success = database.createEmail(db, list, fo, file.filename, extension)
        print(success)
    else:
        success = database.createEmail(db, list)
    log_file = open("log.txt", "a")
    log_file.write("User sent email at %s to %s\n" % datetime.datetime.now(), name)
    return redirect("/", code=302)



@app.route('/createVault', methods=['GET', 'POST'])
def createVault():
    data = {
        'name': 'new_vault'
    }
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'https://api.truevault.com/v1/auth/login'

    return resp.text


@app.route('/createUser', methods=['GET', 'POST'])
def createUser():

    data = {
        'username': 'test_user_PhysiLink1',
        'password': 'physilink1',
    }

    resp = requests.post('https://api.truevault.com/v1/users', data=data, auth=(API_KEY, ''))

    return resp.text


@app.route('/hello', methods=['GET', 'POST'])
def api_hello():
    data = {
        'username': 'new_user',
        'password': 'new_password',
        'account_id': '86444b4a-cb69-4078-96bd-c577e324e886'
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'https://api.truevault.com/v1/auth/login'
    #resp = requests.post('https://api.truevault.com/v1/auth/login', data=data)
    return resp


@app.route('/connect', methods=['GET', 'POST'])
def connect():
    data = {
        'username': 'new_user',
        'password': 'new_password',
        'account_id': '86444b4a-cb69-4078-96bd-c577e324e886'
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'https://api.truevault.com/v1/auth/login'
    list = database.getRecvEmail(db, "Kristina")
    print(list)
    recv_list = []
    for item in list:
        user = database.getUser(db, item["sender"])
        recv_list.append(Sent_Emails(user["name"], item["receiver"], item["document_id"], item["provider"], item["subject"], item["vault_id"]))
    log_file = open("log.txt", "a")
    log_file.write("User viewed incoming mailbox at %s\n" % datetime.datetime.now())
    return render_template('index.html', result = recv_list)


@app.route("/")
def main():
    return render_template('app.html')
    
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=port)
