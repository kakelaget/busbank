import logging
import os
import psycopg2


logger = logging.getLogger("BusBank")

db_host = os.getenv("BB_DB_HOST", "localhost")
db_name = os.getenv("BB_DB_NAME")
username = os.getenv("BB_DB_USER")
password = os.getenv("BB_DB_PASS")

CONNECTION = None

def _connect():
    logger.debug("Connecting to database", extra={
        "db_name": db_name,
    })
    return psycopg2.connect(
        dbname=db_name,
        user=username,
        password=password)


def connection_alive(connection):
    logger.debug("Checking if database connection is alive", extra={
        "db_name": db_name,
    })
    try:
        c = connection.cursor()
        c.execute("SELECT 1")
        logger.debug("Database connection is alive", extra={
        "db_name": db_name,
    })
        return True
    except psycopg2.OperationalError:
        logger.debug("Database connection is not alive", extra={
        "db_name": db_name,
    })
        return False


def get_connection():
    global CONNECTION
    logger.debug("Getting database connection", extra={
        "db_name": db_name,
    })
    if not CONNECTION:
        CONNECTION = _connect()
        return CONNECTION
    
    # Find out if the connection is still alive
    if CONNECTION.closed != 0 or not connection_alive(CONNECTION):
        CONNECTION = _connect()
        return CONNECTION
    
    return CONNECTION


def insert_raw_text(text):
    logger.debug(f"Inserting {len(text)} characters into DB", extra={
        "char_count": len(text),
    })
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO busbank_text (text)
                VALUES (%s);
                """,
                (text,)
            )
            logger.info(f"Inserted {cursor.rowcount} rows.", extra={
                "db_name": db_name,
                "affected_rows": cursor.rowcount,
                "inserted_rows": cursor.rowcount,
            })
