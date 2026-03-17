import streamlit as st
import pandas as pd

st.set_page_config(page_title="EduPro Dashboard", layout="wide")

st.title("📊 EduPro Instructor Performance Dashboard")

# -----------------------------
# DEFAULT DATA (AUTO LOAD)
# -----------------------------

teachers = pd.DataFrame({
    "TeacherID": [1,2,3,4,5,6,7],
    "TeacherName": ["Amit","Riya","Rahul","Neha","Karan","Pooja","Arjun"],
    "Age": [35,29,40,32,45,30,38],
    "Gender": ["Male","Female","Male","Female","Male","Female","Male"],
    "Expertise": ["Data Science","AI","Web Dev","ML","Cloud","AI","Data Science"],
    "YearsOfExperience": [10,5,15,8,20,6,12],
    "TeacherRating": [4.5,4.2,4.8,4.3,4.7,4.4,4.6]
})

courses = pd.DataFrame({
    "CourseID": [101,102,103,104,105,106,107],
    "CourseName": ["Python Basics","AI Intro","Web Dev Advanced","ML Course","Cloud Basics","Deep Learning","Data Analysis"],
    "CourseCategory": ["Programming","AI","Programming","AI","Cloud","AI","Data Science"],
    "CourseLevel": ["Beginner","Intermediate","Advanced","Advanced","Beginner","Advanced","Intermediate"],
    "CourseRating": [4.3,4.5,4.6,4.4,4.2,4.7,4.5]
})

transactions = pd.DataFrame({
    "TransactionID": [1,2,3,4,5,6,7],
    "CourseID": [101,102,103,104,105,106,107],
    "TeacherID": [1,2,3,4,5,6,7]
})

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

# Scatter
st.subheader("📌 Experience vs Teacher Rating")
st.scatter_chart(df[['YearsOfExperience','TeacherRating']])

# Category chart
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

st.success("✅ Project Running Successfully Without Dataset Upload!")
