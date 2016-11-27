from flask import Flask, render_template, Response, request
import requests
import base64
from json2html import *
import cgi
import urlparse
import json
from webbrowser import open_new_tab
import database


class Sent_Emails:
    def __init__(self, name, receiver, doc_id, provider, subject, vault_id):
        self.name = name
        self.receiver = receiver
        self.doc_id = doc_id
        self.provider = provider
        self.subject = subject
        self.vault_id = vault_id


USERNAME = '4920249b-5f3d-4983-94b1-bc4d4a91a2f5-bluemix'
PASSWD = 'c3020144543af9ec9f68d1d35e130fada3233d3dd2c82f7c0991709b147ad0fb'
URL = 'https://4920249b-5f3d-4983-94b1-bc4d4a91a2f5-bluemix.cloudant.com'


document_id = ["134f38fc-380f-4b83-b159-31f85953da12",
"9718c02e-0bf8-481b-bc2e-3be182139ec1",
"3d9ecb99-523e-4325-a12a-f53e4c136ebb",
"56abf767-3fae-4de2-ae56-18958d08ea83",
"d5fb214e-45a0-4e97-9004-a67c7592c950",
"307edff4-6072-4e83-a18c-3aba1d62fefb",
"51b426ef-c90e-4452-b4ce-d91caad29eb3",
"0aa1d099-4221-4607-b047-66e67935982b",
"275de27d-76f5-4a16-8881-3e108cacc030",
"16ed3dfd-51a2-43ef-9eb9-93b5526a998c",
"f6234e2d-0329-4a60-819b-48578ca40a13",
"213ec91f-2f9b-40c3-8de8-a0a3380bf627",
"2cdfbda7-5230-4372-8f3e-990a4f8a656c",
"e5eafd8d-dc4a-4ebc-a11d-95e466896606",
"0ec8f949-c403-45a2-9687-f5cb510de993",
"9c26bf29-c4c6-442e-b7a7-e152b4826ca1",
"40de511e-0f10-4509-8857-a84ed27a8f1d",
"9047c083-312b-4c0e-9636-5cc101cb73b0",
"99b3fbcb-4dc0-4672-ac1f-a70c77cba1d2",
]

app = Flask(__name__)
db = database.ConnectDB(USERNAME, PASSWD, URL, 'physician')


@app.route('/showSignUp', methods=['GET', 'POST'])
def showSignUp():
    return render_template('sent.html')

@app.route('/showSentBox')
def showSentBox():
   # resp = requests.get('https://api.truevault.com/v1/vaults/cada6e4e-39e6-4dbf-b550-3dda6f3e7e9a/documents',
    #             auth=('a4fced3b-820d-488c-b429-884798f5d5c8', ''))

    # Store JSON data into json_file
    #json_data = json.loads(resp.text)
    #print(resp.text)

    #documents = []
    #for x in json_data['data']["items"]:
       # documents.append(x['document_id'])
        #print(x['document_id'])

    list = database.getSentEmail(db, "Kristina")
    sent_list = []
    for item in list:
        print(item["_id"])
        print(item)
        sent_list.append(Sent_Emails(item["sender"], item["receiver"], item["document_id"], item["provider"], item["subject"], VAULT_ID))
    return render_template( 'link1.html', result = sent_list)

@app.route('/sentItems/<key>', methods=['GET', 'POST'])
#@app.route('/hello')
def sentItems(key):
    print(key)
    resp = requests.get(
        'https://api.truevault.com/v1/vaults/cada6e4e-39e6-4dbf-b550-3dda6f3e7e9a/documents/'+ key , auth=('a4fced3b-820d-488c-b429-884798f5d5c8', ''))
    document = base64.b64decode(resp.text).decode('utf-8')
    return document


    # Store JSON data into json_file
   # json_data = json.loads(resp.text)
   # print json_data["data"]["items"][0]["id"]

   # documents = []
   # for x in json_data['data']["items"]:
     #   documents.extends(x['id'])
   # for y in documents:
        #open("sent.html", "w").write('<a href="http://www.example.com"> Link </a>')

    #requests.get(
      #  'https://api.truevault.com/v1/vaults/cada6e4e-39e6-4dbf-b550-3dda6f3e7e9a/documents/00000000-0000-0000-0000-000000000000,00000000-0000-0000-0000-000000000001',
     #   auth=('[API_KEY', ''))



VAULT_ID = "cada6e4e-39e6-4dbf-b550-3dda6f3e7e9a"

@app.route('/createEmail', methods=['GET', 'POST'])
def createEmail():
    name = request.form['name']
    sender = request.form['sender']
    subject = request.form['title']
    message = request.form['document']
    provider = request.form['provider']

    #message_json = json.load(message)
    s = json.dumps(message)
    message_document = base64.b64encode(s.encode('utf-8'))
    data = {
       'document': message_document,
        #schema_id': '00000000-0000-0000-0000-000000000000',
        #'owner_id': 'dae9ccbf-085d-4fc3-a4ff-e97e1ccc6736'
    }

    resp = requests.post('https://api.truevault.com/v1/vaults/cada6e4e-39e6-4dbf-b550-3dda6f3e7e9a/documents', data=data,
                  auth=('a4fced3b-820d-488c-b429-884798f5d5c8', ''))
    print(resp.text)
    json_data = json.loads(resp.text)
    document_id.append(json_data['document_id'])
    print(json_data['document_id'])
    list = [name, sender, subject, message, json_data['document_id'], provider, VAULT_ID]
    print(len(list))
    success = database.createEmail(db, list );
    print(success)




    return resp.text

@app.route('/createVault', methods=['GET', 'POST'])
def createVault():
    data = {
        'name': 'test_vault1'
    }
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'https://api.truevault.com/v1/auth/login'

    return resp


@app.route('/hello', methods=['GET', 'POST'])
#@app.route('/hello')
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


@app.route("/")
def main():

    list = database.getRecvEmail(db, "Kristina")
    print(list)
    recv_list = []
    for item in list:
        user = database.getUser(db, item["sender"])
        recv_list.append(Sent_Emails(user["name"], item["receiver"], item["document_id"], item["provider"], item["subject"], item["vault_id"]))
    return render_template('index.html', result = recv_list)

if __name__ == "__main__":
    app.run(threaded = True)
