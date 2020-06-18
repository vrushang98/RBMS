import flask
from application import db
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Document):
    ws_user_id      = db.IntField(unique=True)
    ws_name         = db.StringField(max_length=50)
    ws_email        = db.StringField(max_length=30,unique=True)
    ws_password     = db.StringField(required=True)
    ws_role_id      = db.StringField(required=True)
    ws_timestamps   = db.DateTimeField()

    def set_password(self,password):
        self.ws_password=generate_password_hash(password)
    
    def get_password(self,password):
        return check_password_hash(self.ws_password,password)
class Role(db.Document):
    roleId  =   db.StringField(unique=True,required=True)
    name    =   db.StringField(required=True)
class Customer(db.Document):
    ws_ssn_id       = db.IntField(unique=True,length=9)
    ws_cust_id      = db.IntField(required=True,length=9)
    ws_name         = db.StringField(max_length=30)
    ws_age          = db.IntField()
    ws_address      = db.StringField(required=True)

class Customer_Status(db.Document):
    ws_ssn_id           = db.IntField(length=9)
    ws_cust_id          = db.IntField(required=True,length=9)
    ws_status           = db.StringField(max_length=30)
    ws_message          = db.StringField()
    ws_cust_lastUdate   = db.DateField()


class Account(db.Document):
    ws_cust_id          = db.IntField(required=True,length=9)
    ws_acct_id          = db.IntField(required=True,length=9)
    ws_acct_type        = db.StringField(required=True,length=9)
    ws_acct_balance     = db.IntField(required=True)
    ws_acct_crdate      = db.DateField(required=True)
    ws_acct_lasttrdate  = db.DateField()

class Account_Status(db.Document):
    ws_cust_id          = db.IntField(required=True,length=9)
    ws_acct_id          = db.IntField(required=True,length=9)
    ws_acct_type        = db.StringField(required=True,length=9)
    ws_acct_status      = db.StringField(required=True)
    ws_message          = db.StringField()
    ws_acct_lastUdate   = db.DateField()
    
class Transaction(db.Document):
    ws_cust_id          = db.IntField(required=True,length=9)
    ws_acct_id          = db.IntField(required=True,length=9)
    ws_transaction_id   = db.IntField(required=True,length=9)
    ws_description       = db.StringField(required=True,length=9)
    ws_amount           = db.IntField(required=True)
    ws_trxn_date        = db.DateField(required=True)

