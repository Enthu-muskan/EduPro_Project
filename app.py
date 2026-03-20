import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

# Load data
df = pd.read_csv("data/users.csv")

# Load model
model = pickle.load(open("model.pkl", "rb"))
encoder = pickle.load(open("encoder.pkl", "rb"))

st.set_page_config(page_title="EduPro ML Dashboard", layout="wide")

st.title("🎓 EduPro Advanced Analytics Dashboard")

# ================= Sidebar Filters =================
st.sidebar.header("🔍 Filters")

selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

age_range = st.sidebar.slider(
    "Select Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (int(df["Age"].min()), int(df["Age"].max()))
)

filtered_df = df[
    (df["Gender"].isin(selected_gender)) &
    (df["Age"].between(age_range[0], age_range[1]))
]

# ================= KPIs =================
st.subheader("📊 Key Metrics")

col1, col2 = st.columns(2)
col1.metric("Total Users", len(filtered_df))
col2.metric("Average Age", round(filtered_df["Age"].mean(), 1))

# ================= Plotly Charts =================

# Age Distribution
st.subheader("📈 Age Distribution")
fig1 = px.histogram(filtered_df, x="Age", nbins=10)
st.plotly_chart(fig1)

# Gender Distribution
st.subheader("👥 Gender Distribution")
fig2 = px.pie(filtered_df, names="Gender")
st.plotly_chart(fig2)

# Scatter Plot
st.subheader("📊 Age Scatter")
fig3 = px.scatter(filtered_df, x="Age", y="Gender")
st.plotly_chart(fig3)

# ================= ML Prediction =================
st.subheader("🤖 Predict User Category")

age_input = st.number_input("Enter Age", 10, 100, 25)
gender_input = st.selectbox("Select Gender", df["Gender"].unique())

if st.button("Predict"):
    gender_encoded = encoder.transform([gender_input])[0]
    prediction = model.predict([[age_input, gender_encoded]])

    st.success(f"Predicted Category: {prediction[0]}")
