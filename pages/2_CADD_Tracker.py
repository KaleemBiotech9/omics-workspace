import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="CADD Tracker", page_icon="🧪", layout="wide")

st.header("🧪 CADD Workflow Tracker")
st.write("Log your molecular docking parameters and binding affinities locally.")

# 1. Initialize Local SQLite Database
# This automatically creates a file named 'cadd_logs.db' in your main folder
conn = sqlite3.connect('cadd_logs.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS docking_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        protein TEXT,
        ligand TEXT,
        affinity REAL,
        software TEXT,
        notes TEXT
    )
''')
conn.commit()

# 2. Input Form for New Docking Results
with st.form("add_log_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        protein = st.text_input("Target Protein (e.g., OCT4)")
    with col2:
        ligand = st.text_input("Ligand / Compound ID")
    with col3:
        affinity = st.number_input("Binding Affinity (kcal/mol)", value=0.0, format="%.2f")
        
    software = st.selectbox("Docking Software", ["AutoDock Vina", "PyRx", "Other"])
    notes = st.text_area("Notes / Grid Box Parameters")
    
    submitted = st.form_submit_button("Save to Database")
    
    if submitted and protein and ligand:
        c.execute("INSERT INTO docking_logs (protein, ligand, affinity, software, notes) VALUES (?, ?, ?, ?, ?)",
                  (protein, ligand, affinity, software, notes))
        conn.commit()
        st.success(f"Successfully logged {ligand} against {protein}!")

# 3. Display the Database
st.subheader("Docking Database")
df = pd.read_sql_query("SELECT * FROM docking_logs", conn)

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Your database is currently empty. Add your first docking log above.")

conn.close()