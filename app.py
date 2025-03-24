import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from etl.kpi import *  # Import KPI functions
from etl.aggregation import *  # Import Aggregation functions
from etl.datamarts import *  # Import Data Mart functions

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Healthcare Analytics Dashboard", layout="wide")

# --- Sidebar Navigation Menu ---
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Overview", "Schema", "KPIs", "Aggregations", "Visualizations", "Data Marts"],
        icons=["house", "diagram-3", "bar-chart", "calculator", "pie-chart", "database"],
        menu_icon="cast",
        default_index=0
    )

# --- Overview Section ---
if selected == "Overview":
    st.title("Project Overview") 
    st.write(
        """
        This project aims to develop a practical healthcare provider analytics repository by utilizing a publicly available dataset from GitHub. The solution will leverage Python for data transformation and the calculation of key healthcare metrics. The system will be implemented using a well-structured schema in MySQL, focusing on specialized data marts for provider productivity and appointment analytics. By integrating and analyzing healthcare data efficiently, this project will enable data-driven decision-making for improved operational performance in the healthcare sector.

        """
    )

# --- Schema Section ---
elif selected == "Schema":
    st.title("Database Schema")
    st.image("schema.png", caption="Database Schema Diagram", use_container_width=True)

# --- KPI Section 
elif selected == "KPIs":
    st.title("Key Performance Indicators")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue ($)", f"${get_total_revenue():,.2f}")
    col2.metric("Total Visits", f"{get_total_visits():,}")
    col3.metric("Avg Revenue per Visit ($)", f"${get_avg_revenue_per_visit():,.2f}")

    st.subheader("Revenue Breakdown")
    revenue_options = ["By Disease", "By Doctor", "By Hospital", "By Patient"]
    selected_revenue = st.selectbox("Select Revenue Type", revenue_options)

    revenue_data_funcs = {
        "By Disease": get_revenue_by_disease,
        "By Doctor": get_revenue_by_doctor,
        "By Hospital": get_revenue_by_hospital,
        "By Patient": get_revenue_per_patient,
    }

    df = revenue_data_funcs[selected_revenue]()
    fig = px.bar(df, x=df.columns[0], y=df.columns[1], title=f"Revenue {selected_revenue}")
    st.plotly_chart(fig)

    st.subheader("Visits Analysis")
    visits_options = ["By Gender", "By Age Group"]
    selected_visits = st.selectbox("Select Visit Analysis", visits_options)

    visits_data_funcs = {
        "By Gender": get_visits_by_gender,
        "By Age Group": get_visits_by_age_group,
    }

    df = visits_data_funcs[selected_visits]()
    fig = px.pie(df, names=df.columns[0], values=df.columns[1], title=f"Visits {selected_visits}")
    st.plotly_chart(fig)

# --- Aggregations Section 
elif selected == "Aggregations":
    st.title("Aggregations")

    agg_options = [
        "Patient Statistics", "Financial Metrics", 
        "Hospital Revenue", "Patients Per Doctor", "Disease Category Counts"
    ]
    selected_agg = st.selectbox("Select Aggregation", agg_options)

    agg_data_funcs = {
        "Patient Statistics": get_patient_statistics,
        "Financial Metrics": get_financial_metrics,
        "Hospital Revenue": get_hospital_revenue,
        "Patients Per Doctor": get_patients_per_doctor,
        "Disease Category Counts": get_disease_category_counts,
    }

    df = agg_data_funcs[selected_agg]()

    if df.empty:
        st.warning("No data available for this selection.")
    else:
        st.table(df)

# --- Visualization Section 
elif selected == "Visualizations":
    st.title("Data Visualizations")

    viz_options = ["Hospital Revenue", "Patients Per Doctor", "Disease Category Distribution"]
    selected_viz = st.selectbox("Select Visualization", viz_options)

    viz_data_funcs = {
        "Hospital Revenue": get_hospital_revenue,
        "Patients Per Doctor": get_patients_per_doctor,
        "Disease Category Distribution": get_disease_category_counts,
    }

    df = viz_data_funcs[selected_viz]()

    if df.empty:
        st.warning("No data available for this visualization.")
    else:
        if selected_viz == "Disease Category Distribution":
            fig = px.pie(df, names=df.columns[0], values=df.columns[1], title=selected_viz)
        else:
            fig = px.bar(df, x=df.columns[0], y=df.columns[1], title=selected_viz)
        
        st.plotly_chart(fig)

# --- Data Marts Section 
elif selected == "Data Marts":
    st.title("Data Marts")

    dm_options = ["Patient Data Mart", "Financial Data Mart", "Doctor Data Mart", "Disease Data Mart"]
    selected_dm = st.selectbox("Select Data Mart", dm_options)

    dm_data_funcs = {
        "Patient Data Mart": get_patient_data_mart,
        "Financial Data Mart": get_financial_data_mart,
        "Doctor Data Mart": get_doctor_data_mart,
        "Disease Data Mart": get_disease_data_mart,
    }

    df = dm_data_funcs[selected_dm]()

    if df.empty:
        st.warning("No data available in this Data Mart.")
    else:
        st.table(df)
