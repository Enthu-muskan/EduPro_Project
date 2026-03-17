import streamlit as st
import pandas as pd

st.set_page_config(page_title="EduPro Dashboard", layout="wide")

st.title("📊 EduPro Instructor Performance Dashboard")

# -----------------------------
# FILE UPLOAD (IMPORTANT FIX)
# -----------------------------
uploaded_file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    
    # Read Excel file
    xls = pd.ExcelFile(uploaded_file)

    st.write("📄 Available Sheets:", xls.sheet_names)

    # Read sheets (make sure names match)
    teachers = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    courses = pd.read_excel(xls, sheet_name=xls.sheet_names[1])
    transactions = pd.read_excel(xls, sheet_name=xls.sheet_names[2])

    # Merge data
    df = transactions.merge(teachers, on="TeacherID")
    df = df.merge(courses, on="CourseID")

    # -----------------------------
    # DASHBOARD
    # -----------------------------

    st.subheader("📊 Full Dataset")
    st.dataframe(df, use_container_width=True)

    # KPIs
    st.subheader("📈 Key Metrics")
    col1, col2 = st.columns(2)
    col1.metric("Average Teacher Rating", round(df['TeacherRating'].mean(),2))
    col2.metric("Average Course Rating", round(df['CourseRating'].mean(),2))

    # Scatter
    st.subheader("📌 Experience vs Teacher Rating")
    st.scatter_chart(df[['YearsOfExperience','TeacherRating']])

    # Category
    st.subheader("📊 Course Category Performance")
    category_avg = df.groupby("CourseCategory")["CourseRating"].mean()
    st.bar_chart(category_avg)

    # Top instructors
    st.subheader("🏆 Top Instructors")
    top = df.sort_values(by="TeacherRating", ascending=False)
    st.dataframe(top[['TeacherName','TeacherRating','Expertise']], use_container_width=True)

    # Filter
    st.subheader("🔍 Filter by Course Category")
    category = st.selectbox("Select Category", df['CourseCategory'].unique())
    filtered = df[df['CourseCategory']==category]
    st.dataframe(filtered, use_container_width=True)

else:
    st.warning("⚠️ Please upload your Excel dataset to proceed.")
