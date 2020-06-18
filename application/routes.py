from application import app,db
from flask import render_template,request,json,Response,redirect,flash,session,url_for

from application.models import User,Customer,Account,Customer_Status,Account_Status,Transaction,Role
from application.forms import LoginForm,RegisterForm,Create_Customer_Form,Create_Account_Form,Search_Customer_Form,Update_Customer_Form,Account_Search_Form,Account_Delete_Form,TransferForm
from datetime import datetime 
import time
import json
import random
from datetime import date
from bson import json_util
from bson.json_util import dumps, loads
import dateutil.parser



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



@app.route("/")
@app.route("/index")
def index():
    if session.get('userId'):
        user=User.objects(ws_user_id=session.get('userId')).first()
        return render_template("index.html",name=session.get('username'),email=user.ws_email)
    
    user_id = User.objects.count()
    if user_id==0:
        user_id += 1

        email       = "executive@gmail.com"
        password    = "123456789"
        name  = "Customer Executive"
        role_id = "1111"

        user=User(ws_user_id=user_id,ws_email=email,ws_name=name,ws_role_id=role_id)
        user.set_password(password)
        user.save()

        user_id += 1

        email       = "cashier@gmail.com"
        password    = "123456789"
        name  = "Cashier/Teller"
        role_id = "2222"

        user=User(ws_user_id=user_id,ws_email=email,ws_name=name,ws_role_id=role_id)
        user.set_password(password)
        user.save()
    role_id=Role.objects.count()
    if role_id==0:
        role_id="1111"
        name="CAE"
        Role(roleId=role_id,name=name).save()
        role_id="2222"
        name="C/T"
        Role(roleId=role_id,name=name).save()

    return redirect("/login")

@app.route("/login",methods=['GET','POST'])
def login():
    if session.get('userId'):
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data

        print("password:",password)

        user=User.objects(ws_email=email).first()
        if user and user.get_password(password):
            flash(f"{user.ws_name},You are successfully logged in!","success")
            session['userId'] = user.ws_user_id
            session['roleId'] = user.ws_role_id
            session['username'] = user.ws_name
            
            return redirect("/index")
        else:
            flash("Invalid username password","danger")
    return render_template("login.html",title="Login",form=form , login=True)


