from flask import Flask, render_template, request, redirect
import psycopg2
import hashlib
from flask_mail import Mail, Message
import pyotp
import datetime
import connection as co
import logging
import os
from dotenv import load_dotenv  # Importation de la bibliothèque python-dotenv pour charger les variables d'environnement
from flask import Flask, render_template, request


# ----------- ----------- ----------- ----------- 
# ----------- CONSTANTES
# ----------- ----------- ----------- ----------- 


nom = ""
mdp = ""
verif = False
expiration = None
otp_code = None




# ----------- ----------- ----------- ----------- 
# ----------- PARTIE 5 : LOG
# ----------- ----------- ----------- ----------- 


# log non séccurisé
"""# création du repertoire des logs
if not os.path.exists('logs'):
    os.makedirs('logs')

# configurer le logger ----------
logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')"""


# log sécurisé

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration de l'application Flask
app = Flask(__name__)

# Configuration du système de journalisation
if not os.path.exists('logs'):  # Vérifie si le dossier "logs" n'existe pas encore
    os.makedirs('logs')  # Si ce n'est pas le cas, crée le dossier "logs" dans le répertoire courant

# Récupération du nom et du niveau de log depuis les variables d'environnement, sinon utilisation des valeurs par défaut
log_file = os.getenv("LOG_FILE") or 'logs/app.log'
log_level = os.getenv("LOG_LEVEL") or logging.INFO

# Configuration de la bibliothèque logging avec le nom et le niveau de log
logging.basicConfig(
    filename=log_file,  # Nom du fichier de log
    level=log_level,  # Niveau de log
    format='%(asctime)s %(levelname)s: %(message)s'  # Format des messages de log
)






# ----------- ----------- ----------- ----------- 
# ----------- MAIL
# ----------- ----------- ----------- ----------- 

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'raphaguarim5@gmail.com'
app.config['MAIL_PASSWORD'] = 'vmpdwvgivpvtcmxz'

Email = Mail(app)




@app.route('/')
def h():
    global verif

    # Si non connecté, home.html, sinon home_connect
    if verif == False:
        return render_template("home.html")
    else:
        return render_template("home_connect.html")

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

        try:
            conn = co.connect(nom, mdp)
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
    global nom, mdp, expiration, otp_code
    
    name = request.form['name'] 
    password = request.form['password']
    
    encoded_password = password.encode('utf-8')
    hash_object = hashlib.sha256(encoded_password)
    password_hash = hash_object.hexdigest()

    try:
        conn = co.connect(nom, mdp)
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
        msg = Message('Hello', sender='raphaguarim5@gmail.com', recipients=[results[0][1]])
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
    global nom, mdp

    name = request.form['name'] 
    password = request.form['password']
    
    conn = co.connect(nom, mdp)
    cursor = conn.cursor()
    
    try:
        encoded_password = password.encode('utf-8')
        hash_object = hashlib.sha256(encoded_password)
        password_hash = hash_object.hexdigest()
        
        # Requete sécurisée
        cursor.execute("SELECT * FROM connexion WHERE name LIKE %s AND password LIKE %s ",(name,password_hash))

        results = cursor.fetchall()
        if (len(results)!= 0):
            return render_template('connected.html')
    except:
        pass
    
    cursor.close()
    conn.close()
    return render_template('home_SQL.html')

@app.route('/submit2', methods=['POST'])
def submit2():
    global nom, mdp
    name = request.form['name'] 
    password = request.form['password']

    conn = co.connect(nom, mdp)
    cursor = conn.cursor()
    
    try:
        encoded_password = password.encode('utf-8')
        hash_object = hashlib.sha256(encoded_password)
        password_hash = hash_object.hexdigest()
        
        # Ancienne requète non sécurisée
        requete = "SELECT * FROM connexion WHERE name LIKE '"+ name +"' AND password LIKE '"+password_hash+"' "
        cursor.execute(requete)
        
        results = cursor.fetchall()
        if (len(results)!= 0):
            return render_template('connected.html')
    except:
        pass

    cursor.close()
    conn.close()
    return render_template('home_SQL.html')

@app.route('/deconnexion', methods=['GET', 'POST'])
def deconnexion():
    global nom, mdp, verif

    nom = "";    mdp = "";    verif = False
    return redirect("/")



# ----------- ----------- ----------- ----------- 
# ----------- PARTIE 2 : Faille XSS
# ----------- ----------- ----------- ----------- 

