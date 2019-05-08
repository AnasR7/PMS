from flask import Flask, flash, redirect, render_template, request, session, abort
import sys, os
from methods.database import connection, authenticate, insertProduct, getProducts, delProduct
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message


UPLOAD_FOLDER = 'static/Products/'
UPLOAD_ORDER = 'Order/'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)

mail_setting = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_PORT": 465,
    "MAIL_USERNAME": 'm7mdbawazeer@gmail.com',
    "MAIL_PASSWORD": 'bawazeer21'
}
app.config.update(mail_setting)
mail = Mail(app)

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
    product = getProducts(10, 0)
    return render_template('market.html', container=product)

@app.route('/product/<int:id>') # nope --> `int:`
def detailProduct_user(id):

    product = getProducts(1, 0, condition={'column': 'id', 'operand': id})
    return render_template('detail_user.html', container=product[0])


@app.route("/admin/catalogue", methods=['GET', 'POST'])
def catalogue():
    if not session.get('logged_in'):
         return redirect('/admin')

    product = getProducts(10, 0)
    return render_template('catalogue.html', container=product)

@app.route('/admin/product/<int:id>') # nope --> `int:`
def detailProduct(id):
    if not session.get('logged_in'):
         return redirect('/admin')

    product = getProducts(1, 0, condition={'column': 'id', 'operand': id})
    return render_template('detail.html', container=product[0])

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
            insertProduct(path = 'Products/'+filename, uploader= session.get('user'))
            return redirect(request.url)

    return render_template('Upload.html')



@app.route('/sendmail', methods=['GET', 'POST'])
def sendmail():
    if request.method == 'POST':
        file =  request.files['file']
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_ORDER, filename)
        file.save(path)

        with app.app_context():
            msg = Message(sender=app.config.get("MAIL_USERNAME"),
                            recipients=[request.form['email']])
            msg.subject=' Printing Order '
            msg.body = "Name: " + request.form['Name'] + '\nphone number: ' + request.form['phone'] + "\nmessage: " + request.form['AdditionalM'] + '  '
            with app.open_resource(UPLOAD_ORDER + filename) as fp:
                msg.attach(filename, 'image/png', fp.read())

            mail.send(msg)
            return home()
    return home()

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
