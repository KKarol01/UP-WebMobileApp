from flask import Flask 
from flask_cors import CORS
from flask import request, jsonify
import sqlite3
from waitress import serve
from flask_jwt_extended import get_jwt_identity, jwt_required, JWTManager, create_access_token, set_access_cookies, get_jwt
from datetime import timedelta
from password_strength import PasswordPolicy
import time
import bcrypt
import random
import dotenv
import datetime
import os

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost", "http://83.6.108.209", "http://192.168.1.31", "http://localhost:5500"])
app.config["JWT_SECRET_KEY"] = "D67V9e+8QvUFoUs6tdIao/jux/RpQbWF"
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
# app.config["JWT_COOKIE_SAMESITE"] = "Strict"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
jwt = JWTManager(app)

def make_db_call(**kwargs):
    try:
        db = sqlite3.connect("db")
        dbcur = db.cursor()
        result = None

        if kwargs.get("one") is not None:
            arguments = kwargs.get("args", ())
            result = dbcur.execute(kwargs.get("one"), arguments)
        elif kwargs.get("many") is not None:
            arguments = kwargs.get("args", [])
            result = dbcur.executemany(kwargs.get("many"), arguments)
        if kwargs.get("fetchone") is not None:
            result = result.fetchone()
        elif kwargs.get("fetchall") is not None:
            result = result.fetchall()
        db.commit()
        db.close()
        return result
    except Exception as err:
        db.close()
        print(err)
        return None

def server_response(message, result, code):
    return jsonify({"message": message, "result": result}), code

@jwt.token_in_blocklist_loader
def is_token_in_blocklist(jwt_header, jwt_payload):
    try:
        jti = jwt_payload["jti"]
        res = make_db_call(one="SELECT jti FROM revoked_jwt WHERE jti=?", args=(jti,), fetchone=1)
        return res is not None
    except Exception as e:
        print(e)
        return True

@app.get("/api/en/jwt")
@jwt_required()
def protected():
    return server_response("You are verified", True, 200)

@app.post("/api/en/register")
def register():
    try:
        print("a")
        # time.sleep(1.0)
        json = request.get_json()
        email = json["email"].lower()
        passwd = json["password"]
        passwdr = json["password_repeat"]

        if(len(email) == 0):
            return server_response("Email cannot be that short", False, 401)
        if(len(email) > 64):
            return server_response("Email cannot be that long", False, 401)
        if(email.find("@") == -1 or email.find(".") == -1):
            return server_response("Email must have valid format with '@' and '.'", False, 401)

        if(len(passwd) < 8):
                return server_response("Password cannot be that short", False, 401)
        if(len(passwd) > 16):
            return server_response("Password cannot be that long", False, 401)
        if(passwd != passwdr):
            return server_response("Passwords are not the same", False, 401)
        
        email_already_exists = make_db_call(one="SELECT COUNT(*) FROM users WHERE email == ?", args = (email,), fetchone=1)[0] > 0
        if(email_already_exists):
            return server_response("Email already exists", False, 401)
        
        passwd_hash = bcrypt.hashpw(passwd, bcrypt.gensalt())
        make_db_call(one="INSERT INTO users VALUES(?, ?)", args=(email, passwd_hash))
        return server_response("OK", True, 200)
    except Exception as err:
        print(err)
        return server_response("Internal Error", False, 500)

@app.post("/api/en/login")
def login():
    try:
        # time.sleep(2.0)
        json_data = request.get_json()
        email = json_data["email"].lower()
        password = json_data["password"]

        if len(email) == 0:
            return server_response("Invalid username or password", False, 401)
        if len(password) == 0:
            return server_response("Invalid username or password", False, 401)

        user = make_db_call(one="SELECT password FROM users WHERE email = ?", args=(email,), fetchone=1)
        if user is None:
            return server_response("Invalid username or password", False, 401)
        
        if bcrypt.checkpw(password.encode(), user[0].encode()) is False:
            print("asddd")
            return server_response("Invalid username or password", False, 401)

        res = server_response({"access_token": create_access_token(identity=email)}, True, 200)
        return res

    except Exception as e:
        print(e)
        return server_response("Internal Error", False, 500)

@app.get("/api/en/logout")
@jwt_required()
def logout():
    try:
        cu = get_jwt()["jti"]
        make_db_call(one="INSERT INTO revoked_jwt VALUES (?)", args=(cu, ))
        return server_response("Successfully logged out", True, 200)
    except Exception as e:
        print(e)
        return server_response("Internal Error", False, 500)