@app.route("/register", methods=['POST','GET'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form=RegisterForm()
    print("hello")
    if form.validate_on_submit():
        print("on submit")
        user_id = User.objects.count()
        user_id += 1

        email       = form.email.data
        password    = form.password.data
        name  = form.name.data
        role_id = form.role_id.data

        user=User(ws_user_id=user_id,ws_email=email,ws_name=name,ws_role_id=role_id)
        user.set_password(password)
        user.save()




        flash("You are registered","success")
        return redirect('/index')
    return render_template("register.html",title="Register",form=form)


@app.route("/logout")
def logout():
    session['userId']=False
    session['roleId']=False
    session['username']=None
    return redirect(url_for('index'))

def obj_dict(data):
    return data.__dict__
@app.route("/getrole")
def getrole():
    if session.get('userId'):
        data=list(User.objects.only(*['email']).aggregate(*[
                {
                    '$match': {
                        'userId': session.get('userId')
                    }
                }, {
                    '$lookup': {
                        'from': 'role', 
                        'localField': session.get('roleId'), 
                        'foreignField': session.get('roleId'), 
                        'as': 'role'
                    }
                }, {
                    '$unwind': {
                        'path': '$role', 
                        'preserveNullAndEmptyArrays': False
                    }
                }
            ]))[0]
        print(data)
        print(data['role']['name'])
        
        return data['role']['name']





def generate_Cutomer_Id():
    st="10"
    num2=random.randint(1000000,9999999)
    cust_id=int(st+str(num2))
    customer=Customer.objects(ws_cust_id=cust_id).first()
    if customer:
        generate_Cutomer_Id()
    return str(cust_id)

def generate_Account_Id():
    st="30"
    num2=random.randint(1000000,9999999)
    acct_id=int(st+str(num2))
    account=Account.objects(ws_acct_id=acct_id).first()
    if account:
        generate_Account_Id()
    return str(acct_id)

def generate_Transaction_Id():
    st="50"
    num2=random.randint(1000000,9999999)
    transaction_id=int(st+str(num2))
    transaction=Transaction.objects(ws_transaction_id=transaction_id).first()
    if transaction:
        generate_Transaction_Id()
    return str(transaction_id)

@app.route("/create_customer",methods=['GET','POST'])
def create_customer():
    if session.get('userId') and session.get('roleId')=="1111":
        form = Create_Customer_Form()
        if(request.method=='POST'):
            if(form.validate_on_submit()):
                
                ssn_id=form.ssn_id.data
                
                customer_name=form.customer_name.data
                age=form.age.data
                address=form.address.data
                cust_id=generate_Cutomer_Id()
                status='Active'
                x = datetime.now()
                d=x.strftime("%x")
                y = datetime.now()
                t=y.strftime("%X")
                dt = d + " " + t 
                print("##############"+dt+"##############")  
                last_updated =datetime.strptime(dt,'%m/%d/%y %H:%M:%S')  
                message='customer created successfully'
                if not ssn_id.isnumeric():
                    flash('Invalid SSN ID', 'danger')
                    return redirect(url_for('create_customer')) 
                
       
                Customer(ws_ssn_id=ssn_id,ws_cust_id=cust_id,ws_name=customer_name,ws_age=age,ws_address=address).save()
                Customer_Status(ws_ssn_id=ssn_id,ws_cust_id=cust_id,ws_status=status,ws_message=message,ws_cust_lastUdate=last_updated).save()
        


                flash('Thank  for submmtimg  your details.we will get  back to you soon', 'success')
                return redirect(url_for('create_customer'))  

        return render_template('create_customer.html',form=form)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")


@app.route("/update_customer/<int:id>",methods=['GET','POST'])
def update_customer(id):
    print(id)
    if session.get('userId') and session.get('roleId')=="1111":
        update_customer=Customer.objects(ws_ssn_id=id).first()
        form=Update_Customer_Form()  
        print(update_customer)
        if update_customer:
            form.ssn_id.data = update_customer.ws_ssn_id
            form.cust_id.data = update_customer.ws_cust_id
            form.old_customer_name.data =update_customer.ws_name
            form.old_age.data = update_customer.ws_age
            form.old_address.data = update_customer.ws_address
            
            customer_name=form.new_customer_name.data
            age=form.new_age.data
            address=form.new_address.data
        else:
            update_customer=Customer.objects(ws_cust_id=id).first()
            if update_customer:
                form.ssn_id.data = update_customer.ws_ssn_id
                form.cust_id.data = update_customer.ws_cust_id
                form.old_customer_name.data =update_customer.ws_name
                form.old_age.data = update_customer.ws_age
                form.old_address.data = update_customer.ws_address
                
                customer_name=form.new_customer_name.data
                age=form.new_age.data
                address=form.new_address.data
            else:
                flash("Invalid ID","danger")
                return redirect("/update_search")
    
        if(request.method=='POST'):
            if (form.validate_on_submit()):
                customer_name=form.new_customer_name.data
                age=form.new_age.data
                address=form.new_address.data
                print(customer_name)
                print(age)
                print(address)
                new_customer=Customer.objects(ws_ssn_id=form.ssn_id.data).first()
                new_customer.ws_name=customer_name
                new_customer.ws_age=age
                new_customer.ws_address=address
                update_customer_status=Customer_Status.objects(ws_ssn_id=form.ssn_id.data).first()
                x = datetime.now()
                d=x.strftime("%x")
                y = datetime.now()
                t=y.strftime("%X")
                dt = d + " " + t
                if update_customer_status:
                    update_customer_status.ws_message='customer update completed'
                    update_customer_status.ws_cust_lastUdate=datetime.strptime(dt,'%m/%d/%y %H:%M:%S') 
                    update_customer_status.save()
                else:
                    Customer_Status(ws_ssn_id=form.ssn_id.data,ws_cust_id=new_customer.ws_cust_id,ws_message='customer update completed',ws_status="Active",ws_cust_lastUdate=datetime.strptime(dt,'%m/%d/%y %H:%M:%S')).save()
                new_customer.save()
                flash('your details are updated', 'success')
                return redirect(url_for('index'))

        return render_template('update_customer1.html',update_customer=update_customer,form=form)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")



@app.route('/update_search',methods=['GET','POST'])
def update_search():
    if session.get('userId') and session.get('roleId')=="1111":
        if(request.method=='POST'):
            ssn_id=request.form.get('ssn_id') 
            cust_id=request.form.get('cust_id')   
            if ssn_id:
                return redirect(url_for('update_customer',id=ssn_id))
            elif cust_id:
                return redirect(url_for('update_customer',id=cust_id))
            else:
                flash("Please enter any one ID","danger")
                return redirect("/update_search")
        
        return render_template('update_search.html')
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")


@app.route("/delete_customer/<int:id>",methods=['GET','POST'])
def delete_customer(id):
    if session.get('userId') and session.get('roleId')=="1111":
            print("delete id",id)
            delete_customer=Customer.objects(ws_ssn_id=id).first()
            if not delete_customer:
                delete_customer=Customer.objects(ws_cust_id=id).first()
                if not delete_customer:
                    flash("Invalid ID","danger")
                    return redirect("/delete_search")
            if(request.method=='POST'):
                delete_customer_status=Customer_Status.objects(ws_ssn_id=id).first()
                delete_customer_status.ws_status='inactive'
                delete_customer_status.ws_message='customer deleted'
                x = datetime.now()
                d=x.strftime("%x")
                y = datetime.now()
                t=y.strftime("%X")
                dt = d + " " + t 
                delete_customer_status.ws_cust_lastUdate=datetime.strptime(dt,'%m/%d/%y %H:%M:%S') 
                delete_customer_status.save()
                delete_customer.delete()
                flash('your details are deleted', 'success')
                return redirect(url_for('index'))

            
            return render_template('delete_customer.html',delete_customer=delete_customer)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")

@app.route("/delete_customer",methods=['POST'])
def delete_customer_data():
    if session.get('userId') and session.get('roleId')=="1111":
        print("delete id",request.form.get('ssn_id'))
        delete_customer=Customer.objects(ws_ssn_id=request.form.get('ssn_id')).first()
        print(delete_customer)
        if(request.method=='POST'):
            delete_customer.delete()
            flash('your details are deleted', 'success')
            return redirect(url_for('index'))

        
        return render_template('delete_customer.html',delete_customer=delete_customer)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")
@app.route('/delete_search',methods=['GET','POST'])
def delete_search():
    if session.get('userId') and session.get('roleId')=="1111":
        if(request.method=='POST'):
            ssn_id=request.form.get('ssn_id')
            cust_id=request.form.get('cust_id')
            if ssn_id:
                return redirect(url_for('delete_customer',id=ssn_id))
            elif cust_id:
                return redirect(url_for('delete_customer',id=cust_id))
            else:
                flash("Please enter any one ID","danger")
                return redirect("/delete_search")
            
        
        return render_template('delete_search.html')
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")

@app.route('/customer_status',methods=['GET','POST'])
def customer_status():
    if session.get('userId'):
        customers=Customer_Status.objects.all()
        return render_template('customer_status.html',customers=customers)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")
#create account
@app.route("/create_account",methods=['GET','POST'])
def create_account():
    if session.get('userId') and session.get('roleId')=="1111":
        form = Create_Account_Form()
        if(request.method=='POST'):
            if form.validate_on_submit():
                ws_cust_id=form.ws_cust_id.data
                ws_acc_id=generate_Account_Id()
                ws_acct_type=form.ws_acct_type.data
                ws_acct_balance=form.ws_acct_balance.data
                status='Active'
                x = datetime.now()
                d=x.strftime("%x")
                y = datetime.now()
                t=y.strftime("%X")
                dt = d + " " + t 
                print("##############"+dt+"##############")  
                ws_acct_lastUdate =datetime.strptime(dt,'%m/%d/%y %H:%M:%S')  
                message='customer created successfully'
                Account(ws_cust_id=ws_cust_id,ws_acct_id=ws_acc_id,ws_acct_type=ws_acct_type,ws_acct_balance=ws_acct_balance,ws_acct_crdate=date.today()).save()
                Account_Status(ws_cust_id=ws_cust_id,ws_acct_id=ws_acc_id,ws_acct_type=ws_acct_type,ws_acct_status=status,ws_message=message,ws_acct_lastUdate=ws_acct_lastUdate).save()
                flash('Thank  for creating account.we will get  back to you soon', 'success')
                return redirect(url_for('create_account'))
            
        
        return render_template('create_account.html',form=form)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")

@app.route('/account_search',methods=['GET','POST'])
def account_search():
    if session.get('userId') and session.get('roleId')=="2222":
        form = Account_Search_Form()
        if(request.method=='POST'):
            ws_acc_id=form.ws_acc_id.data
            print(ws_acc_id)
            ws_cust_id=form.ws_cust_id.data
            if ws_acc_id != None :
                account=Account.objects(ws_acct_id=ws_acc_id).first()
                if account:
                    return render_template('single_account_details.html',account = account)
                else:
                    flash("Invalid Account Id","danger")
            elif ws_cust_id != None :
                print("cust id")
                account=Account.objects(ws_cust_id=ws_cust_id)
                if account:
                    return render_template('account_details.html',account = account)
                else:
                    flash("Invalid Customer Id","danger")
            
            else :
                flash('Enter one of the ID','danger')    
        return render_template('Account_search.html',form=form)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")
@app.route('/account_delete_search',methods=["GET","POST"])
def account_delete_search():
    if session.get('userId') and session.get('roleId')=="1111":
        if request.method=="POST":
            form = Account_Delete_Form()
            accounts = Account.objects(ws_cust_id=request.form["cust_id"]).all()
            acc_id = []
            if accounts:
            
                acct_type=accounts[0]['ws_acct_type']


                for account in accounts:
                    acc_id.append((account.ws_acct_id,account.ws_acct_id))
                
                form.ws_acct_id.choices = acc_id
                form.ws_acct_type.data=acct_type
                return render_template('account_delete.html',form=form, accounts =accounts,acc_id=acc_id)
 
        
            else:
                flash("Invalid Customer Id","danger")
        return render_template("account_delete_search.html")
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")

@app.route('/account_delete',methods=['GET','POST'])
def account_delete():
    if session.get('userId') and session.get('roleId')=="1111":
        form = Account_Delete_Form()   
        if request.method =='POST' :
            acct_id = form.ws_acct_id.data
            delete_account= Account.objects(ws_acct_id=acct_id).first()
            delete_account_status=Account_Status.objects(ws_acct_id=acct_id).first()
            x = datetime.now()
            d=x.strftime("%x")
            y = datetime.now()
            t=y.strftime("%X")
            dt = d + " " + t 
            if delete_account_status:
                delete_account_status.ws_acct_status='inactive'
                delete_account_status.ws_message='account deleted'
                delete_account_status.ws_acct_lastUdate=datetime.strptime(dt,'%m/%d/%y %H:%M:%S') 
                delete_account_status.save()
            else:
                print(delete_account.ws_cust_id)
                account_status=Account_Status(ws_cust_id=delete_account.ws_cust_id,ws_acct_type=delete_account.ws_acct_type,ws_acct_id=acct_id,ws_acct_status='inactive',ws_message='account deleted',ws_acct_lastUdate=datetime.strptime(dt,'%m/%d/%y %H:%M:%S'))
                account_status.save()
            delete_account.delete()
            flash('your Account is deleted', 'success')
            return render_template('layout.html')
        return render_template('account_delete.html',form=form, accounts =accounts,acc_id=acc_id)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")

@app.route("/get_acct_type",methods=['POST'])
def get_acct_type():
    if session["userId"]:
        print("inside acct delete")
        account=Account.objects(ws_acct_id=request.form["acct_id"]).first()
        return account["ws_acct_type"]

@app.route("/view_deposit",methods=['POST'])
def deposit():
    if session.get('userId') and session.get('roleId')=="2222":
       
        account=Account.objects(ws_acct_id=request.form["acct_id"]).first()

        return render_template('view_deposit.html',account=account)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")


@app.route("/view_withdraw",methods=['POST'])
def withdraw():
    if session.get('userId') and session.get('roleId')=="2222":
        account=Account.objects(ws_acct_id=request.form["acct_id"]).first()

        return render_template('view_withdraw.html',account=account)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")

@app.route("/view_transfer",methods=['GET','POST'])
def view_transfer():
    if session.get('userId') and session.get('roleId')=="2222":
        form=TransferForm()
        accounts=Account.objects(ws_cust_id=request.form["cust_id"]).all()
        acct_id = []

        for account in accounts:
            acct_id.append((account.ws_acct_id,str(account.ws_acct_id)))
        print(acct_id)
        form.ws_cust_id.data=request.form["cust_id"]
        form.ws_source_id.choices = acct_id
        form.ws_source_type.data=accounts[0]['ws_acct_type']
        
        form.ws_target_id.choices = acct_id
        form.ws_target_type.data=accounts[0]['ws_acct_type']
        return render_template("view_transfer.html",form=form)

 
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")



@app.route("/view_single/<int:id>",methods=['GET'])
def view_single(id):
    if session.get('userId') and session.get('roleId')=="2222":
        
        account=Account.objects(ws_acct_id=id).first()
        return render_template('single_account_details.html',account = account)
        
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")


@app.route("/deposit_amount",methods=['POST'])
def deposit_amount():
    if session.get('userId') and session.get('roleId')=="2222":
        print("inside acct delete",request.form["acct_id"])
        account=Account.objects(ws_acct_id=request.form["acct_id"]).first()

        if not request.form["deposit_amount"].isnumeric():
            flash("Please enter only digits","danger")
            return render_template('view_deposit.html',account=account)
        print(type(request.form["deposit_amount"]))
        deposit_amount=int(request.form["deposit_amount"])
        account.ws_acct_balance=account.ws_acct_balance+deposit_amount
        ws_cust_id=account.ws_cust_id
        ws_acct_id=account.ws_acct_id
        ws_transaction_id=generate_Transaction_Id()
        ws_description='Deposit'
        ws_amount=deposit_amount
        x = datetime.now()
        d=x.strftime("%x")
        y = datetime.now()
        t=y.strftime("%X")
        dt = d + " " + t 
        ws_trxn_date=datetime.strptime(dt,'%m/%d/%y %H:%M:%S')
        Transaction(ws_cust_id=ws_cust_id,ws_acct_id=ws_acct_id,ws_transaction_id=ws_transaction_id,ws_description=ws_description,ws_amount=ws_amount,ws_trxn_date=ws_trxn_date).save()
        account.save()
        flash("Amount deposited successfully","success")
        return redirect('/view_single/'+request.form["acct_id"])

    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")
        
@app.route("/withdraw_amount",methods=['POST'])
def withdraw_amount():
    if session.get('userId') and session.get('roleId')=="2222":
        account=Account.objects(ws_acct_id=request.form["acct_id"]).first()

        if not request.form["withdraw_amount"].isnumeric():
            flash("Please enter only digits","danger")
            return render_template('view_withdraw.html',account=account)
        withdraw_amount=int(request.form["withdraw_amount"])
        if(account["ws_acct_balance"]<int(withdraw_amount)):
            flash("You dont have enough balance to withdraw given amount","danger")
            return render_template('view_withdraw.html',account=account)
        else:
            account.ws_acct_balance=account.ws_acct_balance-withdraw_amount
            ws_cust_id=account.ws_cust_id
            ws_acct_id=account.ws_acct_id
            ws_transaction_id=generate_Transaction_Id()
            ws_description='withdraw'
            ws_amount=withdraw_amount
            x = datetime.now()
            d=x.strftime("%x")
            y = datetime.now()
            t=y.strftime("%X")
            dt = d + " " + t 
            ws_trxn_date=datetime.strptime(dt,'%m/%d/%y %H:%M:%S')
            Transaction(ws_cust_id=ws_cust_id,ws_acct_id=ws_acct_id,ws_transaction_id=ws_transaction_id,ws_description=ws_description,ws_amount=ws_amount,ws_trxn_date=ws_trxn_date).save()
            account.save()
            flash("Amount withdrawn successfully","success")
            return redirect('/view_single/'+request.form["acct_id"])

    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")

@app.route('/account_status',methods=['GET','POST'])
def account_status():
    if session.get('userId'):
        accounts=Account_Status.objects.all()
        return render_template('account_status.html',accounts=accounts)  

@app.route("/transfer_details/<source_id>/<target_id>/<old_source>/<new_source>/<old_target>/<new_target>",methods=["GET"])
def transfer_details(source_id,target_id,old_source,new_source,old_target,new_target):
    if session.get('userId') and session.get('roleId')=="2222":
        return render_template("transfer_details.html",source_id=source_id,target_id=target_id,old_source=old_source,new_source=new_source,old_target=old_target,new_target=new_target)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")

@app.route("/transfer_amount",methods=['POST'])
def transfer_amount():
    if session.get('userId') and session.get('roleId')=="2222":
        form = TransferForm()
        print(form.ws_source_id.data)
        
        if request.method=="POST":
            
            if form.ws_source_id.data==form.ws_target_id.data:
                flash("Source Account and Target account cannot be same","danger")
                return redirect('/account_search')
            else:
                cust_id=form.ws_cust_id.data
                print("cust_id",form.ws_cust_id.data)
                source_id=form.ws_source_id.data
                target_id=form.ws_target_id.data
                transfer_amount=form.ws_transfer_amount.data
                source_account=Account.objects(ws_acct_id=source_id).first()
                old_source=source_account.ws_acct_balance
                if source_account.ws_acct_balance<transfer_amount:
                    flash("Sorry you dont have enough balance in source account to transfer","danger")
                    accounts=Account.objects(ws_cust_id=cust_id).all()
                    acct_id = []
          
                    for account in accounts:
                        acct_id.append((account.ws_acct_id,str(account.ws_acct_id)))
                    print(acct_id)
                    form.ws_cust_id.data=cust_id
                    form.ws_source_id.choices = acct_id
             
                    
                    form.ws_target_id.choices = acct_id
                 
                    return render_template("view_transfer.html",form=form)
                else:
                    
                    source_account.ws_acct_balance=source_account.ws_acct_balance-transfer_amount
                    new_source=source_account.ws_acct_balance
                    source_account.save()
                    

                    target_account=Account.objects(ws_acct_id=target_id).first()
                    old_target=target_account.ws_acct_balance
                    target_account.ws_acct_balance=target_account.ws_acct_balance+transfer_amount
                    new_target=target_account.ws_acct_balance
                    target_account.save()
                    x = datetime.now()
                    d=x.strftime("%x")
                    y = datetime.now()
                    t=y.strftime("%X")
                    dt = d + " " + t 
                    ws_trxn_date=datetime.strptime(dt,'%m/%d/%y %H:%M:%S')
                    Transaction(ws_cust_id=source_account.ws_cust_id,ws_acct_id=source_id,ws_transaction_id=generate_Transaction_Id(),ws_description="Transfer",ws_amount=transfer_amount,ws_trxn_date=ws_trxn_date).save()

                    flash("Transfer made successfully","success")
                    return redirect(url_for("transfer_details",source_id=source_id,target_id=target_id,old_source=old_source,new_source=new_source,old_target=old_target,new_target=new_target))
                
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")

@app.route('/account_statement',methods=['GET','POST'])
def account_statement():
    if session.get('userId') and session.get('roleId')=="2222":
        accounts = Account.objects.all()
        acc_id = []
        if accounts:
            acct_type=accounts[0]['ws_acct_type']
         
            for account in accounts:
                acc_id.append((account.ws_acct_id))
           
        if(request.method=='POST'):
            acc_id=request.form.get('ws_acct_id')
            type=request.form.get('type')
            if(type=='Last number of Transactions'):
                return render_template('acct_sta_number.html',acc_id=acc_id)
            else:
                return render_template('acct_sta_date.html',acc_id=acc_id)

        return render_template('account_statement.html',acc_id=acc_id)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")

@app.route('/view_account_statement_number',methods=['GET','POST'])
def view_account_statement_number():
    if session.get('userId') and session.get('roleId')=="2222":
        acct_id=request.form.get('ws_acct_id')
        number= request.form.get('number_of_Transactions')
        Transactions=Transaction.objects(ws_acct_id=acct_id)
        tra=Transactions.order_by('-ws_trxn_date').limit(int(number))
        return render_template('view_account_statement.html',Transactions=tra,ws_acct_id=acct_id,records=number)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")
    
@app.route('/view_account_statement_date',methods=['GET','POST'])
def view_account_statement_date():
    if session.get('userId') and session.get('roleId')=="2222":
        acct_id=request.form.get('ws_acct_id')
        start_date=request.form.get('start_date')
        start_date=datetime.strptime(start_date,'%Y-%m-%d')
        start_date1=dateutil.parser.parse(str(start_date)).date()
        end_date=request.form.get('end_date')
        end_date=datetime.strptime(end_date,'%Y-%m-%d')
        end_date1=dateutil.parser.parse(str(end_date)).date()

        print(start_date)
        print('from form')
        print(type(start_date))
        print(end_date)
        print('from form')
        print(type(end_date))
        
        data=[]
        Transactions=Transaction.objects(ws_acct_id=acct_id)
        for x in Transactions:
            print(x.ws_trxn_date)
            print(type(x.ws_trxn_date))
            if(x.ws_trxn_date >= start_date1 and x.ws_trxn_date <= end_date1):
                print('in')
                data.append(x)
        return render_template('view_account_statement.html',Transactions=data,ws_acct_id=acct_id,start_date=start_date1,end_date=end_date1)
    else:
        flash("Sorry You are not authorised to access this page","danger")
        return redirect("/")   

        




