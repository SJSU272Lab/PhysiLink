from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
 
 
app = Flask(__name__)

#Replace with your sample SQL database URI 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['WTF_CSRF_SECRET_KEY'] = 'A33P-XYQB-332I-MW72-PPAJ'

#Insert LDAP URL. Sample LDAP URL has been provided. 
#Sample LDAP Server may or may not be running.
app.config['LDAP_PROVIDER_URL'] = 'ldap://ldap.testathon.net:389/'

app.config['LDAP_PROTOCOL_VERSION'] = 3
db = SQLAlchemy(app)
 
app.secret_key = 'some_random_key'
 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
 
from my_app.auth.views import auth
app.register_blueprint(auth)
 
db.create_all()