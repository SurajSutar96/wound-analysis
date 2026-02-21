import sqlite3
import os
import uuid
from app.doctors_store import DB_PATH

def register_patient(patient_data):
    """
    Persists a new patient to SQLite with doctor association and uniqueness checks.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Uniqueness check for email and phone
    email = patient_data.get("email")
    phone = patient_data.get("phone")
    
    cursor.execute('SELECT id FROM patients WHERE email = ? OR phone = ?', (email, phone))
    if cursor.fetchone():
        conn.close()
        return {"error": "Patient with this email or phone already exists in the surgical node."}
    
    px_id = f"PX-{uuid.uuid4().hex[:6].upper()}"
    
    cursor.execute('''
        INSERT INTO patients (id, name, age, gender, location, phone, email, notes, doctor_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        px_id,
        patient_data.get("name"),
        patient_data.get("age"),
        patient_data.get("gender"),
        patient_data.get("location"),
        phone,
        email,
        patient_data.get("notes"),
        patient_data.get("doctor_id")
    ))
    
    try:
        conn.commit()
        conn.close()
        return {"id": px_id, "name": patient_data.get("name")}
    except sqlite3.Error as e:
        conn.close()
        print(f"Database Error: {e}")
        return {"error": str(e)}

def get_all_patients(doctor_id=None):
    """
    Retrieves patients, filtered by doctor if provided.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if doctor_id:
        cursor.execute('SELECT * FROM patients WHERE doctor_id = ? ORDER BY registered_at DESC', (doctor_id,))
    else:
        cursor.execute('SELECT * FROM patients ORDER BY registered_at DESC')
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_patient_by_id(patient_id):
    """
    Retrieves a single patient by ID.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None
