import csv
import os
import datetime

CSV_PATH = "static/assessments_history.csv"

def log_assessment(patient_data, measurements, diagnosis, doctor_id, image_url=None):
    """
    Persists assessment data to a central CSV file for auditing.
    Diagnosis newlines are preserved so structured sections survive round-trips.
    """
    file_exists = os.path.isfile(CSV_PATH)
    
    m = measurements
    row = {
        "timestamp":    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "patient_id":   patient_data.get("id",   "N/A"),
        "patient_name": patient_data.get("name", "N/A"),
        "doctor_id":    doctor_id,
        "length_cm":    m.get("length", 0),
        "width_cm":     m.get("width",  0),
        "depth_cm":     m.get("depth",  0),
        "area_cm2":     m.get("area",   0),
        "volume_cm3":   m.get("volume", 0),
        # IMPORTANT: preserve newlines so structured ### SECTIONS survive CSV round-trips
        "diagnosis":    (diagnosis or "").strip(),
        "image_url":    image_url or "",
    }
    
    headers = [
        "timestamp", "patient_id", "patient_name", "doctor_id",
        "length_cm", "width_cm", "depth_cm", "area_cm2", "volume_cm3",
        "diagnosis", "image_url"
    ]
    
    with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers, quoting=csv.QUOTE_ALL)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    
    print(f"---LOGGED TO CSV: {CSV_PATH}---")


def get_assessments():
    """
    Reads assessment history from CSV.
    """
    if not os.path.isfile(CSV_PATH):
        return []
        
    assessments = []
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            assessments.append(row)
    return assessments[::-1] # Newest first
