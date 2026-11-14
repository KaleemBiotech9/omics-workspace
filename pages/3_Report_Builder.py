import streamlit as st
import sqlite3
import pandas as pd
import datetime

st.set_page_config(page_title="Report Builder", page_icon="📄", layout="wide")

st.header("📄 Automated Report Builder")
st.write("Compile your docking logs and export your research records.")

try:
    conn = sqlite3.connect('cadd_logs.db')
    df = pd.read_sql_query("SELECT * FROM docking_logs", conn)
    conn.close()
except Exception as e:
    df = pd.DataFrame()

if df.empty:
    st.warning("No data found in the CADD Tracker. Add some logs first!")
else:
    st.subheader("Research Summary")
    
    total_runs = len(df)
    best_affinity = df['affinity'].min() 
    best_ligand = df.loc[df['affinity'].idxmin()]['ligand']
    best_protein = df.loc[df['affinity'].idxmin()]['protein']

    st.markdown(f"""
    **Report Date:** {datetime.date.today()}
    * **Total Docking Runs:** {total_runs}
    * **Top Binding Affinity:** {best_affinity} kcal/mol
    * **Best Ligand/Target Pair:** {best_ligand} / {best_protein}
    """)
    
    st.write("---")
    st.dataframe(df, use_container_width=True)
    
    st.subheader("Export Options")
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"CADD_Report_{datetime.date.today()}.csv",
            mime="text/csv",
        )
        
    with col2:
        st.info("💡 **PDF Export:** To save this entire page as a clean PDF report, just press `Ctrl+P` and select **Save as PDF** in your browser's print menu.")