# 🧠 AI-Based Sales Forecasting Tool for MSMEs

This project is a lightweight, intelligent forecasting tool built for small businesses (MSMEs) to help them make better inventory, staffing, and marketing decisions by predicting future sales. It uses a machine learning model (XGBoost) and provides easy-to-understand visual insights through an interactive web interface built with Streamlit.

---

## 🚨 The Problem

Most MSMEs struggle with overstocking or understocking products due to poor sales forecasting. Traditional methods like gut-feeling, spreadsheets, or static reports don’t scale when the business starts growing or diversifying its product base. Moreover, many MSMEs don’t have the resources or technical expertise to use complex forecasting software.

---

## 💡 The Solution

This tool enables MSMEs to upload their historical sales data in CSV format and get accurate, AI-powered predictions for the next 1, 3, or 6 months — with zero coding or technical setup. It shows monthly sales forecasts per product, side-by-side with actual historical sales, making it easier to plan and make decisions.

It’s designed to be:
- ✅ **Simple** – Easy CSV upload and dropdown-based interaction
- ✅ **Flexible** – Works with any number of products and categories
- ✅ **Visual** – Clear bar charts to compare actual vs forecasted sales
- ✅ **Scalable** – Uses machine learning (XGBoost) to handle complex patterns like seasonality and discounts

---

## ⚙️ How It Works

1. **Data Upload**: Users upload a CSV file containing sales records.
2. **Preprocessing**: The tool encodes product names and categories, and prepares the dataset with features like day of the week, stock availability, discounts, etc.
3. **Model Training**: A machine learning model (XGBoost Regressor) is trained using this data.
4. **Prediction**: The model predicts future sales for each product based on the chosen forecast window (1, 3, or 6 months).
5. **Visualization**: Monthly sales are displayed using grouped bar charts for each product, showing actual vs predicted units sold.
6. **Export**: Users can download the forecast results as a CSV file.

---

## 📊 Features

- 📤 Upload your own sales data (.csv)
- 📆 Forecast for 1, 3, or 6 months using a dropdown
- 🧠 XGBoost-powered model trained on-the-fly
- 📈 Interactive monthly bar charts (with hover values)
- 🟩 Compare predicted sales with actual historical sales
- 🧮 Works with multiple products and categories
- 📥 Download forecast results as a CSV file

---

## 🧪 Sample Dataset Columns

To make predictions, your dataset should include the following columns (a sample CSV is provided):

| Column              | Description                                 |
|---------------------|---------------------------------------------|
| `Date`              | Date of the transaction (YYYY-MM-DD)        |
| `Product_Name`      | Name of the product sold                    |
| `Product_Category`  | Category or department of the product       |
| `Price_per_Unit`    | Final selling price of the product          |
| `Discount_%`        | Discount applied (if any)                   |
| `Stock_Available`   | Inventory stock at time of sale             |
| `DayOfWeek`         | Integer representing day of week (0-6)      |
| `Is_Weekend`        | 1 if Sat/Sun, else 0                         |
| `Is_Holiday`        | 1 if national holiday, else 0               |
| `Units_Sold`        | Number of units sold                        |

The app uses these to train the model and simulate realistic future data for forecasting.

---

## 💻 How to Run It

Make sure you have Python installed. Then:

```bash
git clone https://github.com/thejonsamuel/sales-forecast.git
cd sales-forecast
pip install -r requirements.txt
streamlit run app.py
```

---
## 🎯 Use Cases

- Retail stores or supermarkets forecasting inventory needs
- MSMEs planning promotions based on seasonal demand
- Vendors tracking slow-moving vs fast-selling products
- Business owners exploring AI without hiring a data scientist

---

## 🔭 What's Next

Planned enhancements:
- 🏬 Multi-store support with store-level filtering
- 📅 Toggle between monthly and weekly forecast granularity
- 📉 Forecast accuracy tracker (MAE, RMSE) per product
- 🧠 Option to upload categorical sales drivers like marketing spend
- ☁️ Deployment on Streamlit Cloud for public access
- 📊 Dashboard summary of top-performing or underperforming products

---

If you find it helpful or want to collaborate, feel free to fork the repo or reach out.

---
