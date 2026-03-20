import streamlit as st
import pandas as pd
import pickle

# Safe Plotly import
try:
    import plotly.express as px
except:
    import os
    os.system("pip install plotly")
    import plotly.express as px

# Load data
df = pd.read_csv("data/users.csv")

# Load model
model = pickle.load(open("model.pkl", "rb"))
encoder = pickle.load(open("encoder.pkl", "rb"))

st.set_page_config(page_title="EduPro Dashboard", layout="wide")

st.title("🎓 EduPro User Analytics & ML Dashboard")

# ================= SIDEBAR =================
st.sidebar.header("🔍 Filters")

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    df["Gender"].unique(),
    default=df["Gender"].unique()
)

age_range = st.sidebar.slider(
    "Select Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (int(df["Age"].min()), int(df["Age"].max()))
)

filtered_df = df[
    (df["Gender"].isin(gender_filter)) &
    (df["Age"].between(age_range[0], age_range[1]))
]

# ================= KPI =================
st.subheader("📊 Key Metrics")

col1, col2 = st.columns(2)
col1.metric("Total Users", len(filtered_df))
col2.metric("Average Age", round(filtered_df["Age"].mean(), 2))

# ================= CHARTS =================

# Age Histogram
st.subheader("📈 Age Distribution")
fig1 = px.histogram(filtered_df, x="Age", nbins=10)
st.plotly_chart(fig1, use_container_width=True)

# Gender Pie
st.subheader("👥 Gender Distribution")
fig2 = px.pie(filtered_df, names="Gender")
st.plotly_chart(fig2, use_container_width=True)

# Scatter
st.subheader("📊 Age vs Gender")
fig3 = px.scatter(filtered_df, x="Age", y="Gender")
st.plotly_chart(fig3, use_container_width=True)

# ================= ML PREDICTION =================
st.subheader("🤖 Predict User Category")

age_input = st.number_input("Enter Age", 10, 100, 25)
gender_input = st.selectbox("Select Gender", df["Gender"].unique())

if st.button("Predict"):
    gender_encoded = encoder.transform([gender_input])[0]
    prediction = model.predict([[age_input, gender_encoded]])
    st.success(f"Predicted Category: {prediction[0]}")

# ================= DATA =================
st.subheader("📄 Dataset Preview")
st.dataframe(filtered_df)
