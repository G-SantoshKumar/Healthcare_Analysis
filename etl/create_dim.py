import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

Host=os.getenv('host')
User=os.getenv('user')
Password=os.getenv('password')
Database=os.getenv('database')

# MySQL Database Connection Details
DB_CONFIG = {
        "host": Host,       
        "user":User,            
        "password":Password,     
        "database":Database  
}

# Create SQLAlchemy engine using DB_CONFIG
engine = create_engine(f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")


# Load CSV files
disease_dim = pd.read_csv(r"C:\Users\santosh\Desktop\HealthCare\Data\cleaned_disease_dim.csv")
doctor_dim = pd.read_csv(r"C:\Users\santosh\Desktop\HealthCare\Data\cleaned_doctor_dim.csv")
hospital_dim = pd.read_csv(r"C:\Users\santosh\Desktop\HealthCare\Data\cleaned_hospital_dim.csv")
billing_dim = pd.read_csv(r"C:\Users\santosh\Desktop\HealthCare\Data\cleaned_billing_dim.csv")

# Function to push DataFrame to MySQL
def push_to_mysql(df, table_name):
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"Data pushed to {table_name}")

# Main function to execute
if __name__ == "__main__":
    push_to_mysql(disease_dim, "disease_dim")
    push_to_mysql(doctor_dim, "doctor_dim")
    push_to_mysql(hospital_dim, "hospital_dim")
    push_to_mysql(billing_dim, "billing_dim")

    print("All dimension tables successfully loaded into MySQL!")
