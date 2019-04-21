from flask import Flask, flash, redirect, render_template, request, session, abort
import sys, os
from methods.database import connection, authenticate

app = Flask(__name__)


@app.route("/admin", methods=['GET', 'POST'])
def dashboard():
   if not session.get('logged_in'):
        return render_template('index.html')
   try:
        return(str(session['user']))
   except Exception as e:
        return('failure')

@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if authenticate(request.form['email'], request.form['pass']):
                session['logged_in'] = True
                session['user'] = request.form['email']

    return dashboard()

@app.route('/')
def tree():
    return dashboard()


@app.route("/logout")
def logout():
    session.clear()
    return dashboard()



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
