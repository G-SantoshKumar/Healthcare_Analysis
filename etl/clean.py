import pandas as pd

# Load data
df = pd.read_csv("Data/complete_healthcare_data.csv")

# Check for missing values
print(" Missing values before cleaning:")
print(df.isna().sum())

# Fill missing values
df["alcohol_consumption"].fillna(df["alcohol_consumption"].mode()[0], inplace=True)
df["exercise_frequency"].fillna(df["exercise_frequency"].mode()[0], inplace=True)

# Drop full duplicate rows (if any)
df.drop_duplicates(inplace=True)

# Print missing values after cleaning
print("Missing values after cleaning:")
print(df.isna().sum())

# Create Fact Table (Only Numeric + Foreign Keys)
hospital_visits_fact = df[[
    "visit_id", "patient_id_x", "disease_id", "billing_id", "visit_date",
    "hospital_id", "doctor_id", "total_bill_x"
]].rename(columns={
    "patient_id_x": "patient_id",
    "total_bill_x": "total_bill"
})

# Create Patient Dimension 
patient_dim = df[[
    "patient_id_y", "name", "age", "gender", "location", "blood_type",
    "weight", "height", "smoker_status", "alcohol_consumption", "exercise_frequency"
]].drop_duplicates(subset=["patient_id_y"], keep="first").rename(columns={"patient_id_y": "patient_id"})

# Check for duplicate patient IDs before exporting
duplicate_patients = patient_dim[patient_dim.duplicated(subset=["patient_id"], keep=False)]
if not duplicate_patients.empty:
    print(" Duplicate patient_id found! Investigate before proceeding.")
    print(duplicate_patients)
else:
    print("No duplicate patient IDs found.")

# Create Disease Dimension
disease_dim = df[["disease_id", "disease_name", "category", "severity_level"]].drop_duplicates()

# Create Doctor Dimension
doctor_dim = df[["doctor_id", "doctor_name", "specialization", "years_of_experience"]].drop_duplicates()

# Create Hospital Dimension
hospital_dim = df[["hospital_id", "hospital_name", "city", "type"]].drop_duplicates()

# Create Billing Dimension
billing_dim = df[[
    "billing_id", "total_bill_y", "insurance_type_y", "claim_status_y", "payment_method"
]].drop_duplicates().rename(columns={
    "total_bill_y": "total_bill",
    "insurance_type_y": "insurance_type",
    "claim_status_y": "claim_status"
})

# Save Cleaned Tables as CSV
hospital_visits_fact.to_csv("data/cleaned_hospital_visits_fact.csv", index=False)
patient_dim.to_csv("data/cleaned_patient_dim.csv", index=False)
disease_dim.to_csv("data/cleaned_disease_dim.csv", index=False)
doctor_dim.to_csv("data/cleaned_doctor_dim.csv", index=False)
hospital_dim.to_csv("data/cleaned_hospital_dim.csv", index=False)
billing_dim.to_csv("data/cleaned_billing_dim.csv", index=False)

print("Fact and Dimension tables created successfully with optimized schema!")
