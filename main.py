from flask import Flask, redirect, session, url_for, render_template, request
from passwords import *
import os
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)
@app.route("/")
def home():
    return redirect(url_for("loginPage"))

@app.route("/signUp", methods=["POST", "GET"])
def signUp():
    if request.method == "POST":
        print(request.form.get("btnSignUp"))
        if request.form.get("btnSignUp") == 'Sign Up':
            user = request.form["username"]
            password = request.form["password"]
            password2 = request.form["password2"]

            if password not in password2:
                error = "Passwords did not match"
                return render_template('signUp.html', error=error)

            if len(user) < 1:
                error = "Please enter username"
                return render_template('signUp.html', error=error)
            
            if len(password2) < 3:
                error = "Password not long enough"
                return render_template('signUp.html', error=error)

            ret = newUser(user, password)
            if ret is -1:
                print("an error occured adding user")
                error = "An error occured adding user"
                return render_template('signUp.html', error=error)

            else:
                print(ret)
                error = "User successfully created"
                return render_template('signUp.html', error=error, s=1)
        
        if request.form.get("btnSignUp") == 'Return to login':
            return redirect(url_for("loginPage")) 
        

    return render_template('signUp.html')

@app.route("/login", methods=["POST", "GET"])
def loginPage():
    if request.method == "POST":
            if request.form.get("btnLogIn") == 'Log In': 
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
            if request.form.get("btnLogIn") == 'Sign Up':
                print("sign up")
                return redirect(url_for("signUp"))
    else:
        return render_template('login.html')

@app.route("/<user>", methods=['GET', 'POST'])
def userPage(user):
    # check if actually logged in
    if user in session['username']:
        print("user found")
    else:
        print("no user found in session")
        return render_template('login.html')

    services = listAllServices(user)
    print(services)

    if request.method == "POST":
        service = request.form["service"]
        username = request.form["username"]
        password = request.form["password"]

        if len(service) < 1:
            error = "Please enter a service"
            return render_template('home.html', user=user, services=services, error=error)

        if len(username) < 1:
            error = "Please enter a username"
            return render_template('home.html', user=user, services=services, error=error)

        if len(password) < 1:
            error = "Password not long enough"
            return render_template('home.html', user=user, services=services, error=error)

        r = addService(session['username'], session['password'], service, username, password)
        if r is -1:
            print("An error occured adding service")
            error = "An error occured adding service"
            return render_template('home.html', user=user, services=services, error=error)
        
        else:
            print(r, "Added service?")
            error = f"{service} has been added to password keeper"
            return render_template('home.html', user=user)
    
    return render_template('home.html', user=user, services=services)

@app.route('/getService', methods=['GET', 'POST'])
def getService():
    if user in session['username']:
        print("user found")
        
        services = listAllServices(session['username'])

        if request.method == "POST":
            print(request.form.get("btnAdd"))
            if request.form.get("btnAdd") == 'Add Service':
                service = request.form["service"]
                username = request.form["username"]
                password = request.form["password"]

                if len(service) < 1:
                    print("error")
                    error = "Please enter a service"
                    return render_template('home.html', user=user, services=services, error=error)

                if len(username) < 1:
                    print("error")
                    error = "Please enter a username"
                    return render_template('home.html', user=user, services=services, error=error)

                if len(password) < 1:
                    print("error")
                    error = "Password not long enough"
                    return render_template('home.html', user=user, services=services, error=error)

                r = addService(session['username'], session['password'], service, username, password)
                if r is -1:
                    print("An error occured adding service")
                    error = "An error occured adding service"
                    return render_template('home.html', user=user, services=services, error=error)
                
                else:
                    print("Service added")
                    error = f"{service} has been added to password keeper"
                    return render_template('home.html', user=user)
            
            service = request.form['btnSubmit']

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