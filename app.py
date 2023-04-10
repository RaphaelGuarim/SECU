
from flask import Flask, render_template, request, redirect
import psycopg2
import hashlib
from flask_mail import Mail, Message
import pyotp
import datetime,timedelta

app = Flask(__name__)


nom = ""
mdp = ""
verif = False
expiration = None
otp_code = None


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'raphaguarim5@gmail.com'
app.config['MAIL_PASSWORD'] = 'vmpdwvgivpvtcmxz'

Email = Mail(app)

@app.route('/')
def h():
    return render_template("home.html")

@app.route('/home')
def home_connect():
    return render_template("home_connect.html")

@app.route('/mail')
def mail():
    return render_template("home_mail.html")

@app.route('/SQL')
def post():
    return render_template("home_SQL.html")

@app.route('/connectmail' ,methods=['POST','GET'])
def postmail():
    return render_template("home.html")

@app.route('/connectHome' ,methods=['POST','GET'])
def conn():
    global nom, mdp, verif

    print("verif = ", verif)
    if (verif==False):

        nom = request.form['name'] 
        mdp = request.form['password']
        
        # Parce que guyader rime avec galère, mon port n'est pas celui par défaut
        if nom == 'lguyader': PORT : int = 5433
        else: PORT : int = 5432
        
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=PORT,
                database="secu1",
                user=nom,
                password=mdp
            )
            if conn is not None:
                verif= True
                conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur")
            return render_template("home.html")
    return render_template("home_connect.html")


@app.route('/connect', methods=['POST','GET'])
def home():
    return render_template("home_connect.html")


@app.route('/mail_conn',methods=['POST','GET'])
def mail_conn():
    
    global expiration
    global otp_code
    
    name = request.form['name'] 
    password = request.form['password']
    
    encoded_password = password.encode('utf-8')
    hash_object = hashlib.sha256(encoded_password)
    password_hash = hash_object.hexdigest()
    
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="secu1",
            user=nom,
            password=mdp
        )
    except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur")
            return render_template("home_mail.html")
        
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM connexion WHERE name LIKE %s AND password LIKE %s ",(name,password_hash))
    
    results = cursor.fetchall()
    if (len(results)!= 0):
        
        # Géneration d'un otp de 5 minutes
        otp_secret = pyotp.random_base32()
        otp = pyotp.TOTP(otp_secret, interval=300)
        otp_code = otp.now()
        
        # Enregistrement de la date
        otp_created_at = datetime.datetime.now()
        expiration = otp_created_at + datetime.timedelta(minutes=5)
        
        # Envoi du mail
        msg = Message('Hello', sender='raphaguarim5@gmail.com', recipients=[results[0][0]])
        msg.body = msg.body = f"Votre OTP est : {otp_code}. Il est valable jusqu'à {expiration.strftime('%H:%M:%S')}."
        Email.send(msg)
        return render_template('OTP.html')
    
    cursor.close()
    conn.close()
    
    return render_template("home_mail.html")


@app.route('/OTP', methods=['POST'])
def otp():
    password = request.form['password']
    if (password==otp_code):
        if (expiration != None and datetime.datetime.now()<expiration):
            return render_template('edit.html')
        else:
            return "<div>Le mot de passe a expiré</div>"
    else:
        return "<div>Le mot de passe est mauvais</div>"


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name'] 
    password = request.form['password']
    
    conn = psycopg2.connect(
        host="localhost",
        database="secu1",
        user=nom,
        password=mdp
    )   

    cursor = conn.cursor()
    
    # Requete sécurisée
    cursor.execute("SELECT * FROM connexion WHERE name LIKE %s AND password LIKE %s ",(name,password))
    
    results = cursor.fetchall()
    if (len(results)!= 0):
        return render_template('connected.html')
    
    cursor.close()
    conn.close()
    return render_template('home_SQL.html')

@app.route('/submit2', methods=['POST'])
def submit2():
    name = request.form['name'] 
    password = request.form['password']

    
    conn = psycopg2.connect(
        host="localhost",
        database="secu1",
        user=nom,
        password=mdp
    )   
    
    cursor = conn.cursor()
    
    # Ancienne requète non sécurisée
    requete = "SELECT * FROM connexion WHERE name LIKE '"+ name +"' AND password LIKE '"+password+"' "
    cursor.execute(requete)
    
    results = cursor.fetchall()
    if (len(results)!= 0):
        return render_template('connected.html')
    
    cursor.close()
    conn.close()
    return render_template('home_SQL.html')

@app.route('/deconnexion', methods=['GET', 'POST'])
def deconnexion():
    global nom, mdp, verif

    nom = "";    mdp = "";    verif = False
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)

    # Test
    # Name : client | Password : mdp
    # ' OR 1=1 --