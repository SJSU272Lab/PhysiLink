from cloudant.client import Cloudant
from cloudant.result import Result, ResultByKey
from cloudant.query import Query
from cloudant.index import Index
from cloudant.database import CloudantDatabase
from cloudant.document import Document
import datetime

USERNAME = '4920249b-5f3d-4983-94b1-bc4d4a91a2f5-bluemix'
PASSWD = 'c3020144543af9ec9f68d1d35e130fada3233d3dd2c82f7c0991709b147ad0fb'
URL = 'https://4920249b-5f3d-4983-94b1-bc4d4a91a2f5-bluemix.cloudant.com'
# email, NPI, VaultID, ApiID, name, password, organization
Newuser = ['abc@email.com', '13245679', '7789987', '225588', 'Jane Doe', 'password', 'MedInc']
# sender, reciever, subject, msg
NewEmail = ['abc@email.com', 'xyz@email.com', 'Hello', 'Hello World']


def ConnectDB(UserName, Pwd, url, DBName):
    # Use Cloudant to create a Cloudant client using account
    # client = cloudant.Cloudant(UserName, Pwd, url=url)
    try:
        client = Cloudant(UserName, Pwd, url=url)
    except Exception:
        return -1
    # Connect to the server
    client.connect()
    # Try Open an existing database
    try:
        my_database = client[DBName]
    except Exception:
        return -2
    # Test if database exists and create index for emails
    if my_database.exists():
        my_database.create_query_index(index_name='GetDates', fields=[{'date': 'desc'}])
        return my_database
    else:
        return -3


# endfunction

def createUser(my_database, myList=[]):
    # Check if List is empty
    if not myList:
        return -1
    # Check List is seven elements
    if len(myList) != 7:
        return -2
    # Test if database exists
    try:
        my_database.exists()
    except Exception:
        return -3
    # Check database object
    data = {
        '_id': myList[0],
        'NPI': myList[1],
        'vaultID': myList[2],
        'api_id': myList[3],
        'name': myList[4],
        'password': myList[5],
        'organization': myList[6],
        'date': str(datetime.datetime.now())
    }
    # Try Create a document using the Database API
    try:
        my_document = my_database.create_document(data)
    except Exception:
        return -4

    # Check that the document exists in the database
    if my_document.exists():
        return True
    else:
        return -4


# endfunction

def getUser(my_database, ID):
    # Try Open an existing document
    try:
        my_document = my_database[ID]
    except Exception:
        return -1

    # Return the document
    return my_document


# endfunction

def modifyUser(my_database, ID, field, value):
    # Try Open an existing document
    try:
        my_document = my_database[ID]
    except Exception:
        return -1
    # Update item
    my_document[field] = value
    # Save Document
    my_document.save()
    return True


# endfuction

def createEmail(my_database, myList=[], fd=None, fileName=None, filetype=None):
    # Check if List is empty
    if not myList:
        return -1
    # Check List is four elements
    if len(myList) != 7:
        return -2
    # Test if database exists
    try:
        my_database.exists()
    except Exception:
        return -3
    # Check database object
    data = {
        'sender': myList[0],
        'receiver': myList[1],
        'subject': myList[2],
        'msg': myList[3],
        'document_id': myList[4],
        'provider': myList[5],
        'vault_id': myList[6],
        'attachment_flag': 'N',
        'filename' : fileName,
        'date': str(datetime.datetime.now())
    }
    # Try Create a document using the Database API
    try:
        my_document = my_database.create_document(data)
    except Exception:
        return -4
    # put Attachment
    if ((fd is not None) and (fileName is not None) and (filetype is not None)):
        my_document['attachment_flag'] = 'Y'
        my_document.save()
        my_document.put_attachment('AttachFile', filetype, fd)

    # Check that the document exists in the database
    if my_document.exists():
        return True
    else:
        return -5


def getSentEmail(my_database, SenderID, emailLimit=0):
    # Test if database exists
    try:
        my_database.exists()
    except Exception:
        return -1
    # If zero return all email
    if int(emailLimit) == 0:
        query = Query(my_database, selector={'sender': SenderID, 'date': {'$gt': 0}})
    else:
        query = Query(my_database, selector={'sender': SenderID, 'date': {'$gt': 0}}, limit=int(emailLimit))
    return query(sort=[{'date': 'desc'}])['docs']


# endfunction

def getRecvEmail(my_database, receiverID, emailLimit=0):
    # Test if database exists
    try:
        my_database.exists()
    except Exception:
        return -1
    # If zero return all email
    if int(emailLimit) == 0:
        query = Query(my_database, selector={'receiver': receiverID, 'date': {'$gt': 0}})
    else:
        query = Query(my_database, selector={'receiver': receiverID, 'date': {'$gt': 0}}, limit=int(emailLimit))
    return query(sort=[{'date': 'desc'}])['docs']


# endfunction

def getRecvAttachment(my_database, email_doc_id, outputFile):
    # Test if database exists
    try:
        my_database.exists()
    except Exception:
        return -1
    # Try Open an existing document
    try:
        my_document = my_database[email_doc_id]
    except Exception:
        return -2
    if my_document['attachment_flag'] == 'Y':
        outfile = open(outputFile, 'w')
        my_document.get_attachment('AttachFile', write_to=outfile)


def getEmailDocID(my_database, doc_ID):
    # Test if database exists
    try:
        my_database.exists()
    except Exception:
        return -1
    # return all doc_id that match
    query = Query(my_database, selector={'document_id': doc_ID})
    return query(sort=[{'date': 'desc'}])['docs']