@app.route('/Part2', methods=['POST','GET'])
def Part2():
    global nom, mdp, verif

    if verif == False:  return redirect("/") # Si t'es pas co, rentre chez toi !

    conn = co.connect(nom, mdp) 
    cursor = conn.cursor()

    cursor.execute("SELECT pseudo, content FROM commentaire")

    return render_template("Partie2_failleXSS/failleXSS.html", all_contents = cursor.fetchall())


# Fonction d'ajout de commentaire
@app.route('//Part2_submit', methods=['GET', 'POST'])
def Partie2_failleXSS():
    global verif, nom, mdp
    
    # S'il n'est pas log, go to home
    if verif == False: return redirect("/")
        
    conn = co.connect(nom, mdp) 
    cursor = conn.cursor()

    # Si post, on insert le commentaire
    if request.method == 'POST':
        requete = "INSERT INTO commentaire VALUES (%s, %s);"
        cursor.execute(requete, (request.form.get('name'), request.form.get('content')))
        conn.commit()

    # On affiche mtn tous les commentaires
    cursor.execute("SELECT pseudo, content FROM commentaire")
    return render_template("Partie2_failleXSS/failleXSS.html", all_contents = cursor.fetchall())



# ----------- ----------- ----------- ----------- 
# ----------- PARTIE 4 : Form contrôle front et contrôle middle des données
# ----------- ----------- ----------- ----------- 

@app.route('/Part4', methods=['GET'])
def Part4():
    return render_template('/Partie4_Contrôle_front_middle_data/connection.html')


global part4_id; part4_id : int | None


# Permet de se co à un profil
@app.route('/Partie4/submitConnection', methods=['POST'])
def Part4_submitConnection():
    global part4_id, nom, mdp

    name = request.form['name'] 
    password = request.form['password']
    
    conn = co.connect(nom, mdp)
    cursor = conn.cursor()
    
    try:
        # Requete sécurisée
        encoded_password = password.encode('utf-8')
        hash_object = hashlib.sha256(encoded_password)
        password_hash = hash_object.hexdigest()
        
        cursor.execute("SELECT * FROM connexion WHERE name LIKE %s AND password LIKE %s ",(name,password_hash))

        results = cursor.fetchall()
        if (len(results)!= 0):
            part4_id = int(results[0][0])
        else : 
            cursor.close()
            conn.close()
            return "Le compte n'existe pas"
    except:
        pass
    
    print("Partie4/submitConnection : " , part4_id)
    cursor.close()
    conn.close()
    return render_template('/Partie4_Contrôle_front_middle_data/modifierCompte.html')


# Permet de modifier son profil sans sécurité
@app.route('/Partie4/submitModifNonSecu', methods=['POST'])
def Part4_submitModifNonSecu():
    global part4_id

    print("Partie4/submitModifNonSecu : " , part4_id)

    # Variables locales
    username : str = request.form['username']
    password : str = request.form['password']
    
    # Hachage du mdp
    encoded_password = password.encode('utf-8')
    hash_object = hashlib.sha256(encoded_password)
    password_hash = hash_object.hexdigest()
    
    # Modif
    conn = co.connect(nom, mdp)
    cursor = conn.cursor()

    try:
        if part4_id != None:
            cursor.execute("update connexion set name = %s, password = %s where id = %s;",(username,password_hash, part4_id))
            conn.commit()
            part4_id = None
    except:
        pass

    cursor.close()
    conn.close()
    return render_template('/Partie4_Contrôle_front_middle_data/connection.html')


# Permet de modifier son profil en sécurité
@app.route('/Partie4/submitModifSecu', methods=['POST'])
def Part4_submitModifSecu():
    global part4_id, nom, mdp

    # Variables locales
    username = request.form['username']
    password = request.form['password']

    # Vérif coté client pour empêcher les champs vides
    if not username or not password:
        return 'Veuillez remplir tous les champs'

    # Vérif coté serveur pour empêcher l'enregistrement des champs vides
    if not username.strip() or not password.strip():
        return 'Veuillez remplir tous les champs'

    # Hachage du mdp
    encoded_password = password.encode('utf-8')
    hash_object = hashlib.sha256(encoded_password)
    password_hash = hash_object.hexdigest()

    # Modif
    conn = co.connect(nom, mdp)
    cursor = conn.cursor()

    try:
        if part4_id != None:
            cursor.execute("update connexion set name = %s, password = %s where id = %s;",(username,password_hash, part4_id))
            conn.commit()
            part4_id = None
    except:
        pass

    cursor.close()
    conn.close()
    return render_template('/Partie4_Contrôle_front_middle_data/connection.html')









if __name__ == '__main__':
    app.run(debug=True)