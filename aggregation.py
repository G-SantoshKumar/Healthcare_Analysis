import pymysql
import pandas as pd

# --- Database Connection ---
def connect_db():
    """Establishes a connection to the MySQL database."""
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Santosh",
        database="Health",
        cursorclass=pymysql.cursors.DictCursor  # Returns results as dictionaries
    )

# --- SQL Aggregation Queries ---
QUERIES = {
    "patient_statistics": """
        SELECT 
            COUNT(DISTINCT patient_id) AS total_patients,
            AVG(age) AS average_age,
            COUNT(visit_id) AS total_visits
        FROM hospital_visits_fact 
        JOIN patient_dim USING (patient_id);
    """,

    "financial_metrics": """
        SELECT 
            AVG(total_bill) AS average_bill_per_visit,
            SUM(total_bill) AS total_revenue
        FROM hospital_visits_fact;
    """,

    "hospital_revenue": """
        SELECT 
            h.hospital_name, 
            SUM(f.total_bill) AS revenue
        FROM hospital_visits_fact f
        JOIN hospital_dim h USING (hospital_id)
        GROUP BY h.hospital_name;
    """,

    "patients_per_doctor": """
        SELECT 
            d.doctor_name, 
            COUNT(DISTINCT f.patient_id) AS patient_count
        FROM hospital_visits_fact f
        JOIN doctor_dim d USING (doctor_id)
        GROUP BY d.doctor_name;
    """,

    "disease_category_counts": """
        SELECT 
            d.category, 
            COUNT(f.disease_id) AS disease_count
        FROM hospital_visits_fact f
        JOIN disease_dim d USING (disease_id)
        GROUP BY d.category;
    """
}

# --- Function to Execute SQL Queries ---
def run_query(query):
    """Executes a given SQL query and returns the result as a Pandas DataFrame."""
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            df = pd.DataFrame(result)
            if df.empty:
                return pd.DataFrame(columns=[col[0] for col in cursor.description])  # Return empty DataFrame with correct column names
            return df
    finally:
        conn.close()

# --- Fetch Aggregated Data ---
def get_patient_statistics():
    return run_query(QUERIES["patient_statistics"])

def get_financial_metrics():
    return run_query(QUERIES["financial_metrics"])

def get_hospital_revenue():
    return run_query(QUERIES["hospital_revenue"])

def get_patients_per_doctor():
    return run_query(QUERIES["patients_per_doctor"])

def get_disease_category_counts():
    return run_query(QUERIES["disease_category_counts"])
