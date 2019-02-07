import os
import psycopg2

db_host = os.getenv("BB_DB_HOST", "localhost")
db_name = os.getenv("BB_DB_NAME")
username = os.getenv("BB_DB_USER")
password = os.getenv("BB_DB_PASS")

CONNECTION = None

def _connect():
    print("Connecting to database")
    return psycopg2.connect(
        dbname=db_name,
        user=username,
        password=password)


def connection_alive(connection):
    print("Checking if database connection is alive")
    try:
        c = connection.cursor()
        c.execute("SELECT 1")
        print("Database connection is alive")
        return True
    except psycopg2.OperationalError:
        print("Database connection is not alive")
        return False


def get_connection():
    global CONNECTION
    print("Getting database connection")
    if not CONNECTION:
        CONNECTION = _connect()
        return CONNECTION
    
    # Find out if the connection is still alive
    if CONNECTION.closed != 0 or not connection_alive(CONNECTION):
        CONNECTION = _connect()
        return CONNECTION
    
    return CONNECTION


def insert_raw_text(text):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO busbank_text (text)
        VALUES (%s);
        """,
        (text,)
    )


def database_lol():
    print("databasing")
    conn = get_connection()
    c = conn.cursor()
    print("1", c.execute("SELECT 1"))
