from flask import Flask, flash, redirect, render_template, request, session, abort
import sys, os
from methods.database import connection, authenticate
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'Products/'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/', methods=['GET', 'POST'])
def tree():
    return dashboard()


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return dashboard()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if not session.get('logged_in'):
         return render_template('index.html')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)
    return render_template('upload.html')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
