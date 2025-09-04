# app.py

import streamlit as st
import pandas as pd
import pickle
from sqlalchemy import create_engine, text

# ----------------------------
# Load trained model
# ----------------------------
model = pickle.load(open("StockPrice.pkl", "rb"))

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(
    page_title="📈 Tesla Stock Price Predictor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
    <style>
        body { background-color: #0e1117; color: white; }
        .stApp { background-color: #0e1117; }
        h1, h2, h3, h4 { color: #f5f5f5; }
        .sidebar .sidebar-content { background-color: #1c1f26; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# DB Helper Functions
# ----------------------------
def get_engine():
    # ✅ encode @ as %40 in password
    return create_engine("mysql+pymysql://root:Navjot%40001@localhost:3306/stock_predictions")

def save_prediction_to_db(x_new, prediction):
    try:
        engine = get_engine()
        with engine.begin() as conn:  # begin ensures commit
            sql = text("""
                INSERT INTO Tesla_predictions 
                (open_price, low_price, high_price, volume, year, month, day, 
                 ma7, ma30, daily_return, rsi, volatility, predicted_price)
                VALUES (:open_price, :low_price, :high_price, :volume, :year, :month, :day,
                        :ma7, :ma30, :daily_return, :rsi, :volatility, :predicted_price)
            """)
            values = {
                "open_price": float(x_new['Open'][0]),
                "low_price": float(x_new['Low'][0]),
                "high_price": float(x_new['High'][0]),
                "volume": int(x_new['Volume'][0]),
                "year": int(x_new['Year'][0]),
                "month": int(x_new['Month'][0]),
                "day": int(x_new['Day'][0]),
                "ma7": float(x_new['MA7'][0]),
                "ma30": float(x_new['MA30'][0]),
                "daily_return": float(x_new['Return'][0]),
                "rsi": float(x_new['RSI'][0]),
                "volatility": float(x_new['Volatility'][0]),
                "predicted_price": float(prediction[0])
            }
            conn.execute(sql, values)
        st.success("✅ Prediction saved to database!")
    except Exception as e:
        st.error(f"❌ Database error: {e}")

def load_predictions_from_db():
    try:
        engine = get_engine()
        query = "SELECT * FROM Tesla_predictions ORDER BY prediction_date DESC"
        df = pd.read_sql(query, con=engine)
        return df
    except Exception as e:
        st.error(f"❌ Database fetch error: {e}")
        return pd.DataFrame()

# ----------------------------
# UI Layout
# ----------------------------
st.title("🚀 Tesla Stock Price Predictor")
st.markdown("A Machine Learning project using **XGBoost, Technical Indicators & SQL logging**.")

# Sidebar Inputs
st.sidebar.header("📊 Input Features")

features = ['Open', 'Low','High','Volume','Year','Month','Day', 
            'MA7','MA30','Return','RSI','Volatility']

open_price = st.sidebar.number_input("Open Price", min_value=0.0, value=15.73, step=0.01)
low_price = st.sidebar.number_input("Low Price", min_value=0.0, value=15.36, step=0.01)
high_price = st.sidebar.number_input("High Price", min_value=0.0, value=16.25, step=0.01)
volume = st.sidebar.number_input("Volume", min_value=0, value=98853000, step=1000)
year = st.sidebar.number_input("Year", min_value=2000, max_value=2030, value=2015, step=1)
month = st.sidebar.number_input("Month", min_value=1, max_value=12, value=8, step=1)
day = st.sidebar.number_input("Day", min_value=1, max_value=31, value=21, step=1)
ma7 = st.sidebar.number_input("7-Day Moving Avg", value=16.47, step=0.01)
ma30 = st.sidebar.number_input("30-Day Moving Avg", value=17.17, step=0.01)
returns = st.sidebar.number_input("Daily Returns", value=-0.04, step=0.01)
rsi = st.sidebar.number_input("RSI", min_value=0.0, max_value=100.0, value=34.81, step=0.1)
volatility = st.sidebar.number_input("7-Day Volatility", value=0.68, step=0.01)

x_new = pd.DataFrame([[open_price, low_price, high_price, volume, year, month, day, 
                       ma7, ma30, returns, rsi, volatility]], columns=features)

# ----------------------------
# Prediction
# ----------------------------
if st.sidebar.button("🔮 Predict Stock Price"):
    prediction = model.predict(x_new)
    st.subheader("📌 Predicted Tesla Stock Price (Next Day):")
    st.success(f"💰 ${prediction[0]:.2f}")

    # Save prediction
    save_prediction_to_db(x_new, prediction)

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 RSI", f"{rsi:.2f}")
    col2.metric("📉 Daily Return", f"{returns:.2%}")
    col3.metric("📈 Volatility", f"{volatility:.2f}")

# ----------------------------
# Prediction History
# ----------------------------
st.subheader("🗂 Prediction History")
df_history = load_predictions_from_db()

if not df_history.empty:
    st.dataframe(df_history)

    # Download option
    csv = df_history.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Predictions as CSV",
        data=csv,
        file_name="tesla_predictions.csv",
        mime="text/csv",
    )
else:
    st.info("No predictions saved yet.")
