import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
from contextlib import closing

conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Q10a20Z30!",
        database="dnd_db"
    )

if not conn.is_connected():
  conn.reconnect()

def create_user(email, password, username):
    with closing(conn.cursor(buffered=True)) as cursor:
        hashed_password = generate_password_hash(password)
        query = "INSERT INTO users (email, password, username) VALUES (%s, %s, %s)"
        values = (email, hashed_password, username)
        cursor.execute(query, values)
        conn.commit()

def get_user_by_id(user_id):
    with closing(conn.cursor(buffered=True)) as cursor:
        query = "SELECT * FROM users WHERE id = %s"
        values = (user_id,)
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result:
            user_data = {
                'id': result[0],
                'email': result[1],
                'password': result[2],
                'username': result[3] # Assuming username is the fourth field in your users table.
            }
            return User(**user_data)
        else:
            return None


def validate_user(email, password):
    with closing(conn.cursor(buffered=True)) as cursor:
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        values = (email, password)
        cursor.execute(query, values)
        result = cursor.fetchone()

        return result

def add_character(name, race, class_, level, experience, strength, dexterity, constitution, intelligence, wisdom, charisma):
    with closing(conn.cursor(buffered=True)) as cursor:
        query = "INSERT INTO characters (name, race, class, level, experience, strength, dexterity, constitution, intelligence, wisdom, charisma) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" # added experience
        values = (name, race, class_, level, experience, strength, dexterity, constitution, intelligence, wisdom, charisma)  # added experience
        cursor.execute(query, values)
        conn.commit()


def get_user_by_email(email):
    with closing(conn.cursor(buffered=True)) as cursor:
        query = "SELECT * FROM users WHERE email = %s"
        values = (email,)
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result:
            user_data = {
                'id': result[0],
                'email': result[1],
                'password': result[2],
                'username': result[3] # Assuming username is the fourth field in your users table.
            }
            return user_data
        else:
            return None

def update_password_in_db(email, password):
    # Hash the password
    hashed_password = generate_password_hash(password, method='sha256')

    with closing(conn.cursor(buffered=True)) as cursor:
        query = "UPDATE users SET password=%s WHERE email=%s"
        cursor.execute(query, (hashed_password, email))
        conn.commit()


def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)


def get_characters_by_user_id(user_id):
    with closing(conn.cursor(buffered=True)) as cursor:
        query = "SELECT id, name, class, level FROM characters WHERE user_id = %s"
        values = (user_id,)
        cursor.execute(query, values)
        result = cursor.fetchall()

        return result

def get_character_by_name(name):
    with closing(conn.cursor(buffered=True)) as cursor:
        query = "SELECT * FROM characters WHERE name = %s"
        values = (name,)
        cursor.execute(query, values)
        result = cursor.fetchone()

        if result:
            character_data = {
                'id': result[0],
                'name': result[1],
                'race': result[2],
                'class': result[3],
                'level': result[4],
                'experience': result[5],
                'strength': result[6],
                'dexterity': result[7],
                'constitution': result[8],
                'intelligence': result[9],
                'wisdom': result[10],
                'charisma': result[11]
            }
            return character_data
        else:
            return None


class User:
    def __init__(self, id: int, email: str, password: str, username: str):
        self.id = id
        self.email = email
        self.password = password
        self.username = username

    def is_authenticated(self) -> bool:
        return True

    def is_active(self) -> bool:
        return True

    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return str(self.id)



def get_user(email):
    with closing(conn.cursor(buffered=True)) as cursor:
        query = "SELECT * FROM users WHERE email=%s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            user = User(result[0], result[1], result[2])
            return user

        return None
