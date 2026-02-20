import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
from streamlit_option_menu import option_menu

# PAGE CONFIG

st.set_page_config(layout="wide")

# DB CONNECTION

conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="Ajith23",
    database="Phonepay_data",
    port=5432)

# SIDEBAR

with st.sidebar:
    page = option_menu(
        "Navigation",
        ["Home","Business Case Study"],
        icons=["house","bar-chart"],
        default_index=0)

# UI STYLE
    st.markdown("""<style>.stApp {background: linear-gradient(135deg, #14001f, #2d004d);color: white;}
                
        .kpi-title {
        font-size: 18px;
        color: white;}

        .kpi-value {
        font-size: 22px;
        font-weight: bold;}""", unsafe_allow_html=True)
    
# HOME PAGE

if page == "Home":
    st.title("PhonePe Pulse Dashboard")

    col_filter, col_map, col_summary = st.columns([1,3,2.5])  
    
# LEFT FILTER PANEL

    with col_filter:

        data_type = st.selectbox("Select Data Type", ["Transaction", "User"])
        years = st.selectbox("Select Year", pd.read_sql("SELECT DISTINCT years FROM aggregated_transaction ORDER BY years", conn)["years"])
        quarter = st.selectbox("Select Quarter", pd.read_sql("SELECT DISTINCT quarter FROM aggregated_transaction ORDER BY quarter", conn)["quarter"])

# FETCH DATA

    if data_type == "Transaction":

        df_state = pd.read_sql(f""" SELECT States, sum(transaction_amount) as value
                            FROM aggregated_transaction
                            WHERE years={years} AND quarter={quarter}
                            GROUP BY States""", conn)
        
        df_district = pd.read_sql(f""" SELECT district, sum(transaction_amount) as value
                            FROM map_transaction
                            WHERE years={years} AND quarter={quarter}
                            GROUP BY district""", conn)
        
        df_total = pd.read_sql(f""" SELECT SUM(transaction_count) as total_txn, SUM(transaction_amount) as total_amt
                            FROM aggregated_transaction
                            WHERE years={years} AND quarter={quarter}""", conn)

        df_category = pd.read_sql(f""" SELECT transaction_type, SUM(transaction_amount) as value
                                FROM aggregated_transaction
                                WHERE years={years} AND quarter={quarter}
                                GROUP BY transaction_type""", conn)
        
    else:
        
        df_state = pd.read_sql(f""" SELECT States, SUM(appopens) as value
                            FROM map_user
                            WHERE years={years} AND quarter={quarter}
                            GROUP BY States""", conn)

        df_district = pd.read_sql(f""" SELECT district, SUM(registeredusers) as value
                                FROM map_user
                                WHERE years={years} AND quarter={quarter}
                                GROUP BY district""", conn)

        df_total = pd.read_sql(f""" SELECT SUM(appopens) as total_appopens, SUM(registeredusers) as total_user
                            FROM map_user
                            WHERE years={years} AND quarter={quarter}""", conn)

        df_category = None

