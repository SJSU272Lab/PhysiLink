import ldap
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired
from my_app import db, app
 
 
def get_ldap_connection():
    conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
    return conn
 
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
 
    def __init__(self, username, password):
        self.username = username
 
    @staticmethod
    def try_login(username, password):
        conn = get_ldap_connection()
        conn.simple_bind_s(
            'cn=%s,ou=Users,dc=testathon,dc=net' % username,
            password
        )
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
 
class LoginForm(Form):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])