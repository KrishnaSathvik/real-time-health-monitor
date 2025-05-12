# 🩺 Real-Time Health Monitoring System

This project simulates, processes, stores, and visualizes live health vitals of patients using a complete data pipeline involving Kafka, Spark, MongoDB, and Streamlit.

---

## 📌 Project Features

- 🧾 **Data Generator**: Produces simulated patient vitals (heart rate, blood pressure, SpO2) every 2 seconds via Kafka.
- 🔄 **Spark Streaming**: Consumes Kafka streams, transforms data, and stores it in MongoDB.
- 📊 **Streamlit Dashboard**: Real-time health monitoring UI with visual charts, alerts, and filters.
- 💡 **AI Health Risk Score**: Calculates potential risk using vitals.
- 📥 **Export to CSV**: Save patient records locally.
- 🧠 **Autorefresh**: Dashboard updates every 10 seconds.

---

## 🛠️ Tech Stack

- Python 3.12+
- Kafka (via Homebrew)
- Apache Spark (pyspark)
- MongoDB
- Streamlit
- Matplotlib
- Pandas

---

## 📁 Project Structure

```
real-time-health-monitor/
├── data-generator/
│   └── generator.py         # Kafka producer script
├── spark-streamer/
│   └── main.py              # Spark streaming job
├── streamlit-dashboard/
│   └── app.py               # Streamlit UI
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 🚀 How to Run

### 1. Start Kafka and Zookeeper

```bash
brew services start zookeeper
brew services start kafka
```

### 2. Run Kafka Producer

```bash
cd data-generator
python3 generator.py
```

### 3. Start Spark Structured Streaming

```bash
cd spark-streamer
spark-submit main.py
```

### 4. Launch Streamlit Dashboard

```bash
cd streamlit-dashboard
streamlit run app.py
```

---

## ✅ MongoDB Setup

Make sure MongoDB is running locally on default port `27017`. Data will be stored in:

- **Database**: `healthcare`
- **Collection**: `vitals`

---

## 📦 Install All Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 📌 Sample Visuals

- 📈 Heart Rate Trend per Patient
- 📈 Blood Pressure Trends (Systolic / Diastolic)
- ⚠️ Alerts for abnormal vitals
- 🧠 AI Risk Score based on vitals
- 📋 Tabular view of raw data (latest 100 entries)

---

## 📤 Export

Click on **"Download CSV"** in dashboard to export filtered vitals.

---

## 🤝 Contributing

PRs and feature requests are welcome!

---

## 📄 License

This project is open-source and free to use under the MIT License.
