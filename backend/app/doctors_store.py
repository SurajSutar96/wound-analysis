import sqlite3
import os
import hashlib
import uuid
import datetime

DB_PATH = "static/clinivanta.db"

def init_db():
    """Initializes the SQLite database for Clinivanta AI."""
    if not os.path.exists("static"):
        os.makedirs("static")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Doctors table — extended with age, mobile, address
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            hospital TEXT,
            specialty TEXT,
            age INTEGER,
            mobile TEXT,
            address TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reset_token TEXT
        )
    ''')
    
    # Safe migration: add missing columns if they don't exist yet
    for col, col_type in [('age', 'INTEGER'), ('mobile', 'TEXT'), ('address', 'TEXT')]:
        try:
            cursor.execute(f'ALTER TABLE doctors ADD COLUMN {col} {col_type}')
        except Exception:
            pass  # Column already exists
    
    # Patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            location TEXT,
            phone TEXT,
            email TEXT UNIQUE,
            notes TEXT,
            doctor_id TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (doctor_id) REFERENCES doctors (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_doctor(name, email, password, hospital=""):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    doctor_id = f"DR-{uuid.uuid4().hex[:6].upper()}"
    p_hash = hash_password(password)
    
    try:
        cursor.execute('''
            INSERT INTO doctors (id, name, email, password_hash, hospital)
            VALUES (?, ?, ?, ?, ?)
        ''', (doctor_id, name, email, p_hash, hospital))
        conn.commit()
        conn.close()
        return {"id": doctor_id, "name": name, "email": email, "hospital": hospital}
    except sqlite3.IntegrityError:
        conn.close()
        return None

def authenticate_doctor(email, password):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    p_hash = hash_password(password)
    cursor.execute(
        'SELECT id, name, email, hospital, specialty, age, mobile, address FROM doctors WHERE email = ? AND password_hash = ?',
        (email, p_hash)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "hospital": user[3],
            "specialty": user[4],
            "age": user[5],
            "mobile": user[6],
            "address": user[7],
        }
    return None

def update_doctor_profile(doctor_id, name, hospital, specialty, age, mobile, address):
    """Updates editable profile fields for a doctor."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE doctors
        SET name = ?, hospital = ?, specialty = ?, age = ?, mobile = ?, address = ?
        WHERE id = ?
    ''', (name, hospital, specialty, age, mobile, address, doctor_id))
    conn.commit()
    # Fetch updated record to return
    cursor.execute(
        'SELECT id, name, email, hospital, specialty, age, mobile, address FROM doctors WHERE id = ?',
        (doctor_id,)
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            "id": user[0], "name": user[1], "email": user[2],
            "hospital": user[3], "specialty": user[4],
            "age": user[5], "mobile": user[6], "address": user[7],
        }
    return None

def set_reset_token(email, token):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE doctors SET reset_token = ? WHERE email = ?', (token, email))
    conn.commit()
    conn.close()
