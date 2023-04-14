# R4.A.10 - TP Sécurité web

## **Description**

Ce TP traite de plusieurs menaces importantes de la sécurité web. Voici les cas évoqués :

1. Démontrer une injection SQL via un jeu de formulaires
2. Démontrer une faille XSS
3. Créer une système d’authentification forte via OTP email.
4. Construire un formulaire avec contrôle front et contrôle middle des données <br> ex : Gestion d’un profil utilisateur
5. Mettre en place un système simple de traçabilité via des fichiers de logs
6. Mettre en place un chiffrement applicatif

Pour une approche plus théorique de ces menaces, rendez vous *./compte-rendu.odp*

## **Installation**

Au préalable, vous devez disposer de :
- **Python** : Pour exécuter le code.
- **PostgreSQL** : Pour la base de donnée. Lancer également le script */data/script.sql* dans votre PostgreSQL. 


Pour lancer ce projet, il faut ensuite installer les dépendances suivantes :

- Flask
- psycopg2
- Flask-Mail
- pyotp
- python-dotenv

Ces dépendances peuvent être installées en utilisant pip dans votre shell :

```
pip install -r requirements.txt
```

## **Utilisation**

1ère page : Identifiez-vous avec vos **ID PostgreSQL** pour que nous puissions accéder à votre BDD.

Pour le reste. Identifiez-vous avec les **ID** présent dans la table **BDD**. Vous pouvez vous connecter par défaut avec l'id suivant.
```
Username : client2
Password : mdp
```


## Auteur

- @RaphaelGuarim | Raphael GUARIM
- @ludo3105 | Ludovic GUYADER
- @vsentchev | Vassili SENTCHEV