# RIGHT SIDE SUMMARY

    with col_summary:

        st.markdown("### Transactions")

        if data_type == "Transaction":
    
            total_txn = int(df_total["total_txn"][0] or 0)  # df_total["total_txn"] → selecting column total_txn, [0] → taking the first row value, or 0 → if value is None or NULL, use 0 instead, int() → convert to integer
            total_amt = float(df_total["total_amt"][0] or 0) # Take first row from total_amt, If NULL → use 0, Convert to float

            avg_value = total_amt / total_txn if total_txn != 0 else 0 # This is called a ternary condition (short if-else)

            st.markdown(f"""<div class="kpi-card">
                        <div class="kpi-title">All PhonePe Transactions (UPI + Cards + Wallets)</div>
                        <div class="kpi-value">{total_txn:,}</div>
                        </div>""", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)

            with col1:

                st.markdown(f"""<div class="kpi-card">
                            <div class="kpi-title">Total Payment Value</div>
                            <div class="kpi-value">₹ {total_amt/10000000:.2f} Cr</div>
                            </div>""", unsafe_allow_html=True)
                
            with col2:
            
                st.markdown(f"""
                        <div class="kpi-card">
                            <div class="kpi-title">Avg. Transaction Value</div>
                            <div class="kpi-value">₹ {avg_value:,.2f}</div>
                        </div>""", unsafe_allow_html=True)
        else:
            total_users = int(df_total["total_user"].iloc [0] or 0)
            total_appopens = int(df_total["total_appopens"].iloc [0] or 0)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""<div class="kpi-card">
                            <div class="kpi-title">Total Users</div>
                            <div class="kpi-value">{total_users:,}</div>
                            </div>""", unsafe_allow_html=True)

            with col2:
                st.markdown(f"""<div class="kpi-card">
                            <div class="kpi-title">Total App Opens</div>
                            <div class="kpi-value">{total_appopens:,}</div>
                            </div>""", unsafe_allow_html=True)
                            
# Categories

        if data_type == "Transaction" and df_category is not None:

            st.markdown("### Categories")

            df_category = df_category.sort_values("value", ascending=False)

            for _, row in df_category.iterrows():

                st.markdown(f"""<div class="rank-box">
                            {row['transaction_type']} {row['value']/10000000:.2f} Cr
                            </div>""", unsafe_allow_html=True)            
           
# TOP 10 STATES & DISTRICTS

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("## Top 10 Stat")

            top_States = df_state.sort_values("value", ascending=False).head(10)

            for i, row in enumerate(top_States.itertuples(), 1):
                value_cr = row.value / 10000000
                st.markdown(f"""
                    <div class="rank">
                        {i}. {row.states} : {value_cr:.2f} Cr
                    </div>""", unsafe_allow_html=True)

        with col2:

            st.markdown("## Top 10 Distri")

            df_district.columns = ["District", "value"]
            top_districts = df_district.sort_values("value", ascending=False).head(10)

            for i, row in enumerate(top_districts.itertuples(), 1):
                value_cr = row.value / 10000000
                st.markdown(f"""
                    <div class="rank">
                        {i}. {row.District} : {value_cr:.2f} Cr
                    </div>""", unsafe_allow_html=True)

# BUSINESS CASE STUDY PAGE

else:

    st.title("PHONEPAY DATA ANALYSIS")
    st.subheader("Business Case Study")

# CHART FUNCTION

    def draw_chart(df, chart_type, title):
        st.subheader(title)

        if chart_type=="bar":
            fig=px.bar(df,x=df.columns[0],y=df.columns[1])
        elif chart_type=="pie":
            fig=px.pie(df,names=df.columns[0],values=df.columns[1])
        elif chart_type=="line":
            fig=px.line(df,x=df.columns[0],y=df.columns[1])
        elif chart_type=="column":
            fig=px.bar(df,x=df.columns[0],y=df.columns[1])
        elif chart_type=="area":
            fig=px.area(df,x=df.columns[0],y=df.columns[1])

        st.plotly_chart(fig,use_container_width=True)

# SELECT CASE STUDY

    case = st.selectbox("Select Case Study",[
        "1. Decoding Transaction Dynamics on PhonePe",
        "2. Device Dominance and User Engagement Analysis",
        "3. Insurance Engagement Analysis",
        "4. Transaction Analysis Across States and Districts",
        "5. Insurance Transactions Analysis"])

# CASE 1 – TRANSACTION DYNAMICS

    if case=="1. Decoding Transaction Dynamics on PhonePe":

        state = st.selectbox("Select States",
                pd.read_sql("SELECT DISTINCT States FROM aggregated_transaction ORDER BY States",conn)["states"])

        df1=pd.read_sql(f"""SELECT Years,SUM(Transaction_amount) val
        FROM aggregated_transaction
        WHERE States ='{state}'
        GROUP BY Years ORDER BY Years""",conn)
        draw_chart(df1,"column","States Wise Transaction")
        
        c1,c2=st.columns(2)

        year = c1.selectbox("Select Years",
            pd.read_sql("SELECT DISTINCT Years FROM aggregated_transaction ORDER BY Years",conn)["years"])

        quarter = c2.selectbox("Select quarter",
            pd.read_sql("SELECT DISTINCT Quarter FROM aggregated_transaction ORDER BY Quarter",conn)["quarter"])

        df2=pd.read_sql(f"""SELECT States,SUM(Transaction_amount) val
        FROM aggregated_transaction
        WHERE Years={year} AND Quarter={quarter}
        GROUP BY States ORDER BY val DESC LIMIT 10""",conn)
        draw_chart(df2,"bar","Top 10 States")

        df3=pd.read_sql(f"""SELECT Transaction_type,SUM(Transaction_amount) val
        FROM aggregated_transaction 
        GROUP BY Transaction_type""",conn)
        draw_chart(df3,"pie","Payment Type")

        c1,c2=st.columns(2)

        state = c1.selectbox("Select State",
            pd.read_sql("SELECT DISTINCT States FROM aggregated_transaction ORDER BY States",conn)["states"])

        year = c2.selectbox("Select years",
            pd.read_sql("SELECT DISTINCT Years FROM aggregated_transaction ORDER BY Years",conn)["years"])       
        
        df4=pd.read_sql(f"""SELECT Transaction_type,SUM(Transaction_amount) val
        FROM aggregated_transaction
        WHERE States='{state}' AND Years={year}
        GROUP BY Transaction_type ORDER BY Transaction_type""",conn)
        draw_chart(df4,"line","Transaction By States & Payment Type")

        c1,c2=st.columns(2)

        state = c1.selectbox("Select states",
            pd.read_sql("SELECT DISTINCT States FROM aggregated_transaction ORDER BY States",conn)["states"])

        year = c2.selectbox("Select year",
            pd.read_sql("SELECT DISTINCT Years FROM aggregated_transaction ORDER BY Years",conn)["years"])

        df5=pd.read_sql(f"""SELECT Quarter,SUM(Transaction_count) val
        FROM aggregated_transaction
        WHERE States='{state}' AND Years={year}
        GROUP BY Quarter ORDER BY Quarter""",conn)
        draw_chart(df5,"bar","Transaction Trend")

# CASE 2 – DEVICE DOMINANCE

    elif case=="2. Device Dominance and User Engagement Analysis":

        state = st.selectbox("Select State",
            pd.read_sql("SELECT DISTINCT States FROM aggregated_user ORDER BY States",conn)["states"])
        
        df1=pd.read_sql(f"""SELECT Brands,SUM(Transaction_count) val
        FROM aggregated_user
        WHERE States= '{state}'
        GROUP BY Brands ORDER BY val DESC""",conn)
        draw_chart(df1,"bar","State Wise Device Dominance")

        df2=pd.read_sql("""SELECT Brands,SUM(Percentage) val
        FROM aggregated_user GROUP BY Brands""",conn)
        draw_chart(df2,"pie","Brand Usage Share")

        brand = st.selectbox("Select Brands",
            pd.read_sql("SELECT DISTINCT Brands FROM aggregated_user ORDER BY Brands",conn)["brands"])

        df3=pd.read_sql(f"""SELECT Years,SUM(Transaction_count) val
        FROM aggregated_user 
        WHERE Brands = '{brand}'       
        GROUP BY Years ORDER BY Years""",conn)
        draw_chart(df3,"line","Year Wise Device Usage Trend")

        df4=pd.read_sql("""SELECT Quarter,SUM(Transaction_count) val
        FROM aggregated_user GROUP BY Quarter ORDER BY Quarter""",conn)
        draw_chart(df4,"column","Quarter Device Performance")

        df5=pd.read_sql("""SELECT Years,SUM(Percentage) val
        FROM aggregated_user GROUP BY Years ORDER BY Years""",conn)
        draw_chart(df5,"bar","Engagement Trend Area")

# CASE 3 – INSURANCE ENGAGEMENT

    elif case=="3. Insurance Engagement Analysis":

        df1=pd.read_sql("""SELECT States,SUM(Transaction_amount) val
        FROM aggregated_insurance GROUP BY States ORDER BY val DESC LIMIT 10""",conn)
        draw_chart(df1,"bar","Top 10 States")

        df2=pd.read_sql("""SELECT States,SUM(Transaction_count) Count
        FROM aggregated_insurance GROUP BY States""",conn)
        draw_chart(df2,"pie","Insurance Share")

        df3=pd.read_sql("""SELECT Years,SUM(Transaction_amount) val
        FROM aggregated_insurance GROUP BY Years ORDER BY Years""",conn)
        draw_chart(df3,"line","Insurance Growth Timeline")

        c1,c2 = st.columns(2)

        state = c1.selectbox("Select State",
            pd.read_sql("SELECT DISTINCT States FROM aggregated_insurance ORDER BY States",conn)["states"])

        year = c2.selectbox("Select Years",
            pd.read_sql("SELECT DISTINCT Years FROM aggregated_insurance ORDER BY Years",conn)["years"])

        df4=pd.read_sql(f"""SELECT Quarter,SUM(Transaction_amount) val
        FROM aggregated_insurance
        WHERE States='{state}' AND Years={year}
        GROUP BY Quarter ORDER BY Quarter""",conn)
        draw_chart(df4,"column","Insurance Quarter Trend")

        df5=pd.read_sql("""SELECT Years,SUM(Transaction_count) Count
        FROM aggregated_insurance GROUP BY Years ORDER BY Years""",conn)
        draw_chart(df5,"area","Insurance Volume Trend")

# CASE 4 – STATE & DISTRICT ANALYSIS

    elif case=="4. Transaction Analysis Across States and Districts":

        df1=pd.read_sql("""SELECT District,SUM(Transaction_amount) val
        FROM map_transaction GROUP BY District ORDER BY val DESC LIMIT 10""",conn)
        draw_chart(df1,"bar","Top 10 District")

        df2=pd.read_sql("""SELECT States,SUM(Transaction_amount) val
        FROM map_transaction GROUP BY States""",conn)
        draw_chart(df2,"pie","State Share")
    
        df3=pd.read_sql(f"""SELECT Years,SUM(Transaction_amount) val
        FROM map_transaction
        GROUP BY Years ORDER BY Years""",conn)
        draw_chart(df3,"line","District Growth")

        c1,c2, = st.columns(2)

        state = c1.selectbox("Select States",
            pd.read_sql("SELECT DISTINCT States FROM map_transaction ORDER BY States",conn)["states"])

        year = c2.selectbox("Select Years",
            pd.read_sql("SELECT DISTINCT Years FROM map_transaction ORDER BY Years",conn)["years"])
        
        df4=pd.read_sql(f"""SELECT Quarter,SUM(Transaction_amount) val
        FROM map_transaction
        WHERE States='{state}' AND Years={year}
        GROUP BY Quarter ORDER BY Quarter""",conn)
        draw_chart(df4,"column","Quarter Trend")

        df5=pd.read_sql("""SELECT Years,SUM(Transaction_count) Count
        FROM map_transaction GROUP BY Years ORDER BY Years""",conn)
        draw_chart(df5,"bar","District Volume Trend")

# CASE 5 – INSURANCE TRANSACTIONS

    elif case=="5. Insurance Transactions Analysis":

        df1=pd.read_sql("""SELECT States,SUM(Transaction_amount) val
        FROM map_insurance GROUP BY States ORDER BY val DESC LIMIT 10""",conn)
        draw_chart(df1,"bar","Top Insurance States")

        df2=pd.read_sql("""SELECT District,SUM(Transaction_amount) val
        FROM map_insurance GROUP BY District""",conn)
        draw_chart(df2,"pie","District Insurance Share")

        df3=pd.read_sql(f"""SELECT Years,SUM(Transaction_amount) val
        FROM map_insurance
        GROUP BY Years ORDER BY Years""",conn)
        draw_chart(df3,"line","Insurance Year Trend")

        c1,c2, = st.columns(2)

        state = c1.selectbox("Select States",
            pd.read_sql("SELECT DISTINCT States FROM map_insurance ORDER BY States",conn)["states"])

        year = c2.selectbox("Select Years",
            pd.read_sql("SELECT DISTINCT Years FROM map_insurance ORDER BY Years",conn)["years"])

        df4=pd.read_sql(f"""SELECT Quarter,SUM(Transaction_amount) val
        FROM map_insurance
        WHERE States='{state}' AND Years={year}
        GROUP BY Quarter ORDER BY Quarter""",conn)
        draw_chart(df4,"column","Quarter Insurance Trend")

        df5=pd.read_sql("""SELECT Years,SUM(Transaction_count) Count
        FROM map_insurance GROUP BY Years ORDER BY Years""",conn)
        draw_chart(df5,"area","Insurance Area Trend")