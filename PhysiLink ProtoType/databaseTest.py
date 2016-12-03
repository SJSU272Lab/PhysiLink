import database

#default values
USERNAME = '4920249b-5f3d-4983-94b1-bc4d4a91a2f5-bluemix'
PASSWD = 'c3020144543af9ec9f68d1d35e130fada3233d3dd2c82f7c0991709b147ad0fb'
URL = 'https://4920249b-5f3d-4983-94b1-bc4d4a91a2f5-bluemix.cloudant.com'
my_database = 0

def menu():
	global my_database
	print "1) Connect to Database"
	print "2) Add User"
	print "3) Get User information"
	print "4) Modify a User information"
	print "5) Create an email"
	print "6) Get sent email"
	print "7) Get received email"
	print "0) Exit Program"
	choice = input("\nSelect an option: ")
	if choice == 1:
		my_database = connectDB()
		if my_database < 0:
			print "Error:" + my_database
	elif choice == 2:
		newUser(my_database)
	elif choice == 3:
		getUserInfo(my_database)
	elif choice == 4:
		modifyUserInfo(my_database)
	elif choice == 5:
		createNewEmail(my_database)
	elif choice == 6:
		getSendEmails(my_database)
	elif choice == 7:
		getRecvEmails(my_database)
	else:
		exit()
#endfunction

def connectDB():
	choice = raw_input("Use default values (Y|N): ")
	if choice == 'Y' or choice == 'y':
		mydatabase = database.ConnectDB(USERNAME, PASSWD, URL, 'physician')
	else:
		user = raw_input("Enter User Name: ")
		passwd = raw_input("Enter Password: ")
		url = raw_input("Enter url: ")
		dbname = raw_input("Enter database name: ")
		mydatabase = database.ConnectDB(user, passwd, url, dbname)
	return mydatabase
#endfunction

def newUser(my_database):
	email = raw_input("Enter email address: ") 
	npi = raw_input("Enter npi number: ")		
	vault = raw_input("Enter vault id: ")		 
	api = raw_input("Enter api id: ")		 
	name = raw_input("Enter name: ")		 
	pw = raw_input("Enter password: ") 
	org = raw_input("Enter organization: ")

	data = [email, npi, vault, api, name, pw, org]
	return database.createUser(my_database, data)			
#endfunction

def getUserInfo(my_database):
	email = raw_input("Enter email address: ")
	print database.getUser(my_database, email)
#endfunction

def modifyUserInfo(my_database):
	email = raw_input("Enter email address: ")
	field = raw_input("Enter field to replace (NPI, vaultID, api_id, name, password, or organization: ")
	value = raw_input("Enter new value: ")
	database.modifyUser(my_database, email, field, value)
#endfunction

def createNewEmail(my_database):
	sender = raw_input("Enter your email: ")
	recv = raw_input("Enter receiver email: ")
	subject = raw_input("Enter subject: ")
	msg = raw_input("Enter your message: ")
	data = [sender, recv, subject, msg]
	database.createEmail(my_database, data)
#endfunction

def getSendEmails(my_database):
	email = raw_input("Enter sender email: ")
	limit = raw_input("Enter amount of email to get (0 = all): ")
	print database.getSentEmail(my_database, email, limit)

def getRecvEmails(my_database):
	email = raw_input("Enter your email: ")
	limit = raw_input("Enter amount of email to get (0 = all): ")
	print database.getRecvEmail(my_database, email, limit)

print "Hello, this it database test API program. User must connect first before useing other options"
while(1):
	menu()


