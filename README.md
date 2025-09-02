<h2>Stock Price Predictor</h2>

📈 Stock Price Predictor

A machine learning project for forecasting stock prices using historical
data and predictive modeling techniques.

🚀 Project Overview

This project demonstrates end-to-end machine learning workflow for
predicting stock prices. It includes data collection, preprocessing,
model training, evaluation, and deployment of the final predictive
model.

📂 Project Structure

-   GettingData.ipynb – Data collection and exploration
-   PreProcessor.ipynb – Data preprocessing and feature engineering
-   Stock.ipynb – Model training, evaluation, and prediction
-   Tesla_stock.csv / Tesla_Stock_data.csv – Raw datasets
-   PreProcesseData.csv – Cleaned dataset
-   StockPrice.pkl – Saved ML model

🛠️ Technologies Used

-   Python (Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn)
-   Jupyter Notebook
-   Pickle (for model serialization)

📊 Model

The predictor uses supervised ML regression techniques to analyze stock
market patterns and generate forecasts.

<h6>model = Pipeline(steps=[
    ('preprocessing', preprocessor),
    ('model', XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    ))
])</h6>

⚡ How to Run

1.  Clone this repository
2.  Install requirements: pip install -r requirements.txt
3.  Run Stock.ipynb or load StockPrice.pkl for predictions

📌 Results

The model achieves competitive accuracy in forecasting Tesla stock
<h6>R² Score (%): 92.54181691416991</h6>
prices. Graphs and performance metrics are included in the notebooks.
<img width="1184" height="584" alt="image" src="https://github.com/user-attachments/assets/ecf2095d-af0d-4dcb-a9d7-7f9e97a1a2f9" />


🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

📜 License

This project is licensed under the MIT License.
