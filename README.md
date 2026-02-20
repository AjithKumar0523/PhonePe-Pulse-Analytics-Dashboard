# PhonePe-Pulse-Analytics-Dashboard

An interactive Business Intelligence Dashboard built using Python, Streamlit, PostgreSQL, and Plotly to analyze PhonePe Pulse transaction and user data.

🚀 Project Overview

India’s digital payment ecosystem is growing rapidly. However, raw transaction data alone does not provide actionable insights.

This project converts structured PhonePe Pulse data into interactive visual dashboards to help analyze:

State-wise transaction performance

District-level transaction trends

User engagement patterns

Device dominance analysis

Insurance transaction growth

The dashboard enables data-driven decision-making through filters and visual insights.

🛠 Tech Stack

Frontend:

Streamlit

Backend:

Python

Database:

PostgreSQL

Visualization:

Plotly

Libraries Used:

Pandas

Psycopg2

Streamlit Option Menu

🏗 System Architecture

PostgreSQL Database
⬇
Python (psycopg2 connection)
⬇
SQL Queries
⬇
Pandas Data Processing
⬇
Plotly Visualizations
⬇
Streamlit Interactive Dashboard

📂 Database Tables Used

aggregated_transaction

map_transaction

aggregated_user

map_user

aggregated_insurance

map_insurance

📌 Key Features
🏠 Home Dashboard

Transaction / User data selection

Year & Quarter filters

KPI Cards:

Total Transactions

Total Payment Value

Average Transaction Value

Top 10 States

Top 10 Districts

Category Ranking

📊 Business Case Studies

Decoding Transaction Dynamics

Device Dominance & User Engagement

Insurance Engagement Analysis

Transaction Analysis Across States and Districts

Insurance Transaction Analysis

📈 Business Insights Generated

Identifies high-performing states and districts

Tracks yearly and quarterly transaction growth

Analyzes payment type distribution

Studies device brand dominance

Evaluates insurance transaction trends

🔧 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2️⃣ Install Required Libraries
pip install -r requirements.txt
3️⃣ Configure PostgreSQL

Update your database credentials inside:

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="your_password",
    database="Phonepay_data",
    port=5432)

⚠️ Note: In production, use environment variables instead of hardcoding credentials.

4️⃣ Run the Application
streamlit run phonepay.py
