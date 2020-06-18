from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField,TextAreaField,DateField,SelectField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError,InputRequired

from application.models import User,Customer,Account


class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password",validators=[DataRequired(),Length(min=6,max=15),EqualTo('password')])
    name = StringField("Name",validators=[DataRequired()])
    role_id  =  StringField("Role Id",validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self,email):
        user=User.objects(ws_email=email.data).first()
        if user:
            raise ValidationError("Email is already in use.Pick another one")



class Create_Customer_Form(FlaskForm):
    ssn_id = StringField("Customer SSN ID",validators=[DataRequired(),Length(min=9,max=9)])
    customer_name = StringField("Customer Name",validators=[DataRequired(),Length(min=2,max=30)])
    age = IntegerField("Age",validators=[DataRequired()])
    address=TextAreaField('Address',validators=[DataRequired(),Length(min=1,max=100)])
    submit = SubmitField("Submit")  

    def validate_ssn_id(self,ssn_id):
        print("insdie valid")
        user=Customer.objects(ws_ssn_id=ssn_id.data).first()
        if user:
            raise ValidationError("SSN Id already exists")
    def validate_age(self,age):
        print(age.data)
        print(len(str(age.data)))
        if len(str(age.data))>3:
            raise ValidationError("Age should not be more than 3 digits")



class Update_Customer_Form(FlaskForm):
    ssn_id = StringField("Customer SSN ID",validators=[DataRequired()])
    cust_id = StringField("Customer ID",validators=[DataRequired()])
    old_customer_name = StringField("Old Customer Name",validators=[DataRequired(),Length(min=2,max=30)])
    new_customer_name = StringField("New Customer Name",validators=[DataRequired(),Length(min=2,max=30)])
    old_age = IntegerField("Old Age",validators=[DataRequired()])
    new_age = IntegerField("New Age",validators=[DataRequired()])
    old_address=TextAreaField('Old Address',validators=[DataRequired(),Length(min=1,max=100)])
    new_address=TextAreaField('New Address',validators=[DataRequired(),Length(min=1,max=100)])
    submit = SubmitField("Submit")  
    def validate_new_age(self,new_age):
        if len(str(new_age.data))>3:
            raise ValidationError("Age should not be more than 3 digits")

class Search_Customer_Form(FlaskForm):
    ssn_id = IntegerField("SSN Id",validators=[])
    cust_id = IntegerField("Customer Id",validators=[])
    submit = SubmitField("Submit")  

class Create_Account_Form(FlaskForm):
     ws_cust_id = IntegerField("Customer ID",validators=[DataRequired()])
     ws_acct_type = SelectField("Account Type",choices=[('saving','saving'),('current','current')],validators=[DataRequired()])
     ws_acct_balance = IntegerField("Account Balance", validators=[DataRequired()])
     submit = SubmitField("Submit") 
     
     def validate_ws_cust_id(self,ws_cust_id):
        print("insdie valid")
        account=Customer.objects(ws_cust_id=ws_cust_id.data).first()
        
        if not account:
            raise ValidationError("Customer id does not exist")

class Account_Search_Form(FlaskForm):
    ws_acc_id = IntegerField("Account ID",validators=[])
    ws_cust_id = IntegerField("Customer ID",validators=[])
    submit = SubmitField("Submit")

class Account_Delete_Form(FlaskForm):
    ws_acct_id = SelectField("Account Id",coerce=int,validators=[])
    ws_acct_type = StringField("Account Type",validators=[DataRequired()])
    submit = SubmitField("Delete")

class TransferForm(FlaskForm):
    ws_cust_id = IntegerField("Customer ID",validators=[DataRequired()])
    ws_source_id = SelectField("Source Account Id",coerce=int)
    ws_source_type = StringField("Source Account Type",validators=[])
    ws_target_id = SelectField("Target Account Id",coerce=int)
    ws_target_type = StringField("Target Account Type",validators=[])
    ws_transfer_amount = IntegerField("Transfer Amount",validators=[DataRequired()])
    submit = SubmitField("Transfer")

    def validate_ws_total_amount(self,ws_total_amount):
        if ws_total_amount.data=="" or ws_total_amount.data==0:
            raise ValidationError("Null") 