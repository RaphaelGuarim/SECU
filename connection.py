import psycopg2


def connect(name : str, mdp : str):
    # Parce que guyader rime avec galère, mon port n'est pas celui par défaut
    if name == 'lguyader': PORT : int = 5433
    else: PORT : int = 5432

    conn = psycopg2.connect(
        host="localhost",
        port=PORT,
        database="secu1",
        user=name,
        password=mdp
    )
    return conn