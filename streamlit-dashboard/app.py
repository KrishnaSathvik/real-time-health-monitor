
# streamlit-dashboard/app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 🔧 Always first command
st.set_page_config(page_title="Real-Time Health Dashboard", layout="wide")

# 🔄 Auto-refresh every 10 seconds
st_autorefresh(interval=10000, limit=None, key="refresh")

# 🔌 Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["healthcare"]
collection = db["vitals"]

# ⛏️ Fetch last 100 records, sorted by latest timestamp
cursor = collection.find().sort("timestamp", -1)
data = list(cursor)
if not data:
    st.warning("No vitals data found in MongoDB.")
    st.stop()

# 🧾 Convert to DataFrame
df = pd.DataFrame(data)
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
df = df.sort_values("timestamp", ascending=True)

# ✅ Show dashboard updated time
st.markdown(f"🕒 **Last updated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ✅ Show MongoDB record count
total_records = collection.count_documents({})
st.markdown(f"📊 **MongoDB total record count:** {total_records}")

# 🎚️ Patient Filter
st.sidebar.title("🔍 Filters")
patient_ids = df["patient_id"].unique()
selected_patient = st.sidebar.selectbox("Select Patient ID", patient_ids)

filtered_df = df[df["patient_id"] == selected_patient]

# 📤 Export to CSV
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download CSV", data=csv, file_name=f"patient_{selected_patient}_vitals.csv", mime="text/csv")

# 🧠 Dashboard Title
st.title("🩺 Real-Time Health Monitoring Dashboard")
st.write(f"Showing recent data for **Patient {selected_patient}**")

# 📈 Heart Rate Trend Chart
st.subheader("📊 Heart Rate Over Time")
fig1, ax1 = plt.subplots()
ax1.plot(filtered_df["timestamp"], filtered_df["heart_rate"], marker="o", color="red")
ax1.set_xlabel("Time")
ax1.set_ylabel("Heart Rate (BPM)")
ax1.set_title(f"Heart Rate Trend - Patient {selected_patient}")
plt.xticks(rotation=45)
st.pyplot(fig1)

# 📈 Blood Pressure Trend Chart
st.subheader("📊 Blood Pressure Over Time")

# 🧠 Split blood pressure into systolic and diastolic safely
bp_split = filtered_df["blood_pressure"].str.extract(r"(?P<systolic>\d+)/(?P<diastolic>\d+)")
filtered_df["systolic"] = pd.to_numeric(bp_split["systolic"], errors="coerce")
filtered_df["diastolic"] = pd.to_numeric(bp_split["diastolic"], errors="coerce")

# 🚫 Drop rows with invalid/missing values
filtered_df = filtered_df.dropna(subset=["systolic", "diastolic"])

# 📊 Plot
fig2, ax2 = plt.subplots()
ax2.plot(filtered_df["timestamp"], filtered_df["systolic"], label="Systolic", marker="o", color="blue")
ax2.plot(filtered_df["timestamp"], filtered_df["diastolic"], label="Diastolic", marker="o", color="green")
ax2.set_xlabel("Time")
ax2.set_ylabel("Blood Pressure (mmHg)")
ax2.set_title(f"Blood Pressure Trend - Patient {selected_patient}")
ax2.legend()
plt.xticks(rotation=45)
st.pyplot(fig2)


# 🚨 Show Latest Vitals Only If Data Exists
st.subheader("🚨 Latest Vitals")
if not filtered_df.empty:
    latest = filtered_df.iloc[-1]
    st.write(latest[["heart_rate", "blood_pressure", "spo2", "timestamp"]])

    if latest["heart_rate"] < 60 or latest["heart_rate"] > 100:
        st.error("⚠️ Abnormal Heart Rate!")

    if latest["spo2"] < 90:
        st.error("⚠️ Low Oxygen Saturation (SpO2)!")
    
    # 🧠 AI Risk Score
    def calculate_risk(hr, spo2, bp):
        systolic = int(bp.split("/")[0])
        risk_score = 0
        if hr < 60 or hr > 100:
            risk_score += 1
        if spo2 < 90:
            risk_score += 1
        if systolic > 130:
            risk_score += 1
        return risk_score

    risk = calculate_risk(latest["heart_rate"], latest["spo2"], latest["blood_pressure"])
    st.metric("🧠 AI Health Risk Score", f"{risk}/3")
else:
    st.warning("No valid vitals available for this patient to calculate risk score.")


# 📋 Display Table
st.subheader("📋 Raw Vitals Data (Latest 100 Records)")
st.dataframe(df.sort_values("timestamp", ascending=False).reset_index(drop=True))
