import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor
import streamlit as st
import plotly.express as px
import os
import warnings

warnings.filterwarnings("ignore")
st.set_page_config(page_title="Sales Forecast Dashboard", layout="wide")
st.title("📊 MSME Sales Forecast")

# Upload
uploaded_file = st.file_uploader("📤 Upload your sales CSV file", type="csv")

# Load file
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("No file uploaded. Using sample data.")
    df = pd.read_csv("supermarket_sales_data.csv")

df['Date'] = pd.to_datetime(df['Date'])

# Dropdown: Forecast Range (in months)
forecast_months = st.selectbox("📆 Select forecast duration (months):", [1, 3, 6])

# Encode
le_product = LabelEncoder()
le_category = LabelEncoder()
df['Product_Name_enc'] = le_product.fit_transform(df['Product_Name'])
df['Product_Category_enc'] = le_category.fit_transform(df['Product_Category'])

# Train
X = df.drop(columns=['Date', 'Units_Sold', 'Product_Name', 'Product_Category'])
y = df['Units_Sold']
model = XGBRegressor(n_estimators=100, learning_rate=0.1)
model.fit(X, y)
st.success("✅ Model trained")

# Forecast
forecast_df_list = []

# Start from the 1st of the next full month
last_date = df['Date'].max()
first_of_next_month = (last_date + pd.offsets.MonthBegin(1)).replace(day=1)
future_start = first_of_next_month
future_end = future_start + pd.DateOffset(months=forecast_months) - pd.Timedelta(days=1)

# Generate all dates in forecast window
future_dates = pd.date_range(start=future_start, end=future_end, freq='D')


holiday_set = set(["2025-01-01", "2025-01-26", "2025-04-14", "2025-05-01", "2025-06-15"])
os.makedirs("forecast_charts", exist_ok=True)

for product_name in df['Product_Name'].unique():
    product_df = df[df['Product_Name'] == product_name]
    product_info = product_df.iloc[-1]
    encoded_name = le_product.transform([product_name])[0]
    encoded_cat = le_category.transform([product_info['Product_Category']])[0]

    pred_data = []

    for date in future_dates:
        day = date.weekday()
        is_weekend = int(day >= 5)
        is_holiday = int(date.strftime('%Y-%m-%d') in holiday_set)
        base_price = product_info['Price_per_Unit'] / (1 - product_info['Discount_%'] / 100)
        discount = np.random.choice([0, 5, 10, 15])
        price = base_price * (1 - discount / 100)
        stock = np.random.randint(20, 100)

        pred_data.append({
            'Price_per_Unit': round(price, 2),
            'Discount_%': discount,
            'Stock_Available': stock,
            'DayOfWeek': day,
            'Is_Weekend': is_weekend,
            'Is_Holiday': is_holiday,
            'Product_Name_enc': encoded_name,
            'Product_Category_enc': encoded_cat,
            'Date': date,
            'Product_Name': product_name
        })

    pred_df = pd.DataFrame(pred_data)
    predict_input = pred_df.drop(columns=["Date", "Product_Name"])
    pred_df['Predicted_Units'] = np.round(model.predict(predict_input)).astype(int)
    forecast_df_list.append(pred_df)

# Combine forecasts
forecast_df = pd.concat(forecast_df_list)
forecast_df['Month'] = forecast_df['Date'].dt.to_period('M').astype(str)

# Monthly aggregation
monthly_pred = forecast_df.groupby(['Product_Name', 'Month'])['Predicted_Units'].sum().reset_index(name="Predicted_Sales")

# Historical Monthly aggregation (latest months only)
latest_date = df['Date'].max()
cutoff = latest_date - pd.DateOffset(months=forecast_months)
recent_hist = df[df['Date'] > cutoff].copy()
recent_hist['Month'] = recent_hist['Date'].dt.to_period('M').astype(str)
monthly_hist = recent_hist.groupby(['Product_Name', 'Month'])['Units_Sold'].sum().reset_index(name="Actual_Sales")

# Merge
comparison = pd.merge(monthly_pred, monthly_hist, on=['Product_Name', 'Month'], how='outer').fillna(0)

# Melt for grouped bar chart
chart_data = comparison.melt(id_vars=['Product_Name', 'Month'],
                             value_vars=['Actual_Sales', 'Predicted_Sales'],
                             var_name='Type', value_name='Sales')

# Plot
fig = px.bar(chart_data,
             x='Month',
             y='Sales',
             color='Type',
             barmode='group',
             facet_col='Product_Name',
             title="📊 Forecast vs Actual Sales (Monthly)",
             labels={'Sales': 'Units Sold'},
             height=600)

st.plotly_chart(fig, use_container_width=True)

# Data Preview
st.subheader("🔍 Monthly Forecast Summary")
st.dataframe(comparison)

# Download option
st.download_button("📥 Download Forecast CSV",
                   data=comparison.to_csv(index=False).encode(),
                   file_name="monthly_sales_forecast.csv",
                   mime="text/csv")
