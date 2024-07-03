"""
This script handles the execution of the Flask Web Server(Web Application + JSON API)
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
#from flaskext.mysql import MySQL
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import tree 
from sklearn import model_selection
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
#from googleplaces import GooglePlaces, types, lang 
from flask_socketio import SocketIO
import pandas as pd 
import numpy as np
import pickle
import re
import os
import random
import hashlib 
import bcrypt
import json
import requests
import nltk
import pybase64
from datetime import date
from sklearn.preprocessing import normalize
import MySQLdb
from datetime import timedelta
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

import seaborn as sns
import scipy.stats as stats
import sklearn
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing

import pdfdemo as pdfgen
import pdfdemo1 as pdfgen1
import pdfdemo2 as pdfgen2
from flask import send_file

app = Flask(__name__)

port = int(os.environ.get('PORT', 5000))


# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'canada$God7972#'

# Enter your database connection details below
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD	'] ="tiger"
app.config['MYSQL_DATABASE_DB'] = 'fetalhealth'

# Intialize MySQL
# mysql = MySQL(autocommit=True)
# mysql.init_app(app)
mydb = MySQLdb.connect(host='localhost',user='root',passwd='tiger',db='fetalhealth')
#app.permanent_session_lifetime = timedelta(minutes=15)




    
#Homepage
@app.route('/')
def index():
    if 'loggedin' not in session:
        return render_template('index.html')
    else:
        return home()

#Dashboard
@app.route('/dashboard')
def home():
    # Check if user is loggedin
    print("session===22",session)
    if 'loggedin' in session:
        print("Inside If in dashbord")
        # User is loggedin show them the home page
        if(session['isdoctor']==0):
            cursor = mydb.cursor()
            cursor.execute('SELECT * FROM users WHERE ID = %s', (session['id'],))
        else:
            cursor = mydb.cursor()
            cursor.execute('SELECT * FROM doctors WHERE ID = %s', (session['id'],))
        account = cursor.fetchone()
        print("Account==",account)
        print("account[1]==",account[1])
        cursor1 = mydb.cursor()
        cursor1.execute('SELECT * FROM pdffiles where pname = %s',(account[1],)) 
        appoint=cursor1.fetchall()
        
        
        return render_template('dashboard.html', account = account, isdoctor=session['isdoctor'],appoint=appoint)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#Patient Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' not in session:
    # Output message if something goes wrong...
        msg = None
        # Check if "username" and "password" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            if(username and password):
            # Check if account exists using MySQL
                cursor = mydb.cursor()
                cursor.execute('SELECT * FROM users WHERE Username = %s', (username,))
                # Fetch one record and return result
                account = cursor.fetchone()
                # If account exists in accounts table in out database
                if account:
                    if bcrypt.checkpw(password.encode('utf-8'), account[2].encode('utf-8')):
                        # Create session data, we can access this data in other routes
                        session['loggedin'] = True
                        session['id'] = account[0]
                        session['username'] = account[1]
                        session['api'] = account[8]
                        session['isdoctor'] = 0
                        # Redirect to dashboard
                        
                        return home()
                    else:
                        # Account doesnt exist or username/password incorrect
                        msg = 'Incorrect username/password!'
                        flash(msg)
                else:
                    # Account doesnt exist or username/password incorrect
                    msg = 'Incorrect username/password!'
                    flash(msg)
            else:
                msg = 'Please provide both username and password!'
                flash(msg)
        # Show the login form with message (if any)
    else:
        return home()
    return render_template('patientlogin.html', msg=msg)

#Patient Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    if('loggedin' not in session):
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            full_name = request.form['full_name']
            address = request.form['address']
            age = request.form['age']
            blood = request.form['blood']
            if(username and password and email and full_name and address and age and blood):
                # Check if account exists using MySQL
                cursor = mydb.cursor()
                cursor.execute('SELECT * FROM users WHERE Username = %s', (username,))
                account = cursor.fetchone()
                # If account exists show error and validation checks
                if account:
                    msg = 'Account already exists!'
                    flash(msg)
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address!'
                    flash(msg)
                elif not re.match(r'[A-Za-z0-9]+', username):
                    msg = 'Username must contain only characters and numbers!'
                    flash(msg)
                else:
                    # Account doesnt exists and the form data is valid, now insert new account into users table
                    apistr = username;
                    result = hashlib.md5(apistr.encode()) 
                    comb = username+'(~)'+password
                    s = comb.encode()
                    s1 = pybase64.b64encode(s)
                    api=s1.decode('utf-8')
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)', (username, hashed_password, email, full_name, address, blood, age, api))
                    mydb.commit()
                    cursor.execute('SELECT * FROM users WHERE Username = %s', (username,))
                    # Fetch one record and return result
                    account = cursor.fetchone()
                    session['loggedin'] = True
                    session['id'] = account[0]
                    session['username'] = account[1]
                    session['api'] = account[8]
                    session['isdoctor'] = 0
                    msg = 'You have successfully registered!'
                    return home()
            else:
                msg = 'Please fill out the form!'
                flash(msg)
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
        # Show registration form with message (if any)
    else:
        return home()
    return render_template('patientlogin.html', msg=msg)

#Doctor Register
@app.route('/docregister', methods=['GET', 'POST'])
def docregister():
    if 'loggedin' not in session:
    # Output message if something goes wrong...
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            full_name = request.form['full_name']
            registration_number = request.form['registration_number']
            contact_number = request.form['contact_number']
            spec = request.form['specialization']
            address = request.form['address']
            if(username and password and email and full_name and registration_number and contact_number and spec and address):
            # Check if account exists using MySQL
                cursor = mydb.cursor()
                cursor.execute('SELECT * FROM doctors WHERE Username = %s', (username,))
                account = cursor.fetchone()
                # If account exists show error and validation checks
                if account:
                    msg = 'Account already exists!'
                    flash(msg)
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address!'
                    flash(msg)
                elif not re.match(r'[A-Za-z0-9]+', username):
                    msg = 'Username must contain only characters and numbers!'
                    flash(msg)
                else:
                    # Account doesnt exists and the form data is valid, now insert new account into users table
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute('INSERT INTO doctors VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)', ( username, hashed_password, email, full_name, registration_number, contact_number, "Default Hospital" , spec, address ))
                    mydb.commit()
                    msg = 'You have successfully registered!'
                    cursor.execute('SELECT * FROM doctors WHERE Username = %s', (username,))
                    # Fetch one record and return result
                    account = cursor.fetchone()
                    session['loggedin'] = True
                    session['id'] = account[0]
                    session['username'] = account[1]
                    session['isdoctor'] = 1
                    return home()
            else:
                msg = 'Please fill out the form!'
                flash(msg)
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
    else:
        return home()
    # Show registration form with message (if any)
    return render_template('doctorlogin.html', msg=msg)


    



    
#Doctor Login
@app.route('/doclogin', methods=['GET', 'POST'])
def doclogin():
    if 'loggedin' not in session:
    # Output message if something goes wrong...
        msg = ''
        # Check if "username" and "password" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            if(username and password):

                # Check if account exists using MySQL
                cursor = mydb.cursor()
                cursor.execute('SELECT * FROM doctors WHERE Username = %s', (username,))
                # Fetch one record and return result
                account = cursor.fetchone()
                # If account exists in accounts table in out database
                if account:
                    if bcrypt.checkpw(password.encode('utf-8'), account[2].encode('utf-8')):
                        # Create session data, we can access this data in other routes
                        session['loggedin'] = True
                        session['id'] = account[0]
                        session['username'] = account[1]
                        session['isdoctor'] = 1
                        # Redirect to home page
                        print("session==",session)
                        return home()
                    else:
                        # Account doesnt exist or username/password incorrect
                        msg = 'Incorrect username/password!'
                        flash(msg)
                else:
                    # Account doesnt exist or username/password incorrect
                    msg = 'Incorrect username/password!'
                    flash(msg)
            else:
                msg = 'Please provide both username and password!'
                flash(msg)
    else:
        return home()
    # Show the login form with message (if any)
    return render_template('doctorlogin.html', msg=msg)

#BMI for the dashboard(Written by Mayank)
@app.route('/bmi',methods=['GET', 'POST'])
def bmi():
    print("session in bmi==",session)
    if 'loggedin' in session:
        result=0
        cursor = mydb.cursor()
        print('session["isdoctor"]',session["isdoctor"])
        if session["isdoctor"]:
            cursor.execute('SELECT * FROM doctors WHERE ID = %s', (session['id'],))
        else:
            cursor.execute('SELECT * FROM users WHERE ID = %s', (session['id'],))
        account = cursor.fetchone()
        if request.method=='POST':
            h=request.form["height"]
            w=request.form["weight"]
            if h and w:
                h=float(h)
                h = h/100
                w=float(w)
                result=w/(h*h)
                result=round(result,2)
                return render_template('bmi.html',ans=result,account=account, height=h, weight=w)
            else:
                msg = 'Please provide height and weight' 
                flash(msg)
        return render_template('bmi.html',ans=result,account=account) 
    return redirect(url_for('login'))









# Account information visible inside dashboard
@app.route('/myaccount')
def myaccount():
    if 'loggedin' in session:
        cursor = mydb.cursor()
        if session["isdoctor"]:
            cursor.execute('SELECT * FROM doctors WHERE ID = %s', (session['id'],))
        else:
            cursor.execute('SELECT * FROM users WHERE ID = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('myaccount.html', account=account, isDoctor = session["isdoctor"])
    else:
        return redirect(url_for('login'))



@app.route('/hospitalset1',methods=['GET', 'POST'])
def hospitalset1():
    if 'loggedin' in session:
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM doctors WHERE ID = %s', (session['id'],))
        account = cursor.fetchone()
        if(request.method == 'POST'):
            hname = request.form['week']
            week=int(hname)
            if week==1:
                cursor.execute("SELECT Username FROM users")
                l = cursor.fetchall()
                places = []
                for i in l:
                    places.append(i) 
                return render_template('hospitalset.html', places=places, account=account)
            if week==2:
                cursor.execute("SELECT Username FROM users")
                l = cursor.fetchall()
                places = []
                for i in l:
                    places.append(i) 
                return render_template('hospitalset2.html', places=places, account=account)
            if week==3:
                cursor.execute("SELECT Username FROM users")
                l = cursor.fetchall()
                places = []
                for i in l:
                    places.append(i) 
                return render_template('hospitalset3.html', places=places, account=account)  
        return render_template("hospitalset1.html",account=account)
    return redirect(url_for('login'))

@app.route('/thirdtremister',methods=['GET','POST'])
def thirdtremister():
    if 'loggedin' in session:
        print("Inside if====")
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM doctors WHERE ID = %s', (session['id'],))
        account = cursor.fetchone()
        if(request.method == 'POST'):
            hname = request.form['hname']
            hname=hname.replace(",","")
            hname=hname.replace("'","")
            hname=hname.replace("(","")
            hname=hname.replace(")","")
            examres=request.form['examres']
            cvm=request.form['cvm']
            al=request.form['al']
            fhr=request.form['fhr']
            bpd=request.form['bpd']
            ofd=request.form['ofd']
            hdc=request.form['hdc']
            abdc=request.form['abdc']
            fl=request.form['fl']
            ci=request.form['ci']
            hc=request.form['hc']
            flbda=request.form['flbda']
            flac=request.form['flac']
            ubpi=request.form['ubpi']
            ubri=request.form['ubri']
            ubsd=request.form['ubsd']
            rubpi=request.form['rubpi']
            rubri=request.form['rubri']
            rubsd=request.form['rubsd']
            lubpi=request.form['lubpi']
            lubri=request.form['lubri']
            lubsd=request.form['lubsd']
            fmcapi=request.form['fmcapi']
            fmcri=request.form['fmcri']
            fmcsd=request.form['fmcsd']
            bpdw=request.form['bpdw']
            hccw=request.form['hccw']
            abdcw=request.form['abdcw']
            flw=request.form['flw']
            eddu=request.form['eddu']
            today = date.today()
            docname=account[1]
            cursor = mydb.cursor()
            cursor.execute("SELECT Age FROM users where Username='"+hname+"'")
            userage = cursor.fetchone()
            age=int(userage[0])
            print("Read from 3==",[hname,examres,cvm,al,fhr,bpd,ofd,hdc,abdc,fl,ci,hc,flbda,flac,ubpi,ubri,ubsd,rubpi,rubri,rubsd,lubpi,lubri,lubsd,fmcapi,fmcri,fmcsd,bpdw,hccw,abdcw,flw,eddu,str(today),docname,str(age)])
            pdfgen2.process(hname,examres,cvm,al,fhr,bpd,ofd,hdc,abdc,fl,ci,hc,flbda,flac,ubpi,ubri,ubsd,rubpi,rubri,rubsd,lubpi,lubri,lubsd,fmcapi,fmcri,fmcsd,bpdw,hccw,abdcw,flw,eddu,str(today),docname,str(age))
            cursor1 = mydb.cursor()
            cursor1.execute('INSERT INTO pdffiles VALUES (NULL, %s, %s,%s)', ( docname, hname,"3"))
            mydb.commit()
            return render_template('dashboard.html', account=account)

@app.route('/download_file/<int:aid>',methods=['GET'])
def download_file(aid):
    if 'loggedin' in session:
        print("aid==",aid)
        aid1=int(aid)
        cursor = mydb.cursor()
        cursor.execute("SELECT pname,trimester FROM pdffiles where id = %s",(aid1,))
        userage = cursor.fetchone()
        pname=userage[0]
        trimester=userage[1]
        print("pname==",pname)
        print("trimester==",trimester)
        path=""
        
        #print("uname==",uname)
        path="./static/"+str(pname)+"_"+trimester+".pdf"
        return send_file(path, as_attachment=True)



@app.route('/secondtremister',methods=['GET', 'POST'])
def secondtremister():
    if 'loggedin' in session:
        print("Inside if====")
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM doctors WHERE ID = %s', (session['id'],))
        account = cursor.fetchone()
        if(request.method == 'POST'):
            hname = request.form['hname']
            hname=hname.replace(",","")
            hname=hname.replace("'","")
            hname=hname.replace("(","")
            hname=hname.replace(")","")
            examres=request.form['examres']
            cvm=request.form['cvm']
            bpd=request.form['bpd']
            al=request.form['al']
            fhr=request.form['fhr']
            ofd=request.form['ofd']
            hdc=request.form['hdc']
            abdc=request.form['abdc']
            fl=request.form['fl']
            humer=request.form['humer']
            rad=request.form['rad']
            ulna=request.form['ulna']
            tib=request.form['tib']
            fib=request.form['fib']
            bpdw=request.form['bpdw']
            hdcw=request.form['hdcw']
            abdcw=request.form['abdcw']
            flw=request.form['flw']
            hw=request.form['hw']
            rw=request.form['rw']
            uw=request.form['uw']
            tw=request.form['tw']
            fw=request.form['fw']
            efw=request.form['efw']
            lmp=request.form['lmp']
            mp=request.form['mp']
            edd=request.form['edd']
            eddu=request.form['eddu']
            adv=request.form['adv']
            
            today = date.today()
            docname=account[1]
            cursor = mydb.cursor()
            cursor.execute("SELECT Age FROM users where Username='"+hname+"'")
            userage = cursor.fetchone()
            age=int(userage[0])
            #print("Fetched values==2",hname,examres,cvm,bpd,al,fhr,ofd,hdc,abdc,fl,humer,rad,ulna,tib,fib,bpdw,hdcw,abdcw,flw,hw,rw,uw,tw,fw,efw,lmp,mp,edd,eddu,adv,str(today),docname,str(userage))
            pdfgen1.process(hname,examres,cvm,bpd,al,fhr,ofd,hdc,abdc,fl,humer,rad,ulna,tib,fib,bpdw,hdcw,abdcw,flw,hw,rw,uw,tw,fw,efw,lmp,mp,edd,eddu,adv,str(today),docname,str(userage))
            cursor1 = mydb.cursor()
            cursor1.execute('INSERT INTO pdffiles VALUES (NULL, %s, %s,%s)', ( docname, hname,"2"))
            mydb.commit()
            return render_template('dashboard.html', account=account)
    return render_template('dashboard.html', account=account)


@app.route('/hospitalset',methods=['GET', 'POST'])
def hospitalset():
    # Check if user is loggedin
    print("session in Hospital set==",session)
    if 'loggedin' in session:
        print("Inside if====")
        
        
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM doctors WHERE ID = %s', (session['id'],))
        account = cursor.fetchone()
        cursor = mydb.cursor()
        cursor.execute("SELECT Username FROM users")
        l = cursor.fetchall()
        places = []
        for i in l:
            places.append(i) 
                  
        
            
        if(request.method == 'POST'):
            hname = request.form['hname']
            hname=hname.replace(",","")
            hname=hname.replace("'","")
            hname=hname.replace("(","")
            hname=hname.replace(")","")
            bpd=request.form['bpd']
            hdc=request.form['hdc']
            abdc=request.form['abdc']
            fl=request.form['fl']
            bpdw=request.form['bpdw']
            hdcw=request.form['hdcw']
            abdcw=request.form['abdcw']
            flw=request.form['flw']
            lmp=request.form['lmp']
            ega=request.form['ega']
            edd=request.form['edd']
            eddu=request.form['eddu']
            imp=request.form['imp']
            adv=request.form['adv']
            al=request.form['al']
            fhr=request.form['fhr']
            efw=request.form['efw']
            examres=request.form['examres']
            cvm=request.form['cvm']

            today = date.today()
            docname=account[1]
            cursor = mydb.cursor()
            cursor.execute("SELECT Age FROM users where Username='"+hname+"'")
            userage = cursor.fetchone()
            age=int(userage[0])
            #print("Fetched values==",hname,examres,cvm,bpd,hdc,abdc,f1,bpdw,hdcw,abdcw,f1w,lmp.ega,edd,eddu,imp,adv,al,fhr,efw,str(today),docname,str(userage))
            pdfgen.process(hname,examres,cvm,bpd,hdc,abdc,fl,bpdw,hdcw,abdcw,flw,lmp,ega,edd,eddu,imp,adv,al,fhr,efw,str(today),docname,str(userage))
            cursor1 = mydb.cursor()
            cursor1.execute('INSERT INTO pdffiles VALUES (NULL, %s, %s,%s)', ( docname, hname,"1"))
            mydb.commit()
            




            
            #print("Hname=2==",hname)
            
            return render_template('dashboard.html', account=account)
        return render_template('hospitalset1.html', places=places, account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))




"""
Code for the Chat App
which is based on Sockets.io
"""

socketio = SocketIO(app)



# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
   # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('index'))

#run the Flask Server
if __name__ == '__main__':
	socketio.run(app, debug=True)
    
"""-------------------------------End of Web Application-------------------------------"""
