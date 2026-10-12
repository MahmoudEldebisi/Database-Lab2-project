import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "registration"),
        cursorclass=DictCursor,
        autocommit=True,
    )


def fetch_one(sql, params=()):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)          # values always go in params, never in the SQL text
            return cur.fetchone()
    finally:
        conn.close()


def fetch_all(sql, params=()):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        conn.close()


def execute(sql, params=()):
    """Run INSERT/UPDATE/DELETE. Returns (rows_changed, last_insert_id)."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            rows = cur.execute(sql, params)
            return rows, cur.lastrowid
    finally:
        conn.close()