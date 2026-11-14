import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Explorer", page_icon="📊", layout="wide")

st.header("📊 Exploratory Data Explorer")
st.write("Upload a dataset (CSV) to view automated statistical summaries and distributions.")

# File Uploader
uploaded_file = st.file_uploader("Upload your dataset", type=["csv"])

if uploaded_file is not None:
    # Read the dataset
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Raw Data Preview")
    st.dataframe(df.head())
    
    # Generate columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Statistical Summary")
        st.write(df.describe())
        
    with col2:
        st.subheader("Data Visualization")
        # Select a numeric column to plot
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        if numeric_cols:
            selected_col = st.selectbox("Select a variable to visualize:", numeric_cols)
            
            # Matplotlib Figure
            fig, ax = plt.subplots()
            ax.hist(df[selected_col].dropna(), bins=20, color='skyblue', edgecolor='black')
            ax.set_title(f'Distribution of {selected_col}')
            ax.set_xlabel(selected_col)
            ax.set_ylabel('Frequency')
            
            # Display plot in Streamlit
            st.pyplot(fig)
        else:
            st.warning("No numeric columns found for visualization.")