@app.get("/api/en/notes/<index>/<count>")
@jwt_required()
def notes(index, count):
    try:
        res = make_db_call(one="SELECT title,desc,added FROM notes WHERE email=? ORDER BY added DESC LIMIT ? OFFSET ?", args=(get_jwt_identity(), count, index), fetchall=1)
        return server_response({"notes": res}, True, 200)
    except Exception as e:
        print(e)
        return server_response("Internal Error", False, 500)

@app.post("/api/en/addnote")
@jwt_required()
def addnote():
    try:
        json = request.get_json()
        title = json["title"]
        desc = json["desc"]
        print(title, desc)

        if(len(title) == 0 or len(desc) == 0):
            return server_response("Title and note fields cannot be empty", False, 401)

        make_db_call(one="INSERT INTO notes(title, desc, email) VALUES (?, ?, ?)", args=(title, desc, get_jwt_identity()))
        return server_response("Successfully logged out", True, 200)
    except Exception as e:
        print(e)
        return server_response("Internal Error", False, 500)

@app.put("/api/en/updatenote")
@jwt_required()
def updatenote():
    try:
        json = request.get_json()
        title = json["title"]
        desc = json["desc"]
        added = json["added"]
        if(len(title) == 0 or len(desc) == 0):
            return server_response("Title and note fields cannot be empty", False, 401)
        make_db_call(one="UPDATE notes SET title=?,desc=? WHERE email=? AND added=?", args=(title, desc, get_jwt_identity(), added))
        return server_response("OK", True, 200)
    except Exception as err:
        print(err)
        return server_response("Internal Error", False, 500)

@app.delete("/api/en/deletenote/<added>")
@jwt_required()
def deletenote(added):
    try:
        print(added)
        make_db_call(one="DELETE FROM notes WHERE email=? AND added=?", args=(get_jwt_identity(), added))
        return server_response("OK", True, 200)
    except Exception as err:
        print(err)
        return server_response("Internal Error", False, 500)

@app.get("/api/en/notecount")
@jwt_required()
def notecount():
    try:
        res = make_db_call(one="SELECT COUNT(*) FROM notes WHERE email=?", args=(get_jwt_identity(), ), fetchone=1)
        return server_response({"count": res[0]}, True, 200)
    except Exception as err:
        print(err)
        return server_response("Internal Error", False, 500)

#=================== PL =========================
@app.get("/api/pl/jwt")
@jwt_required()
def pl_protected():
    return server_response("Jesteś zweryfikowany", True, 200)

@app.post("/api/pl/register")
def pl_register():
    try:
        print("a")
        # time.sleep(1.0)
        json = request.get_json()
        email = json["email"].lower()
        passwd = json["password"]
        passwdr = json["password_repeat"]

        if(len(email) == 0):
            return server_response("Email nie może być tak krótki", False, 401)
        if(len(email) > 64):
            return server_response("Email nie może być tak długi", False, 401)
        if(email.find("@") == -1 or email.find(".") == -1):
            return server_response("Email musi zawierać znaki '@' i '.'", False, 401)

        if(len(passwd) < 8):
                return server_response("Hasło nie może być krótsze niz 8 znaków", False, 401)
        if(len(passwd) > 16):
            return server_response("Hasło nie może być dłuższe niż 16 znaków", False, 401)
        if(passwd != passwdr):
            return server_response("Hasła nie są identyczne", False, 401)
        
        email_already_exists = make_db_call(one="SELECT COUNT(*) FROM users WHERE email == ?", args = (email,), fetchone=1)[0] > 0
        if(email_already_exists):
            return server_response("Email już jest zarejestrowany", False, 401)
        
        passwd_hash = bcrypt.hashpw(passwd, bcrypt.gensalt())
        make_db_call(one="INSERT INTO users VALUES(?, ?)", args=(email, passwd_hash))
        return server_response("OK", True, 200)
    except Exception as err:
        print(err)
        return server_response("Błąd serwera", False, 500)

