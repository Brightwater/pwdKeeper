from flask import Flask, redirect, session, url_for, render_template, request
from passwords import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
@app.route("/")
def home():
    return redirect(url_for("loginPage"))

@app.route("/signUp", methods=["POST", "GET"])
def signUp():
    return render_template('signUp.html')

@app.route("/login", methods=["POST", "GET"])
def loginPage():
    if request.method == "POST":
            user = request.form["username"]
            password = request.form["password"]

            session['attemps'] = 1
            
            b = login(user, password)
            if b is -1:
                error = "Incorrect login credentials"
                return render_template('login.html', error=error)
            
            session['username'] = user
            session['password'] = password
            
            print("Logged in as", user, "\n")
            return redirect(url_for("userPage", user=user))
    else:
        return render_template('login.html')

@app.route("/<user>")
def userPage(user):
    # check if actually logged in
    if user in session['username']:
        print("user found")
    else:
        print("no user found in session")
        return render_template('login.html')

    services = listAllServices(user)
    print(services)
    
    return render_template('home.html', user=user, services=services)

@app.route('/getService', methods=['GET', 'POST'])
def getService():
    if user in session['username']:
        print("user found")
        
        if request.method == "POST":
            service = request.form['btnSubmit']

            services = listAllServices(session['username'])

            cred, s = getServiceCredentials(session['username'], service, session['password'])
            if cred is -1:
                print("Service not found")
            if cred is 0:
                print("Could not verify master password")
            else:
                print(s)
            return render_template('home.html', info=s, services=services, user=session['username'])
        else:
            return render_template('home.html', user=session['username'], services=services)
    else:
        print("no user found in session")
        return render_template('login.html')

    

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)