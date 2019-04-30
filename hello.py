from flask import Flask, flash, redirect, render_template, request, session, abort
import sys, os
from methods.database import connection, authenticate, insertProduct, getProducts
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
        return render_template('dashboard.html')
   except Exception as e:
        return('failure')

@app.route('/admin/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if authenticate(request.form['email'], request.form['pass']):
                session['logged_in'] = True
                session['user'] = request.form['email']
                return dashboard()

    return redirect('/admin')


@app.route('/', methods=['GET', 'POST'])
def tree():
    return home()

@app.route("/admin/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/admin')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('market.html')


@app.route("/test", methods=['GET', 'POST'])
def test():
    return str(getProducts(offset=1,limit=10))


@app.route('/admin/upload', methods=['GET', 'POST'])
def upload_file():
    if not session.get('logged_in'):
         return redirect('/admin')

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file =  request.files['file']
        if file == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            insertProduct(path = path, uploader= session.get('user'))
            return redirect(request.url)

    return render_template('Upload.html')

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
