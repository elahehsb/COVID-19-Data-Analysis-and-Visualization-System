import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load data
data = pd.read_csv('covid_data.csv')

# Preprocess data
data['Date'] = pd.to_datetime(data['Date'])
data = data.groupby(['Country', 'Date']).sum().reset_index()

# Visualization
plt.figure(figsize=(10, 6))
sns.lineplot(data=data, x='Date', y='TotalConfirmed', hue='Country')
plt.title('Total Confirmed Cases Over Time')
plt.show()

# Feature Engineering
data['Day'] = data['Date'].dt.dayofyear

# Train/Test Split
X = data[['Day']]
y = data['TotalConfirmed']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
print('R2 Score:', r2_score(y_test, y_pred))

# Plot predictions
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color='black')
plt.plot(X_test, y_pred, color='blue', linewidth=3)
plt.title('COVID-19 Confirmed Cases Prediction')
plt.xlabel('Day of Year')
plt.ylabel('Total Confirmed Cases')
plt.show()