@app.post("/api/pl/login")
def pl_login():
    try:
        # time.sleep(2.0)
        json_data = request.get_json()
        email = json_data["email"].lower()
        password = json_data["password"]

        if len(email) == 0:
            return server_response("Niepoprawne hasło lub email", False, 401)
        if len(password) == 0:
            return server_response("Niepoprawne hasło lub email", False, 401)

        user = make_db_call(one="SELECT password FROM users WHERE email = ?", args=(email,), fetchone=1)
        if user is None:
            return server_response("Niepoprawne hasło lub email", False, 401)
        
        if bcrypt.checkpw(password.encode(), user[0].encode()) is False:
            print("asddd")
            return server_response("Niepoprawne hasło lub email", False, 401)

        res = server_response({"access_token": create_access_token(identity=email)}, True, 200)
        return res

    except Exception as e:
        print(e)
        return server_response("Błąd serwera", False, 500)

@app.get("/api/pl/logout")
@jwt_required()
def pl_logout():
    try:
        cu = get_jwt()["jti"]
        make_db_call(one="INSERT INTO revoked_jwt VALUES (?)", args=(cu, ))
        return server_response("Poprawnie wylogowano.", True, 200)
    except Exception as e:
        print(e)
        return server_response("Błąd serwera", False, 500)

@app.get("/api/pl/notes/<index>/<count>")
@jwt_required()
def pl_notes(index, count):
    try:
        res = make_db_call(one="SELECT title,desc,added FROM notes WHERE email=? ORDER BY added DESC LIMIT ? OFFSET ?", args=(get_jwt_identity(), count, index), fetchall=1)
        return server_response({"notes": res}, True, 200)
    except Exception as e:
        print(e)
        return server_response("Błąd serwera", False, 500)

@app.post("/api/pl/addnote")
@jwt_required()
def pl_addnote():
    try:
        json = request.get_json()
        title = json["title"]
        desc = json["desc"]
        print(title, desc)

        if(len(title) == 0 or len(desc) == 0):
            return server_response("Pola na tytuł i treść notatki nie mogą być puste", False, 401)

        make_db_call(one="INSERT INTO notes(title, desc, email) VALUES (?, ?, ?)", args=(title, desc, get_jwt_identity()))
        return server_response("Pomyślnie dodano notatke", True, 200)
    except Exception as e:
        print(e)
        return server_response("Błąd serwera", False, 500)

@app.put("/api/pl/updatenote")
@jwt_required()
def pl_updatenote():
    try:
        json = request.get_json()
        title = json["title"]
        desc = json["desc"]
        added = json["added"]
        if(len(title) == 0 or len(desc) == 0):
            return server_response("Pola na tytuł i treść notatki nie mogą być puste", False, 401)
        make_db_call(one="UPDATE notes SET title=?,desc=? WHERE email=? AND added=?", args=(title, desc, get_jwt_identity(), added))
        return server_response("OK", True, 200)
    except Exception as err:
        print(err)
        return server_response("Błąd serwera", False, 500)

@app.delete("/api/pl/deletenote/<added>")
@jwt_required()
def pl_deletenote(added):
    try:
        print(added)
        make_db_call(one="DELETE FROM notes WHERE email=? AND added=?", args=(get_jwt_identity(), added))
        return server_response("OK", True, 200)
    except Exception as err:
        print(err)
        return server_response("Błąd serwera", False, 500)

@app.get("/api/pl/notecount")
@jwt_required()
def pl_notecount():
    try:
        res = make_db_call(one="SELECT COUNT(*) FROM notes WHERE email=?", args=(get_jwt_identity(), ), fetchone=1)
        return server_response({"count": res[0]}, True, 200)
    except Exception as err:
        print(err)
        return server_response("Błąd serwera", False, 500)

#================================================

if __name__ == "__main__":
    # make_db_call(one = "DROP TABLE IF EXISTS users")
    # make_db_call(one = "DROP TABLE IF EXISTS notes")
    # make_db_call(one = "DROP TABLE IF EXISTS revoked_jwt")
    make_db_call(one = """
    CREATE TABLE IF NOT EXISTS users(
        email TEXT UNIQUE NOT NULL, 
        password TEXT UNIQUE NOT NULL
    )
    """)
    make_db_call(one = """
    CREATE TABLE IF NOT EXISTS notes(
        title TEXT NOT NULL, 
        desc TEXT NOT NULL, 
        email TEXT NOT NULL,
        added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    make_db_call(one = """
    CREATE TABLE IF NOT EXISTS revoked_jwt(
        jti 
    )  
    """)

    serve(app, host="0.0.0.0", port=8080, threads=4, url_scheme="https")
