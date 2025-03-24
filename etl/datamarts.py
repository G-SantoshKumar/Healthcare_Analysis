import pymysql
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

Host=os.getenv('host')
User=os.getenv('user')
Password=os.getenv('password')
Database=os.getenv('database')

# --- Database Connection ---
def connect_db():
    """Establishes a connection to the MySQL database."""
    return pymysql.connect(
        host=Host,       
        user=User,            
        password=Password,     
        database=Database,
        cursorclass=pymysql.cursors.DictCursor
    )

# --- Data Mart Queries ---
DATAMART_QUERIES = {
    "patient_data_mart": """
        SELECT 
            pd.patient_id,
            pd.name,
            pd.age,
            pd.gender,
            pd.location,
            pd.blood_type,
            pd.smoker_status,
            pd.alcohol_consumption,
            pd.exercise_frequency,
            COUNT(hvf.visit_id) AS total_visits,
            AVG(hvf.total_bill) AS avg_bill
        FROM patient_dim pd
        JOIN hospital_visits_fact hvf ON pd.patient_id = hvf.patient_id
        GROUP BY pd.patient_id;
    """,

    "financial_data_mart": """
        SELECT
            hf.billing_id,
            hf.total_bill,
            hf.insurance_type,
            hf.claim_status,
            hf.payment_method,
            hvf.hospital_id,
            SUM(hvf.total_bill) AS total_revenue_per_hospital
        FROM hospital_visits_fact hvf
        JOIN billing_dim hf ON hvf.billing_id = hf.billing_id
        GROUP BY hvf.hospital_id, hf.billing_id;
    """,

    "doctor_performance_data_mart": """
        SELECT 
            dd.doctor_id,
            dd.doctor_name,
            dd.specialization,
            dd.years_of_experience,
            COUNT(hvf.visit_id) AS total_patients_seen,
            AVG(hvf.total_bill) AS avg_bill_per_patient
        FROM doctor_dim dd
        JOIN hospital_visits_fact hvf ON dd.doctor_id = hvf.doctor_id
        GROUP BY dd.doctor_id;
    """,

    "disease_analytics_data_mart": """
        SELECT 
            dd.disease_id,
            dd.disease_name,
            dd.category,
            dd.severity_level,
            COUNT(hvf.visit_id) AS total_cases,
            AVG(hvf.total_bill) AS avg_treatment_cost
        FROM disease_dim dd
        JOIN hospital_visits_fact hvf ON dd.disease_id = hvf.disease_id
        GROUP BY dd.disease_id;
    """
}

# --- Functions to Fetch Data ---
def run_query(query):
    """Executes SQL query and returns a Pandas DataFrame."""
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall())
            return df
    finally:
        conn.close()

def get_patient_data_mart():
    return run_query(DATAMART_QUERIES["patient_data_mart"])

def get_financial_data_mart():
    return run_query(DATAMART_QUERIES["financial_data_mart"])

def get_doctor_data_mart():
    return run_query(DATAMART_QUERIES["doctor_performance_data_mart"])

def get_disease_data_mart():
    return run_query(DATAMART_QUERIES["disease_analytics_data_mart"])
