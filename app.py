import streamlit as st
import pandas as pd

st.set_page_config(page_title="EduPro Dashboard", layout="wide")

st.title("📊 EduPro Instructor Performance Dashboard")

# -----------------------------
# LOAD YOUR DATASET
# -----------------------------
file = "EduPro Online Platform.xlsx"   # Make sure this file is uploaded in GitHub

# Try reading sheets (edit names if needed)
teachers = pd.read_excel(file, sheet_name="Teachers")
courses = pd.read_excel(file, sheet_name="Courses")
transactions = pd.read_excel(file, sheet_name="Transactions")

# -----------------------------
# MERGE DATA
# -----------------------------
df = transactions.merge(teachers, on="TeacherID")
df = df.merge(courses, on="CourseID")

# -----------------------------
# DASHBOARD
# -----------------------------

# KPIs
st.subheader("📈 Key Performance Indicators")

col1, col2 = st.columns(2)
col1.metric("Average Teacher Rating", round(df['TeacherRating'].mean(),2))
col2.metric("Average Course Rating", round(df['CourseRating'].mean(),2))

# Dataset
st.subheader("📊 Full Dataset")
st.dataframe(df, use_container_width=True)

# Scatter plot
st.subheader("📌 Experience vs Teacher Rating")
st.scatter_chart(df[['YearsOfExperience','TeacherRating']])

# Course category analysis
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

st.success("✅ Project Ready Using Your Dataset!")
