
from flask import Flask, render_template, request, flash
import psycopg2

app = Flask(__name__)

nom=""
mdp=""
verif = False

@app.route('/')
def h():
    return render_template("home.html")

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
    global nom
    global mdp
    global verif
    
    if (verif==False):

        nom = request.form['name'] 
        mdp = request.form['password']
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="secu1",
                user=nom,
                password=mdp
            )
            if conn is not None:
                conn.close()
                verif= True
        except (Exception, psycopg2.DatabaseError) as error:
            print("Erreur")
            return render_template("home.html")
    return render_template("home_connect.html")


@app.route('/connect', methods=['POST','GET'])
def home():
    return render_template("home_connect.html")



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


if __name__ == '__main__':
    app.run(debug=True)

    # Test
    # Name : client | Password : mdp
    # ' OR 1=1 --