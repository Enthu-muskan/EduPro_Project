import streamlit as st
import pandas as pd
import pickle
import plotly.express as px

# Load dataset
df = pd.read_csv("data/users.csv")

# ================= CREATE PROJECT-LIKE FEATURES =================
# (Simulating missing columns from your dataset)

df["Expertise"] = df["Gender"]  # using Gender as proxy
df["YearsOfExperience"] = df["Age"] - 20  # approximate logic
df["TeacherRating"] = (df["Age"] / df["Age"].max()) * 5
df["CourseRating"] = df["TeacherRating"] + 0.2

# ================= LOAD MODEL =================
model = pickle.load(open("model.pkl", "rb"))
encoder = pickle.load(open("encoder.pkl", "rb"))

st.set_page_config(page_title="EduPro Dashboard", layout="wide")

st.title("🎓 Instructor Performance & Course Quality (Simulated)")

# ================= KPI =================
st.subheader("📊 Key Metrics")

col1, col2 = st.columns(2)
col1.metric("Avg Teacher Rating", round(df["TeacherRating"].mean(), 2))
col2.metric("Avg Course Rating", round(df["CourseRating"].mean(), 2))

# ================= FILTERS =================
st.sidebar.header("🔍 Filters")

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

filtered_df = df[df["Gender"].isin(gender_filter)]

# ================= CHARTS =================

# Distribution of Instructor Ratings
st.subheader("📈 Distribution of Instructor Ratings")
fig1 = px.histogram(filtered_df, x="TeacherRating")
st.plotly_chart(fig1, use_container_width=True)

# Experience vs Rating
st.subheader("📊 Experience vs Rating")
fig2 = px.scatter(filtered_df, x="YearsOfExperience", y="TeacherRating")
st.plotly_chart(fig2, use_container_width=True)

# Teacher vs Course Rating
st.subheader("📊 Teacher vs Course Rating")
fig3 = px.scatter(filtered_df, x="TeacherRating", y="CourseRating")
st.plotly_chart(fig3, use_container_width=True)

# Expertise Performance
st.subheader("🏆 Expertise Performance")
exp = filtered_df.groupby("Expertise")["CourseRating"].mean().reset_index()
fig4 = px.bar(exp, x="Expertise", y="CourseRating")
st.plotly_chart(fig4, use_container_width=True)

# Top Performers
st.subheader("👨‍🏫 Top Performers")
top = filtered_df.sort_values(by="TeacherRating", ascending=False).head(5)
st.dataframe(top[["UserName", "TeacherRating"]])

# ================= ML =================
st.subheader("🤖 Predict User Category")

age_input = st.number_input("Enter Age", 10, 100, 25)
gender_input = st.selectbox("Select Gender", df["Gender"].unique())

if st.button("Predict"):
    gender_encoded = encoder.transform([gender_input])[0]
    prediction = model.predict([[age_input, gender_encoded]])
    st.success(f"Predicted Category: {prediction[0]}")
